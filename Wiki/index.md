---
type: meta
title: "Wiki Index"
updated: 2026-06-24
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

Last updated: 2026-06-24 | Total pages: 40 | Sources ingested: 10

Navigation: [[log]] | [[hot]]

---

## Concepts

- [[Hot Cache]] — ~500-word session context file, updated after every ingest and session (status: mature)
- [[Ollama]] — local LLM runner with API compatibility layers (status: developing)
- [[Local LLM Deployment]] — full ecosystem of local model tools and integrations (status: developing)
- [[Claude Code Local Setup]] — configuring Claude Code to use local models (status: developing)
- [[Anthropic Compatible API]] — Ollama's Anthropic-compatible endpoint protocol (status: developing)
- [[Apple Silicon Optimization]] — techniques for running LLMs on M-series Macs (status: developing)
- [[Model Quantization]] — reducing model memory footprint via lower precision (status: developing)

## Agent Design

- [[Agent Skill Design Patterns]] — 5 standardized patterns for structuring Agent skill logic (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline) (status: developing)
- [[Intent Recognition]] — 意图识别，判断用户要什么然后路由到对应工作流或技能，三种实现方法及混合使用策略 (status: developing)
- [[Open Knowledge Format]] — Google Cloud 推出的开源知识格式标准，将 Karpathy 的 LLM Wiki 设想变成可执行工程标准 (status: developing)
- [[Skill Five-Layer Structure]] — Skill 的五层架构：方法论→规则→工作流→输出工具→质量控制 (status: developing)
- [[AI技能自管理]] — AI 自动创建、优化、归档技能的方法论：技能自动生成、使用追踪、生命周期管理 (status: developing)

## Image Generation

### 基础原则
- [[AI打光五法]] — 五种导演级打光方法：侧逆光、轮廓光、侧光、硬光、低位光 (status: developing)
- [[光线布置模块化]] — 把光线写成独立的 `【光线布置】` 段落，说清四要素 (status: developing)
- [[AI室内光控制]] — 光源锚定、衰减路径、漫反射，三大法则掌控室内光影 (status: developing)
- [[AI光源提示词模板库]] — 20 种可直接复用的光源提示词模板 (status: developing)
- [[描述比重原则]] — 画面元素的描述字数要和重要性成正比，次要元素描述过多会喧宾夺主 (status: mature)
- [[视觉描述优先原则]] — AI 需要的是视觉画面，不是文字描述；技术术语和抽象词会让 AI 跑偏 (status: mature)
- [[参考图优先原则]] — 一张参考图比一千字描述都管用，能图生图就不要纯文字生图 (status: mature)
- [[克制原则]] — AI 对程度词和动态词容易走极端，要用静态、状态、克制的描述 (status: mature)
- [[一致性锚点原则]] — 同一系列图片必须有锚点保持风格一致，可以是参考图、关键词或成功案例 (status: mature)
- [[摄影语言锚定质感]] — 用摄影镜头语言（镜头/光线/构图）替代"超逼真"等抽象词，获得真实质感 (status: mature)
- [[Gobo投影光影]] — 用 Gobo 素材图作为垫图/参考图，给产品图加投影光影提升质感 (status: developing)
- [[反向约束]] — 明确说不要什么，比只说要什么更有效；约束越紧，模型执行越准 (status: mature)
- [[提示词模板八要素]] — GPT-4o 提示词的标准化模板：交付物/受众/画布/文字/层级/视觉/数据/质量 (status: mature)

### 角色与人物
- [[AI角色资产搭建]] — 人物资产三件套、妆造设计、AI捏脸、活人感、微表情三控、微表情情绪特征对照表、多人动作控制 (status: developing)
- [[人感审美与材质重塑]] — 减法审美、手工感回归、材质层级重置、打破摆拍感 (status: developing)
- [[AI角色声音控制]] — 声音公式控制音色、声音过程控制语气、标点符号控制语速、Seedance 2.0 标点控声实战深化 (status: developing)


### 镜头与光线
- [[AI镜头语言进阶]] — 反向写提示词、低角度原理、空镜三作用、情绪蒙太奇 (status: developing)
- [[AI视觉语法体系]] — 提示词五板块、词序规则、摄影三参数、反向提示词 (status: developing)

### 环境与构图
- [[AI环境空间设计]] — 环境三层写法、因果逻辑、场景一致性、伪透视技巧 (status: developing)
- [[视觉平衡与动线构图]] — 视觉动线、视觉重量分配、手绘草图强控制 (status: developing)

### 氛围与色彩
- [[AI氛围与色彩控制]] — 氛围三要素、调色三法、减法审美、特征塌陷 (status: developing)

### 视频与动作
- [[AI视频动作设计]] — ARC视角、打斗结构、单主体动作原则、人物一致性 (status: developing)
- [[时间补偿机制与动态词学]] — 时间词三态、运动矢量反推、时间逻辑约束 (status: developing)

### 高级控制
- [[AI底层机制与高级控制]] — 误解机制、风格泄漏、鲁棒性破坏、JSON提示词 (status: developing)
- [[风格提取与约束系统]] — 不可变约束点、风格边界锁定、结构骨架反推 (status: developing)

### 创作思维
- [[AI导演创作思维]] — 调度优先、核心行动驱动、补拍重构、Codex自动化 (status: developing)
- [[AI创意方法论]] — 打破物理定律、让时间失控、把镜头变成角色 (status: developing)

- [[物理模拟控制流（Cinema Studio）]] — 真实摄影机模拟、物理模拟引擎 (status: developing)

### 工作流与方法
- [[产物先行]] — 先定义交付物类型，再写提示词；不同产物触发不同精修逻辑 (status: mature)
- [[小步迭代]] — 不要让 AI 一次生成全部，先出基础图再逐步编辑，每步只改一个变量 (status: mature)
- [[变量与不变量分离]] — 编辑任务的核心：先锁死不变量，再开放一个变量 (status: mature)
- [[编辑三要素]] — 变量（改什么）+ 不变量（保持什么）+ 关键句（只改什么） (status: mature)
- [[角色锚定]] — 详细角色描述锁定角色一致性，后续场景复用锚定描述 (status: developing)
- [[AI 生图决策规则]] — 6 条可执行 if-then 规则：冗余信号稀释/Generic对抗/注意力前置/省略接管/加法非增强/批量一致性锚点 (status: developing)
- [[利益视觉化原则]] — 配图的本质是利益视觉化，利益是主角、产品是配角、渠道是装饰；附配图思维链模板 (status: developing)

- [[AI空镜设计]] — 空镜三类提取方法、五要素提示词公式、叙事改写、放置策略 (status: developing)

## Video Generation

- [[AI Camera Movements]] — AI 视频生成运镜手法提示词 + 英文速查词汇表 + 灯光词汇表 (status: developing)
- [[Pacing and Rhythm]] — 叙事节奏与韵律，不同场景的速度分类和控制方法 (status: developing)
- [[sources/Seedance 2.0 标点控声]] — Seedance 2.0 高阶技能：标点控制语气语调、情绪感染力（来源页）(status: ingested)

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
- [[sources/Google OKF 2026]] — Google OKF 开放知识格式标准 (status: ingested)
