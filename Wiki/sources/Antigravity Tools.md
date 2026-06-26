---
type: source
title: "Antigravity Tools Supported Models"
source_url: "http://127.0.0.1:8002/v1"
fetched: 2026-06-23
tags:
  - source
  - antigravity
  - api-proxy
  - model-list
status: ingested
related:
  - "[[Antigravity Tools]]"
  - "[[Local LLM Deployment]]"
  - "[[Tencent Cloud Copilot]]"
  - "[[Claude Code Local Setup]]"
---

# Antigravity Tools Supported Models

> Source: `.raw/Antigravity Tools 支持的模型.md` — model list from Antigravity Tools v1.2.2 local API proxy

Antigravity Tools is a local API proxy that forwards requests to Tencent Cloud Copilot (`https://copilot.tencent.com/v2`). It exposes an OpenAI-compatible endpoint at `http://127.0.0.1:8002/v1` and supports 15 models across 4 vendors.

## Supported Models (15 total)

### DeepSeek (6)
- `deepseek-v4-pro` — V4 Pro (strongest)
- `deepseek-v4-flash` — V4 Flash (fast)
- `deepseek-v3-2-volc` — V3 Volcano Engine
- `deepseek-v3-1` — V3-1
- `deepseek-v3-0324` — V3 0324
- `deepseek-r1` — R1 (reasoning)

### GLM / Zhipu AI (7)
- `glm-5.2`, `glm-5.1`, `glm-5.0`, `glm-5.0-turbo`, `glm-5v-turbo`, `glm-4.7`, `glm-4.6`

### Kimi (1)
- `kimi-k2.6`

### MiniMax (3)
- `minimax-m2.5`, `minimax-m2.7`, `minimax-m3`

## Proxy Strategy

- Key management: upstream key pool (sequential exhaustion)
- Auth: sub API key management
- Interface: OpenAI-compatible (`/v1/chat/completions`, `/v1/models`)
- Rate limiting: supported with automatic key switching

## Client Configuration

| Field | Value |
|-------|-------|
| API Base URL | `http://127.0.0.1:8002/v1` |
| API Key | Sub API key from Antigravity Tools UI |
| Model | Any from the list above (e.g. `deepseek-v4-flash`) |

Compatible clients: ChatBox, NextChat, Open WebUI, CodeBuddy/WorkBuddy, any OpenAI-compatible SDK.
