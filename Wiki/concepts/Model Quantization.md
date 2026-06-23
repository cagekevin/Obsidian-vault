---
type: concept
title: "Model Quantization"
complexity: intermediate
domain: local-llm
aliases:
  - "模型量化"
  - "混合精度量化"
created: 2026-06-23
updated: 2026-06-23
tags:
  - concept
  - quantization
  - local-llm
  - optimization
status: developing
related:
  - "[[OptiQ]]"
  - "[[Apple Silicon Optimization]]"
  - "[[Local LLM Deployment]]"
sources:
  - "[[sources/OptiQ Tutorial]]"
---

# Model Quantization

Techniques to reduce the memory footprint of LLMs by using lower-precision numerical representations for weights and/or activations.

## Types

- **Uniform Quantization**: Same bit-width for all layers (e.g., Q4_K_M, Q5_K_M)
- **Mixed-Precision Quantization** ([[OptiQ]]): Different bit-widths per layer based on sensitivity analysis
- **KV Cache Quantization**: Quantize the key-value cache to reduce memory during long context inference

## Recommended Settings

| Setting | Value | Effect |
|---------|-------|--------|
| KV cache type | `q8_0` | Halves KV cache memory vs `f16` |
| Model precision | 4-bit | ~4x memory reduction vs fp16 |
| OptiQ target bits | 5.0 | Balanced quality/size |

## Connections

- [[OptiQ]] — implements mixed-precision quantization
- [[Apple Silicon Optimization]] — quantization is key for Apple Silicon
- [[Local LLM Deployment]] — quantization enables running larger models on limited hardware
