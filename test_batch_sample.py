#!/usr/bin/env python3
"""
测试批量处理脚本处理前几篇论文
"""
import os
import sys

# 添加当前目录到路径，以便导入batch_process_papers模块
sys.path.append('.')

# 修改batch_process_papers.py中的main函数，只处理前3篇论文进行测试
def test_sample_processing():
    # 读取前3个论文ID
    with open('nips2024_reject_id.txt', 'r') as f:
        all_paper_ids = [line.strip() for line in f if line.strip()]
    
    # 只取前3个进行测试
    sample_paper_ids = all_paper_ids[:3]
    print(f"测试处理前3篇论文: {sample_paper_ids}")
    
    # 导入并修改批量处理类
    from batch_process_papers import PaperProcessor, load_env
    
    # 加载API token
    api_token = load_env()
    if not api_token:
        print("无法获取API token")
        return
    
    # 创建处理器
    processor = PaperProcessor(api_token, output_file="sample_test_results.jsonl")
    
    # 处理样本论文
    successful, failed = processor.process_papers(sample_paper_ids, max_workers=2)
    
    print(f"\n测试完成!")
    print(f"成功: {successful}")  
    print(f"失败: {failed}")
    
    # 检查结果文件
    if os.path.exists("sample_test_results.jsonl"):
        with open("sample_test_results.jsonl", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"结果文件包含 {len(lines)} 条记录")
        
        # 显示每条记录的概要
        import json
        for i, line in enumerate(lines):
            try:
                record = json.loads(line)
                status = record.get('status', 'unknown')
                paper_id = record.get('paper_id', 'unknown')
                if status == 'success':
                    content_len = len(record.get('markdown_content', ''))
                    print(f"  记录 {i+1}: {paper_id} - 成功 ({content_len} 字符)")
                else:
                    error = record.get('error', 'unknown error')
                    print(f"  记录 {i+1}: {paper_id} - 失败 ({error})")
            except json.JSONDecodeError:
                print(f"  记录 {i+1}: JSON解析错误")
    else:
        print("未找到结果文件")

if __name__ == "__main__":
    test_sample_processing()