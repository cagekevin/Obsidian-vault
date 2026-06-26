---
name: 技能规范审计
description: Audit a skill file for structural compliance, naming conventions, and most importantly — content-level consistency, variable alignment, and logic coherence. Use when user wants to check if a skill follows project conventions and has no internal contradictions.
---

# 技能规范审计 (Skill Audit)

<what-to-do>
作为系统架构师，对 Skill 文件执行从外层结构到内层逻辑的逐层审计：

### A — 结构规范
1. **文件与目录结构**：前缀（S/W）是否正确？目录是否单层扁平？
2. **Frontmatter**：`name` 纯中文且无编号前缀；`description` 以功能描述开头、以 `Use when` 结尾。
3. **核心标签**：是否完整包含 `<what-to-do>` 和 `<supporting-info>`？

### B — 内容一致性（核心）
4. **变量命名一致性**：同一个概念在全文中是否使用相同名称？
   - 例如：某处叫 `{Payload_Badges}`，另一处叫 `{Payload_Badge}` → 不一致，需统一。
   - 例如：Rules 区叫"零占位符准则"，正文里却写"不得出现 {}"引用的是同一个规则吗？
5. **前后逻辑通顺**：两条规则是否自相矛盾？
   - 例如：A 处说 "手动编辑 .mdc"，B 处说 "mdc 只读自动生成" → 冲突。
   - 例如：先定义 "<=3 走角标"，后面又说 "3 个以下走清单" → 矛盾。
6. **引用完整性**：文件内引用的子文件/路径是否存在？`<route-table>` 中声明的文件在目录中是否真实存在？
7. **重复与冗余**：同一件事情是否在不同位置以不同表述各说了一遍？是否合并后更清晰？
8. **Hub-Spoke 路由完整性**：如果是枢纽文件，`<route-table>` 声明了哪些分支？分支文件在磁盘上物理存在吗？磁盘上有但没有声明到路由表的文件是否存在遗漏？
9. **Trigger 实现完整性**：声明了双模触发（MODE A / MODE B），两种模式的逻辑都实现了吗？还是只写了 MODE A 留了 MODE B 的空壳？
10. **Example 与正文对齐**：End-to-End Example 中的步骤/参数数量是否与正文 Checklist 一致？
    - 例如：Checklist 有 5 项，Example 表格却列了 7 项 → 不一致。
11. **种子文件存在性**：`<supporting-info>` 引用的文件（如 `deep-modules.md`、`refactoring.md`、`triage-labels.md`）在目录中物理存在吗？路径正确吗？

### D — 架构设计评价
12. **模块边界**：这个技能的职责边界是否清晰？有没有越界做了不该做的事（例如 S1/S2/S3 合并前，各自的功能在心理模型上是否正交）？
13. ** Hub-Spoke 必要性**：枢纽 + 分支的架构是否真的有必要？还是说当前内容的复杂度一张 .md 就能装下，不需要分流？
14. **同类技能重叠**：这个技能和已有的其他技能之间有没有功能重叠？用户应该在什么情况下选这个，什么情况下选另一个？边界是否清楚？
15. **流程设计是否合理**：技能的阶段/步骤划分是否自然？有没有"为了凑结构而硬分阶段"的情况？用户使用这个技能的直觉路径通顺吗？

### C — 输出报告
- 🟢 **通过项**：结构合规 + 无内容矛盾。
- 🔴 **违规项**：列出具体位置（行号或段落引用）和违规描述，直接提供修复代码块。
- 💡 **防呆提醒**：报告末尾提醒"已在两处注册（桶 README、根 README）并运行 `skills-init`"。
</what-to-do>

<supporting-info>
子技能分支文件同样需完整 Frontmatter（`name` + `description`），纯英文命名且无需编号前缀。
</supporting-info>
