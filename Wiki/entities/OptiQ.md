---
type: entity
title: "OptiQ"
entity_type: tool
role: "Mixed-precision quantization tool for MLX models, enables running Qwen3.5-9B on 16GB Macs"
first_mentioned: "[[sources/OptiQ Tutorial]]"
created: 2026-06-23
updated: 2026-06-23
tags:
  - entity
  - tool
  - quantization
  - apple-silicon
  - optiq
status: mature
related:
  - "[[oMLX]]"
  - "[[Local LLM Deployment]]"
  - "[[Claude Code Local Setup]]"
  - "[[Apple Silicon Optimization]]"
  - "[[Model Quantization]]"
sources:
  - "[[sources/OptiQ Tutorial]]"
---

# OptiQ (mlx-optiq)

A mixed-precision quantization tool that applies different bit-widths per layer, optimizing memory usage while preserving model quality. Built on Apple's MLX framework.

Key features: supports Claude Code directly (dual protocol), MTP decode acceleration, hybrid-precision KV cache for long context. Recommended model: Qwen3.5-9B-OptiQ-4bit (6.6 GB).
