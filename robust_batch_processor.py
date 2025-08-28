#!/usr/bin/env python3
"""
支持断点续传的NIPS 2024论文批量解析工具
特性:
- 自动检测已处理论文，支持断点续传
- 错误后可重启继续处理
- 美观的进度条显示
- 详细的日志记录
- 结果验证和统计
"""
import os
import sys
import json
import time
import requests
import zipfile
import io
from datetime import datetime
from tqdm import tqdm
import logging
from pathlib import Path
import signal
import threading
from collections import defaultdict

class RobustPaperProcessor:
    def __init__(self, api_token, output_file="nips2024_papers.jsonl", 
                 log_file="processing.log", checkpoint_file="checkpoint.json"):
        self.api_token = api_token
        self.output_file = output_file
        self.log_file = log_file
        self.checkpoint_file = checkpoint_file
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 统计信息
        self.stats = {
            'total': 0,
            'completed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'errors': defaultdict(int)
        }
        
        # 信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        self.should_stop = False
        
    def _signal_handler(self, signum, frame):
        """处理中断信号，优雅退出"""
        self.logger.info(f"\n收到信号 {signum}，正在优雅退出...")
        self.should_stop = True
        self._save_checkpoint()
        
    def _load_checkpoint(self):
        """加载检查点，获取已处理论文列表"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint = json.load(f)
                self.stats.update(checkpoint.get('stats', {}))
                self.logger.info(f"加载检查点：已处理 {checkpoint.get('completed_count', 0)} 篇论文")
                return set(checkpoint.get('completed_papers', []))
            except Exception as e:
                self.logger.warning(f"加载检查点失败: {e}")
                return set()
        return set()
    
    def _save_checkpoint(self):
        """保存检查点"""
        try:
            completed_papers = self._get_completed_papers_from_file()
            checkpoint = {
                'stats': self.stats,
                'completed_papers': list(completed_papers),
                'completed_count': len(completed_papers),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"保存检查点失败: {e}")
    
    def _get_completed_papers_from_file(self):
        """从输出文件中获取已完成的论文ID"""
        completed = set()
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            completed.add(data.get('paper_id'))
            except Exception as e:
                self.logger.warning(f"读取已完成论文列表失败: {e}")
        return completed
    
    def _save_result(self, result):
        """线程安全地保存结果"""
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
                f.flush()  # 立即写入磁盘
        except Exception as e:
            self.logger.error(f"保存结果失败 {result.get('paper_id', 'unknown')}: {e}")
    
    def submit_task(self, paper_id):
        """提交单个论文的解析任务"""
        pdf_url = f"https://openreview.net/pdf?id={paper_id}"
        
        task_data = {
            "url": pdf_url,
            "is_ocr": True,
            "enable_formula": True,
            "enable_table": True,
            "language": "en",
            "data_id": paper_id
        }
        
        try:
            response = requests.post(
                "https://mineru.net/api/v4/extract/task",
                headers=self.headers,
                json=task_data,
                timeout=30
            )
            
            if response.status_code != 200:
                return None, f"HTTP {response.status_code}: {response.text[:200]}"
            
            result = response.json()
            if result.get("code") != 0:
                return None, result.get("msg", "Unknown API error")
            
            return result["data"]["task_id"], None
            
        except requests.exceptions.Timeout:
            return None, "提交任务超时"
        except Exception as e:
            return None, str(e)
    
    def wait_for_completion(self, task_id, paper_id, max_wait_time=1800):
        """等待任务完成，支持中断检查"""
        start_time = time.time()
        status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
        check_interval = 15  # 15秒检查一次
        
        while time.time() - start_time < max_wait_time:
            if self.should_stop:
                return None, "用户中断"
            
            try:
                response = requests.get(status_url, headers=self.headers, timeout=30)
                
                if response.status_code != 200:
                    return None, f"状态查询失败: {response.status_code}"
                
                result = response.json()
                if result.get("code") != 0:
                    return None, f"状态API错误: {result.get('msg')}"
                
                state = result["data"]["state"]
                
                if state == "done":
                    full_zip_url = result["data"]["full_zip_url"]
                    return self.download_and_extract(full_zip_url, paper_id)
                    
                elif state == "failed":
                    err_msg = result["data"].get("err_msg", "Unknown error")
                    return None, f"任务失败: {err_msg}"
                    
                # 等待状态
                time.sleep(check_interval)
                
            except requests.exceptions.Timeout:
                self.logger.warning(f"状态查询超时 {paper_id}")
                time.sleep(check_interval)
            except Exception as e:
                self.logger.warning(f"状态查询异常 {paper_id}: {e}")
                time.sleep(check_interval)
        
        return None, "任务超时"
    
    def download_and_extract(self, zip_url, paper_id):
        """下载ZIP文件并提取markdown内容"""
        try:
            response = requests.get(zip_url, timeout=120)
            
            if response.status_code != 200:
                return None, f"下载ZIP失败: {response.status_code}"
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                # 查找markdown文件
                markdown_files = [name for name in zip_file.namelist() if name.endswith('.md')]
                
                if not markdown_files:
                    return None, "ZIP中未找到Markdown文件"
                
                # 读取第一个markdown文件
                markdown_content = zip_file.read(markdown_files[0]).decode('utf-8')
                
                return {
                    "paper_id": paper_id,
                    "pdf_url": f"https://openreview.net/pdf?id={paper_id}",
                    "markdown_content": markdown_content,
                    "status": "success",
                    "markdown_file": markdown_files[0],
                    "content_length": len(markdown_content),
                    "processed_at": datetime.now().isoformat()
                }, None
                
        except Exception as e:
            return None, f"ZIP处理错误: {str(e)}"
    
    def process_single_paper(self, paper_id, pbar=None):
        """处理单个论文的完整流程"""
        try:
            # 更新进度条描述
            if pbar:
                pbar.set_description(f"处理 {paper_id}")
            
            # 提交任务
            task_id, error = self.submit_task(paper_id)
            if error:
                self.stats['errors'][f"提交失败: {error}"] += 1
                result = {
                    "paper_id": paper_id,
                    "status": "error",
                    "error": f"提交失败: {error}",
                    "processed_at": datetime.now().isoformat()
                }
                self._save_result(result)
                self.stats['failed'] += 1
                return False
            
            self.logger.info(f"已提交任务 {paper_id}: {task_id}")
            
            # 等待完成
            if pbar:
                pbar.set_description(f"等待 {paper_id}")
            
            result, error = self.wait_for_completion(task_id, paper_id)
            if error:
                self.stats['errors'][f"处理失败: {error}"] += 1
                result = {
                    "paper_id": paper_id,
                    "status": "error",
                    "error": error,
                    "task_id": task_id,
                    "processed_at": datetime.now().isoformat()
                }
                self._save_result(result)
                self.stats['failed'] += 1
                return False
            
            # 保存成功结果
            self._save_result(result)
            self.stats['successful'] += 1
            self.logger.info(f"成功处理 {paper_id}: {result['content_length']} 字符")
            return True
            
        except Exception as e:
            self.logger.error(f"处理异常 {paper_id}: {e}")
            self.stats['errors'][f"异常: {str(e)}"] += 1
            result = {
                "paper_id": paper_id,
                "status": "error",
                "error": f"处理异常: {str(e)}",
                "processed_at": datetime.now().isoformat()
            }
            self._save_result(result)
            self.stats['failed'] += 1
            return False
        finally:
            self.stats['completed'] += 1
            if pbar:
                pbar.update(1)
                pbar.set_postfix(
                    成功=self.stats['successful'],
                    失败=self.stats['failed'],
                    跳过=self.stats['skipped']
                )
    
    def process_papers(self, paper_ids):
        """批量处理论文，支持断点续传"""
        # 加载检查点
        completed_papers = self._load_checkpoint()
        
        # 过滤已完成的论文
        pending_papers = [pid for pid in paper_ids if pid not in completed_papers]
        
        self.stats['total'] = len(paper_ids)
        self.stats['skipped'] = len(completed_papers)
        self.stats['start_time'] = datetime.now().isoformat()
        
        if not pending_papers:
            self.logger.info("所有论文已处理完成！")
            return
        
        self.logger.info(f"总计: {len(paper_ids)} 篇论文")
        self.logger.info(f"已完成: {len(completed_papers)} 篇")
        self.logger.info(f"待处理: {len(pending_papers)} 篇")
        self.logger.info(f"结果保存到: {self.output_file}")
        
        # 创建进度条
        with tqdm(
            total=len(pending_papers),
            desc="批量处理",
            unit="篇",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}"
        ) as pbar:
            
            for paper_id in pending_papers:
                if self.should_stop:
                    self.logger.info("收到停止信号，保存进度...")
                    break
                
                success = self.process_single_paper(paper_id, pbar)
                
                # 定期保存检查点
                if self.stats['completed'] % 10 == 0:
                    self._save_checkpoint()
                
                # 出现错误时短暂休息
                if not success:
                    time.sleep(2)
        
        # 最终保存检查点
        self._save_checkpoint()
        self._print_final_stats()
    
    def _print_final_stats(self):
        """打印最终统计信息"""
        print("\n" + "="*60)
        print("📊 处理完成统计")
        print("="*60)
        print(f"总计论文: {self.stats['total']}")
        print(f"成功处理: {self.stats['successful']}")
        print(f"处理失败: {self.stats['failed']}")
        print(f"跳过已完成: {self.stats['skipped']}")
        print(f"实际处理: {self.stats['completed']}")
        
        if self.stats['start_time']:
            start_time = datetime.fromisoformat(self.stats['start_time'])
            duration = datetime.now() - start_time
            print(f"处理耗时: {duration}")
            
            if self.stats['successful'] > 0:
                avg_time = duration.total_seconds() / self.stats['successful']
                print(f"平均耗时: {avg_time:.1f}秒/篇")
        
        print(f"\n📁 结果文件: {self.output_file}")
        print(f"📁 日志文件: {self.log_file}")
        print(f"📁 检查点文件: {self.checkpoint_file}")
        
        # 显示错误统计
        if self.stats['errors']:
            print(f"\n❌ 错误统计:")
            for error_type, count in self.stats['errors'].items():
                print(f"  {error_type}: {count}")
        
        print("="*60)

def load_env():
    """从.env文件加载环境变量"""
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    return os.environ.get('API_TOKEN') or os.environ.get('API')

def main():
    # 加载API token
    api_token = load_env()
    if not api_token:
        print("❌ 未找到API token，请检查.env文件")
        return
    
    # 读取论文ID列表
    paper_ids_file = 'nips2024_reject_id.txt'
    if not os.path.exists(paper_ids_file):
        print(f"❌ 未找到论文ID文件: {paper_ids_file}")
        return
    
    with open(paper_ids_file, 'r') as f:
        paper_ids = [line.strip() for line in f if line.strip()]
    
    print(f"🚀 NIPS 2024 论文批量解析工具 v2.0")
    print(f"📄 找到 {len(paper_ids)} 个论文ID")
    
    # 创建处理器并开始处理
    processor = RobustPaperProcessor(api_token)
    processor.process_papers(paper_ids)

if __name__ == "__main__":
    main()