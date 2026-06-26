---
type: source
title: "Google Open Knowledge Format (OKF)"
source_url: "https://cloud.google.com/blog/products/ai-machine-learning/google-open-knowledge-format-okf"
fetched: 2026-06-26
tags:
  - source
  - google
  - knowledge-management
status: ingested
related:
  - "[[LLM Wiki Pattern]]"
  - "[[Open Knowledge Format]]"
  - "[[Andrej Karpathy]]"
---

# Google Open Knowledge Format (OKF)

Google Cloud 推出的开源、中立的规范标准。将 Karpathy 的 "LLM Wiki" 设想变成可执行的工程标准。

## 核心结构

- **Markdown + YAML**：目录 + 概念文件，顶部 YAML frontmatter
- **文件规范**：UTF-8 编码，.md 扩展名
- **仅强制 `type` 字段**：其他字段（title, description, tags, timestamp）自选
- **网状链接**：使用标准相对路径 Markdown 链接 `[文本](./文件.md)`
- **推荐可选字段**：title, description, tags（数组）, owner/author，以及任意自定义 KV 字段

## 三大设计原则

1. **最少干预（Minimally Opinionated）**：只强制 type，不干涉内容模型
2. **生产者与消费者解耦（Producer/Consumer Independence）**：写入者和读取者彻底分离
3. **是格式，不是平台（Format, not platform）**：不绑定任何云服务/模型/框架

## 设计哲学

OKF 的精髓是极简——不需要数据库，普通编辑器 + Git 就能管理。通过强制 type 分类和 Markdown 文件链接，AI 智能体可以像网络爬虫一样遍历出完整的企业知识图谱。
