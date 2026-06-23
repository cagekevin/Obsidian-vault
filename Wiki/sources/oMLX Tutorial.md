---
type: source
title: "oMLX + Claude Code Local Model Tutorial"
source_url: "https://mp.weixin.qq.com/s/THJsVVM2D9AB5Wn7yYHZ7w"
fetched: 2026-06-21
tags:
  - source
  - tutorial
  - omlx
  - claude-code
  - local-model
status: ingested
related:
  - "[[oMLX]]"
  - "[[Claude Code Local Setup]]"
  - "[[Local LLM Deployment]]"
  - "[[Apple Silicon Optimization]]"
---

# oMLX + Claude Code Local Model Tutorial

> Source: `Clippings/raw/oMLX教程.md` — from WeChat public account "朱攀"

oMLX is a local inference engine optimized for Apple Silicon (M1-M4). It serves models via an API and can be connected to Claude Code.

## Setup

```bash
brew tap jundot/omlx https://github.com/jundot/omlx
brew install omlx
brew services start omlx
omlx serve --model-dir ~/models
```

Default port: 8000. Model download via browser at `http://localhost:8000/admin`.

## Claude Code Connection

```bash
export ANTHROPIC_MODEL="Qwen3.6-27B-8bit"
export ANTHROPIC_SMALL_FAST_MODEL="Qwen3.6-27B-8bit"
export ANTHROPIC_BASE_URL="http://localhost:8000"
export ANTHROPIC_AUTH_TOKEN="<your_api_key>"
claude
```

## Optimization Parameters

- Memory limit: `--max-process-memory 80%`
- SSD cache for long context: `--paged-ssd-cache-dir ~/.omlx/cache`
- China mirror: `--hf-endpoint https://hf-mirror.com`
