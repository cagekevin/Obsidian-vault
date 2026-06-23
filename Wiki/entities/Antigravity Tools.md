---
type: entity
title: "Antigravity Tools"
entity_type: tool
role: "Local API proxy to Tencent Cloud Copilot, supporting 15 models across 4 vendors"
first_mentioned: "[[sources/Antigravity Tools]]"
created: 2026-06-23
updated: 2026-06-23
tags:
  - entity
  - tool
  - api-proxy
  - tencent-cloud
status: mature
related:
  - "[[Ollama]]"
  - "[[Local LLM Deployment]]"
  - "[[Claude Code Local Setup]]"
  - "[[Tencent Cloud Copilot]]"
sources:
  - "[[sources/Antigravity Tools]]"
---

# Antigravity Tools

A local API proxy tool (v1.2.2) that forwards requests to Tencent Cloud Copilot (`https://copilot.tencent.com/v2`). Exposes an OpenAI-compatible endpoint at `http://127.0.0.1:8002/v1`.

## Supported Models: 15 total

- **DeepSeek** (6): v4-pro, v4-flash, v3-2-volc, v3-1, v3-0324, r1
- **GLM / Zhipu** (7): 5.2, 5.1, 5.0, 5.0-turbo, 5v-turbo, 4.7, 4.6
- **Kimi** (1): k2.6
- **MiniMax** (3): m2.5, m2.7, m3

## Usage

API Key created in Antigravity Tools UI. Compatible with any OpenAI-compatible client.
