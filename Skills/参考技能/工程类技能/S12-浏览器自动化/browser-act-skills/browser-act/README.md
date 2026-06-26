# AI 浏览器 CLI（browser-act）

给 AI Agent 用的浏览器自动化工具。AI 直接敲命令就能操作浏览器，**不需要写代码**。

---

## 它能做什么

### 1. 浏览器操作（替代人手动操作网页）

```
打开网页 → 查看页面内容 → 点击按钮 → 输入文字 → 截图 → 填表单 → 登录
```

**一句话：凡是你在浏览器里能手动做的事，它都能做。**

### 2. 突破反爬屏障

- 三层防检测：环境指纹伪装 → 自动验证码识别 → 人工远程接管
- 一条命令提取受保护的页面内容

### 3. 三种浏览器模式

| 模式 | 用法 | 最佳场景 |
|------|------|---------|
| `chrome` | 复用你本地 Chrome 登录态 | 用你已登录的账号操作 |
| `stealth privacy` | 隐身+零残留 | 批量采集不想留痕迹 |
| `stealth fixed` | 固定指纹+固定 IP | 多个账号隔离，互不影响 |

### 4. 64 个现成的数据采集方案（开箱即用）

包含在 `solutions/` 目录下，直接安装就能用：

**电商（20个）：**
- 淘宝/天猫：商品搜索、详情、评论、店铺目录
- Amazon：ASIN查询、热销榜、Buy Box监控、竞品分析、评论
- 闲鱼：商品详情、搜索列表

**社交媒体（18个）：**
- 小红书：笔记详情、关键词搜索、用户主页
- 抖音/TikTok：话题标签、用户主页、视频详情、搜索
- 微信：公众号文章全文提取
- 知乎：文章详情
- 微博/X(Twitter)：推文搜索、DM自动化
- Reddit：帖子/评论提取、账号预热
- Instagram：帖子、评论、用户主页、地点标签
- Facebook：广告库、群组帖子、主页帖子

**视频平台（14个）：**
- YouTube：视频数据、字幕提取（批量）、评论、频道搜索、网红查找
- TikTok：视频爬取、用户主页、关键词搜索、话题标签

**线索生成（9个）：**
- LinkedIn：职位搜索+详情
- Google Maps：商家数据+评论
- 企业官网联系方式提取
- GitHub贡献者查找
- 跨平台社交媒体账号发现

**搜索研究（5个）：**
- Google SERP（含广告/PAA/AI概览）
- Google 新闻、图片搜索
- 任意网站转 Markdown
- 多来源网络研究自动化

### 5. Skill Forge（自定义网站采集）

如果这 64 个方案没有你想要的，**Skill Forge 可以自动探索任何网站**：

```
你告诉 AI："帮我抓取XXX网站的数据"
  ↓
AI 自动探索该网站的 API 和数据加载方式
  ↓
自动生成一个可复用的采集脚本（SKILL.md + Python）
  ↓
以后随时复用，不用再探索
```

---

## 快速上手

```bash
# 1. 首次使用——查看完整指南
browser-act get-skills core --skill-version 2.0.2

# 2. 一句话提取网页内容
browser-act stealth-extract https://example.com

# 3. 打开浏览器交互
browser-act --session task1 browser open <id> https://example.com
browser-act --session task1 state                 # 看页面有什么
browser-act --session task1 click 3               # 点第3个元素
browser-act --session task1 input 2 "搜索词"      # 输入文字
browser-act --session task1 screenshot            # 截图
```

---

## 安装

```bash
uv tool install browser-act-cli --python 3.12
```

---

## 来源

此仓库克隆自 [browser-act/skills](https://github.com/browser-act/skills)，MIT 协议开源。
