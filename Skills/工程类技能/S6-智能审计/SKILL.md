---
name: 智能审计
description: 结构化审计引擎。对照检查清单对技能文档、代码质量、提示词编写及 PR 架构进行逐项审查并输出严重等级报告。Use when user wants to audit a skill, review code, check skill compliance, audit prompts, inspect a project, run PR architecture review, verify skill standards, audit skill structure, or says "帮我审计" / "审一下" / "检查合规".
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

# 智能审计

<what-to-do>
1. **识别意图**：分析用户提供的是技能文档、代码片段、提示词还是 PR diff。
2. **按 5 大模式指派审计类型**：本库所有审计均遵循 Reviewer 模式——对照检查清单，按严重程度分级输出。
3. **路由分发**：根据下方路由表调用对应的审计标准文件进行深度检查。

# <route-table>
| 路由 | 审计类型 | 5大模式归类 | 文件 | 触发关键词 |
|---|---|---|---|---|
| 技能规范审计 | 技能 .md 结构 + 内容一致性 | reviewer | skill-audit.md | 技能, skill, md, 结构, 规范 |
| 提示词审计 | Prompt 质量与结构 | reviewer | prompt-audit.md | 提示词, prompt, prompt engineering |
| 代码质量审计 | 代码安全/性能/健壮性 | reviewer | code-audit.md | 代码, bug, python, review |
| PR架构审查 | Git diff 架构/需求对齐 | reviewer | 代码审查评估.md | pr, diff, 架构, git diff, merge |
| 文本叙事审计 | 故事逻辑/人类叙事直觉/80%受众接受度 | reviewer | 文本叙事审计/文本叙事审计.md | 文本审计, 故事逻辑, 叙事连贯, 像不像人写的 |
</what-to-do>

<supporting-info>
## 审计总则
- **保持客观中立**：所有指出的问题必须附带"修改建议"或"修复代码"。
- **幻觉防御**：不确定的东西不要编造。如果是对某个模式的推测，必须标明"疑似"或"建议确认"。严禁把大概率猜测包装成事实。
- **废话防御**：每个发现必须至少用一句话说清楚"为什么这是个问题"。禁止写"需要优化"、"建议改进"这种空话。如果没有发现，就不要写那一块的结论段落。
- **内容决定格式**：审计输出时，存在问题的维度写详细，没问题的维度直接跳过。不要每个维度都写一段"未发现问题"——没有结论就是最好的结论。
- 所有审计结果必须按严重等级分层：🔴 违规 / 🟡 值得商榷 / 💡 建议优化。
</supporting-info>
