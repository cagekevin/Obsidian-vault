---
name: 浏览器自动化 / Browser Automation
description: 浏览器自动化路由枢纽。分流到 AI 浏览器 CLI（一次性操作）、Skill Forge（造复用脚本）、Playwright 方法论（开发测试）、CDP 网页抓取（登录态爬虫）和 browser-harness（坐标点击/云浏览器）。
---

# 浏览器自动化路由

<what-to-do>

## 分流规则

| 路由 | 文件 | 触发关键词 |
|------|------|-----------|
| **AI 浏览器 CLI（browser-act）** | browser-act-skills/browser-act/SKILL.md | 帮我打开XX, 帮我查一下, 帮我抓一下, 帮我看看, 帮我操作网页, 帮我截图, 帮我登录, 帮我看一下这个页面 |
| **Skill Forge（造复用脚本）** | browser-act-skills/browser-act-skill-forge/SKILL.md | 帮我造一个能重复用的工具, 帮我做一个脚本以后直接跑 |
| **Playwright 网页抓取** | Playwright网页抓取/SKILL.md | Playwright, Puppeteer, 浏览器自动化, 表单, UI测试, 无头浏览器 |
| **CDP 网页抓取** | CDP网页抓取/SKILL.md | CDP, 网页抓取, 抓取, 爬数据, 登录后, web access, 需要登录的网站 |
| **browser-harness** | browser-harness/SKILL.md | browser-harness, 坐标点击, 截图操作, 云浏览器, 远程浏览器, iframe穿透, shadow dom穿透, 无人值守 |

## 选择指引

- **AI 浏览器 CLI（browser-act）** — 给 AI Agent 用的浏览器自动化 CLI，突破反爬屏障、支持多浏览器并行、验证码自动处理、跨平台远程接管。一次性操作。
- **Skill Forge（造复用脚本）** — 自动探索网站 API 和数据加载方式，生成可复用的采集脚本（SKILL.md + Python）。长期使用。
- **Playwright 网页抓取** — 启动独立无头浏览器，适合开发测试、表单填写、UI 自动化
- **CDP 网页抓取** — 直连你日常 Chrome，天然带登录态，适合爬取需要登录的网站
- **browser-harness** — 坐标点击优先 + 截图驱动的 CDP 框架，穿透 iframe/Shadow DOM/cross-origin，支持 Browser Use 云浏览器（远程代理、验证码破解）

</what-to-do>
