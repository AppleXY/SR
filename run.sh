#!/bin/bash

# NIPS 2024 论文批量解析运行脚本
# 支持断点续传和优雅退出

set -e  # 遇到错误立即退出

# 脚本配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_SCRIPT="robust_batch_processor.py"
LOG_FILE="processing.log"
OUTPUT_FILE="nips2024_papers.jsonl"
CHECKPOINT_FILE="checkpoint.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# 打印标题
print_header() {
    echo ""
    print_color $BLUE "=================================="
    print_color $BLUE "$1"
    print_color $BLUE "=================================="
    echo ""
}

# 显示帮助信息
show_help() {
    print_header "NIPS 2024 论文批量解析工具 v2.0"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  start     - 开始/继续批量处理"
    echo "  status    - 查看当前进度"
    echo "  clean     - 清理所有文件（谨慎使用）"
    echo "  logs      - 查看实时日志"
    echo "  help      - 显示此帮助信息"
    echo ""
    echo "文件说明:"
    echo "  $OUTPUT_FILE  - 输出结果文件（JSONL格式）"
    echo "  $LOG_FILE      - 日志文件"
    echo "  $CHECKPOINT_FILE    - 检查点文件（用于断点续传）"
    echo ""
}

# 检查依赖
check_dependencies() {
    print_color $CYAN "🔍 检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_color $RED "❌ 未找到 python3"
        exit 1
    fi
    
    # 检查必要文件
    local required_files=("nips2024_reject_id.txt" ".env" "$PYTHON_SCRIPT")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            print_color $RED "❌ 未找到必要文件: $file"
            exit 1
        fi
    done
    
    # 检查Python包
    python3 -c "import requests, tqdm" 2>/dev/null || {
        print_color $YELLOW "⚠️  安装Python依赖包..."
        pip install requests tqdm
    }
    
    print_color $GREEN "✅ 依赖检查通过"
}

# 显示进度状态
show_status() {
    print_header "📊 当前进度状态"
    
    # 检查输出文件
    if [[ -f "$OUTPUT_FILE" ]]; then
        local processed_count=$(wc -l < "$OUTPUT_FILE" 2>/dev/null || echo "0")
        print_color $GREEN "已处理论文: $processed_count 篇"
        
        # 统计成功和失败
        local success_count=$(grep -c '"status": "success"' "$OUTPUT_FILE" 2>/dev/null || echo "0")
        local error_count=$(grep -c '"status": "error"' "$OUTPUT_FILE" 2>/dev/null || echo "0")
        
        print_color $GREEN "  └─ 成功: $success_count 篇"
        print_color $RED "  └─ 失败: $error_count 篇"
    else
        print_color $YELLOW "尚未开始处理"
    fi
    
    # 检查检查点文件
    if [[ -f "$CHECKPOINT_FILE" ]]; then
        print_color $CYAN "📁 检查点文件存在，支持断点续传"
        local checkpoint_info=$(python3 -c "
import json
try:
    with open('$CHECKPOINT_FILE', 'r') as f:
        data = json.load(f)
    print(f'最后更新: {data.get(\"timestamp\", \"未知\")}')
    print(f'统计信息: 成功={data.get(\"stats\", {}).get(\"successful\", 0)}, 失败={data.get(\"stats\", {}).get(\"failed\", 0)}')
except:
    print('检查点文件读取失败')
" 2>/dev/null)
        echo "$checkpoint_info"
    fi
    
    # 显示总论文数
    local total_papers=$(wc -l < "nips2024_reject_id.txt" 2>/dev/null || echo "0")
    print_color $BLUE "📄 总计论文: $total_papers 篇"
    
    echo ""
}

# 开始处理
start_processing() {
    print_header "🚀 开始批量处理"
    
    check_dependencies
    
    # 显示启动信息
    print_color $CYAN "📅 启动时间: $(date '+%Y-%m-%d %H:%M:%S')"
    print_color $CYAN "📁 工作目录: $SCRIPT_DIR"
    print_color $CYAN "📝 日志文件: $LOG_FILE"
    print_color $CYAN "💾 输出文件: $OUTPUT_FILE"
    echo ""
    
    # 设置信号处理
    trap 'print_color $YELLOW "🛑 收到中断信号，正在优雅退出..."; exit 0' INT TERM
    
    # 启动主处理脚本
    print_color $GREEN "🏃 启动处理程序..."
    echo ""
    
    python3 "$PYTHON_SCRIPT"
    
    local exit_code=$?
    echo ""
    
    if [[ $exit_code -eq 0 ]]; then
        print_color $GREEN "🎉 处理完成！"
    else
        print_color $YELLOW "⚠️  处理中断或出现错误（退出码: $exit_code）"
        print_color $CYAN "💡 可以重新运行此脚本继续处理"
    fi
    
    echo ""
    show_status
}

# 查看实时日志
view_logs() {
    print_header "📋 实时日志查看"
    
    if [[ ! -f "$LOG_FILE" ]]; then
        print_color $YELLOW "日志文件不存在"
        return
    fi
    
    print_color $CYAN "按 Ctrl+C 退出日志查看"
    echo ""
    
    tail -f "$LOG_FILE"
}

# 清理文件
clean_files() {
    print_header "🧹 清理文件"
    
    print_color $YELLOW "⚠️  这将删除以下文件："
    echo "  - $OUTPUT_FILE"
    echo "  - $LOG_FILE" 
    echo "  - $CHECKPOINT_FILE"
    echo "  - test_result_*.json"
    echo "  - sample_test_results.jsonl"
    echo ""
    
    read -p "确定要继续吗？(y/N) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "$OUTPUT_FILE" "$LOG_FILE" "$CHECKPOINT_FILE"
        rm -f test_result_*.json sample_test_results.jsonl
        print_color $GREEN "✅ 清理完成"
    else
        print_color $CYAN "取消清理"
    fi
}

# 主逻辑
main() {
    case "${1:-start}" in
        "start")
            start_processing
            ;;
        "status")
            show_status
            ;;
        "logs")
            view_logs
            ;;
        "clean")
            clean_files
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_color $RED "❌ 未知选项: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"