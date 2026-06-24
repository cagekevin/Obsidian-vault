---
type: meta
title: "Wiki Log"
updated: 2026-06-23
tags:
  - meta
  - log
status: evergreen
related:
  - "[[index]]"
  - "[[hot]]"
---

# Wiki Log

Navigation: [[index]] | [[hot]]

---

## [2026-06-24] Concept rewrite & cleanup | W6 方法论提炼
- 背景：用户指出纯概念定义对技能仓库没用，LLM 本来就知道，有用的是"怎么用"
- 删除的页面（移到 Temp/old-wiki-concepts/ 备份）：
  - 15 个纯概念编剧页面：Catharsis, Character Bible, Chekhov's Gun, Controlling Idea, Hamartia, Hero's Journey, Inciting Incident, Pacing and Rhythm, Peripeteia and Anagnorisis, Progressive Complications, Three-Act Structure, Worldbuilding 等
- 新建的页面（从 W6-俄语详细剧本技能中提炼的可复用方法论）：
  - [[If You Remove It Does It Change]] — 必要性测试
  - [[Spot Edit Principle]] — 点式修改原则
  - [[Show Don't Tell]] — 展示而非讲述（重写，从纯概念改为方法论）
  - [[Scene Value]] — 场景价值转换（重写，从纯概念改为方法论）
  - [[Causal Chain Audit]] — 因果链审计
  - [[Single Version Principle]] — 单一版本原则
  - [[Binary Question]] — 二进制提问法
  - [[Cut Priority Method]] — 删减优先级方法
- Pages updated: [[index]], [[concepts/_index]], [[log]]
- Key insight: Wiki 存的是**方法论**，不是纯概念定义。只有被多个 Skill 复用的方法论才值得放到 Wiki 里。从 W6 里提炼的这 8 个方法论都是跨领域可复用的，不只是写剧本能用，做设计、写文案、出图、做产品、写代码都能用。

## [2026-06-23] Concept creation | Skill Five-Layer Structure
- Extracted from analysis of W5, W6, and HKH image workflow skills
- Pages created:
  - Concepts: [[Skill Five-Layer Structure]]
- Pages updated: [[index]], [[concepts/_index]], [[log]]
- Key insight: A complete Skill has 5 layers: methodology → execution rules → workflow → output tools → quality control. Wiki stores layer 1 (methodology), Skills store all 5 layers. This framework can be used to evaluate and improve any existing skill.

## [2026-06-23] Entity creation | Google ADK
- Created [[Google ADK]] entity page (framework type)
- Pages updated: [[index]], [[entities/_index]], [[hot]], [[log]]
- Key insight: Fills the gap from the earlier 5 Agent Skill Design Patterns ingest — the source mentioned ADK extensively but didn't have a dedicated entity page. ADK Core Skills are all Tool Wrapper pattern; Google dogfoods the same SKILL.md format for both development workflow and production runtime.

## [2026-06-23] Entity creation | Google ADK
- Created entity page for Google ADK (Agent Development Kit)
- Pages created:
  - Entities: [[Google ADK]]
- Pages updated: [[index]], [[log]]
- Key insight: ADK is Google's framework for building production AI agents with modular skills. Implements the Agent Skills specification adopted by 30+ tools. Directly relevant to Kevin's skills-main project — same SKILL.md format and design patterns.

## [2026-06-23] Ingest | 5 Agent Skill Design Patterns
- Source: Google Cloud Tech (Twitter/X), Chinese translation via CSDN
- Raw file: `Clippings/raw/5 Agent Skill设计模式.md`
- Pages created:
  - Concepts: [[Agent Skill Design Patterns]]
  - Sources: [[5 Agent Skill Design Patterns]]
- Pages updated: [[index]], [[hot]], [[log]]
- Key insight: Five standardized patterns for structuring Agent skill logic (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline). The progressive disclosure mechanism is foundational — skills load in layers (metadata → instructions → references on-demand). Patterns are composable, not mutually exclusive. Directly relevant to Kevin's skills-main project.

## [2026-06-23] Wiki structure initialized
- Adopted claude-obsidian LLM Wiki structure
- Folders: concepts/, entities/, sources/, questions/, meta/
- Imported 14 concept pages, 7 entity pages, 1 source page, 1 question page from claude-obsidian reference
- Status: initial setup complete

## [2026-06-23] Concept extraction | Image Generation principles from HKH project
- Extracted 5 core principles from HKH brand image generation experience
- Pages created:
  - Concepts: [[描述比重原则]], [[视觉描述优先原则]], [[参考图优先原则]], [[克制原则]], [[一致性锚点原则]]
- Pages updated: [[index]], [[concepts/_index]], [[log]], [[hot]]
- Backlinks added to 7 skill/case files in Projects/HKH品牌/作图经验/
- Key insight: These 5 principles appear across multiple skills (burning scenes, white background, lyrical realism, collaboration flow), confirming they are generalizable principles rather than project-specific tricks. They form the foundation of a prompt engineering methodology for AI image generation.

## [2026-06-23] Lint | Full health check
- Pages scanned: 30
- Issues found: 6 (3 frontmatter gaps, 1 missing page reference, 1 isolated concept, 1 entity missing fields)
- Report: [[meta/lint-report-2026-06-23]]
- Key finding: 3 imported concept pages lack frontmatter fields; 2 historical ingest targets never synced to this vault

## [2026-06-23] Batch ingest | Local LLM Deployment ecosystem (7 sources)
- Sources: Ollama Official Documentation, Antigravity Tools, Claude Code+Ollama/LM Studio/oMLX/OptiQ tutorials
- Pages created:
  - Concepts: [[Ollama]], [[Local LLM Deployment]], [[Claude Code Local Setup]], [[Anthropic Compatible API]], [[Apple Silicon Optimization]], [[Model Quantization]]
  - Entities: [[Antigravity Tools]], [[LM Studio]], [[oMLX]], [[OptiQ]], [[Tencent Cloud Copilot]]
  - Sources: [[sources/Ollama Official Documentation]], [[sources/Antigravity Tools]], [[sources/Claude Code + Ollama Tutorial]], [[sources/Claude Code + LM Studio Tutorial]], [[sources/oMLX Tutorial]], [[sources/OptiQ Tutorial]]
- Pages updated: [[index]], [[concepts/_index]], [[entities/_index]], [[sources/_index]], [[log]]
- Key insight: The local LLM ecosystem for Claude Code has multiple runtimes (Ollama/LM Studio/oMLX/OptiQ) plus cloud proxy (Antigravity Tools), all sharing the same Anthropic-compatible API pattern. Ollama is the primary runtime; Antigravity Tools provides an alternative cloud path via Tencent Copilot.

## [2026-06-23] Concept ingest | AI Camera Movements from Bilibili video
- Source: Bilibili video [BV1xBjW6pEym](https://www.bilibili.com/video/BV1xBjW6pEym) (AI 运镜提示词)
- Pages created:
  - Concepts: [[AI Camera Movements]]
- Pages updated: [[concepts/_index]], [[log]]
- Key insight: 30+ 种运镜手法，分为基础运镜、动态情绪运镜、角度视角、进阶技巧四类。讲故事并不需要大量运镜，许多优秀电影仅用硬切也能达到很好效果。

## [2026-06-23] Batch ingest | Storytelling concepts from W6 screenwriting skill
- Source: W6-视频创作/俄语详细剧本 skill (methodology.md, style-rules.md, timing-and-cutting.md)
- Pages created (13 concepts):
  - Core principles: [[Show Don't Tell]], [[Controlling Idea]], [[Scene Value]], [[Chekhov's Gun]], [[If You Remove It Does It Change]], [[Progressive Complications]], [[Pacing and Rhythm]]
  - Classic structures: [[Three-Act Structure]], [[Hero's Journey]], [[Inciting Incident]]
  - Tragedy theory (Aristotle): [[Hamartia]], [[Peripeteia and Anagnorisis]], [[Catharsis]]
- Pages updated: [[concepts/_index]], [[log]]
- Key insight: Many screenwriting principles map directly to AI image/video generation best practices. "Show don't tell" = Visual Description First Principle; "Controlling Idea" = Description Weight Principle. The same underlying logic applies across domains.

## [2026-06-23] Concept ingest | Character Bible & Worldbuilding from W6 templates
- Source: W6-视频创作/俄语详细剧本 templates (characters.template.md, worldbuilding.template.md)
- Pages created (2 concepts):
  - [[Character Bible]] — 8层角色构建系统：基础→外观→心理学→传记→弧线→声音→关系→关联物体
  - [[Worldbuilding]] — 世界观构建：世界规则→系统→历史→势力→地点→物体地雷→知识层级
- Pages updated: [[concepts/_index]], [[index]], [[log]]
- Key insight: 角色圣经的核心是"欲望 vs 需求"——角色以为自己想要的和真正需要的，这是角色弧线的引擎。世界观的核心是"规则与限制"——没有限制的系统=作弊器，没有戏剧张力。

## [2026-06-23] Concept ingest | Intent Recognition from Bilibili video + W6 workflow
- Source: Bilibili video [BV1HTGy68EUF](https://www.bilibili.com/video/BV1HTGy68EUF) (《浅入深出》Agent系列之十二：意图识别) + W6-视频创作/俄语详细剧本 workflow.md
- Pages created:
  - Concepts: [[Intent Recognition]]
- Pages updated: [[concepts/_index]], [[index]], [[log]]
- Key insight: 意图识别不只是"第一次路由"，而是贯穿整个交互过程——每一轮用户输入都要先识别意图，再走对应的工作流。技能选择本质上就是意图识别。

## [2026-06-23] Concept ingest | Intent Recognition from Bilibili video + W6 workflow
- Source: Bilibili video [BV1HTGy68EUF](https://www.bilibili.com/video/BV1HTGy68EUF) (《浅入深出》Agent系列之十二：意图识别) + W6-视频创作/俄语详细剧本 workflow.md
- Pages created:
  - Concepts: [[Intent Recognition]]
- Pages updated: [[concepts/_index]], [[index]], [[log]]
- Key insight: 意图识别不只是"第一次路由"，而是贯穿整个交互过程——每一轮用户输入都要先识别意图，再走对应工作流。技能选择本质上就是意图识别。
