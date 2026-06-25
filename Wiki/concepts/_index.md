---
type: meta
title: "Concepts Index"
updated: 2026-06-24
tags:
  - meta
  - index
  - concept
domain: knowledge-management
status: evergreen
related:
  - "[[index]]"
  - "[[Hot Cache]]"
---

# Concepts Index

Navigation: [[index]] | [[entities/_index|Entities]] | [[sources/_index|Sources]]

All concept pages — ideas, patterns, and frameworks extracted from sources.

---

## Agent Design

- [[Agent Skill Design Patterns]] — 5 standardized patterns for structuring Agent skill logic (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline)
- [[Intent Recognition]] — 意图识别，判断用户要什么然后路由到对应工作流或技能
- [[Skill Five-Layer Structure]] — Skill 的五层架构：方法论→规则→工作流→输出工具→质量控制
- [[AI技能自管理]] — AI 自动创建、优化、归档技能的方法论

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
- [[AI 生图决策规则]] — 6 条可执行 if-then 规则：冗余信号稀释/Generic对抗/注意力前置/省略接管/加法非增强/批量一致性锚点 (status: developing)
- [[文案完整保留与信息层级原则]] — 文案必须完整保留，排版只写信息层级不写具体位置 (status: developing)

---

## Video Generation

- [[AI Camera Movements]] — AI 视频生成中常用的 30+ 种运镜手法提示词，包括基础运镜、动态情绪运镜、角度视角、进阶技巧等
- [[Pacing and Rhythm]] — 叙事节奏与韵律，不同场景的速度分类和控制方法，与运镜配合使用

---

## Storytelling & Screenwriting

从 W6-俄语详细剧本技能中提炼的**可复用方法论**。不只是写剧本，做设计、写文案、出图、做产品都能用。

### 核心创作方法
- [[Scene Value]] — 场景价值转换，每个场景/段落都要有价值的正负变化，没有变化就是废话
- [[Show Don't Tell]] — 展示而非讲述，用动作和物件展示信息，不用描述性语言直接说
- [[Causal Chain Audit]] — 因果链审计，检查每个步骤是不是由前一个导致的，而不只是时间顺序

### 质量控制与编辑
- [[If You Remove It Does It Change]] — 必要性测试，删掉它结果会变吗？没变就删掉
- [[Cut Priority Method]] — 删减优先级方法，先删最不重要的，核心绝对不动

### 工作流与沟通
- [[Spot Edit Principle]] — 点式修改原则，只改用户要求改的那一点，不全量返工
- [[Single Version Principle]] — 单一版本原则，只给一个最优解 + 理由，不给一堆选项让用户选
- [[Binary Question]] — 二进制提问法，信息不够时问窄的二选一问题，不问开放问题

---

## Add new concepts here as they are extracted from sources.
