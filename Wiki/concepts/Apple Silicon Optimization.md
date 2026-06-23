---
type: concept
title: "Apple Silicon Optimization"
complexity: intermediate
domain: local-llm
aliases:
  - "Apple Silicon 推理优化"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - apple-silicon
  - optimization
  - mlx
  - local-llm
status: developing
related:
  - "[[oMLX]]"
  - "[[OptiQ]]"
  - "[[Local LLM Deployment]]"
  - "[[Model Quantization]]"
sources:
  - "[[sources/oMLX Tutorial]]"
  - "[[sources/OptiQ Tutorial]]"
---

# Apple Silicon Optimization

Techniques and tools for running LLMs efficiently on Apple Silicon (M1-M4) hardware. Apple's unified memory architecture allows running models up to the system's total RAM, but requires specialized optimizations.

## Key Tools

- **[[oMLX]]** — MLX-native inference engine, optimized for Apple Silicon
- **[[OptiQ]]** — Mixed-precision quantization for MLX models

## Optimization Techniques

- **Model Quantization**: Reduce model precision (e.g., 4-bit) to fit in available RAM
- **KV Cache Quantization**: `OLLAMA_KV_CACHE_TYPE=q8_0` halves KV cache memory
- **Flash Attention**: `OLLAMA_FLASH_ATTENTION=1` for faster attention computation
- **SSD Cache**: Page KV cache to SSD for long context (oMLX)
- **MTP Decode**: Multi-token prediction for faster generation (OptiQ)
