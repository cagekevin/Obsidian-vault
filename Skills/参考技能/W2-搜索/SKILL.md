---
name: 搜索
description: 搜索技能路由枢纽——统一实时搜索引擎。支持通用网页搜索、垂直搜索、批量搜索、页面内容提取。Use when user wants to search the web, crawl web pages, extract content, find information online.
metadata:
  pattern: pipeline+tool-wrapper
---

# 搜索 Hub

<route-table>

## 路由表

| 路由 | 文件 | 触发关键词 |
|------|------|-----------|
| AnySearch 统一搜索 | `anysearch/SKILL.md` | anysearch, 搜索, 搜一下, 查资料, 找信息, web search, search engine, google, bing, baidu |

</route-table>

<what-to-do>

## 使用方式

直接说需求，Hub 会根据触发词自动分流到对应的搜索技能。

### AnySearch

说"搜一下xxx"或"查资料xxx"等，会自动加载 anysearch 处理。

</what-to-do>
