# 教程：Claude Code + LM Studio 免费使用本地模型

> 来源：微信公众号"Dom AI 驾驶舱"
> 作者：DomCockpit
> 发布时间：2026-04-09
> 链接：https://mp.weixin.qq.com/s/BTk__lhK7Av2pT_e9ygJ4Q

## 核心工具

- **LM Studio** — 本地模型运行器
- **Claude Code** — AI 编程代理
- **推荐模型**：Qwen 3.5 9B（Q4_K_M 或 Q5_K_M）

## 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| 内存 | 16GB | 24GB+ |
| 处理器 | Apple Silicon | M4 Mini / M3 Pro |
| 系统 | macOS 12.0+ | macOS 14+ |

## 安装配置

### 1. 安装 LM Studio

从 https://lmstudio.ai/ 下载安装。

### 2. 下载模型

在 LM Studio 内搜索 Qwen 3.5 9B，下载 Q4_K_M 量化版（~6-8GB）。

### 3. 启动本地服务器

在 Developer 标签页 → Local Server → Start Server（默认 `http://127.0.0.1:1234`）

Server Settings 优化建议：
- Context Length: 32768
- GPU Offload: 32-48 layers
- CPU Thread Pool: 7-8
- Max Concurrent Requests: 4-8

## 连接 Claude Code

```bash
# 设置环境变量
export ANTHROPIC_BASE_URL=http://127.0.0.1:1234/v1
export ANTHROPIC_API_KEY=local-key

# 启动 Claude Code
claude
```

## 常用命令

```bash
# 直接对话
claude "你好"

# 交互模式
claude --interactive

# 代码生成
claude "请用 Python 写一个快速排序算法"

# 文档分析
claude "请总结这篇文章" < article.txt

# 管道操作
cat code.py | claude "请检查代码 bug"
```

## 推理参数调整

```bash
claude "写一首诗" --temperature 0.8 --max-tokens 500
```

- `--temperature`: 0.7-0.9（创意）/ 0.2-0.5（事实）
- `--max-tokens`: 回复最大长度
- `--top-p`: 核采样参数（推荐 0.9）

## 创建快捷别名


<!-- processed: 2026-06-23 → Wiki/sources/Claude Code + LM Studio Tutorial.md + Wiki/entities/LM Studio.md + Wiki/concepts/Local LLM Deployment.md -->
