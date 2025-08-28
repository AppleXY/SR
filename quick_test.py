#!/usr/bin/env python3
import requests
import time
import json

# 请在这里填入你的MinerU API Token
API_TOKEN = input("请输入你的MinerU API Token: ").strip()

def quick_test():
    # 使用第一个论文ID进行测试
    paper_id = "01I55gys19"
    pdf_url = f"https://openreview.net/pdf?id={paper_id}"
    
    print(f"Testing paper: {paper_id}")
    print(f"PDF URL: {pdf_url}")
    
    # 验证PDF可访问
    print("1. 验证PDF可访问性...")
    try:
        response = requests.head(pdf_url, timeout=10)
        print(f"   PDF状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"   警告: PDF可能无法访问")
    except Exception as e:
        print(f"   PDF访问测试失败: {e}")
        return False
    
    # 提交MinerU任务
    print("2. 提交MinerU解析任务...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
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
        response = requests.post(
            "https://mineru.net/api/v4/extract/task",
            headers=headers,
            json=task_data,
            timeout=30
        )
        
        print(f"   API响应状态码: {response.status_code}")
        result = response.json()
        print(f"   API响应内容: {json.dumps(result, indent=2)}")
        
        if result.get("code") != 0:
            print(f"   错误: {result.get('msg')}")
            return False
        
        task_id = result["data"]["task_id"]
        print(f"   任务ID: {task_id}")
        
    except Exception as e:
        print(f"   任务提交失败: {e}")
        return False
    
    # 检查任务状态
    print("3. 检查任务状态...")
    status_url = f"https://mineru.net/api/v4/extract/task/{task_id}"
    
    for i in range(3):  # 只检查3次，不等待完成
        try:
            response = requests.get(status_url, headers=headers, timeout=30)
            result = response.json()
            
            state = result["data"]["state"]
            print(f"   第{i+1}次检查 - 状态: {state}")
            
            if state == "done":
                print(f"   任务已完成! ZIP URL: {result['data']['full_zip_url']}")
                break
            elif state == "failed":
                print(f"   任务失败: {result['data'].get('err_msg')}")
                return False
            elif state in ["pending", "running"]:
                if i < 2:  # 不是最后一次
                    print(f"   等待5秒后再次检查...")
                    time.sleep(5)
            
        except Exception as e:
            print(f"   状态检查失败: {e}")
            return False
    
    print("\n✅ 快速测试完成!")
    print("如果看到任务已提交且状态正常，说明工作流程可以正常运行。")
    print("现在可以运行完整的批量处理脚本。")
    return True

if __name__ == "__main__":
    if not API_TOKEN:
        print("未提供API Token，退出测试")
        exit(1)
    
    success = quick_test()
    if success:
        print("\n可以开始批量处理了！")
        print("运行: python3 batch_process_papers.py")
    else:
        print("\n测试失败，请检查API Token或网络连接")