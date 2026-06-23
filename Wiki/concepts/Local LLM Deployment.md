---
type: concept
title: "Local LLM Deployment"
complexity: intermediate
domain: local-llm
aliases:
  - "本地模型部署"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - local-llm
  - deployment
status: developing
related:
  - "[[Ollama]]"
  - "[[LM Studio]]"
  - "[[oMLX]]"
  - "[[OptiQ]]"
  - "[[Antigravity Tools]]"
  - "[[Claude Code Local Setup]]"
  - "[[Anthropic Compatible API]]"
  - "[[Apple Silicon Optimization]]"
  - "[[Model Quantization]]"
sources:
  - "[[sources/Ollama Official Documentation]]"
  - "[[sources/Antigravity Tools]]"
---

# Local LLM Deployment

Running large language models locally on personal hardware, as opposed to relying on cloud API services. This covers the full ecosystem of tools, models, and integration patterns.

## Ecosystem Overview

### Local Runtimes

| Tool | Platform | Strengths |
|------|----------|-----------|
| [[Ollama]] | macOS, Windows, Linux | Easiest setup, Claude Code integration, API compatibility |
| [[LM Studio]] | macOS, Windows | GUI-first, model browser, server mode |
| [[oMLX]] | Apple Silicon only | MLX-optimized, efficient on M-series chips |
| [[OptiQ]] | Apple Silicon only | Mixed-precision quantization for memory efficiency |

### API Proxy to Cloud

| Tool | Backend | Purpose |
|------|---------|---------|
| [[Antigravity Tools]] | Tencent Cloud Copilot | Local proxy to cloud models (15 models, 4 vendors) |

## Common Integration Pattern

All local runtimes connect to Claude Code / other AI tools via environment variables:

```bash
export ANTHROPIC_BASE_URL=http://localhost:<PORT>
export ANTHROPIC_AUTH_TOKEN=<token>  # or ANTHROPIC_API_KEY
claude
```

## Model Recommendations by Hardware

| Hardware | Recommended Model | Runtime |
|----------|------------------|---------|
| 16GB RAM | Qwen3.5-9B (OptiQ 4bit) | OptiQ / Ollama |
| 16-32GB RAM | qwen3-coder:7b / gemma2:9b | Ollama |
| M high-end / RTX 4090 | qwen3-coder:30b / GLM-4 | Ollama / LM Studio |
| Any (cloud) | deepseek-v4-flash / glm-5 | Antigravity Tools |

## Connections

- [[Ollama]] — primary local runner used by Kevin
- [[Claude Code Local Setup]] — how all these tools connect to Claude Code
- [[Anthropic Compatible API]] — the protocol bridge
- [[Model Quantization]] — techniques for running larger models on limited hardware
- [[Apple Silicon Optimization]] — M-series specific optimizations (MLX, oMLX)
