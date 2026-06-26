---
name: 提示词审计
description: Audit and optimize prompts using advanced prompt engineering standards. Use when user wants to review, diagnose, or improve a prompt.
---

# 提示词质量审计 (Prompt Audit)

<what-to-do>
基于高阶提示词工程（Prompt Engineering）标准，对用户的提示词进行外科手术式的拆解和优化：

1. **结构完整性审查**：
   - **Role (角色)**：是否赋予了 AI 明确的专家身份和能力边界？
   - **Context (上下文)**：背景信息是否充足？任务目的（Why）是否交代清楚？
   - **Task (任务)**：指令是否清晰无歧义？是否存在多重复杂任务揉杂在一起未做分步（Step-by-step）拆解的情况？
   - **Format (输出格式)**：是否明确规定了输出形式（如 JSON, Markdown 表格, 或禁用特定的客套话）？
2. **边界与反向约束 (Negative Prompts)**：
   - 是否定义了 AI "绝对不能做什么"（例如：禁止虚构数据，禁止脱离上下文猜测）？
3. **Token 效率检查**：
   - 提示词中是否存在冗余的废话？是否可以通过精简词汇来节省上下文窗口？

**执行输出**：
1. **【当前质量评分】**：给出 1-10 分的综合评估。
2. **【诊断报告】**：直白地列出缺失或冗余的部分。
3. **【重构版本】**：直接输出一个经过你优化、结构严谨、可直接复制使用的专业级 Prompt 模板。
</what-to-do>

<supporting-info>
优秀的 Prompt 往往包含 Few-Shot（少样本）。如果用户的 Prompt 缺乏示例，务必在【重构版本】中为其预留或生成对应的 `<examples>` 区块。
</supporting-info>
