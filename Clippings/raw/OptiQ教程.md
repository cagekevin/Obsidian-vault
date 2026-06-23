# 教程：Mac 本地部署 Qwen3.5-9B-OptiQ-4bit 接入 Claude Code

> 来源：微信公众号"玩AI的老章"
> 链接：https://mp.weixin.qq.com/s/ayqUwPbqGtMuGWdpmjH6Gw

## 核心工具

- **mlx-optiq** — 按层下刀的混合精度量化工具
- **模型**：`mlx-community/Qwen3.5-9B-OptiQ-4bit`（6.6 GB）
- **硬件**：16 GB 以上 Apple Silicon Mac

## 安装

```bash
# 最小化安装（纯推理）
pip install mlx-lm

# 完整安装（含 Claude Code 接入、KV cache、LoRA 微调、Web UI）
pip install mlx-optiq
```

要求：Python ≥ 3.11、Apple Silicon Mac、mlx-lm ≥ 0.30

## 将本地模型接入 Claude Code

### 启动本地模型服务

```bash
optiq serve --model mlx-community/Qwen3.5-9B-OptiQ-4bit --port 8080
```

可选 MTP 加速 decode：
```bash
optiq serve --model mlx-community/Qwen3.5-9B-OptiQ-4bit --port 8080 --mtp
```

### 设置环境变量

```bash
export ANTHROPIC_BASE_URL="http://localhost:8080"
export ANTHROPIC_API_KEY="not-used"
claude
```

**关键点**：`optiq serve` 同时支持 OpenAI 和 Anthropic 双协议，Claude Code 直接可用。

## 混合精度 KV Cache（长上下文优化）

```bash
# 先跑一次 KV 敏感度分析
optiq kv-cache mlx-community/Qwen3.5-9B-OptiQ-4bit --target-bits 5.0 -o ./kv

# 启动带 KV cache 的服务
optiq serve --model mlx-community/Qwen3.5-9B-OptiQ-4bit \
    --kv-config ./kv/kv_config.json \
    --port 8080 \
    --max-tokens 32768 --temp 0.6 --top-p 0.95
```

## 采样参数推荐

- 推理类：`temp=0.6, top_p=0.95, top_k=20`

<!-- processed: 2026-06-23 → Wiki/sources/OptiQ Tutorial.md + Wiki/entities/OptiQ.md + Wiki/concepts/Model Quantization.md -->
