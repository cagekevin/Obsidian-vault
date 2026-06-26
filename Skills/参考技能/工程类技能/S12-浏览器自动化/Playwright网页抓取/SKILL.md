---
name: Playwright 网页抓取 / Playwright Web Scraping
description: 浏览器自动化完整方法论——选择器优先级、自动等待、隐身反爬、错误恢复、并发限流。Use when user wants to automate browser, scrape web pages, fill forms, test UI, or needs Playwright/Puppeteer methodology guidance.
metadata:
  pattern: tool-wrapper+reviewer
  category: 开发
---

# 浏览器自动化方法论

<what-to-do>

## 一句话总结

```
选元素: getByRole > getByText > getByLabel > getByTestId > CSS
等元素: 永远不手动等，Playwright 自动等
防检测: 隐藏 webdriver + 模拟人类行为
容错:   try/catch + 截图 + 指数退避重试
隔离:   每个任务独立 browser context
限速:   并发控制 + 随机延迟
```

## 核心原则

1. **用面向用户的定位器**（getByRole, getByText），避免 CSS/XPath
2. **永远不加手动等待** — Playwright 自动等待
3. **每个任务完全隔离** — 独立 browser context
4. **截图和 Trace 是调试命脉**
5. **CI 无头模式**，调试有头模式
6. **反检测是猫鼠游戏**

## 什么时候用

- 用户说"帮我自动填表单/爬数据/点按钮/测页面"
- 需要 Playwright/Puppeteer 选选择器、等元素、反爬、容错的标准化流程
- 写自动化脚本前对照方法论，避免踩坑

## 参考文件

| 文件 | 说明 |
|------|------|
| `references/核心方法论-中文版.md` | ← **完整中文版**（推荐阅读） |
| `references/SKILL.md` | 原版英文完整文档（1116行） |

</what-to-do>
