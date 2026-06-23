---
type: source
title: "Claude Code + Ollama Local Model Tutorial"
source_url: "https://mp.weixin.qq.com/s/xhtVwnBJIpIGsMTCajDlcA"
fetched: 2026-06-21
tags:
  - source
  - tutorial
  - ollama
  - claude-code
  - local-model
status: ingested
related:
  - "[[Ollama]]"
  - "[[Claude Code Local Setup]]"
  - "[[Local LLM Deployment]]"
---

# Claude Code + Ollama Local Model Tutorial

> Source: `Clippings/raw/ClaudeCode+Ollama教程.md` — from WeChat public account "GitHubStore" by 小G

A 5-minute quickstart guide for running Claude Code with local Ollama models.

## Quick Steps

1. Install Ollama from ollama.com
2. Pull a model: `ollama pull qwen3-coder:7b`
3. Install Claude Code: `curl -fsSL https://claude.ai/install.sh | sh`
4. Connect: `ollama launch claude --model qwen3-coder:7b`

## Recommended Models

| Memory | Model |
|--------|-------|
| 16-32GB | `qwen3-coder:7b` or `gemma2:9b` |
| RTX 4090 / M high-end | `qwen3-coder:30b` or GLM-4 series |
