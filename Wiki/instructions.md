---
type: meta
title: "Wiki Instructions"
updated: 2026-06-23
tags:
  - meta
  - instructions
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[hot]]"
---

# Wiki Instructions

## 这是什么

**AI 构建的知识图谱。** 从原始资料中提取的原子化概念页面，互相链接形成网络。

Wiki 里放的是**通用方法论、概念、原则、框架**——结构化、可链接、跨项目复用的知识。不是个人偏好，不是具体项目经验，不是操作步骤。

## 什么不放 Wiki（放哪里）

- **身份、目标、风格、做事方式** → 放 `Context/`（个人化、关于"Kevin 是谁"）
- **具体工作流、操作方法、执行步骤** → 放 `Skills/`（可执行、有输入输出、有流程）
- **最核心、最稳定的原则和习惯** → 放 `.codebuddy/memory/MEMORY.md`（少而精，每天都要用）
- **犯过的错、踩过的坑、修复方式** → 放 `.codebuddy/memory/YYYY-MM-DD.md`（按天记、有时间属性）
- **项目相关的文档、资产、经验** → 放 `Projects/`（项目结束就归档）
- **每天的工作记录、想法** → 放 `Daily Notes/`（流水账，给人看的）

---

## Structure

```
Wiki/
├── skills/       ← skill 指令文件（ingest/lint/query/save）
├── concepts/     ← 概念页
├── entities/     ← 实体页
├── sources/      ← 来源页
├── questions/    ← 问答存档
├── meta/         ← 元数据
├── index.md      ← 主索引
├── hot.md        ← 热上下文
└── log.md        ← 操作日志
```

## Frontmatter 模板

### 概念页

```yaml
---
type: concept
title: "Concept Name"
complexity: intermediate
domain: knowledge-management
aliases:
  - "Alternative Name"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - concept
  - <domain>
status: developing
related:
  - "[[Related Page]]"
sources:
---
```

### 实体页

```yaml
---
type: entity
title: "Entity Name"
entity_type: person
role: "Brief role description"
first_mentioned: "[[First Source]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - entity
  - <type>
status: mature
related:
  - "[[Related Page]]"
sources:
---
```

### 来源页

```yaml
---
type: source
title: "Source Title"
source_url: "https://..."
fetched: YYYY-MM-DD
tags:
  - source
  - <type>
status: ingested
related:
  - "[[concepts/Extracted Concept]]"
---
```

### 问答存档

```yaml
---
type: question
title: "Question Title"
question: "The original question as asked."
answer_quality: solid
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - question
  - <domain>
related:
  - "[[Referenced Page]]"
sources:
  - "[[sources/Source Page]]"
---
```

## 命名规则

- 文件名：英文 Title Case 带空格（`Machine Learning.md`）
- 子文件夹：英文小写（`concepts/`）
- Wikilink：和文件名完全一致（`[[Machine Learning]]`）
- 文件名全 vault 唯一

## 页面内容规范

- 使用 `---` 分隔线分段
- 每个概念页应有 `## Connections` 段落
- 用 `[[Wikilink]]` 建立交叉引用
- 不写空段落

## 内容写入规范

向 wiki 写入内容时，必须遵守以下规则：

1. **保留原文不编辑** — 用户提供的原始内容，示例、对比、判断依据必须一字不差写入。可以删减示例数量，但不能修改保留的示例原文
2. **改完即检查** — 每次修改后立即重读改动区域，确认没有误删或篡改
3. **操作记录完整** — 新建或更新概念页后，必须同步更新 hot.md、log.md、index.md，并重建搜索索引（contextual-prefix + bm25-index）
