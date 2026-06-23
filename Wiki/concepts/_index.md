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

## Agent Design

- [[Agent Skill Design Patterns]] — 5 standardized patterns for structuring Agent skill logic (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline)
- [[Intent Recognition]] — 意图识别，判断用户要什么然后路由到对应工作流或技能
- [[Skill Five-Layer Structure]] — Skill 的五层架构：方法论→规则→工作流→输出工具→质量控制

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

## Video Generation

- [[AI Camera Movements]] — AI 视频生成中常用的 30+ 种运镜手法提示词，包括基础运镜、动态情绪运镜、角度视角、进阶技巧等
- [[Pacing and Rhythm]] — 叙事节奏与韵律，不同场景的速度分类和控制方法，与运镜配合使用

---

## Storytelling & Screenwriting

从 W6-俄语详细剧本技能中提炼的经典编剧理论和创作方法论。

### 核心原则
- [[Show Don't Tell]] — 展示而非讲述，用动作和物体代替内心独白和描述
- [[Controlling Idea]] — 主控思想，一句话概括故事核心，每个场景都要为它服务
- [[Scene Value]] — 场景价值转换，每个场景都要有价值的正负变化
- [[Chekhov's Gun]] — 契诃夫之枪，每个出现的元素都要有其作用
- [[If You Remove It Does It Change]] — 必要性测试，去掉它结果会变吗？没变就删掉
- [[Progressive Complications]] — 渐进式复杂化，冲突越来越强，赌注越来越高

### 经典结构
- [[Three-Act Structure]] — 三幕式结构：铺垫→对抗→结局
- [[Hero's Journey]] — 英雄之旅，坎贝尔的 12 阶段单一神话
- [[Inciting Incident]] — 激励事件，打破主角生活平衡的事件，故事正式开始

### 角色与世界观
- [[Character Bible]] — 角色圣经，从内到外的 8 层角色构建系统
- [[Worldbuilding]] — 世界观构建，6 大模块 + 知识层级，有规则的世界才有戏剧

### 悲剧理论（亚里士多德）
- [[Hamartia]] — 悲剧缺陷，主角性格中的弱点在极端情况下变成灾难
- [[Peripeteia and Anagnorisis]] — 突转与发现，行动走向反面+真相揭露的双重打击
- [[Catharsis]] — 宣泄/净化，悲剧的最终目的，通过怜悯和恐惧释放情感

---

## Add new concepts here as they are extracted from sources.
