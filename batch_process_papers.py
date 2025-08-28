#!/usr/bin/env python3
import requests
import time
import json
import zipfile
import io
from tqdm import tqdm
import os
import concurrent.futures
from threading import Lock

# API Token - 支持.env文件、命令行参数或交互式输入
import sys

def load_env():
    """Load environment variables from .env file"""
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    return os.environ.get('API_TOKEN') or os.environ.get('API')

# 尝试从不同来源获取API Token
API_TOKEN = None

# 1. 先尝试从.env文件读取
API_TOKEN = load_env()

# 2. 如果没有，尝试命令行参数
if not API_TOKEN and len(sys.argv) > 1:
    API_TOKEN = sys.argv[1]

# 3. 最后尝试交互式输入
if not API_TOKEN:
    API_TOKEN = input("请输入你的MinerU API Token (或在.env文件中设置API_TOKEN): ").strip()

# 全局锁用于写入文件
write_lock = Lock()

class PaperProcessor:
    def __init__(self, api_token, output_file="processed_papers.jsonl"):
        self.api_token = api_token
        self.output_file = output_file
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        
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
                return None, f"HTTP {response.status_code}: {response.text}"
            
            result = response.json()
            if result.get("code") != 0:
                return None, result.get("msg", "Unknown API error")
            
            return result["data"]["task_id"], None
            
        except Exception as e:
            return None, str(e)
    
    def wait_for_completion(self, task_id, paper_id, max_wait_time=1800):  # 30分钟超时
        """等待任务完成并返回结果"""
        start_time = time.time()
        status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
        
        while time.time() - start_time < max_wait_time:
            try:
                response = requests.get(status_url, headers=self.headers, timeout=30)
                
                if response.status_code != 200:
                    return None, f"Status check failed: {response.status_code}"
                
                result = response.json()
                if result.get("code") != 0:
                    return None, f"Status API error: {result.get('msg')}"
                
                state = result["data"]["state"]
                
                if state == "done":
                    full_zip_url = result["data"]["full_zip_url"]
                    return self.download_and_extract(full_zip_url, paper_id)
                    
                elif state == "failed":
                    err_msg = result["data"].get("err_msg", "Unknown error")
                    return None, f"Task failed: {err_msg}"
                    
                # 等待状态：pending, running, converting
                time.sleep(15)  # 每15秒检查一次
                
            except Exception as e:
                return None, f"Status check exception: {str(e)}"
        
        return None, "Task timeout"
    
    def download_and_extract(self, zip_url, paper_id):
        """下载ZIP文件并提取markdown内容"""
        try:
            response = requests.get(zip_url, timeout=60)
            
            if response.status_code != 200:
                return None, f"Failed to download ZIP: {response.status_code}"
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                # 查找markdown文件
                markdown_files = [name for name in zip_file.namelist() if name.endswith('.md')]
                
                if not markdown_files:
                    return None, "No markdown file found in ZIP"
                
                # 读取第一个markdown文件
                markdown_content = zip_file.read(markdown_files[0]).decode('utf-8')
                
                return {
                    "paper_id": paper_id,
                    "pdf_url": f"https://openreview.net/pdf?id={paper_id}",
                    "markdown_content": markdown_content,
                    "status": "success",
                    "markdown_file": markdown_files[0]
                }, None
                
        except Exception as e:
            return None, f"ZIP processing error: {str(e)}"
    
    def process_single_paper(self, paper_id):
        """处理单个论文的完整流程"""
        # 提交任务
        task_id, error = self.submit_task(paper_id)
        if error:
            return {
                "paper_id": paper_id,
                "status": "error",
                "error": f"Submit failed: {error}"
            }
        
        # 等待完成
        result, error = self.wait_for_completion(task_id, paper_id)
        if error:
            return {
                "paper_id": paper_id,
                "status": "error", 
                "error": error,
                "task_id": task_id
            }
        
        return result
    
    def save_result(self, result):
        """线程安全地保存结果到JSONL文件"""
        with write_lock:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    def process_papers(self, paper_ids, max_workers=3):
        """批量处理论文"""
        print(f"开始处理 {len(paper_ids)} 篇论文...")
        print(f"结果将保存到: {self.output_file}")
        
        # 清空输出文件
        open(self.output_file, 'w').close()
        
        successful = 0
        failed = 0
        
        # 使用进度条
        with tqdm(total=len(paper_ids), desc="Processing papers") as pbar:
            # 使用线程池并行处理（但要控制并发数避免API限制）
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有任务
                future_to_paper = {
                    executor.submit(self.process_single_paper, paper_id): paper_id 
                    for paper_id in paper_ids
                }
                
                # 处理完成的任务
                for future in concurrent.futures.as_completed(future_to_paper):
                    paper_id = future_to_paper[future]
                    try:
                        result = future.result()
                        
                        # 保存结果
                        self.save_result(result)
                        
                        if result["status"] == "success":
                            successful += 1
                            pbar.set_postfix(success=successful, failed=failed)
                        else:
                            failed += 1
                            print(f"\nFailed {paper_id}: {result.get('error', 'Unknown error')}")
                            pbar.set_postfix(success=successful, failed=failed)
                            
                    except Exception as e:
                        failed += 1
                        error_result = {
                            "paper_id": paper_id,
                            "status": "error",
                            "error": f"Processing exception: {str(e)}"
                        }
                        self.save_result(error_result)
                        print(f"\nException processing {paper_id}: {str(e)}")
                        pbar.set_postfix(success=successful, failed=failed)
                    
                    pbar.update(1)
        
        print(f"\n处理完成!")
        print(f"成功: {successful}")
        print(f"失败: {failed}")
        print(f"结果保存在: {self.output_file}")
        
        return successful, failed

def main():
    if not API_TOKEN:
        print("未提供API Token")
        return
    
    # 读取论文ID列表
    with open('nips2024_reject_id.txt', 'r') as f:
        paper_ids = [line.strip() for line in f if line.strip()]
    
    print(f"找到 {len(paper_ids)} 个论文ID")
    
    # 创建处理器
    processor = PaperProcessor(API_TOKEN)
    
    # 开始批量处理
    processor.process_papers(paper_ids, max_workers=3)  # 控制并发数避免API限制

if __name__ == "__main__":
    main()