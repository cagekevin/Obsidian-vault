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

### 1.6 组件强制使用规则（铁律）

以下规则**不得违反**，违反视为设计违规：

| 组件 | 强制场景 | 搭配规范 | 禁止用法 |
|------|---------|---------|---------|
| `.num` 大数字 | 数码/3C 类产品的功率、时长、温度、转化率、数量等所有核心数据**必须使用** | 默认追加 `.gold` 品牌色；与 `.lead` 搭配（标题在上，数字在下） | 核心数据使用 `.body` / `.lead` 展示 |
| `.quote` / `.pullquote` 引文 | 每屏提炼 1 条核心金句、结论、售后主张 | 金句在上，`.deco-line` 居下，形成仪式感 | 金句混入正文段落 |
| `.gold` 颜色修饰符 | 优势卖点、核心数据、品牌主张 | 加在 `.lead` / `.num` / `.claim` 等 class 后 | 纯负面痛点、正文描述禁止滥用 |
| `rule` 分割线 | 单模块内超过 2 组独立信息 | 置于 `.mod-body` 内，分隔不同信息组 | 替代标题区 `.deco-line` |
| `icon-circle` 圆形图标 | 正面功能/卖点（默认色），负面痛点（`.is-negative`） | 与 `.lead` 搭配，单模块 ≤ 8 个 | 纯装饰无语义的空白图标 |
| `.h-sub` / `.en-deco` 英文装饰 | 数码/轻奢产品标题区提升质感 | 放在 `.h1`/`.h1-sm` 上方 | 每个标题区 ≤ 1 组 |

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
- **铁则：禁止多段 `.body` 无层级连续堆砌。超过 2 段必须提取 `.lead` 作为小标题引导，或拆分重组为「标签+说明」模块**

### 2.8 分割线组件使用铁则

> 分割线组件是设计系统中最易滥用/遗漏的元素，以下规则**必须遵守**。

#### `deco-line`（金色装饰线）

| 规则 | 说明 |
|------|------|
| 位置 | 仅放置在 `.mod-top-c` 标题区内，标题与导语/标签之间 |
| 数量 | 单模块标题区**最多 1 条** |
| 禁止 | 放入 `.mod-body` 内容区、用于多段内容之间的分隔、多个标题叠加使用 |

#### `rule`（灰色通用分割线）

| 规则 | 说明 |
|------|------|
| 位置 | 仅放置在 `.mod-body` 内容区内，用于不同信息组之间的分隔 |
| 触发条件 | 单模块内超过 2 组独立信息，**必须**添加 `rule` 分割 |
| 禁止 | 放入标题区、替代模块间边框、替代 `deco-line` |

#### 选择速查

```
标题下需要仪式感停顿 → .deco-line（金色，品牌感）
内容区内需要分组    → .rule（灰色，功能性）
不确定              → .rule
```

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

### 新增：字号 Token（主题可覆盖）

| Token | 默认值 | 作用域 |
|-------|--------|-------|
| `--fs-h1` | 44px | `.h1` |
| `--fs-h1-sm` | 36px | `.h1-sm` |
| `--fs-h-md` | 40px | `.h-md` |
| `--fs-h2` | 32px | `.h2` |
| `--fs-claim` | 40px | `.claim` |
| `--fs-num` | 28px | `.num` |
| `--fs-body` | 14px | `.body` |
| `--fs-lead` | 16px | `.lead` |
| `--fs-sub` | 16px | `.sub` `.sub-muted` |
| `--fs-meta` | 12px | `.meta` |

### 新增：形态 Token（主题可覆盖）

| Token | 默认值 | 作用域 | 说明 |
|-------|--------|-------|------|
| `--weight-title` | 400 | `.h1` `.h2` `.claim` `.num` `.pullquote` `.quote` | 展示性字重，luxe 主题改为 300 |
| `--weight-lead` | 700 | `.lead` | 导语字重，luxe 主题改为 500 |
| `--weight-body` | 400 | `.body` `.meta` | 正文字重 |
| `--weight-sub` | 500 | `.sub` `.kicker` `.spec` | 标签字重 |
| `--en-transform` | `none` | `.en-deco` `.h-sub` | 英文转换，可选 `uppercase` |
| `--en-font-style` | `italic` | `.en-deco` `.h-sub` | 英文样式，可选 `normal` |
| `--radius-sm` | 0 | 小尺寸装饰 | 圆角，luxe 主题改为 6px |
| `--radius-md` | 0 | `.frame-img` `.mod-img` | 中圆角，luxe 主题改为 12px |
| `--radius-lg` | 0 | `.callout-box` | 大圆角，luxe 主题改为 16px |
| `--radius-full` | 99px | `.tag-item` | 胶囊圆角 |
| `--shadow-soft` | none | `.frame-img` `.icon-circle` | 微阴影 |
| `--shadow-card` | none | `.callout-box` | 卡片阴影 |
| `--shadow-elevated` | none | 预留 | 高位阴影 |

> **主题文件位于 `tokens/` 目录**：`luxe-warm.css`（高奢温润）。
> 改 `<link href="">` 为 `<link href="tokens/luxe-warm.css">` 即可切换风格。

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
| 圆形图标 | `.icon-circle` | 正面功能符号/极简象形 | grid-item 内 | ≤4 个/屏，负面加 `.is-negative`。内部仅允许填入 1-2 个汉字或极简图标，禁止留空或填入长文案 |
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

### 反模式 E：核心数据遗漏 .num

```html
<!-- ❌ 错误：核心数据用 .body / .lead 展示 -->
<p class="body">转化率高达93%</p>

<!-- ✅ 正确：数码品类核心数据强制使用 .num + .gold -->
<p class="num gold">93%</p>
```

### 反模式 F：分割线位置错误 / 缺失

```html
<!-- ❌ 错误 1：deco-line 放入内容区 -->
<div class="mod-body">
  <p class="body">正文</p>
  <div class="deco-line"></div>  <!-- 错误 -->
</div>

<!-- ❌ 错误 2：多组内容不添加 rule 分割 -->
<div class="mod-body">
  <p class="body">第一组信息</p>
  <p class="body">第二组信息</p>
  <!-- 缺少 rule -->
</div>

<!-- ✅ 正确 -->
<div class="mod-top-c">
  <h2 class="h2">标题</h2>
  <div class="deco-line"></div>  <!-- 正确：deco-line 在标题区 -->
</div>
<div class="mod-body">
  <p class="body">第一组信息</p>
  <div class="rule"></div>  <!-- 正确：多组内容用 rule 分割 -->
  <p class="body">第二组信息</p>
</div>
```

### 反模式 G：纯文字密集网格

```html
<!-- ❌ 错误：大量纯文字放入 grid 网格，无图标、无分组 -->
<div class="grid-2x2">
  <div class="grid-2x2-item"><p class="body">过压保护</p></div>
  <div class="grid-2x2-item"><p class="body">过流保护</p></div>
  <div class="grid-2x2-item"><p class="body">短路保护</p></div>
  <!-- ... 12 项纯文字堆砌 -->
</div>

<!-- ✅ 正确：文字搭配 icon-circle，多内容用 rule 分组 -->
<div class="mod-body stack gap-4">
  <div class="grid-2x2">
    <div class="grid-2x2-item">
      <div class="icon-circle"></div>
      <p class="body">过压保护</p>
    </div>
    <div class="grid-2x2-item">
      <div class="icon-circle"></div>
      <p class="body">过流保护</p>
    </div>
  </div>
</div>
```

### 反模式 H：连续多屏均分网格

```html
<!-- ❌ 错误：连续 3 屏及以上使用全均分网格，版式无节奏 -->
屏 3：grid-3 均分 → 屏 4：grid-3 均分 → 屏 5：grid-2x2 均分 → 视觉疲劳

<!-- ✅ 正确：穿插主次分栏、单图大图、对比布局调节节奏 -->
屏 3：grid-3 均分 → 屏 4：双列主次对比 → 屏 5：单图+列表 → 有起伏
```

---

## 十、品类专属设计规范

不同品类的详情页有差异化设计侧重点，以下规则**辅助 AI 和设计师针对品类做组件选择**。

### 风格视觉特征

默认「冷峻硬核」风格（删除 `<link>` 行）的视觉特征描述，供 AI 直观参考：

| 维度 | 特征 |
|------|------|
| 色彩印象 | 深灰 · 黑 · 暖金 · 米白 · 克制 |
| 主色 | `--text-main:#2B2826`（深灰黑） |
| 背景 | `--bg:#FAF8F5`（米白）`--body-bg:#E0E0E0`（灰） |
| 强调色 | `--accent:#B89670`（暖金） |
| 辅助色 | `--text-muted:#827A73`（中度灰）`--line:#E8E2DB`（浅米灰） |
| 圆角 | 全部 0（直角、硬朗） |
| 阴影 | 无 |
| 字重倾向 | 展示标题 400（轻盈），功能导语 700（有力） |
| 气质关键词 | 克制 · 理性 · 极简 · 文字驱动 · 去装饰化 |

### 10.1 数码 / 3C 类（充电器、耳机、配件、数码设备）

| 维度 | 强制规则 |
|------|---------|
| 数字展示 | 所有功率、时长、温度、次数、转化率等数值 → **强制使用 `.num` + `.gold`** |
| 技术卖点 | 图标+文字组合，禁止纯文字网格；技术点用 `.lead` + `.body` 搭配 `.icon-circle` |
| 安全防护 | 核心防护项配图标，次要项纯文字，用 `rule` 分组 |
| 布局 | 核心技术屏优先主次分栏，陈列场景可用均分网格 |
| 配图 | 透视结构图、数据图表必须加 `.fit-contain` |

### 10.2 美妆 / 轻奢类（适配 luxe-warm 风格）

| 维度 | 强制规则 |
|------|---------|
| 数字展示 | 弱化大数字组件，优先用文字描述质感 |
| 质感表达 | 优先使用 `h-sub` 英文装饰、`.quote` 引文组件强化文案情绪 |
| 视觉效果 | 可切换 luxe-warm 主题获得圆角、阴影、暖色系 |
| 布局 | 强制使用 `page-flex-2` 配合 task-scoped CSS 实现左文 40%/右图 60% 分栏：<br>`.page-text-col { flex: 2; }` `.page-img-col { flex: 3; }`<br>图片优先 `.r-3x4` 纵向撑满。严禁在美妆屏使用无差别的 `grid-3` 均分网格 |

---

## 十一、组件组合范式

以下为标准高频组合写法，对应 `template.html` 中的预制区块，可直接复用。

### 11.1 标准标题组合

```
.mod-top-c
  ├── .kicker（可选分类标签，mono 字体，如 "TECHNOLOGY" / "安全防护"）
  ├── .h-sub（可选英文装饰）
  ├── .h1 / .h1-sm / .h2（按字数选）
  ├── .deco-line（装饰线，仅1条）
  ├── .lead / .body（导语）
  └── .tag-wrap > .tag-item × N（可选标签）
```

### 11.1.2 高奢序数标题组合

适用于轻奢/美妆品类标题区，通过 `.en-deco`（Playfair Display 意大利斜体）打造仪式感：

```
.mod-top-c
  ├── .en-deco（序数/章号，如 "01" / "CHAPTER I"）
  ├── .h2 / .h1-sm（主标题，Serif）
  └── .deco-line（金色装饰线，仅1条）
```

### 11.2 数据强调组合

```
.lead（卖点标题）
.num.gold（核心数值，强制使用）
.body（卖点描述）
```

### 11.3 对比组合（A vs B）

```
双列布局（stack gap-1-5 内放 2 个 grid-2x2-item）
├── 左侧：.lead muted（唯一合法内联样式）+ .frame-img
└── 右侧：.lead gold + .frame-img
```

### 11.4 卡片强调组合

```
.callout-box
  └── .body × 1（单条核心信息，禁止多条）
```

### 11.5 图文分栏组合

```
.stack.gap-1-5（左列 文字区）
  ├── .lead（标签）
  └── .body（说明）
.frame-img.r-3x4（右列 图片区）
```

> `.tag-wrap` 不仅限于 `.mod-top-c` 标题区，也可放在 `.mod-body` 内作为卖点/参数标签组。使用方式一致：`.tag-wrap` > `.tag-item` × N。

### 11.6 引用来源组合

用于专家背书、产品金句、用户证言——引用必须有出处才可信。

```
.pullquote（引文主体）
.meta（来源/作者，sans 12px 灰，加 "——" 前缀）
```

示例：
```html
<div class="mod-top-c">
  <p class="pullquote">一款真正能保护电池的充电器。</p>
  <p class="meta">—— 数码测评博主 @XXX</p>
</div>
```

### 11.7 参数解释组合

用于成分表中的参数展开——`.spec`（参数名，mono）在上，`.body`（含义解释，sans）在下。

```
.spec（参数名，mono 16px）
.body（含义解释，sans 14px）
```

示例：
```html
<div class="stack gap-1-5">
  <p class="spec">椰油酰甘氨酸钾</p>
  <p class="body">温和氨基酸表活，接近皮肤 pH 值，不破坏皮脂膜</p>
</div>
```

### 11.8 品牌主张组合

用于品牌宣言屏——`.en-deco` 在上做情绪铺垫，`.claim` 在下做核心主张。

```
.mod-top-c
  ├── .en-deco（英文装饰，如 "A NEW STANDARD" / "OUR PROMISE"）
  ├── .claim（品牌主张，≤8 字，Serif 40px accent）
  └── .deco-line（金色装饰线，仅1条）
```

### 11.9 数据图标组合

仪表盘式的数据展示——图标 + 类别名 + 核心数据，适合技术参数总览屏。

```
.icon-circle（功能图标）
.sub（类别名，sans 16px 品牌色）
.num.gold（核心数据，mono 28px 品牌金）
```

示例：
```html
<div class="grid-3-item">
  <div class="icon-circle"></div>
  <p class="sub">转换效率</p>
  <p class="num gold">93%</p>
</div>
```

### 11.10 跨屏节奏组合范式

连续屏幕必须避免排版疲劳，遵循"疏密交替"原则：

- **痛点-方案组合**：屏 A（对比/痛点 muted）→ 屏 B（平行列表/优势 accent）。情绪从负到正，排版从密到疏
- **理性-感性组合**：屏 A（参数/列表/ledger）→ 屏 B（大主张/quote + 全幅大图）。左脑转右脑，视觉呼吸
- **禁止**：连续 2 屏使用 `grid-3` 均分列表，或连续 2 屏使用双列对比

---

## 十二、换肤示例

改 `:root` 变量即可换色：

```css
:root {
  --bg: #F5F7FA;
  --text-main: #1A1A2E;
  --accent: #4A90D9;   /* 暖金→科技蓝 */
  --text-muted: #6B7280;
  --line: #D1D5DB;
}
