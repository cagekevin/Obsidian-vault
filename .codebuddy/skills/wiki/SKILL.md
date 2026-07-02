---
name: wiki
description: |
  Obsidian wiki 知识库管理。支持摄入、检查、查询、保存四种操作。
  触发词：wiki、知识库、ingest、摄入、吸收、整理进wiki、吃下这份资料、摄取、
  分析这篇、整理这篇、lint、检查wiki、校验、query、查询wiki、搜索wiki、
  save、保存、归档、归档到wiki、record、记录到wiki。
  NOT for: 非 wiki 知识库的文档管理。
---

# Wiki 知识库管理

Obsidian wiki 知识库的四种操作。根据用户意图选择对应模式，详细流程见 `references/`。

## 路由表

| 意图 | 模式 | 详细流程 |
|------|------|----------|
| 把资料吸收进 wiki | 摄入（Ingest） | `references/ingest.md` |
| 检查 wiki 质量 | 检查（Lint） | `references/lint.md` |
| 查询 wiki 内容 | 查询（Query） | `references/query.md` |
| 记录到 wiki | 保存（Save） | `references/save.md` |

判断用户意图后，直接加载对应的 references 文件执行。
