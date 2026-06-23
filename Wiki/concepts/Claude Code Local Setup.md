---
type: concept
title: "Claude Code Local Setup"
complexity: intermediate
domain: local-llm
aliases:
  - "Claude Code 本地模型配置"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - claude-code
  - local-model
  - configuration
status: developing
related:
  - "[[Ollama]]"
  - "[[LM Studio]]"
  - "[[oMLX]]"
  - "[[OptiQ]]"
  - "[[Antigravity Tools]]"
  - "[[Local LLM Deployment]]"
  - "[[Anthropic Compatible API]]"
sources:
  - "[[sources/Ollama Official Documentation]]"
  - "[[sources/Claude Code + Ollama Tutorial]]"
  - "[[sources/Claude Code + LM Studio Tutorial]]"
  - "[[sources/oMLX Tutorial]]"
  - "[[sources/OptiQ Tutorial]]"
---

# Claude Code Local Setup

How to configure Claude Code CLI to use local LLM models instead of Anthropic's cloud API. Multiple approaches exist depending on the local runtime.

## Environment Variable Pattern

Claude Code uses Anthropic SDK environment variables to connect to local runtimes:

```bash
export ANTHROPIC_BASE_URL=http://localhost:<PORT>
export ANTHROPIC_AUTH_TOKEN=<token>    # for Ollama (Anthropic compat)
# OR
export ANTHROPIC_API_KEY=<key>         # for LM Studio / OptiQ
# OR (via settings.json)
export ANTHROPIC_MODEL=<model-name>    # optional, model name override
```

## Per-Runtime Configuration

| Runtime | Port | Auth Variable | URL Suffix |
|---------|------|---------------|------------|
| [[Ollama]] | 11434 | `ANTHROPIC_AUTH_TOKEN=ollama` | No `/v1` |
| [[LM Studio]] | 1234 | `ANTHROPIC_API_KEY=local-key` | `/v1` |
| [[oMLX]] | 8000 | `ANTHROPIC_AUTH_TOKEN=<key>` | No `/v1` |
| [[OptiQ]] | 8080 | `ANTHROPIC_API_KEY=not-used` | No `/v1` |
| [[Antigravity Tools]] | 8002 | Sub API Key | `/v1` |

## One-Click Method

```bash
ollama launch claude --model qwen3-coder:7b
```

This auto-configures the environment and launches Claude Code with the specified Ollama model.

## settings.json Method

For CodeBuddy / persistent config, use `settings.json` env section:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_MODEL": "qwen3.5:9b"
  }
}
```

## Connections

- [[Ollama]] — primary runtime, supports `ollama launch claude`
- [[LM Studio]] — GUI alternative
- [[oMLX]] — Apple Silicon optimized
- [[OptiQ]] — mixed-precision quantization
- [[Antigravity Tools]] — cloud proxy alternative
- [[Anthropic Compatible API]] — protocol details
