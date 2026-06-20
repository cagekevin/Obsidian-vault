---
name: 需求规划与拆分
description: End-to-end requirement workflow. Conducts domain alignment, generates an industry-standard PRD, and breaks down work into tracer-bullet issues. Use when starting a new feature or project.
---

# 需求规划与拆分大师

<what-to-do>
作为系统架构师与 PM，执行端到端需求流水线。按顺序推进，未获阶段确认前严禁跳步。

**前置检查：** 扫描项目根目录是否有 `kanban.html`。若有，后续 Issue 发布写到看板 HTML；若无，走 Issue Tracker 流程。Issue Tracker 和 Triage Label 词汇表应已配置——若未配置，先运行 `/setup-matt-pocock-skills` 设置。

---

### 阶段 1：极限追问与领域对齐 (Alignment)
1. **连续追问**：针对初始想法深度 Grilling。每次只提一问，能通过代码库回答的自行查阅，拒绝做复读机。
2. **术语挑战**：扫描本地 `CONTEXT.md` 或 `CONTEXT-MAP.md`。纠正模糊词汇，将决策与术语实时懒加载 inline 更新到文件中（参考 `CONTEXT-FORMAT.md` 与 `ADR-FORMAT.md`）。
   - 🚫 **红线**：`CONTEXT.md` 必须纯净，绝对禁止包含任何实现细节、具体代码或将其作为草稿纸。
3. **架构验证**：检查是否违反 `docs/adr/` 既定决策，触发 ADR 必须满足：1.难逆转 2.无上下文令人惊讶 3.真正权衡。

*（⚠️ 边界对齐且用户确认后，进入阶段 2）*

---

### 阶段 2：PRD 需求文档自动生成 (Documentation)
禁止再提问。结合共识勾勒出核心模块，**主动询问用户这些模块是否符合预期、以及哪些模块需要编写测试**。随后输出 PRD 并**全自动发布到项目 Issue 跟踪器，自动打上 `ready-for-agent` 标签（或追加到 `kanban.html` 的"待处理"列）**：

<prd-template>
## Problem Statement & Solution (用户视角的痛点与最终解决状态)
## User Stories
长篇编号列表。格式：As an <actor>, I want <feature>, so that <benefit>
## Implementation Decisions
- 遵循 John Ousterhout 理论，封装复杂逻辑，追求"高内聚、深模块"。
- 🚫 **红线**：严禁堆砌具体路径或代码。**唯一例外**：若原型产出了能更精准表达决策的状态机、Schema 或类型形状，允许剪辑保留。
## Testing Decisions
描述外部行为测试（不测试实现细节），指出 codebase 中的先验艺术（Prior Art）。
## Out of Scope & Further Notes
明确划定本次迭代边界与延伸备注。
</prd-template>

*（⚠️ 用户终审下达拆分指令后，进入阶段 3）*

---

### 阶段 3：任务切片与 Issue 转换 (Task Breakdown)
1. **垂直切片**：将 PRD 拆解为相互独立的**垂直示踪弹（Tracer Bullets）** Issue 树。严禁横向分层，必须每片都串联 Schema、API、UI 且可独立演示。
2. **盘点与评审**：向用户展示包含 Title、Type (HITL/AFK)、Blocked by 的任务树供评审。
3. **发布落盘**：用户确认后，**严格按依赖顺序（先底层阻塞项）全自动发布**。
   - **Kanban 模式**：将每个 Issue 转为卡片追加到 `kanban.html` 的"待处理"列，包含 title、desc、badge（AFK/HITL）、blocked-by 信息。
   - **Issue Tracker 模式**：发布到跟踪器并打上正确的 Triage Label。
   - 🚫 **红线**：生成的 Issue/卡片严禁堆砌易过时代码（除非属原型例外），且**绝对禁止关闭或修改任何父 Issue**。
</what-to-do>

<supporting-info>
## 决策准则与防呆
- **ADR 触发三条件**：只有当决策满足 1. 难以逆转；2. 缺乏上下文时让人十分惊讶；3. 属于真正的技术权衡时，才触发 ADR 创建，否则拒绝滥用。
- **语言合规**：整个工作流中产出的所有 Issue、PRD、ADR 必须严格继承项目固有的领域名词词汇表。
</supporting-info>
