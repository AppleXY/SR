#!/usr/bin/env python3
"""
演示脚本：展示NIPS 2024论文批量解析的完整工作流程
"""
import os

def main():
    print("=" * 60)
    print("NIPS 2024 论文批量解析工具演示")
    print("=" * 60)
    
    # 检查文件是否存在
    required_files = [
        'MINERU_API.md',
        'nips2024_reject_id.txt',
        'test_single_paper.py',
        'batch_process_papers.py',
        'quick_test.py',
        'requirements.txt'
    ]
    
    print("\n1. 检查必要文件...")
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n缺少文件: {missing_files}")
        return
    
    # 读取论文ID数量
    print("\n2. 检查论文ID数据...")
    with open('nips2024_reject_id.txt', 'r') as f:
        paper_ids = [line.strip() for line in f if line.strip()]
    
    print(f"   找到 {len(paper_ids)} 个论文ID")
    print(f"   第一个ID: {paper_ids[0]}")
    print(f"   对应URL: https://openreview.net/pdf?id={paper_ids[0]}")
    
    # 显示工作流程
    print("\n3. 工作流程说明:")
    print("   步骤1: 运行快速测试")
    print("   命令: python3 quick_test.py")
    print("   作用: 验证API token和网络连接")
    print()
    print("   步骤2: 批量处理所有论文")
    print("   命令: python3 batch_process_papers.py [可选:API_TOKEN]")
    print("   作用: 处理所有268个论文，保存为JSONL格式")
    
    # 显示API说明
    print("\n4. MinerU API 参数设置:")
    print("   - is_ocr: True (启用OCR)")
    print("   - enable_formula: True (启用公式识别)")
    print("   - enable_table: True (启用表格识别)")
    print("   - language: en (英文)")
    print("   - 最大文件大小: 200MB")
    print("   - 最大页数: 600页")
    print("   - 超时时间: 30分钟/论文")
    
    # 显示输出格式
    print("\n5. 输出格式 (JSONL):")
    print("   成功案例:")
    print("   {")
    print('     "paper_id": "01I55gys19",')
    print('     "pdf_url": "https://openreview.net/pdf?id=01I55gys19",')
    print('     "markdown_content": "# 论文标题\\n\\n## 摘要\\n...",')
    print('     "status": "success",')
    print('     "markdown_file": "example.md"')
    print("   }")
    print()
    print("   失败案例:")
    print("   {")
    print('     "paper_id": "xxxxx",')
    print('     "status": "error",')
    print('     "error": "错误描述"')
    print("   }")
    
    print("\n6. 性能参数:")
    print("   - 并发数: 3 (避免API限制)")
    print("   - 状态检查间隔: 15秒")
    print("   - 估计总时间: 2-4小时 (268个论文)")
    
    print("\n" + "=" * 60)
    print("准备开始测试！")
    print("首先运行: python3 quick_test.py")
    print("=" * 60)

if __name__ == "__main__":
    main()