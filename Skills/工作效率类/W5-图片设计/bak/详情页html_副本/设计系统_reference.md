# 详情页设计系统 — 组件手册

> 操作流程见 `SKILL.md`，这里只查 class 定义、CSS、规格参数。

---

## 一、文字 Class 速查表

### 1.1 完整列表

| Class | 角色 | 字体 | 字号 | 字重 | 颜色 | 字距 | 特殊 |
|-------|------|------|------|------|------|------|------|
| `.h1` | 大标题(≤8字) | serif | 44px | 400 | main | +.05em | line-height:1.3 |
| `.h1-sm` | 大标题(9-14字) | serif | 36px | 400 | main | +.03em | line-height:1.3 |
| `.h-md` | 中标题(≤10字) | serif | 40px | 400 | main | +.02em | line-height:1.3 |
| `.h2` | 模块标题(15-23字) | serif | 32px | 400 | main | +.05em | line-height:1.4 |
| `.claim` | 品牌大主张(≤8字) | serif | 40px | 400 | accent | +.05em | - |
| `.num` | 大数字(≤4字) | serif | 28px | 400 | accent | +.03em | - |
| `.pullquote` | 拉取引用 | serif | 32px | 400 it | accent | normal | line-height:1.5 |
| `.quote` | 短引文 | serif | 24px | 400 | accent | +.05em | - |
| `.h-sub` | 英文副标题 | display | 20px | 400 it | muted | normal | - |
| `.sub` | 强调标签 | sans | 16px | 500 | accent | +.10em | margin-top:16px |
| `.sub-muted` | 淡化标签 | sans | 16px | 400 | muted | +.10em | - |
| `.lead` | 主导语 | sans | 16px | 700 | main | normal | margin-bottom:8px |
| `.body` | 段落正文 | sans | 14px | 400 | muted | normal | line-height:1.8 |
| `.kicker` | 分类标签 | mono | 13px | 500 | muted | +.22em | uppercase,margin-bottom:12px |
| `.meta` | 元数据 | sans | 12px | 400 | meta | normal | margin-top:24px,text-align:center |
| `.spec` | 规格参数 | mono | 16px | 400 | main | +.02em | - |
| `.en-deco` | 英文装饰 | display | 24px | 400 it | accent | normal | - |
| `.gold` | accent色覆写 | 继承 | 继承 | 继承 | accent | 继承 | 加在任何 class 上改色 |

> **字体角色**：serif（Noto Serif SC）只用于展示性文字。sans（Noto Sans SC）只用于功能性文字。mono（IBM Plex Mono）仅用于 kicker/spec。display（Playfair Display）仅用于 h-sub/en-deco。
>
> **选 class 规则**：如果长度或大小恰好落在两个 class 之间，选接近的那个，不要 inline 覆写字号。例如 28px 品牌色数字用 `.num`，36px 标题用 `.h1-sm`。
>
> **硬规则"越大越轻"**：展示性标题（h1/h-md/h2/claim）字重 400，宽字距（+.02~+.05em）。小字（kicker/spec）是唯一可以用 mono + 宽字距（+.22em）的地方。正文和标签（body/lead/sub）用 sans，正常字距。

### 1.2 修饰符

- `.gold` → 把文字颜色改为 `--accent`（品牌金）
- `.text-center` → 居中对齐
- `.text-left` → 左对齐

### 1.3 中文标题长度（先算字数再选 class）

| 标题形态 | class | 字号 | 最多字/行 | 最多行 |
|---------|-------|------|----------|-------|
| 1行 ≤8 字 | `.h1` | 44px | 8 | 1 |
| 1行 9-14 字 | `.h1-sm` | 36px | 14 | 1 |
| 2行 每行 ≤8 字 | `.h1`（font-size:32px） | 32px | 8 | 2 |
| 中标题 ≤10 字 | `.h-md` | 40px | 10 | 1 |
| 模块标题 15-23 字 | `.h2` | 32px | 23 | 1 |
| 品牌主张 ≤8 字 | `.claim` | 40px | 8 | 1 |
| 大数字 ≤4 字 | `.num` | 28px | 4 | 1 |

### 1.4 可用宽度限制（940px 模块，内容体 ≈844px）

| 场景 | 可用宽度 | 最多字/行 | 超限后果 |
|------|---------|----------|---------|
| h1 全宽 | 844px | ≤17 字 | 变 3 行挤占正文区 |
| h1 两列内 | ~382px | ≤7 字 | 图片被压下 |
| h2 全宽 | 844px | ≤23 字 | 超长换行 |
| body 正文 | 844px | ∞ | 自动换行 |

### 1.5 最小可读字号（移动端）

| 角色 | 当前字号 | 安全下限 |
|------|---------|---------|
| body | 14px | ≥13px |
| meta | 12px | ≥11px |
| sub/lead | 16px | ≥14px |

---

## 二、排版模板规格

> **一屏可组合多个排版模板**：用 `.rule` 在 `.mod-body` 内分割上下区域，每个区域各自套用一种模板。总高度不超过 940px（`.mod`）或自然撑满（`.mod-auto`）。例如：上半屏对比（2 列）+ 下半屏平行列表（3 项 grid-3）。

### 2.1 对比（A vs B）

- 布局：2 列等宽 `gap:40px`，中间 `border-right` 分隔
- 对照方：`<p class="lead" style="color:var(--text-muted);">`（唯一允许的 inline style）
- 优势方：`<p class="lead gold">`
- 正文说明：`<p class="body">`
- 图片：每列上方，`.frame-img.r-4x3`，占 ~55% 内容体高度
- 截图/参数表：加 `.fit-contain`

```
┌─ muted ─┐  │  ┌─ accent ┐
│  BEFORE │  │  │  AFTER   │
│ [图]    │  │  │ [图]     │
└─────────┘  │  └──────────┘
```

> **对比方改色（唯一允许的 inline style）**：
> ```html
> <!-- 对照方 -->
> <p class="lead" style="color:var(--text-muted);">BEFORE 分叉毛躁</p>
> <!-- 产品方 -->
> <p class="lead gold">AFTER 顺滑清爽</p>
> ```

### 2.2 平行列表（N 个平等项）

**项数决定排版**：

| 数量 | 排版方案 |
|------|---------|
| 2 项 | 左右两列等宽 |
| 3 项 | grid-3（图标）或 3 行左文右图（实物图） |
| 4 项 | 2 × 2 网格 |

**布局和配图**：

| 项数 | 布局 | 配图 |
|------|------|------|
| 2 项 | 左右 2 列等宽，gap:40px | `.frame-img.r-4x3` |
| 3 项（图标） | grid-3（三列等宽，图标在文字上方） | `.frame-img.r-1x1` |
| 3 项（实物图） | 3 行左文右图（Z 字型） | `.frame-img.r-4x3` |
| 4 项 | 2×2 网格，gap:40px | `.frame-img.r-1x1` |

- 功能标签：`<p class="lead">`，核心项加 `.gold`
- 说明文字：`<p class="body">`
- 类别名（3 项方案用）：`<p class="sub">`
- 情感语义：accent 色图标（icon-circle）只用于正面表达；负面用 muted 色或省略图标

### 2.3 标签+说明（一对多）

- 布局：左文 40% + 右图 60%，间距 40px
- 纵向堆叠，每对间距 `gap-1-5`（16px）
- 标签：`<p class="lead">`
- 说明：`<p class="body">`
- 图片：`.frame-img.r-3x4` 撑满高度，参数表用 `.fit-contain`

```
┌─ 40% ─┐  ┌─ 60% ─┐
│ 标签1  │  │        │
│ 说明1  │  │ [ 图 ] │
│ 标签2  │  │        │
│ 说明2  │  └────────┘
└────────┘
```

### 2.4 大主张

- 居中独占一行
- 大数字/强主张：`<p class="claim">`（40px serif gold）
- 短语：`<p class="quote">`（24px serif gold）
- 不可加副标题

### 2.5 标签集合

- 容器：`<div class="tag-wrap">`（line-height:2.4）
- 每个标签：`<span class="tag-item">`
- 位置：`.mod-top-c` 标题下方，或 `.mod-body` 内

### 2.6 特殊卡片

- `<div class="callout-box">`
- 白底 + 边框 + 居中
- 内部仅 `<p class="body">`
- 一屏最多 3 个

### 2.7 正文陈述

- 正常流式排列
- 正文：`<p class="body">`
- 可选配底部大图（`.mod-img`）

---

## 三、Token（CSS 变量）

| Token | 值 | 用途 | 禁止用在哪 |
|-------|-----|------|-----------|
| `--text-main` | #2B2826 | 标题(h1/h2)、主导语(lead)、规格(spec) | 正文(body) |
| `--text-muted` | #827A73 | 正文(body)、淡化标签(sub-muted) | 不要改成 main |
| `--text-meta` | #A6A09A | 脚注(meta) | 仅用于 meta |
| `--accent` | #B89670 | 品牌主张(claim)、优势方(gold)、装饰线(deco-line)、图标(icon-circle)、大数字(num) | 正文、标签底色、脚注 |
| `--bg` | #FAF8F5 | 页面底色 | 内容区域不用 body-bg 替代 |
| `--body-bg` | #E0E0E0 | 浏览器 chrome | 内容区域内 |
| `--card-bg` | #FFFFFF | callout-box 白底 | 纯文字模块 |
| `--line` | #E8E2DB | 边框、分割线、tag-item 边框 | 不用其他颜色做边框 |
| `--ph-bg` | #EFECE8 | 占位图背景 | 交付前替换 |
| `--ph-text` | #C4BCB4 | 占位图文字 | 交付前替换 |

---

## 四、模块容器

| class | 说明 |
|-------|------|
| `.mod` | height:940px; border-top:1px solid var(--line) |
| `.mod-auto` | height:auto; min-height:940px |
| `.mod-top-c` | padding:80px 48px 0; text-align:center（标题区） |
| `.mod-body` | flex:1; padding:24px 48px 48px（内容体） |
| `.mod-img` | margin:0 48px 48px; min-height:200px（底部图片） |

- 首屏模块无 border-top：给第一个 `.mod` 加 `style="border-top:none;"` 或 task-scoped CSS `.page-hero{border-top:none}`
- 内容物足够撑满 940px 用 `.mod`，不适合填满用 `.mod-auto`
- 退路：内置 class 不够时在 `<head>` 写 `page-xxx` 前缀的 task-scoped CSS，禁止 inline style

### 基础结构

```
┌─────────────────────────────────┐  ← border-top: 1px（首屏无）
│  标题（居中，h2）              │  ← 上方留白 80px
│  副标题/装饰线（可选）           │
├─────────────────────────────────┤
│  内容体                          │  ← 文案类型决定排版
│  （文字/网格/对比列/图片...）     │
│                                  │
│  图片（可选）                    │  ← 左右/bottom 各留 48px
└─────────────────────────────────┘
```

- 标题区 padding：80px 48px 0（文字不贴顶）
- 内容体 padding：24px 48px 48px
- 图片边距：0 48px 48px
- 标题区最后一个元素如果是装饰线，其下 margin 与 `.mod-body` 的 padding-top 合并，不需要额外调整

### 间距规格

| 场景 | 留白 |
|------|------|
| 模块之间 | 1px 细线 `var(--line)` |
| 标题上下 | 80px |
| 内容体左右 | 48px |
| 图片边缘 | 48px（左右 bottom） |
| 两列之间 | 40px |
| 三列之间 | 32px |

---

## 五、布局辅助

| class | 作用 |
|-------|------|
| `.stack` | display:flex; flex-direction:column |
| `.gap-1`(12px) / `.gap-1-5`(16px) / `.gap-2`(24px) / `.gap-3`(36px) / `.gap-4`(48px) / `.gap-5`(64px) | 纵向间距 |
| `.grid-3` | display:flex; gap:32px（三列） |
| `.grid-3-item` | flex:1; text-align:center |
| `.grid-2x2` | display:flex; flex-wrap:wrap; gap:40px |
| `.grid-2x2-item` | flex:1 1 calc(50% - 20px); text-align:center |

---

## 六、图片

| class | 说明 |
|-------|------|
| `.frame-img` | 真实图片容器，width:100%; overflow:hidden |
| `.frame-img > img` | object-fit:cover（裁切填满） |
| `.frame-img.fit-contain > img` | object-fit:contain（截图/参数表完整显示） |
| `.r-16x9` | 16:9，底部大图 |
| `.r-4x3` | 4:3，对比/平行图 |
| `.r-1x1` | 1:1，方形网格 |
| `.r-3x4` | 3:4，标签+说明右侧纵向图 |
| `.img-fluid` | 占位图（宽100%, flex居中, 占位色背景） |
| `.img-box` | 占位图（同 img-fluid，但 font-size:12px） |

### 占位图 → 真实图替换

```html
<!-- 替换前（占位阶段） -->
<figure class="frame-img r-4x3">
  <div class="img-fluid page-ph-full">产品透视图 · 内部结构件 · 对比传统设计</div>
</figure>

<!-- 真实产品图：cover 裁切填满 -->
<figure class="frame-img r-4x3">
  <img src="assets/product-xray.jpg" alt="产品内部透视结构图">
</figure>

<!-- 截图/参数表：fit-contain 完整显示 -->
<figure class="frame-img fit-contain r-4x3">
  <img src="assets/spec-chart.jpg" alt="性能对比图表">
</figure>

<!-- N 格网格中的单个特写 -->
<figure class="frame-img r-1x1">
  <img src="assets/detail-texture.jpg" alt="外壳磨砂纹理微距特写">
</figure>
```

---

## 七、装饰组件

| 组件 | class | 用途 | 位置 | 限制 |
|------|-------|------|------|------|
| 通用分割线 | `.rule` | 模块内容体内部切割两块信息 | `.mod-body` 内 | 不用于模块间分割 |
| 强调装饰线 | `.deco-line` | 标题区→内容体视觉过渡 | `.mod-top-c` 末尾 | 仅金色（--accent） |
| 胶囊标签 | `.tag-item` | 短关键词流式排列 | `.tag-wrap` 内 | 不放 callout-box 内部 |
| 白底卡片 | `.callout-box` | 强调信息框 | `.mod-body` 内 | ≤3 个/屏，内部仅 body |
| 圆形图标 | `.icon-circle` | 正面功能符号 | grid-item 内 | ≤4 个/屏，负面加 `.is-negative` |
| 参数行 | `.ledger` | 规格列表 | `.mod-body` 内 | 2-8 行 |
| 参数标签 | `.ledger-label` | 左侧参数名 | `.ledger-row` 内 | sans/14px/muted |
| 参数值 | `.ledger-value` | 右侧参数值 | `.ledger-row` 内 | mono/16px/main |

### 选择规则

```
需要分隔两块内容 → .rule（无品牌感）
标题下做仪式感停顿 → .deco-line（金色）
不确定 → .rule
```

### 禁止规则

- 不使用多色渐变（只用 --accent / --line / --text-muted）
- 不加整页网格、点阵、方格纸背景
- 不加装饰性斑点、圆圈、飘浮元素（每个装饰必须有功能目的）
- 不在文字下方加底色块
- 任何装饰不遮挡内容

---

## 八、HTML 模板

**必须使用 `template.html` 作为起点。** 所有 CSS 和字体加载已内置，只需编辑 `<body>` 内的模块代码：

```html
<!-- <head> 中已包含字体加载 + 全部 CSS，只需编辑 <body> 内的模块 -->
```

如需查看或修改 CSS 定义，同目录下 `template.html` 中的 `<style>` 块：

```css
:root{--text-main:#2B2826;--text-muted:#827A73;--text-meta:#A6A09A;--accent:#B89670;--bg:#FAF8F5;--body-bg:#E0E0E0;--card-bg:#FFFFFF;--line:#E8E2DB;--ph-bg:#EFECE8;--ph-text:#C4BCB4;--font-serif:"Noto Serif SC","Songti SC","STSong",serif;--font-sans:"Noto Sans SC",-apple-system,"PingFang SC","Microsoft YaHei UI",sans-serif;--font-display:"Playfair Display","Noto Serif SC",serif;--font-mono:"IBM Plex Mono",Consolas,"Courier New",monospace;}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
body{font-family:var(--font-sans);background:var(--body-bg);color:var(--text-main);-webkit-font-smoothing:antialiased;}
.page{width:790px;margin:0 auto;background:var(--bg);overflow:hidden;}
.h1{font-family:var(--font-serif);font-size:44px;font-weight:400;line-height:1.3;color:var(--text-main);text-align:center;letter-spacing:0.05em;}
.h1-sm{font-family:var(--font-serif);font-size:36px;font-weight:400;line-height:1.3;color:var(--text-main);text-align:center;letter-spacing:0.03em;}
.h-md{font-family:var(--font-serif);font-size:40px;font-weight:400;line-height:1.3;color:var(--text-main);text-align:center;letter-spacing:0.02em;}
.h2{font-family:var(--font-serif);font-size:32px;font-weight:400;line-height:1.4;color:var(--text-main);text-align:center;letter-spacing:0.05em;}
.claim{font-family:var(--font-serif);font-size:40px;font-weight:400;color:var(--accent);text-align:center;letter-spacing:0.05em;}
.num{font-family:var(--font-serif);font-size:28px;font-weight:400;color:var(--accent);text-align:center;letter-spacing:0.03em;}
.pullquote{font-family:var(--font-serif);font-size:32px;font-weight:400;font-style:italic;color:var(--accent);text-align:center;line-height:1.5;}
.quote{font-family:var(--font-serif);font-size:24px;font-weight:400;color:var(--accent);text-align:center;letter-spacing:0.05em;}
.sub{font-family:var(--font-sans);font-size:16px;font-weight:500;color:var(--accent);text-align:center;letter-spacing:0.1em;margin-top:16px;}
.sub-muted{font-family:var(--font-sans);font-size:16px;font-weight:400;color:var(--text-muted);text-align:center;letter-spacing:0.1em;}
.lead{font-family:var(--font-sans);font-size:16px;font-weight:700;color:var(--text-main);margin-bottom:8px;}
.body{font-family:var(--font-sans);font-size:14px;font-weight:400;line-height:1.8;color:var(--text-muted);}
.meta{font-family:var(--font-sans);font-size:12px;color:var(--text-meta);text-align:center;margin-top:24px;}
.kicker{font-family:var(--font-mono);font-size:13px;font-weight:500;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.22em;margin-bottom:12px;}
.spec{font-family:var(--font-mono);font-size:16px;font-weight:400;color:var(--text-main);letter-spacing:0.02em;}
.h-sub{font-family:var(--font-display);font-style:italic;font-size:20px;font-weight:400;color:var(--text-muted);}
.en-deco{font-family:var(--font-display);font-style:italic;font-size:24px;font-weight:400;color:var(--accent);}
.gold{color:var(--accent);font-weight:inherit;}
.text-center{text-align:center;}
.text-left{text-align:left;}
.mod{height:940px;display:flex;flex-direction:column;border-top:1px solid var(--line);}
.mod-auto{height:auto;min-height:940px;display:flex;flex-direction:column;border-top:1px solid var(--line);}
.mod-top-c{padding:80px 48px 0;text-align:center;}
.mod-body{flex:1;padding:24px 48px 48px;display:flex;flex-direction:column;}
.mod-img{margin:0 48px 48px;min-height:200px;display:flex;align-items:center;justify-content:center;background:var(--ph-bg);color:var(--ph-text);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;}
.stack{display:flex;flex-direction:column;}
.gap-1{gap:12px;}.gap-1-5{gap:16px;}.gap-2{gap:24px;}.gap-3{gap:36px;}.gap-4{gap:48px;}.gap-5{gap:64px;}
.grid-3{display:flex;gap:32px;}
.grid-3-item{flex:1;text-align:center;}
.grid-2x2{display:flex;flex-wrap:wrap;gap:40px;}
.grid-2x2-item{flex:1 1 calc(50% - 20px);text-align:center;}
.img-box{display:flex;align-items:center;justify-content:center;background:var(--ph-bg);color:var(--ph-text);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;}
.frame-img{width:100%;display:block;overflow:hidden;}
.frame-img>img{width:100%;height:100%;object-fit:cover;display:block;}
.frame-img.fit-contain>img{object-fit:contain;}
.r-16x9{aspect-ratio:16/9;}.r-4x3{aspect-ratio:4/3;}.r-1x1{aspect-ratio:1/1;}.r-3x4{aspect-ratio:3/4;}
.img-fluid{width:100%;display:flex;align-items:center;justify-content:center;background:var(--ph-bg);color:var(--ph-text);font-size:13px;letter-spacing:0.15em;text-transform:uppercase;}
.rule{height:1px;background:var(--line);border:0;margin:24px 0;}
.deco-line{width:40px;height:1px;background:var(--accent);margin:24px auto;}
.tag-item{display:inline-block;padding:6px 16px;border:1px solid var(--line);border-radius:99px;font-size:13px;color:var(--text-muted);margin:4px;}
.tag-wrap{line-height:2.4;}
.callout-box{background:var(--card-bg);padding:20px;text-align:center;border:1px solid var(--line);}
.icon-circle{width:120px;height:120px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-size:28px;color:var(--accent);}
.icon-circle.is-negative{color:var(--text-muted);}
.ledger{display:flex;flex-direction:column;}
.ledger-row{display:grid;grid-template-columns:1fr auto;gap:24px;padding:14px 0;border-bottom:1px solid var(--line);align-items:baseline;}
.ledger-label{font-family:var(--font-sans);font-size:14px;font-weight:400;color:var(--text-muted);}
.ledger-value{font-family:var(--font-mono);font-size:16px;font-weight:400;color:var(--text-main);text-align:right;}
```

### Google Fonts 加载

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
```

---

## 九、反模式

### 反模式 A：内联样式代替 class

```html
<!-- ❌ 错误 -->
<p class="body" style="margin-top:16px;max-width:480px;color:var(--text-muted);">

<!-- ✅ 正确 -->
<div class="stack gap-1-5">
  <p class="body">正文描述</p>
</div>
```

### 反模式 B：找不到 class 就编 class

```html
<!-- ❌ 错误 -->
<div class="col" style="flex:2;gap:32px;">

<!-- ✅ 正确：用 .stack + gap，special 布局加 task-scoped CSS -->
<div class="stack gap-3" style="flex:2;">
```

### 反模式 C：h1 不按长度调整

```html
<!-- ❌ 错误：9 个字还用 44px -->
<h1 class="h1">充得快，只是一种本能</h1>

<!-- ✅ 正确：9-14 字用 .h1-sm -->
<h1 class="h1-sm">充得快，只是一种本能</h1>
```

### 反模式 D：装饰线位置混乱

```html
<!-- ❌ 错误 -->
<div class="mod-body">
  <p class="body">...</p>
  <div class="deco-line"></div>
</div>

<!-- ✅ 正确 -->
<div class="mod-top-c">
  <h2 class="h2">标题</h2>
  <div class="deco-line"></div>
</div>
```

---

## 十、换肤示例

改 `:root` 变量即可换色：

```css
:root {
  --bg: #F5F7FA;
  --text-main: #1A1A2E;
  --accent: #4A90D9;   /* 暖金→科技蓝 */
  --text-muted: #6B7280;
  --line: #D1D5DB;
}
