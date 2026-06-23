---
type: meta
title: "Concepts Index"
updated: 2026-06-23
tags:
  - meta
  - index
  - concept
domain: knowledge-management
status: evergreen
related:
  - "[[index]]"
  - "[[dashboard]]"
  - "[[Wiki Map]]"
  - "[[Hot Cache]]"
  - "[[LLM Wiki Pattern]]"
  - "[[Compounding Knowledge]]"
  - "[[Local LLM Deployment]]"
---

# Concepts Index

Navigation: [[index]] | [[entities/_index|Entities]] | [[sources/_index|Sources]]

All concept pages — ideas, patterns, and frameworks extracted from sources.

---

## Knowledge Management

- [[LLM Wiki Pattern]] — the core architecture for persistent, compounding knowledge bases
- [[Hot Cache]] — ~500-word session context file, updated after every ingest
- [[Compounding Knowledge]] — why the wiki grows more valuable over time, unlike RAG
- [[DragonScale Memory]] — memory-layer spec: fold operator, deterministic page addresses, semantic tiling, boundary-first autoresearch (status: shipped v0.4, all four mechanisms opt-in)
- [[Persistent Wiki Artifact]]: durable Markdown page as the LLM's memory object (developing)
- [[Source-First Synthesis]]: provenance discipline for LLM wiki layers (developing)
- [[Query-Time Retrieval]]: query synthesis with citations, complementary to Obsidian search (developing)

---

## Local LLM Ecosystem

- [[Ollama]] — local LLM runner with Anthropic/OpenAI API compatibility
- [[Local LLM Deployment]] — full ecosystem: runtimes, proxies, and integration patterns
- [[Claude Code Local Setup]] — configuring Claude Code to use local models
- [[Anthropic Compatible API]] — the protocol bridge between local LLMs and AI tools
- [[Apple Silicon Optimization]] — techniques for running LLMs on M-series Macs
- [[Model Quantization]] — reducing model memory footprint via lower precision

---

## Image Generation

Core principles for AI image generation and prompt engineering, extracted from HKH brand project experience.

- [[描述比重原则]] — 画面元素的描述字数要和重要性成正比，次要元素描述过多会喧宾夺主
- [[视觉描述优先原则]] — AI 需要的是视觉画面，不是文字描述；技术术语和抽象词会让 AI 跑偏
- [[参考图优先原则]] — 一张参考图比一千字描述都管用，能图生图就不要纯文字生图
- [[克制原则]] — AI 对程度词和动态词容易走极端，要用静态、状态、克制的描述
- [[一致性锚点原则]] — 同一系列图片必须有锚点保持风格一致，可以是参考图、关键词或成功案例

---

## Add new concepts here as they are extracted from sources.
