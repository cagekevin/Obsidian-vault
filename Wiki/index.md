w---
type: meta
title: "Wiki Index"
updated: 2026-06-23
tags:
  - meta
  - index
status: evergreen
related:
  - "[[log]]"
  - "[[hot]]"
  - "[[concepts/_index]]"
  - "[[entities/_index]]"
  - "[[sources/_index]]"
---

# Wiki Index

Last updated: 2026-06-23 | Total pages: 51 | Sources ingested: 9

Navigation: [[log]] | [[hot]]

---

## Concepts

- [[LLM Wiki Pattern]] — the pattern for building persistent, compounding knowledge bases using LLMs (status: mature)
- [[Compounding Knowledge]] — why wiki knowledge grows more valuable over time, unlike RAG (status: mature)
- [[Hot Cache]] — ~500-word session context file, updated after every ingest and session (status: mature)
- [[Persistent Wiki Artifact]] — the wiki is a persistent artifact, not a chat transcript (status: developing)
- [[Source-First Synthesis]] — synthesis should reflect everything that was read, not training data (status: developing)
- [[Query-Time Retrieval]] — RAG vs persistent wiki comparison (status: developing)
- [[DragonScale Memory]] — advanced memory mechanisms for wiki vaults (status: developing)
- [[cherry-picks]] — prioritized feature backlog from ecosystem research (status: current)
- [[Pro Hub Challenge]] — community challenge pattern (status: evergreen)
- [[Semantic Topic Clustering]] — SERP-based keyword grouping (status: evergreen)
- [[Search Experience Optimization]] — search ranking and UX patterns (status: evergreen)
- [[SEO Drift Monitoring]] — tracking SEO changes over time (status: evergreen)
- [[SVG Diagram Style Guide]] — canonical visual style for diagrams (status: evergreen)
- [[Claude SEO]] — SEO tooling for Claude-generated content (status: evergreen)
- [[Ollama]] — local LLM runner with API compatibility layers (status: developing)
- [[Local LLM Deployment]] — full ecosystem of local model tools and integrations (status: developing)
- [[Claude Code Local Setup]] — configuring Claude Code to use local models (status: developing)
- [[Anthropic Compatible API]] — Ollama's Anthropic-compatible endpoint protocol (status: developing)
- [[Apple Silicon Optimization]] — techniques for running LLMs on M-series Macs (status: developing)
- [[Model Quantization]] — reducing model memory footprint via lower precision (status: developing)

## Agent Design

- [[Agent Skill Design Patterns]] — 5 standardized patterns for structuring Agent skill logic (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline) (status: developing)
- [[Intent Recognition]] — 意图识别，判断用户要什么然后路由到对应工作流或技能，三种实现方法及混合使用策略 (status: developing)
- [[Skill Five-Layer Structure]] — Skill 的五层架构：方法论→规则→工作流→输出工具→质量控制 (status: developing)
- [[AI技能自管理]] — AI 自动创建、优化、归档技能的方法论：技能自动生成、使用追踪、生命周期管理 (status: developing)

## Image Generation

### 基础原则
- [[描述比重原则]] — 画面元素的描述字数要和重要性成正比，次要元素描述过多会喧宾夺主 (status: mature)
- [[视觉描述优先原则]] — AI 需要的是视觉画面，不是文字描述；技术术语和抽象词会让 AI 跑偏 (status: mature)
- [[参考图优先原则]] — 一张参考图比一千字描述都管用，能图生图就不要纯文字生图 (status: mature)
- [[克制原则]] — AI 对程度词和动态词容易走极端，要用静态、状态、克制的描述 (status: mature)
- [[一致性锚点原则]] — 同一系列图片必须有锚点保持风格一致，可以是参考图、关键词或成功案例 (status: mature)
- [[摄影语言锚定质感]] — 用摄影镜头语言（镜头/光线/构图）替代"超逼真"等抽象词，获得真实质感 (status: mature)
- [[Gobo投影光影]] — 用 Gobo 素材图作为垫图/参考图，给产品图加投影光影提升质感 (status: developing)
- [[反向约束]] — 明确说不要什么，比只说要什么更有效；约束越紧，模型执行越准 (status: mature)
- [[提示词模板八要素]] — GPT-4o 提示词的标准化模板：交付物/受众/画布/文字/层级/视觉/数据/质量 (status: mature)

### 工作流与方法
- [[产物先行]] — 先定义交付物类型，再写提示词；不同产物触发不同精修逻辑 (status: mature)
- [[小步迭代]] — 不要让 AI 一次生成全部，先出基础图再逐步编辑，每步只改一个变量 (status: mature)
- [[变量与不变量分离]] — 编辑任务的核心：先锁死不变量，再开放一个变量 (status: mature)
- [[编辑三要素]] — 变量（改什么）+ 不变量（保持什么）+ 关键句（只改什么） (status: mature)
- [[角色锚定]] — 详细角色描述锁定角色一致性，后续场景复用锚定描述 (status: developing)

## Video Generation

- [[AI Camera Movements]] — AI 视频生成中常用的 30+ 种运镜手法提示词 (status: developing)
- [[Pacing and Rhythm]] — 叙事节奏与韵律，不同场景的速度分类和控制方法 (status: developing)

## Storytelling & Screenwriting

从 W6-俄语详细剧本技能中提炼的**可复用方法论**。不只是写剧本，做设计、写文案、出图、做产品都能用。

### 核心创作方法
- [[Scene Value]] — 场景价值转换，每个场景/段落都要有价值的正负变化 (status: developing)
- [[Show Don't Tell]] — 展示而非讲述，用动作和物件展示信息 (status: developing)
- [[Causal Chain Audit]] — 因果链审计，检查每个步骤是不是由前一个导致的 (status: developing)

### 质量控制与编辑
- [[If You Remove It Does It Change]] — 必要性测试，删掉它结果会变吗？没变就删掉 (status: developing)
- [[Cut Priority Method]] — 删减优先级方法，先删最不重要的，核心绝对不动 (status: developing)

### 工作流与沟通
- [[Spot Edit Principle]] — 点式修改原则，只改用户要求改的那一点 (status: developing)
- [[Single Version Principle]] — 单一版本原则，只给一个最优解 + 理由 (status: developing)
- [[Binary Question]] — 二进制提问法，信息不够时问窄的二选一问题 (status: developing)

### 叙事结构与角色（编剧专用）
- [[Controlling Idea]] — 主控思想，一句话概括故事核心 (status: developing)
- [[Chekhov's Gun]] — 契诃夫之枪，每个出现的元素都要有其作用 (status: developing)
- [[Progressive Complications]] — 渐进式复杂化，冲突越来越强 (status: developing)
- [[Three-Act Structure]] — 三幕式结构：铺垫→对抗→结局 (status: developing)
- [[Hero's Journey]] — 英雄之旅，坎贝尔的 12 阶段单一神话 (status: developing)
- [[Inciting Incident]] — 激励事件，打破主角生活平衡的事件 (status: developing)
- [[Character Bible]] — 角色圣经，从内到外的 8 层角色构建系统 (status: developing)
- [[Worldbuilding]] — 世界观构建，6 大模块 + 知识层级 (status: developing)
- [[Hamartia]] — 悲剧缺陷，主角性格中的弱点变成灾难 (status: developing)
- [[Peripeteia and Anagnorisis]] — 突转与发现，双重打击 (status: developing)
- [[Catharsis]] — 宣泄/净化，悲剧的最终目的 (status: developing)
- [[Pacing and Rhythm]] — 叙事节奏与韵律，时间计算和删减优先级 (status: developing)

## Entities

- [[Andrej Karpathy]] — AI researcher, educator, founder (person)
- [[kepano-obsidian-skills]] — Obsidian skills plugin by kepano (project)
- [[Ar9av-obsidian-wiki]] — alternative obsidian wiki implementation (project)
- [[ballred-obsidian-claude-pkm]] — PKM system using Obsidian + Claude (project)
- [[Claudian-YishenTu]] — contributor (person)
- [[Nexus-claudesidian-mcp]] — MCP bridge for claude-obsidian (project)
- [[rvk7895-llm-knowledge-bases]] — research on LLM knowledge bases (project)
- [[Antigravity Tools]] — local API proxy to Tencent Cloud Copilot (tool)
- [[LM Studio]] — GUI-based local LLM runner (tool)
- [[oMLX]] — Apple Silicon optimized inference engine (tool)
- [[OptiQ]] — mixed-precision quantization tool for MLX models (tool)
- [[Tencent Cloud Copilot]] — cloud LLM API service (service)
- [[Google ADK]] — Google's Agent Development Kit for building production AI agents (tool)

## Sources

- [[claude-obsidian-ecosystem-research]] — ecosystem research (status: ingested)
- [[sources/Ollama Official Documentation]] — full Ollama docs dehydrated (status: ingested)
- [[sources/Antigravity Tools]] — supported model list v1.2.2 (status: ingested)
- [[sources/Claude Code + Ollama Tutorial]] — WeChat tutorial (status: ingested)
- [[sources/Claude Code + LM Studio Tutorial]] — WeChat tutorial (status: ingested)
- [[sources/oMLX Tutorial]] — WeChat tutorial (status: ingested)
- [[sources/OptiQ Tutorial]] — WeChat tutorial (status: ingested)
- [[5 Agent Skill Design Patterns]] — Google Cloud Tech Twitter thread on 5 ADK skill patterns (status: ingested)

---

> **Note**: This wiki follows the claude-obsidian LLM Wiki pattern. Pages are organized into concepts/, entities/, sources/, questions/, and meta/ folders.
