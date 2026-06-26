---
type: source
title: "Ollama Official Documentation"
source_url: "https://docs.ollama.com"
fetched: 2026-06-21
tags:
  - source
  - ollama
  - local-model
  - documentation
status: ingested
related:
  - "[[Ollama]]"
  - "[[Local LLM Deployment]]"
  - "[[Claude Code Local Setup]]"
  - "[[Anthropic Compatible API]]"
  - "[[Antigravity Tools]]"
---

# Ollama Official Documentation

> Source: `.raw/Ollama官方文档完整整理.md` — downloaded and dehydrated via browser_control.py

Ollama is a local LLM runner that provides both Ollama-native API and Anthropic-compatible API endpoints for connecting local models to AI tools like Claude Code, Claudian, and other agents.

## Key Sections

1. **Modelfile Reference** — defines how to create custom models: FROM (base model/GGUF), PARAMETER (num_ctx, temperature, etc.), TEMPLATE (Go template syntax, ChatML for Qwen), SYSTEM, ADAPTER, LICENSE, MESSAGE, REQUIRES
2. **CLI Commands** — ollama run/pull/rm/ls/ps/stop/serve/create/cp/launch
3. **Anthropic Compatible API** — connects to Claudian/Claude Code via `ANTHROPIC_AUTH_TOKEN=ollama` and `ANTHROPIC_BASE_URL=http://localhost:11434` (no `/v1`)
4. **OpenAI Compatible API** — `/v1/chat/completions`, `/v1/embeddings`, etc.
5. **Claude Code Integration** — `ollama launch claude` or manual env var setup
6. **FAQ** — context window, flash attention, KV cache quantization, concurrent requests, thinking mode

## Key Technical Details

- Default context window: 4096 tokens (configurable via `num_ctx` or `OLLAMA_CONTEXT_LENGTH`)
- Thinking mode: supported for Qwen3, DeepSeek, GPT-OSS models
- Vision: base64 only (no URL support)
- Tools/function calling: supported
- Prompt caching: NOT supported
- Model storage: macOS `~/.ollama/models`, Windows `C:\Users\%username%\.ollama\models`, Linux `/usr/share/ollama/.ollama/models`
- Flash attention: `OLLAMA_FLASH_ATTENTION=1`
- KV cache quantization: `OLLAMA_KV_CACHE_TYPE=q8_0` (recommended, halves memory)

## Recommended Models

| Model | Type | Notes |
|-------|------|-------|
| `kimi-k2.5:cloud` | Cloud | Recommended |
| `glm-5:cloud` | Cloud | Recommended |
| `qwen3-coder` | Local (30B) | Coding, needs ≥24GB VRAM |
| `qwen3.5` | Local | General purpose |
| `gpt-oss:20b` | Local | General purpose |
