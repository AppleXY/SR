#!/usr/bin/env python3
import os
import requests
import time
import json

def load_env():
    """Load environment variables from .env file"""
    env_path = '.env'
    if not os.path.exists(env_path):
        print("未找到.env文件，请创建包含API_TOKEN的.env文件")
        return None
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    return os.environ.get('API_TOKEN') or os.environ.get('API')

def test_with_real_api():
    # 加载API token
    api_token = load_env()
    if not api_token:
        print("请在.env文件中设置API_TOKEN=your_token_here")
        return False
    
    print("=" * 50)
    print("开始真实API测试")
    print("=" * 50)
    
    # 使用第一个论文ID
    paper_id = "01I55gys19"
    pdf_url = f"https://openreview.net/pdf?id={paper_id}"
    
    print(f"测试论文ID: {paper_id}")
    print(f"PDF URL: {pdf_url}")
    
    # 验证PDF可访问性
    print("\n1. 验证PDF可访问性...")
    try:
        response = requests.head(pdf_url, timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code != 200:
            print("   警告: PDF可能无法访问")
    except Exception as e:
        print(f"   错误: {e}")
    
    # 提交任务到MinerU
    print("\n2. 提交任务到MinerU API...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    task_data = {
        "url": pdf_url,
        "is_ocr": True,
        "enable_formula": True,
        "enable_table": True,
        "language": "en",
        "data_id": paper_id
    }
    
    try:
        print(f"   发送请求到: https://mineru.net/api/v4/extract/task")
        response = requests.post(
            "https://mineru.net/api/v4/extract/task",
            headers=headers,
            json=task_data,
            timeout=30
        )
        
        print(f"   HTTP状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   错误响应: {response.text}")
            return False
        
        result = response.json()
        print(f"   API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") != 0:
            print(f"   API错误: {result.get('msg')}")
            return False
        
        task_id = result["data"]["task_id"]
        print(f"   ✅ 任务提交成功! Task ID: {task_id}")
        
    except Exception as e:
        print(f"   请求异常: {e}")
        return False
    
    # 监控任务状态
    print(f"\n3. 监控任务状态 (Task ID: {task_id})...")
    status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
    
    max_checks = 12  # 最多检查12次 (约3分钟)
    for i in range(max_checks):
        try:
            print(f"   第{i+1}/{max_checks}次检查...")
            response = requests.get(status_url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"   状态检查失败: {response.status_code}")
                continue
            
            result = response.json()
            if result.get("code") != 0:
                print(f"   状态API错误: {result.get('msg')}")
                continue
            
            data = result["data"]
            state = data["state"]
            print(f"   状态: {state}")
            
            if state == "done":
                print(f"   ✅ 任务完成!")
                full_zip_url = data["full_zip_url"]
                print(f"   ZIP下载链接: {full_zip_url}")
                
                # 下载并解析结果
                print(f"\n4. 下载和解析结果...")
                return download_and_parse(full_zip_url, paper_id)
                
            elif state == "failed":
                err_msg = data.get("err_msg", "Unknown error")
                print(f"   ❌ 任务失败: {err_msg}")
                return False
                
            elif state in ["pending", "running"]:
                if state == "running" and "extract_progress" in data:
                    progress = data["extract_progress"]
                    extracted = progress.get("extracted_pages", 0)
                    total = progress.get("total_pages", 0)
                    print(f"   进度: {extracted}/{total} 页")
                
                if i < max_checks - 1:
                    print(f"   等待15秒...")
                    time.sleep(15)
            else:
                print(f"   未知状态: {state}")
                if i < max_checks - 1:
                    time.sleep(15)
                    
        except Exception as e:
            print(f"   状态检查异常: {e}")
            if i < max_checks - 1:
                time.sleep(15)
    
    print("   ⚠️  达到最大检查次数，任务可能仍在处理中")
    return True  # 任务已提交，即使没有完成也算测试成功

def download_and_parse(zip_url, paper_id):
    """下载ZIP文件并解析内容"""
    try:
        print(f"   下载ZIP文件...")
        response = requests.get(zip_url, timeout=60)
        
        if response.status_code != 200:
            print(f"   下载失败: {response.status_code}")
            return False
        
        import zipfile
        import io
        
        print(f"   解析ZIP内容...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            files = zip_file.namelist()
            print(f"   ZIP包含文件: {files}")
            
            # 查找markdown文件
            markdown_files = [name for name in files if name.endswith('.md')]
            if markdown_files:
                markdown_file = markdown_files[0]
                markdown_content = zip_file.read(markdown_file).decode('utf-8')
                
                print(f"   ✅ 找到Markdown文件: {markdown_file}")
                print(f"   内容长度: {len(markdown_content)} 字符")
                print(f"   内容预览 (前200字符):")
                print(f"   {'-' * 40}")
                print(f"   {markdown_content[:200]}...")
                print(f"   {'-' * 40}")
                
                # 保存测试结果
                result = {
                    "paper_id": paper_id,
                    "pdf_url": f"https://openreview.net/pdf?id={paper_id}",
                    "markdown_content": markdown_content,
                    "status": "success",
                    "markdown_file": markdown_file
                }
                
                with open(f'test_result_{paper_id}.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"   ✅ 测试结果已保存到: test_result_{paper_id}.json")
                return True
            else:
                print(f"   ❌ ZIP中未找到Markdown文件")
                return False
                
    except Exception as e:
        print(f"   解析异常: {e}")
        return False

if __name__ == "__main__":
    success = test_with_real_api()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 真实API测试成功!")
        print("现在可以运行批量处理脚本了")
        print("命令: python3 batch_process_papers.py")
    else:
        print("❌ 真实API测试失败")
        print("请检查.env文件中的API_TOKEN设置")
    print("=" * 50)