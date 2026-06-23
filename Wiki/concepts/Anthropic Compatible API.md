---
type: concept
title: "Anthropic Compatible API"
complexity: intermediate
domain: local-llm
aliases:
  - "Anthropic 兼容 API"
  - "/v1/messages"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - api
  - anthropic
  - protocol
status: developing
related:
  - "[[Ollama]]"
  - "[[Claude Code Local Setup]]"
  - "[[Local LLM Deployment]]"
sources:
  - "[[sources/Ollama Official Documentation]]"
---

# Anthropic Compatible API

Ollama implements an Anthropic-compatible API endpoint that allows any tool using the Anthropic Python/TypeScript SDK to connect to local models. This is the key bridge between local LLMs and tools like Claude Code, Claudian, and CodeBuddy.

## Endpoint

`/v1/messages` — same as Anthropic's Messages API.

## Environment Variables

```bash
export ANTHROPIC_AUTH_TOKEN=ollama    # required but value is ignored
export ANTHROPIC_BASE_URL=http://localhost:11434    # NO /v1 suffix
```

Key difference from OpenAI-compatible setup: Anthropic endpoint does NOT use `/v1` in the base URL.

## Supported Features

| Feature | Status |
|---------|--------|
| Messages / Streaming | ✅ |
| System prompts | ✅ |
| Multi-turn conversations | ✅ |
| Vision (base64 images) | ✅ (URL not supported) |
| Tools / function calling | ✅ |
| Thinking / extended thinking | ✅ |
| Tool choice | ❌ |
| Prompt caching | ❌ |
| PDF support | ❌ |

## Connections

- [[Ollama]] — implements this API
- [[Claude Code Local Setup]] — uses this API for local connection
- [[Local LLM Deployment]] — parent concept
