---
type: concept
title: "Ollama"
complexity: intermediate
domain: local-llm
aliases:
  - "Ollama Local Model Runner"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - local-llm
  - ollama
  - model-runner
status: developing
related:
  - "[[Local LLM Deployment]]"
  - "[[Claude Code Local Setup]]"
  - "[[Anthropic Compatible API]]"
  - "[[LM Studio]]"
  - "[[oMLX]]"
  - "[[OptiQ]]"
  - "[[Antigravity Tools]]"
sources:
  - "[[sources/Ollama Official Documentation]]"
  - "[[sources/Claude Code + Ollama Tutorial]]"
---

# Ollama

Ollama is a local LLM runner that simplifies running open-source models on personal hardware. It provides both a native API and compatibility layers for Anthropic and OpenAI protocols.

## Core Features

- **Model Management**: `ollama pull/run/rm/ls/ps/stop` for model lifecycle
- **Custom Models**: Modelfile with FROM (base/GGUF/safetensors), PARAMETER, TEMPLATE, SYSTEM instructions
- **API Compatibility**: Anthropic-compatible (`/v1/messages`) and OpenAI-compatible (`/v1/chat/completions`)
- **Integration Launch**: `ollama launch claude` for one-click Claude Code connection
- **Thinking Mode**: Supported for Qwen3, DeepSeek R1, GPT-OSS models

## Key Configuration

| Feature | Variable / Parameter |
|---------|---------------------|
| Context window | `num_ctx` (default 4096) or `OLLAMA_CONTEXT_LENGTH` |
| Flash attention | `OLLAMA_FLASH_ATTENTION=1` |
| KV cache quantization | `OLLAMA_KV_CACHE_TYPE=q8_0` (recommended) |
| Keep model in memory | `keep_alive=-1` |
| Concurrent requests | `OLLAMA_NUM_PARALLEL` (default 1) |

## Anthropic Compatible API

Connect to Claudian / Claude Code:
```bash
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_BASE_URL=http://localhost:11434
# No /v1 suffix for Anthropic endpoint
```

## Recommended Cloud Models via Ollama

- `kimi-k2.5:cloud` — best overall
- `glm-5:cloud` — strong alternative
- `minimax-m2.7:cloud` — solid performer
- `qwen3.5:cloud` — available

## Connections

- [[Local LLM Deployment]] — parent concept covering all local LLM tools
- [[Claude Code Local Setup]] — how to connect Claude Code to various local runtimes
- [[Anthropic Compatible API]] — the protocol standard used for connection
- [[LM Studio]] — alternative local LLM runner with GUI
- [[oMLX]] — Apple Silicon optimized inference engine
- [[OptiQ]] — mixed-precision quantization tool for MLX models
- [[Antigravity Tools]] — local API proxy to cloud models (different approach)
