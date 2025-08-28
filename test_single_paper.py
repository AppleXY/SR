#!/usr/bin/env python3
import requests
import time
import json

# 需要在这里填入你的MinerU API Token
API_TOKEN = "YOUR_API_TOKEN_HERE"  # 请替换为实际的token

def test_single_paper():
    # 读取第一个论文ID进行测试
    with open('nips2024_reject_id.txt', 'r') as f:
        first_id = f.readline().strip()
    
    print(f"Testing with paper ID: {first_id}")
    
    # 构建OpenReview PDF URL
    pdf_url = f"https://openreview.net/pdf?id={first_id}"
    print(f"PDF URL: {pdf_url}")
    
    # 提交解析任务
    task_url = "https://mineru.net/api/v4/extract/task"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    task_data = {
        "url": pdf_url,
        "is_ocr": True,
        "enable_formula": True,
        "enable_table": True,
        "language": "en",  # 英文论文
        "data_id": first_id
    }
    
    print("Submitting task to MinerU API...")
    response = requests.post(task_url, headers=headers, json=task_data)
    
    if response.status_code != 200:
        print(f"Failed to submit task: {response.status_code}")
        print(response.text)
        return None
    
    result = response.json()
    print(f"Task submission response: {result}")
    
    if result.get("code") != 0:
        print(f"API error: {result.get('msg')}")
        return None
    
    task_id = result["data"]["task_id"]
    print(f"Task ID: {task_id}")
    
    # 轮询任务状态
    status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
    
    print("Waiting for task completion...")
    while True:
        status_response = requests.get(status_url, headers=headers)
        
        if status_response.status_code != 200:
            print(f"Failed to get task status: {status_response.status_code}")
            return None
        
        status_result = status_response.json()
        
        if status_result.get("code") != 0:
            print(f"Status API error: {status_result.get('msg')}")
            return None
        
        state = status_result["data"]["state"]
        print(f"Task state: {state}")
        
        if state == "done":
            full_zip_url = status_result["data"]["full_zip_url"]
            print(f"Task completed! ZIP URL: {full_zip_url}")
            
            # 下载并解析结果
            zip_response = requests.get(full_zip_url)
            if zip_response.status_code == 200:
                import zipfile
                import io
                
                # 解压ZIP内容
                with zipfile.ZipFile(io.BytesIO(zip_response.content)) as zip_file:
                    # 查找markdown文件
                    markdown_files = [name for name in zip_file.namelist() if name.endswith('.md')]
                    if markdown_files:
                        markdown_content = zip_file.read(markdown_files[0]).decode('utf-8')
                        print(f"Found markdown file: {markdown_files[0]}")
                        print(f"Content preview (first 500 chars):\n{markdown_content[:500]}...")
                        
                        # 保存结果为JSON格式
                        result_data = {
                            "paper_id": first_id,
                            "pdf_url": pdf_url,
                            "markdown_content": markdown_content,
                            "status": "success"
                        }
                        
                        return result_data
                    else:
                        print("No markdown file found in the ZIP")
                        return None
            else:
                print(f"Failed to download ZIP file: {zip_response.status_code}")
                return None
                
        elif state == "failed":
            err_msg = status_result["data"].get("err_msg", "Unknown error")
            print(f"Task failed: {err_msg}")
            return None
        elif state in ["pending", "running"]:
            if state == "running" and "extract_progress" in status_result["data"]:
                progress = status_result["data"]["extract_progress"]
                extracted = progress.get("extracted_pages", 0)
                total = progress.get("total_pages", 0)
                print(f"Progress: {extracted}/{total} pages")
            
            print("Waiting 10 seconds before next check...")
            time.sleep(10)
        else:
            print(f"Unknown state: {state}")
            time.sleep(10)

if __name__ == "__main__":
    if API_TOKEN == "YOUR_API_TOKEN_HERE":
        print("请在脚本中设置正确的API_TOKEN")
        exit(1)
    
    result = test_single_paper()
    if result:
        print("Test successful!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Test failed!")