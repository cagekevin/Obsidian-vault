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
