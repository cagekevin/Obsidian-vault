---
type: source
title: "Claude Code + LM Studio Local Model Tutorial"
source_url: "https://mp.weixin.qq.com/s/BTk__lhK7Av2pT_e9ygJ4Q"
fetched: 2026-06-21
tags:
  - source
  - tutorial
  - lm-studio
  - claude-code
  - local-model
status: ingested
related:
  - "[[LM Studio]]"
  - "[[Claude Code Local Setup]]"
  - "[[Local LLM Deployment]]"
---

# Claude Code + LM Studio Local Model Tutorial

> Source: `.raw/LMStudio教程.md` — from WeChat public account "Dom AI 驾驶舱" by DomCockpit

A guide for running Claude Code with LM Studio local models.

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 16GB | 24GB+ |
| Processor | Apple Silicon | M4 Mini / M3 Pro |
| System | macOS 12.0+ | macOS 14+ |

## Setup

1. Install LM Studio from lmstudio.ai
2. Download Qwen 3.5 9B (Q4_K_M or Q5_K_M, ~6-8GB)
3. Start local server at `http://127.0.0.1:1234`
4. Set env vars: `ANTHROPIC_BASE_URL=http://127.0.0.1:1234/v1` + `ANTHROPIC_API_KEY=local-key`

## Server Settings

- Context Length: 32768
- GPU Offload: 32-48 layers
- CPU Thread Pool: 7-8
- Max Concurrent Requests: 4-8
