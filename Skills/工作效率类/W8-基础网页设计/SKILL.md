---
name: 基础网页设计
description: 基础网页设计路由枢纽。根据用户需求分流到 claud（自带规范快速出图）、标准规范需下载样式（专业标准路线需搭配 Refero）或界面淬炼（专业设计精修工作流，22个子命令）。Use when user wants to design web pages, build UI, create prototypes, or needs visual design guidance.
metadata:
  pattern: tool-wrapper
---

# 基础网页设计路由

<what-to-do>
用户表达设计需求后，先问清楚风格偏好，然后根据路由分发。

## 路由选择说明

| 路由 | 风格 | 适合谁 | 需要做什么 |
|------|------|--------|-----------|
| **claud** | 自带设计规范，快速出图 | 想直接开工，不想折腾配置 | 直接告诉需求即可 |
| **标准规范需下载样式** | 参考真实品牌风格，专业标准路线 | 追求行业级精度，想参考 Apple/Stripe 等真实品牌规范 | 需先安装 Refero MCP 或去网站下载 DESIGN.md |
| **界面淬炼** | 专业设计精修工作流 | 需要设计评审、精修、动画增强、UX 优化的设计师 | 内置 22 个子命令，直接调用即可 |
| **lucide-icons** | 图标库 | 页面需要图标时 | 直接引用图标名即可 |

如果用户输入模糊，主动解释三者区别，让用户选。

# <route-table>
| 路由 | 文件 | 触发关键词 |
|---|---|---|
| claud | claud_design/claud_design.md | 网页, UI, 页面, 界面, 视觉, 前端, 设计页面, landing page, 网站 |
| 标准规范需下载样式 | 标准规范需下载样式/前端设计规范.md | 前端设计规范, design system, 设计系统, 组件规范, component, 样式参考 |
| 界面淬炼 | 界面淬炼/界面淬炼.md | 设计评审, 设计精修, 设计审计, UX评审, 界面抛光, animate, craft, shape, critique, audit, polish, bolder, 设计增强, 设计迭代, 动效设计, 设计淬炼 |
| lucide-icons | lucide-icons/SKILL.md | 图标, icon, 图标库, lucide |
| 网页部署 | 网页部署/SKILL.md | 部署, deploy, 发布, 分享链接, 公网链接, 在线预览html, 临时页面 |
| Netlify 项目部署 | Netlify项目部署/SKILL.md | netlify, 项目部署, 生产发布, 预览部署, 自定义域名, CI/CD |

匹配后载入对应文件执行。
</what-to-do>

<supporting-info>
`标准规范需下载样式/references/` 和 `claud_design/references/` 包含样式参考及设计规范。
</supporting-info>
