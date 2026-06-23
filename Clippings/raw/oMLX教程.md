# 教程：用 oMLX 跑 Qwen3.6-27B 接入 Claude Code

> 来源：微信公众号"朱攀"
> 链接：https://mp.weixin.qq.com/s/THJsVVM2D9AB5Wn7yYHZ7w

## 核心工具

- **oMLX** — 为 Apple Silicon 优化的本地推理引擎
- **模型**：Qwen3.6-27B（MLX 格式）
- **硬件**：Apple Silicon（M1-M4），macOS 15.0+

## 安装 oMLX

```bash
# Homebrew 安装
brew tap jundot/omlx https://github.com/jundot/omlx
brew install omlx
brew services start omlx
```

## 启动服务

```bash
omlx serve --model-dir ~/models
```

默认端口 8000。

## 下载模型

浏览器打开 `http://localhost:8000/admin`，在模型下载器中搜索并下载。

## 连接 Claude Code

```bash
export ANTHROPIC_MODEL="Qwen3.6-27B-8bit"
export ANTHROPIC_SMALL_FAST_MODEL="Qwen3.6-27B-8bit"
export ANTHROPIC_BASE_URL="http://localhost:8000"
export ANTHROPIC_AUTH_TOKEN="<your_api_key>"
claude
```

**关键点**：模型名必须与下载的文件夹名完全一致；`ANTHROPIC_AUTH_TOKEN` 设任意值。

## 调优参数

```bash
# 内存限制
omlx serve --model-dir ~/models --max-process-memory 80%

# SSD 缓存（长上下文）
omlx serve --model-dir ~/models --paged-ssd-cache-dir ~/.omlx/cache

# 国内镜像
omlx serve --model-dir ~/models --hf-endpoint https://hf-mirror.com
```
<!-- processed: 2026-06-23 → Wiki/sources/oMLX Tutorial.md + Wiki/entities/oMLX.md + Wiki/concepts/Apple Silicon Optimization.md -->
