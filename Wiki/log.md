我---
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

## [2026-06-30] Concept creation | AI 长视频丝滑衔接
- Source: B 站视频 [BV1qyjb6XEmX](https://www.bilibili.com/video/BV1qyjb6XEmX/) — 李一帆AIGC 2026-06-21
- Summary: [[AI长视频丝滑衔接]]
- Pages created: [[AI长视频丝滑衔接]] (concept)
- Pages updated: [[concepts/_index]], [[index]], [[hot]], [[log]]
- Key insight: 真正限制 AI 长视频制作的不是 15 秒，而是硬续长镜头。电影本来就不是一镜到底，而是靠镜头组接完成叙事。三种方法由浅入深：切换景别角度（基础）、动作中衔接利用视觉暂留（进阶）、分镜组接镜头（终极）。

## [2026-06-29] Audit + skill update | Wiki 流程审计与执行链补全
- Summary: 对 4 个 wiki skill + schema.md 做完整审计，发现 8 个问题（A 类 5 条「删了会出错」+ B 类 3 条「加了有好处」）。按方案 II 全部修复。
- Files updated: `Wiki/skills/ingest.md`（加中文触发词 + Step 0 hot.md/manifest 检查 + manifest 更新入主流程）, `Wiki/skills/save.md`（加 Type 映射提示脚注）, `Wiki/skills/lint.md`（加第 11 项 Schema rule enforcement + 报告模板）, `Context/schema.md`（加 Type 字典）
- Key insight: **规则加进 schema 但不进入执行链 = 形同虚设**。今天 3 条新规则同步进 lint.md 第 11 项后，规则 → skill → lint 形成闭环。A 类 5 条全是「删了会出错」类必加；B 类 3 条把规则"穿透"到执行链。
- 跳过：B-#8（query.md Deep mode 默认存答案）属于"用户偏好调整"，等 Kevin 显式要求再做。
- 审计报告：本次对话内输出，未单独存档。

## [2026-06-29] Schema update | 工具调用与 wikilink 规范（第七节）
- Summary: 在 `Context/schema.md` 新增第七节，写入 3 条规则——工具调用路径用 `Wiki/` 大写、Manifest 必建必更新、Wikilink 避免中文 `#章节锚点`
- Files updated: `Context/schema.md`
- Key insight: 3 条规则均来自今天 ingest 的实战教训（路径大小写、manifest 缺失、wikilink 锚点），是「系统长远必加」类。生效范围仅限新写入内容，旧页面不追溯修复。
- 来源：本次 Seedance 2.0 标点控声 ingest 的维护性修复（见上一条 log）

## [2026-06-29] Maintenance | Manifest 骨架 + wikilink 锚点修复
- Summary: 建 `.raw/.manifest.json` 骨架（补 c-000015 条目）+ 修 [[AI角色声音控制]] 第 186-187 行的 `#章节锚点`（含中文冒号，第三方解析会失败）
- Files created: `.raw/.manifest.json`
- Files updated: `Wiki/concepts/AI角色声音控制.md`
- Key insight: 今天 ingest 暴露 2 个系统性问题——manifest 缺失让 delta tracking 流程空转、wikilink 锚点含中文让跨工具解析失败。两者都不是单点问题，而是"以后同类问题会反复出现"的系统问题。配套的 schema 规则建议已提交，等 Kevin 确认后再加到 `Context/schema.md`。
- 跳过：address 跳号（c-000016~c-000041）经查是历史 cleanup 删除页面导致，DragonScale 设计预期（counter 不回收），无需修。

## [2026-06-29] Concept update + Source creation | Seedance 2.0 标点控声
- Source: 用户从 B 站下载的视频转录稿（AI 智能夏老师 BV1VTTG6kEHN，2026-06-28）
- Summary: [[sources/Seedance 2.0 标点控声]]（address: c-000015）
- Pages created: [[sources/Seedance 2.0 标点控声]]
- Pages updated: [[AI角色声音控制]]（追加"标点控声实战深化"小节，保留原标点表不变）, [[concepts/_index]], [[sources/_index]], [[index]], [[log]], [[hot]]
- Key insight: AI 默认不懂情绪，标点符号（特别是省略号"声断气连"）是最被低估的情绪控制工具；拆句+换行 = 多镜头的情感落点节奏。补强了 [[AI角色声音控制]] 在"标点控声"维度的实战案例。

## [2026-06-27] Concept creation | AI 室内光控制
- Summary: 光源锚定、衰减路径、漫反射三大法则
- Pages created: [[AI室内光控制]]
- Pages updated: [[concepts/_index]], [[index]], [[log]], [[hot]]
- Key insight: 室内光的本质不是"亮度控制"，而是"空间理解"。拒绝AI的"无源之光"，手动接管布光权。

## [2026-06-27] Concept creation | AI 创意方法论
- Summary: 打破物理定律、让时间失控、把镜头变成角色
- Pages created: [[AI创意方法论]]
- Pages updated: [[concepts/_index]], [[index]], [[log]], [[hot]]
- Key insight: 创意往往来自"不合理"——观众在信息流里不是被"清晰度"吸引的，而是被"违和感"抓住的。

## [2026-06-27] Concept update | AI 镜头语言进阶
- Summary: 情绪蒙太奇三法扩展：客观对应物法则、库里肖夫效应、视觉聚焦法则
- Pages updated: [[AI镜头语言进阶]], [[concepts/_index]], [[log]], [[hot]]
- Key insight: 不要只告诉 AI 角色"看起来怎么样"，要告诉 AI 画面"让观众感受到什么"。

## [2026-06-27] Concept creation | AI 角色声音控制
- Summary: 声音公式、语气控制、多句台词递进、标点符号节奏、声音模板
- Pages created: [[AI角色声音控制]]
- Pages updated: [[concepts/_index]], [[index]], [[log]], [[hot]]
- Key insight: 控制 AI 声音的核心不是堆砌情绪词，而是搭建声音结构。不要只告诉 AI 角色是谁，要告诉 AI 角色怎么说话。

## [2026-06-27] Concept update | AI 导演创作思维
- Summary: 新增"画面结构拆解法"章节
- Pages updated: [[AI导演创作思维]], [[concepts/_index]], [[log]], [[hot]]
- Key insight: 反推提示词的误区（标签词 vs 画面结构）、画面结构四维度、时间线逐帧拆解法、物理世界描述原则。

## [2026-06-27] Concept creation | AI 空镜设计
- Source: 用户提供的 AI 短剧空镜设计资料
- Summary: [[AI空镜设计]]
- Pages created: [[AI空镜设计]]
- Pages updated: [[AI镜头语言进阶]]（空镜章节改为引用）, [[concepts/_index]], [[index]], [[log]], [[hot]]
- Key insight: 空镜不只是风景画面，三类提取（环境/道具/情绪）+ 五要素公式（主体/状态/动态/光线/运镜）+ 放置策略构成完整方法论。

## [2026-06-27] Concept creation | 利益视觉化原则
- Source: Skills/W5-图片设计/通用图片设计流程.md
- Summary: [[利益视觉化原则]]
- Pages created: [[利益视觉化原则]]
- Pages updated: [[通用图片设计流程]], [[concepts/_index]], [[index]], [[log]], [[hot]]
- Key insight: 配图的本质是利益视觉化——利益是主角，产品是配角，渠道是装饰。附配图思维链模板作为落地工具。

## [2026-06-27] Batch ingest | 刺猬星球 AI 创作系列（66 篇视频教程）
- Source: `.raw/articles/刺猬星球系列/_刺猬星球系列合辑-2026-06-27.md`（66 个视频的文字转录稿，共 4.2 万字）
- Summary: [[sources/刺猬星球AI创作系列]]
- Pages created:
  - Concepts: [[AI角色资产搭建]], [[AI视觉语法体系]], [[AI镜头语言进阶]], [[AI环境空间设计]], [[AI氛围与色彩控制]], [[AI视频动作设计]], [[AI底层机制与高级控制]], [[AI导演创作思维]], [[时间补偿机制与动态词学]], [[视觉平衡与动线构图]], [[风格提取与约束系统]], [[人感审美与材质重塑]], [[物理模拟控制流（Cinema Studio）]]
  - Sources: [[sources/刺猬星球AI创作系列]]
- Pages updated: [[AI打光五法]]（补充光线控制关联）, [[AI Camera Movements]]（补充镜头语言关联）, [[光线布置模块化]]（补充刺猬星球源关联）, [[concepts/_index]]（新增角色/环境/氛围/视频/机制/思维分类）, [[sources/_index]], [[index]], [[log]], [[hot]]
- Key insight: 刺猬星球的 66 篇教程覆盖了 AI 图片/视频创作的完整技能树，从基础提示词到导演思维。这批内容与现有 Wiki 高度互补——填补了角色设计、环境空间、动作设计、底层机制等空白领域，同时丰富了镜头语言和氛围色彩。提炼出的 13 个概念页形成了"基础→进阶→高级→创作思维"的递进体系。

## [2026-06-27] Ingest | AI 打光 5 种导演级方法 + 20 种光源模板
- Source: `.raw/articles/AI打光5种导演级方法-2026-06-27.md` + `.raw/articles/20种光照参考资料-2026-06-27.md`
- Summary: [[sources/AI打光5种导演级方法]]
- Pages created: [[AI打光五法]], [[光线布置模块化]], [[AI光源提示词模板库]], [[sources/AI打光5种导演级方法]]
- Pages updated: [[摄影语言锚定质感]]（补充打光相关概念关联）, [[AI Camera Movements]]（补充打光概念关联）, [[concepts/_index]], [[sources/_index]], [[index]], [[log]], [[hot]]
- Key insight: 光线是 AI 画面从"生成感"走向"影像感"的关键。五法提供方法论（怎么想），光线布置模块化提供写法结构（怎么写），20 种模板提供可直接复制使用的实战工具（直接用）。三者构成"原理→结构→模板"的完整打光知识链。

## [2026-06-26] Ingest | Google Open Knowledge Format (OKF)
- Source: Google Cloud Blog + Kevin 提供的摘要
- Summary: [[sources/Google OKF 2026]]
- Pages created: [[Open Knowledge Format]], [[sources/Google OKF 2026]]
- Pages updated: [[LLM Wiki Pattern]]（补充 OKF 作为其标准化实现）, [[index]], [[log]], [[hot]]
- Key insight: OKF 是 Karpathy 的 LLM Wiki 模式的具体标准化实现，三大原则（最少干预、生产者与消费者解耦、格式非平台）解决了此前 Obsidian/Notion/AGENTS.md 各自为战的知识孤岛问题。

## [2026-06-25] Concept creation | 文案完整保留与信息层级原则
- Source: `Skills/工作效率类/W5-图片设计/amazon-skincare/skill_副本.md`（天猫详情页 9:16 图片生成引擎）
- Pages created: [[文案完整保留与信息层级原则]]
- Pages updated: [[一致性锚点原则]]（补充"全局风格只写一次"技巧）, [[产物先行]]（补充"九宫格预览"交付物写法）, [[concepts/_index]], [[log]], [[hot]]
- Key insight: 两条规则——1) 用户提供的文案必须一字不漏完整保留，不受描述比重原则约束；2) 排版布局不写具体位置和对齐方式，改为写信息层级（哪个最重要、哪个次重要），让 AI 自行决定。这两个规则来自实战——AI 无法精确执行布局指令，但能理解优先级。

## [2026-06-24] Concept creation | AI 生图决策规则
- Source: GitHub - c3115644151/imageforge-skill
- Summary: [[sources/ImageForge-生图决策引擎]]
- Pages created: [[AI 生图决策规则]]
- Pages updated: [[index]], [[concepts/_index]], [[sources/_index]], [[hot]], [[log]]
- Key insight: 从 imageforge 的 19 条 if-then 规则中提炼了 6 条可复用规则，每条标注了与已有 Wiki 概念（克制原则/视觉描述优先原则/一致性锚点原则/变量与不变量分离）的关联。核心模式是用 if-then 的可执行格式替代教育原理式的解释。

## [2026-06-24] Concept update | AI Camera Movements 补充英文运镜词汇 + 灯光词汇表
- Source: GitHub - anil-matcha/Awesome-Seedance-2.5-API-Prompts（第三方 Seedance 2.5 提示词指南，非官方）
- Summary: [[sources/Seedance-2.5-Prompt-Guide]]
- Pages updated: [[AI Camera Movements]]
- Key insight: 一个灯光关键词 > 十个形容词。运镜词用英文精确术语比中文描述效果更好。灯光词汇表和运镜词汇表可以直接在写提示词时复制使用。

## [2026-06-24] ingest | Hermes Agent 技能自管理机制
- Source: GitHub - NousResearch/hermes-agent
- Summary: [[sources/Hermes-Agent]]
- Pages created: [[AI技能自管理]]
- Pages updated: [[index]], [[sources/_index]]
- Key insight: 三个可复用机制——技能自动生成（AI 按模板填坑写 SKILL.md）、使用追踪（记录最后使用时间）、生命周期管理（30天没用标记 stale，90天归档）

## [2026-06-24] ingest | Dramatic Gobo Lighting
- Source: GitHub - Mixiaxiaoyu/dramatic-gobo-lighting
- Summary: [[sources/Dramatic-Gobo-Lighting]]
- Pages created: [[Gobo投影光影]]
- Pages updated: [[index]], [[sources/_index]]
- Key insight: 核心价值是 64 张 Gobo 素材图，不是标签。用法是把 Gobo 图作为垫图 + 提示词模板告诉模型"只改光影不改其他"

## [2026-06-24] ingest | AI 图像生成提示词 28 案例
- Source: `.raw/我拆了OpenAI官方28个案例，发现提示词的核心根本不是词汇量.md`
- Summary: [[sources/OpenAI-GPT-4o-Image-Generation-28案例]]
- Pages created: [[变量与不变量分离]], [[产物先行]], [[小步迭代]], [[提示词模板八要素]], [[角色锚定]], [[摄影语言锚定质感]], [[编辑三要素]], [[反向约束]]
- Pages updated: [[index]]
- Key insight: 从 GPT-4o 官方案例中提炼了8个可复用的提示词方法论，核心模式是"变量与不变量分离"和"编辑三要素"，与现有的克制原则/一致性锚点原则互补

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
- Raw file: `.raw/5 Agent Skill设计模式.md`
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
