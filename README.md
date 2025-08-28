# NIPS 2024 论文批量解析工具

这个工具用于批量解析NIPS 2024拒稿论文，使用MinerU API将PDF转换为Markdown格式。

## 文件说明

- `MINERU_API.md` - MinerU API文档
- `nips2024_reject_id.txt` - 包含268个论文ID的文件
- `test_single_paper.py` - 单个论文解析测试脚本
- `batch_process_papers.py` - 批量处理脚本
- `requirements.txt` - Python依赖包

## 使用步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置API Token

在使用脚本之前，需要获取MinerU API的token，然后在脚本中替换 `YOUR_API_TOKEN_HERE`。

### 3. 测试单个论文解析

首先运行测试脚本验证工作流程：

```bash
python test_single_paper.py
```

这将：
- 读取第一个论文ID (01I55gys19)
- 构建OpenReview PDF URL: https://openreview.net/pdf?id=01I55gys19
- 提交到MinerU API进行解析
- 等待处理完成
- 下载并解析结果

### 4. 批量处理所有论文

确认测试成功后，运行批量处理脚本：

```bash
python batch_process_papers.py
```

这将：
- 处理所有268个论文ID
- 显示实时进度条
- 使用3个并发线程（可调整）
- 将结果保存到 `processed_papers.jsonl`

## 输出格式

结果保存为JSONL格式，每行一个JSON对象：

```json
{
  "paper_id": "01I55gys19",
  "pdf_url": "https://openreview.net/pdf?id=01I55gys19",
  "markdown_content": "# 论文标题\n\n## 摘要\n...",
  "status": "success",
  "markdown_file": "example.md"
}
```

对于失败的情况：
```json
{
  "paper_id": "xxxxx",
  "status": "error",
  "error": "错误描述"
}
```

## 注意事项

1. **API限制**: MinerU API有使用限制，建议控制并发数
2. **超时设置**: 每个任务最大等待30分钟
3. **错误处理**: 脚本会跳过失败的论文并继续处理其他论文
4. **文件大小**: PDF文件不能超过200MB，页数不能超过600页

## 监控进度

脚本运行时会显示：
- 实时进度条
- 成功/失败计数
- 失败论文的错误信息

处理完成后会显示总结信息。