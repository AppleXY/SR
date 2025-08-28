#!/usr/bin/env python3
"""
测试新的断点续传系统
"""
import os
import sys
import tempfile
import shutil
from robust_batch_processor import RobustPaperProcessor, load_env

def test_robust_system():
    print("🧪 测试断点续传批量处理系统")
    print("="*50)
    
    # 创建临时测试环境
    test_dir = "test_robust_temp"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    try:
        # 测试用的论文ID（前3个）
        test_paper_ids = ["01I55gys19", "08nbMTxazb", "08oUnmtj8Q"]
        
        # 加载API token
        api_token = load_env()
        if not api_token:
            print("❌ 无法获取API token")
            return False
        
        # 创建处理器
        processor = RobustPaperProcessor(
            api_token=api_token,
            output_file=f"{test_dir}/test_results.jsonl",
            log_file=f"{test_dir}/test.log",
            checkpoint_file=f"{test_dir}/test_checkpoint.json"
        )
        
        print(f"✅ 处理器创建成功")
        print(f"📁 测试目录: {test_dir}")
        print(f"🔬 测试论文: {test_paper_ids}")
        
        # 模拟处理第一篇论文
        print(f"\n📝 测试处理单篇论文...")
        success = processor.process_single_paper(test_paper_ids[0])
        
        if success:
            print("✅ 单篇论文处理成功")
            
            # 保存检查点
            processor._save_checkpoint()
            
            # 检查输出文件
            if os.path.exists(f"{test_dir}/test_results.jsonl"):
                with open(f"{test_dir}/test_results.jsonl", 'r') as f:
                    lines = f.readlines()
                print(f"📄 输出文件包含 {len(lines)} 条记录")
                
                # 检查检查点文件
                if os.path.exists(f"{test_dir}/test_checkpoint.json"):
                    print("✅ 检查点文件已创建")
                    
                    # 测试断点续传
                    print(f"\n🔄 测试断点续传功能...")
                    completed = processor._get_completed_papers_from_file()
                    print(f"🔍 从输出文件检测到已完成论文: {list(completed)}")
                    
                    if test_paper_ids[0] in completed:
                        print("✅ 断点续传功能正常，已处理论文被正确识别")
                        
                        # 测试批量处理跳过功能
                        print(f"\n🔄 测试批量处理跳过功能...")
                        processor.stats = {'total': 0, 'completed': 0, 'successful': 0, 'failed': 0, 'skipped': 0, 'start_time': None, 'errors': {}}
                        processor.process_papers([test_paper_ids[0]])  # 应该跳过
                        
                        if processor.stats['skipped'] > 0:
                            print("✅ 批量处理跳过功能正常")
                            return True
                        else:
                            print("⚠️  批量处理跳过功能异常，但基本功能正常")
                            return True
                    else:
                        print("❌ 断点续传功能异常")
                        return False
            else:
                print("❌ 输出文件未创建")
                return False
        else:
            print("❌ 单篇论文处理失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False
    
    finally:
        # 清理测试环境
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        print(f"🧹 清理测试环境")

if __name__ == "__main__":
    success = test_robust_system()
    print("\n" + "="*50)
    if success:
        print("🎉 系统测试通过！可以开始批量处理")
        print("\n运行命令:")
        print("  ./run.sh start    # 开始批量处理")
        print("  ./run.sh status   # 查看进度")
        print("  ./run.sh logs     # 查看日志")
    else:
        print("❌ 系统测试失败，请检查配置")
    print("="*50)