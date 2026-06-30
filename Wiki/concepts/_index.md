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

### 核心原则
提取自 HKH 品牌项目经验。

- [[描述比重原则]]
- [[视觉描述优先原则]]
- [[参考图优先原则]]
- [[克制原则]]
- [[一致性锚点原则]]
- [[AI 生图决策规则]] — 6 条可执行 if-then 规则 (status: developing)
- [[文案完整保留与信息层级原则]] — 文案必须完整保留，排版只写信息层级 (status: developing)
- [[利益视觉化原则]] — 配图的本质是利益视觉化，利益是主角、产品是配角、渠道是装饰 (status: developing)

### 摄影与光线
- [[摄影语言锚定质感]] — 用摄影镜头语言替代抽象词获得真实质感
- [[AI打光五法]] — 五种导演级打光方法：侧逆光、轮廓光、侧光、硬光、低位光 (status: developing)
- [[光线布置模块化]] — 把光线写成独立的 `【光线布置】` 段落，说清四要素 (status: developing)
- [[AI室内光控制]] — 光源锚定、衰减路径、漫反射，三大法则掌控室内光影 (status: developing)
- [[AI光源提示词模板库]] — 20 种可直接复用的光源提示词模板 (status: developing)
- [[AI镜头语言进阶]] — 反向写提示词、低角度原理、空镜三作用、情绪蒙太奇三法、分镜落差 (status: developing)
- [[AI空镜设计]] — 空镜三类提取方法、五要素提示词公式、叙事改写、放置策略 (status: developing)

### 角色与人物
- [[AI角色资产搭建]] — 人物资产三件套、妆造设计、AI捏脸、活人感、微表情 (status: developing)
- [[人感审美与材质重塑]] — 减法审美、手工感回归、材质层级重置 (status: developing)
- [[AI角色声音控制]] — 声音公式控制音色、声音过程控制语气、标点符号控制语速、Seedance 2.0 标点控声实战深化 (status: developing)

### 环境与构图
- [[AI环境空间设计]] — 环境三层写法、因果逻辑、场景一致性、伪透视 (status: developing)
- [[视觉平衡与动线构图]] — 视觉动线、视觉重量分配、手绘草图控制 (status: developing)

### 氛围与色彩
- [[AI氛围与色彩控制]] — 氛围三要素、调色三法、减法审美、特征塌陷 (status: developing)

### 视频与动作
- [[AI视频动作设计]] — ARC视角、打斗结构、单主体动作原则 (status: developing)
- [[时间补偿机制与动态词学]] — 时间词三态、运动矢量反推 (status: developing)

### 提示词与底层机制
- [[AI视觉语法体系]] — 提示词五板块、词序规则、反向提示词 (status: developing)
- [[AI底层机制与高级控制]] — 误解机制、风格泄漏、鲁棒性破坏 (status: developing)
- [[风格提取与约束系统]] — 不可变约束点、风格边界锁定 (status: developing)

### 创作思维与工具
- [[AI导演创作思维]] — 调度优先、核心行动驱动、补拍重构、画面结构拆解法、Codex自动化 (status: developing)
- [[AI创意方法论]] — 打破物理定律、让时间失控、把镜头变成角色 (status: developing)
- [[物理模拟控制流（Cinema Studio）]] — 真实摄影机模拟 (status: developing) — 画面元素的描述字数要和重要性成正比，次要元素描述过多会喧宾夺主
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
- [[AI长视频丝滑衔接]] — 多段 15 秒 AI 视频拼接的三种方法：切换景别角度、动作中衔接、分镜组接 (status: developing)
- [[AI视频电影质感]] — 颜色有情绪、空间有呼吸、材质有真实感 (status: developing)

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
