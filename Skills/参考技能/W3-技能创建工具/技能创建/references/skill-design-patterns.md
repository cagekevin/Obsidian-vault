# Skill 设计技法大全

本文件收录来自 Anthropic 官方 skill-creator、社区最佳实践（Alireza Rezvani、VoltAgent 等）以及 Claude Code 官方文档的 18 种核心设计技法。

---

## 一、触发与加载技法

### 1. 描述触发法（Trigger Engineering）
Claude 根据 skill 的 description 决定是否调用。最关键的设计技法。

**核心原则**：
- description 要写得**带点侵略性（pushy）**：不只写"做什么"，还要写**什么场景下必须用**
- 格式：`首句核心功能 + 末句 Use when [场景关键词].`
- 背景：AI 天生有 undertrigger（触发冷淡）倾向，所以要主动"抢"触发

**好例子**：
```
不触发日志："完整数据仪表盘"
触发定位："每次用户需要可视化数据时，无论是否明确说出"仪表盘"关键词，都应考虑使用本技能"
```

**进阶技巧**：写 20 条 realistic query（10 条应触发 + 10 条不应触发），跑自动优化循环迭代 description。

### 2. 三级加载解耦法（Progressive Disclosure）
内容拆成三层，按需加载，节约上下文预算。

| 层级 | 内容 | 加载时机 | 体积限制 |
|------|------|---------|---------|
| Level 1 | name + description | 永远在上下文 | ~100 词 |
| Level 2 | SKILL.md 正文 | 技能触发时 | <500 行 |
| Level 3 | references/ scripts/ assets/ | 需要时才读 | 无限制 |

**应用**：你的技能已经用了这个技法 —— 把长表格放 references/，可执行脚本放 scripts/。

### 3. 文件分流法（Domain Organization）
当一个 skill 支持多个领域时，用文件分流代替 if-else 嵌套：

```
cloud-deploy/
├── SKILL.md (工作流 + 选择逻辑)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude 只加载与当前场景相关的参考文件。

### 4. 动态上下文注入法（Dynamic Context Injection）
用 `` !`command` `` 语法在 Claude 读到内容之前执行命令，注入实时数据：

```markdown
## Current changes
!`git diff HEAD`
```

这个命令在 Claude 看到之前就执行，输出直接替换掉这一行。

多行命令用 \`\`\`! 代码块：
```
## Environment
```!
node --version
npm --version
git status --short
```
```

---

## 二、内容写作技法

### 5. 解释原因法（Explain the Why）
**不用 `ALWAYS` / `NEVER` / 必须**，而是解释**为什么这么做**。现代 LLM 有 theory of mind，解释了原因它能举一反三。

**差**：
```
ALWAYS add error handling
```

**好**：
```
Add error handling for network requests. Network calls can fail for many reasons —
timeouts, rate limits, server errors — and without handling these, the user
gets a cryptic crash instead of a helpful message.
```

### 6. 示例驱动法（Examples Pattern）
给出 Input → Output 对照示例，比长篇描述管用：

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### 7. Practitioner Voice（从业者语气法）
每个 skill 以专家身份和明确目标开头。不是教科书 —— 是干了 100 次的资深从业者在指导你。

**好**：
```markdown
You are an expert in SaaS pricing. Your goal is to help design pricing that captures value.
Lead with their world, not yours.
```

**反例**：
```markdown
❌ This skill provides comprehensive coverage of...
❌ The following section outlines the various approaches to...
❌ It is recommended that one should consider...  (被动语态)
```

**规则**：
- 用缩略语、直接口语
- "Do X" 优于 "You might consider X"
- 有观点 > 中立 —— 直接说哪个有效、哪个无效
- 对圈内人用行话 OK，对创始人要解释

### 8. 避免过拟合法（Generalize from Feedback）
迭代 skill 时，不要针对单个测试用例做"补丁式"修改（overfit）。如果某个问题反复出现：
- 换**不同的比喻/模式**来重写指令，不要加更多 MUST
- 如果用户反馈很简短，要去真正理解他**为什么**这么说

### 9. 透明输出格式法（Define Output Format）
用模板锁死输出结构：

```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

---

## 三、交互与流程技法

### 10. 反转面试法（Inversion）
AI 拿到需求后**不能直接干活**，必须一次只问一个问题，收集完所有约束才动手。

**核心指令**：`DO NOT start building until all phases are complete`

**应用**：你的 W3-技能创建工具 的"反转面试"阶段就用这个。

### 11. Hub-Spoke 路由法
一个入口文件 + `<route-table>` 路由表，根据用户需求分流到不同子技能。

**应用**：你的 `W1-沟通/W1-沟通.md` 就用这个模式。

### 12. 步骤检查点法（Pipeline Checkpoint）
多个串行步骤，每步设**硬性检查点**，前一步未确认不进下一步。

**应用**：你的技能中最常用的模式（第一、二、三步），关键是要加："→ 用户确认后方可进入下一步"

### 13. 子代理隔离法（context: fork）
复杂任务在隔离的子代理中运行，不污染主对话上下文：

```yaml
---
name: deep-research
context: fork
agent: Explore
---
```

### 14. 多模式工作流法（Multi-Mode Workflows）
大多数技能有 2-3 个自然入口点。全部设计好：

```markdown
## How This Skill Works
### Mode 1: Build from Scratch
### Mode 2: Optimize Existing
### Mode 3: [Situation-Specific]
```

每种模式自包含，不假设用户读过其他模式。

### 15. 上下文优先法（Context-First）
每次执行先检查领域上下文是否存在，如果存在则直接使用，只问缺失的信息：

```markdown
## Before Starting
**Check for context first:** If `marketing-context.md` exists, read it before asking questions.
Use that context and only ask for information not already covered.
```

---

## 四、质量保障技法

### 16. Eval 评测闭环法
写测试用例 → 跑 with-skill 和 without-skill 对比 → 量化打分 → 迭代改进。

**关键指标**：
- 通过率（pass_rate）
- 执行耗时（time_seconds）
- Token 消耗
- with-skill vs without-skill 的增量（delta）

**你的 W3 已经有完整的这套体系**（run_eval.py、grading.json、benchmark.json）。

### 17. 盲比法（Blind Comparison）
两个版本的输出给独立 agent 做 A/B 盲比，不告诉它版本号，避免主观偏见。

### 18. 重复工作打包法（Bundle Repeated Work）
读测试日志，如果多个测试用例都独立写了同样的辅助脚本，打包到 `scripts/`：

> 核心信号：如果 3 个测试用例的子代理都写了 `create_docx.py`，说明 skill 应该内置这个脚本。

---

## 五、高级技巧

### 19. 前置触发法（Proactive Triggers）
Skill 在上下文中检测到特定模式时，主动标记问题，不等用户问：

```markdown
## Proactive Triggers
Surface these without being asked:
- **[Condition]** → [What to flag and why]
- **[Condition]** → [What to flag and why]
```

示例：
- SEO：检测到关键词重叠 → 标记关键词冲突
- 定价：转化率 > 40% → 标记可能定价过低
- CRO：表单字段 > 7 个且非多步骤 → 标记

### 20. 输出制品表法（Output Artifacts）
把常见请求映射到具体可交付物：

```markdown
## Output Artifacts
| 当你要求... | 你会得到... |
|------------|------------|
| "帮我定价" | 定价建议（层级结构 + 价值指标 + 竞争定位）|
| "审计 SEO" | SEO 评分卡（0-100）+ 优先级修复列表 |
```

### 21. 信心标记法（Confidence Tagging）
每个发现都带上信心级别：
- 🟢 已验证 / 🟡 中等 / 🔴 假设
- "不知道" 好过 假自信
- 高风险建议额外审查

### 22. 精简上下文法（Keep It Lean）
SKILL.md 控制在 10KB 以内。定期检查：每一行是否物有所值？删掉不干活的内容。

### 23. Related Skills 导航法
每个 skill 末尾放关联技能列表，带**什么时候用**和**什么时候不用**的消歧义：

```markdown
## Related Skills
- **copywriting**: 用于落地页和网站文案。**不用于**邮件序列或广告文案。
- **page-cro**: 用于优化营销页面。**不用于**注册流程。
```

---

## 技法选择决策树

```
你的 skill 遇见了什么问题？
│
├─ AI 不知道什么时候该触发 → 描述触发法 + 前置触发法
├─ 内容太长装不下 → 三级加载解耦法 + 文件分流法
├─ AI 不按流程走 → 步骤检查点法
├─ 约束不明确 → 反转面试法
├─ 跨多个子领域 → Hub-Spoke 路由法
├─ 需要实时数据 → 动态上下文注入法
├─ 输出不稳定 → 透明输出格式法 + 示例驱动法
├─ 效果不好不知道怎么改 → Eval 评测闭环法 + 盲比法
├─ AI 不理解为什么这么要求 → 解释原因法
├─ 测试通过但实际用不好 → 避免过拟合法
├─ 触发不准 → Undertrigger 对抗法
├─ 语气像教科书 → Practitioner Voice 法
└─ 重复工作太多 → 重复工作打包法
```

---

## 参考来源

- Anthropic 官方 skill-creator SKILL.md
- Claude Code 官方文档（code.claude.com/docs）
- Alireza Rezvani SKILL-AUTHORING-STANDARD.md（alirezarezvani/claude-skills）
- Antigravity Awesome Skills（sickn33/antigravity-awesome-skills）
- VoltAgent Awesome Agent Skills（voltagent/awesome-agent-skills）
