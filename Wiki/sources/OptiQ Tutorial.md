---
type: source
title: "OptiQ + Claude Code Local Model Tutorial"
source_url: "https://mp.weixin.qq.com/s/ayqUwPbqGtMuGWdpmjH6Gw"
fetched: 2026-06-21
tags:
  - source
  - tutorial
  - optiq
  - claude-code
  - local-model
  - quantization
status: ingested
related:
  - "[[OptiQ]]"
  - "[[Claude Code Local Setup]]"
  - "[[Local LLM Deployment]]"
  - "[[Apple Silicon Optimization]]"
  - "[[Model Quantization]]"
---

# OptiQ + Claude Code Local Model Tutorial

> Source: `.raw/OptiQ教程.md` — from WeChat public account "玩AI的老章"

OptiQ (mlx-optiq) is a mixed-precision quantization tool that applies different bit-widths per layer. It enables running Qwen3.5-9B on Apple Silicon Macs with 16GB+ RAM.

## Setup

```bash
# Minimal (inference only)
pip install mlx-lm

# Full (Claude Code, KV cache, LoRA, Web UI)
pip install mlx-optiq
```

Requirements: Python ≥ 3.11, Apple Silicon Mac, mlx-lm ≥ 0.30

## Running

```bash
optiq serve --model mlx-community/Qwen3.5-9B-OptiQ-4bit --port 8080
# With MTP acceleration:
optiq serve --model mlx-community/Qwen3.5-9B-OptiQ-4bit --port 8080 --mtp
```

Model size: 6.6 GB (Q4_K_M quantization)

## Claude Code Connection

```bash
export ANTHROPIC_BASE_URL="http://localhost:8080"
export ANTHROPIC_API_KEY="not-used"
claude
```

Key point: `optiq serve` supports both OpenAI and Anthropic protocols simultaneously.

## Sampling Parameters

- Reasoning: `temp=0.6, top_p=0.95, top_k=20`
- Chat: `temp=0.7, top_p=0.9`
