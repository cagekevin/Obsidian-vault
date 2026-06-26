---
type: concept
title: "Open Knowledge Format"
complexity: intermediate
domain: knowledge-management
aliases:
  - "OKF"
created: 2026-06-26
updated: 2026-06-26
tags:
  - concept
  - knowledge-management
  - google
status: developing
related:
  - "[[LLM Wiki Pattern]]"
  - "[[Andrej Karpathy]]"
sources:
  - "[[sources/Google OKF 2026]]"
---

# Open Knowledge Format (OKF)

Google Cloud 推出的开源、中立的规范标准，将 [[LLM Wiki Pattern]] 从概念变成可执行的工程标准。

## 文件格式规范

- **扩展名**：`.md`
- **编码**：UTF-8
- **组成**：顶部 YAML 元数据（Frontmatter）+ 下方 Markdown 正文（Body）

## YAML 元数据规范

- **唯一必填字段**：`type`（字符串），告诉 AI 或解析器这个文件是什么知识实体（如 `type: table`、`type: api_endpoint`、`type: playbook`）
- **推荐可选字段**：`title`、`description`、`tags`（数组）、`owner`/`author`，以及任意业务自定义 KV 字段

## 正文与链接规范

- **正文**：标准 Markdown（CommonMark / GFM），人类和 AI 都能读
- **交叉引用**：使用 **标准相对路径 Markdown 链接**，格式为 `[显示文本](./其他文件.md)` 或 `[显示文本](../目录/文件.md)`，确保在 GitHub、本地 IDE、AI Agent 中引用关系都不会断裂

## 三大设计原则

### 1. 最少干预（Minimally Opinionated）
只强制 `type` 字段，不干涉内容模型。不同团队可以按自己的习惯组织正文，无需在分类学上达成一致。

### 2. 生产者与消费者解耦（Producer/Consumer Independence）
写入者和读取者彻底分离。人类手写的 Markdown 可被 AI 消费；数据管道导出的知识可被人类浏览；一个 LLM 总结的知识可被另一个 LLM 检索。

### 3. 是格式，不是平台（Format, not platform）
不绑定任何云服务、数据库、大模型厂商或智能体框架。无需专有 SDK、账号或运行环境，普通编辑器 + Git 即可管理。

## 与 LLM Wiki 的关系

此前 Obsidian、Notion、AGENTS.md 等方案各自为战，格式互不相通，产生知识孤岛。OKF 提供了一套标准化的"容器"和"目录"，让 AI 智能体可以顺畅读取、交叉比对、自动更新，最终将静态文档库变成真正"活着"的 LLM Wiki。

## 标准示例

```markdown
---
type: database_table
title: users_v2
description: 核心用户表，包含用户的基本信息和认证状态。
owner: data-engineering-team
tags:
  - core-data
  - pii
last_updated: "2026-06-26"
---

# users_v2 数据表说明

这是系统中用于存储所有注册用户基础数据的核心表。

## 字段说明 (Schema)

| 字段名 | 类型 | 描述 |
|---|---|---|
| `user_id` | UUID | 用户的全局唯一标识符（主键） |
| `email` | String | 用户注册邮箱 |
| `status` | String | 账户状态，参考 [Account Status Enum](./enums/account_status.md) |

## 依赖关系

该表的数据来源于上游的统一认证服务，具体的同步逻辑请参考 [User Auth Pipeline](../pipelines/user_auth_sync.md)。
```

## 设计哲学

OKF 的精髓是**极简**：不需要数据库，普通文本编辑器就能创建，Git 原生管理版本。通过强制 `type` 分类和 Markdown 文件链接，AI 智能体可以像网络爬虫一样在本地文件夹中遍历出完整的企业知识图谱。

## 与 Kevin 的 Wiki 对比

| 维度 | OKF 标准 | Kevin 的 Wiki |
|------|----------|--------------|
| 链接格式 | `[文本](./文件.md)` 相对路径 | `[[Wikilink]]` |
| 必填字段 | 仅 `type` | `type` + 更多字段 |
| frontmatter 丰富度 | 极简 | `complexity`, `status`, `aliases`, `related`, `sources` 等 |
| 目录分类 | 无强制 | concepts/ entities/ sources/ 分类 |
| 链接工具 | 纯文本编辑器 + Git | Obsidian（图谱、双向链接面板） |

Kevin 的 Wiki 是 OKF 的超集——OKF 是最小公分母标准，Kevin 的标准是面向 Obsidian + AI 协同的实践标准，更丰富但需要 Obsidian 生态支持。

## Connections

- [[LLM Wiki Pattern]] — OKF 是其具体标准化实现
- [[Andrej Karpathy]] — 提出了 LLM Wiki 设想
- [[sources/Google OKF 2026]] — 来源页
