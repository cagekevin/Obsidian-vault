# 详情页设计系统

## 一、设计 Token（换这 11 个值 = 换整个皮肤）

所有颜色、字体集中在 `:root`，改这里的值，全局自动换肤。

```css
/* === 文字色（3 级权重: 高→低） === */
--text-main: #2B2826;     /* 最高：标题、标签、主导语 */
--text-muted: #827A73;    /* 正文、次要信息、普通标签 */
--text-meta: #A6A09A;     /* 最低：脚注、免责声明、辅助说明 */

/* === 强调色（独立，不属于文字层级） === */
--accent: #B89670;         /* 品牌色：大主张（claim）、对比优势方（gold）、装饰线（deco-line）、图标（icon-circle）。节省使用，不用于正文或脚注 */

/* === 背景 === */
--bg: #FAF8F5;            /* 全页统一底色 */
--body-bg: #E0E0E0;       /* 页面外部环境（非内容区域） */

/* === 内部卡片 === */
--card-bg: #FFFFFF;        /* 白底卡片、callout 框 */

/* === 边框 === */
--line: #E8E2DB;           /* 所有 1px 分割线、边框 */

/* === 占位图 === */
--ph-bg: #EFECE8;
--ph-text: #C4BCB4;

/* === 字体 === */
--font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
--font-sans:  "Noto Sans SC", -apple-system, "PingFang SC", "Microsoft YaHei UI", sans-serif;
--font-display: "Playfair Display", "Noto Serif SC", serif;  /* 英文装饰斜体：品牌标语、点缀 */
--font-mono: "IBM Plex Mono", Consolas, "Courier New", monospace;  /* 等宽：规格参数、价格标签、尺寸 */
```

### 颜色使用规则

- `--text-main` 是最高权重文字：模块主标题（h1/h2）、主导语（lead）。**正文（body）不用它，正文用 `--text-muted`**
- `--text-muted` 是正文和标签的默认色（body、sub-muted）。**不要为了让文字"更明显"而改成 main**
- `--text-meta` 是最低权重：脚注、免责、购买须知等辅助文字。**仅用于 meta**，不用于其他 class
- `--accent` 是**唯一品牌色**，同时用于文字强调（claim / quote / gold）和装饰元素（deco-line / icon-circle）。**节省使用，不用于正文、标签底色或脚注**
- `--bg` 是页面背景，`--body-bg` 是浏览器 chrome 区域。**内容区域内不用 `--body-bg`**
- `--card-bg` 用于 callout-box 等白底区块。**纯文字模块不用它**
- `--line` 用于模块分割线、tag-item 边框、卡片边框。**不用其他颜色做边框**
- `--ph-bg` / `--ph-text` 仅开发阶段占位使用。**交付前替换为真实图片**

---

## 二、文字类（14 个 Class + 2 修饰符）

### 2.1 速查表

| Class | 角色 | 字体 | 字号 | 字重 | 颜色 | 字距 |
|---|---|---|---|---|---|---|---|
| `.h1` | 大标题 | Noto Serif SC | 44px | 400 | main | +.05em |
| `.h1-sm` | 大标题(短) | Noto Serif SC | 36px | 400 | main | +.03em |
| `.h-md` | 中标题 | Noto Serif SC | 40px | 400 | main | +.02em |
| `.h2` | 模块标题 | Noto Serif SC | 32px | 400 | main | +.05em |
| `.claim` | 品牌主张 | Noto Serif SC | 40px | 400 | accent | +.05em |
| `.num` | 大数字 | Noto Serif SC | 28px | 400 | accent | +.03em |
| `.pullquote` | 拉取引用 | Noto Serif SC | 32px | 400 it | accent | normal |
| `.quote` | 短引文 | Noto Serif SC | 24px | 400 | accent | +.05em |
| `.h-sub` | 英文副标题 | Playfair Display | 20px | 400 it | muted | normal |
| `.sub` | 强调标签 | Noto Sans SC | 16px | 500 | accent | +.10em |
| `.sub-muted` | 淡化标签 | Noto Sans SC | 16px | 400 | muted | +.10em |
| `.lead` | 主导语 | Noto Sans SC | 16px | 700 | main | normal |
| `.body` | 段落正文 | Noto Sans SC | 14px | 400 | muted | normal |
| `.kicker` | 分类标签 | IBM Plex Mono | 13px | 500 | muted | +.22em |
| `.meta` | 元数据 | Noto Sans SC | 12px | 400 | meta | normal |
| `.spec` | 规格参数 | IBM Plex Mono | 16px | 400 | main | +.02em |
| `.en-deco` | 英文装饰 | Playfair Display | 24px | 400 it | accent | normal |

> **如果长度或大小恰好落在两个 class 之间**：选接近的那个，不要 inline 覆写字号。例如 28px 品牌色数字用 `.num`，36px 标题用 `.h1-sm`。

> **字体角色规则：** Noto Serif SC 只用于展示性文字——标题、主张、引文。Noto Sans SC 用于所有功能性文字——标注、标签、正文、脚注。两类字体不可混用。IBM Plex Mono 仅用于分类标签（kicker）和规格参数（spec）。Playfair Display 仅用于英文副标题（h-sub）和装饰英文（en-deco）。
>
> **硬规则："越大越轻"。** 展示性标题（h1 / h-md / h2 / claim）字重 400，宽字距（+.02~+.05em）。小字（kicker / spec）是唯一可以用 mono + 宽字距（+.22em）的地方。正文和标签（body / lead / sub）用 sans，正常字距。

### 2.2 Google Fonts 加载

在 HTML `<head>` 中加入：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
```

> `Noto Serif SC` 加载 400/500/700（宋体展示），`Noto Sans SC` 加载 400/500/700（黑体功能），`Playfair Display` 加载 400/italic（英文装饰），`IBM Plex Mono` 加载 400/500（等宽规格）

### 2.3 完整 CSS

```css
/* ===== 字体族对应 ===== */

/* Serif 展示 */
.h1   { font-family:var(--font-serif); font-size:44px; font-weight:400; line-height:1.3; color:var(--text-main); text-align:center; letter-spacing:0.05em; }
.h1-sm { font-family:var(--font-serif); font-size:36px; font-weight:400; line-height:1.3; color:var(--text-main); text-align:center; letter-spacing:0.03em; }
.h-md { font-family:var(--font-serif); font-size:40px; font-weight:400; line-height:1.3; color:var(--text-main); text-align:center; letter-spacing:0.02em; }
.h2   { font-family:var(--font-serif); font-size:32px; font-weight:400; line-height:1.4; color:var(--text-main); text-align:center; letter-spacing:0.05em; }
.claim { font-family:var(--font-serif); font-size:40px; font-weight:400; color:var(--accent); text-align:center; letter-spacing:0.05em; }
.num   { font-family:var(--font-serif); font-size:28px; font-weight:400; color:var(--accent); text-align:center; letter-spacing:0.03em; }
.pullquote { font-family:var(--font-serif); font-size:32px; font-weight:400; font-style:italic; color:var(--accent); text-align:center; line-height:1.5; }
.quote { font-family:var(--font-serif); font-size:24px; font-weight:400; color:var(--accent); text-align:center; letter-spacing:0.05em; }

/* Sans 功能 */
.sub   { font-family:var(--font-sans);  font-size:16px; font-weight:500; color:var(--accent); text-align:center; letter-spacing:0.1em; margin-top:16px; }
.sub-muted { font-family:var(--font-sans);  font-size:16px; font-weight:400; color:var(--text-muted); text-align:center; letter-spacing:0.1em; }
.lead  { font-family:var(--font-sans);  font-size:16px; font-weight:700; color:var(--text-main); margin-bottom:8px; }
.body  { font-family:var(--font-sans);  font-size:14px; font-weight:400; line-height:1.8; color:var(--text-muted); }
.meta  { font-family:var(--font-sans);  font-size:12px; color:var(--text-meta); text-align:center; margin-top:24px; }

/* Mono 标签 */
.kicker { font-family:var(--font-mono); font-size:13px; font-weight:500; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.22em; margin-bottom:12px; }
.spec   { font-family:var(--font-mono); font-size:16px; font-weight:400; color:var(--text-main); letter-spacing:0.02em; }

/* Display 英文装饰 */
.h-sub   { font-family:var(--font-display); font-style:italic; font-size:20px; font-weight:400; color:var(--text-muted); }
.en-deco { font-family:var(--font-display); font-style:italic; font-size:24px; font-weight:400; color:var(--accent); }

/* 修饰符 */
.gold      { color:var(--accent); font-weight:inherit; }
.text-center { text-align:center; }
.text-left   { text-align:left; }
```

### 2.4 中文标题长度表

先看标题有多长，再选字号。**不可在文案不变的情况下缩小字号**。

| 标题形态 | 用哪个 class | 默认字号 | 最多字/行 | 最多行 |
|---|---|---|---|---|
| 1行 ≤8 字 | `.h1` | 44px | 8 | 1 |
| 1行 9-14 字 | `.h1-sm` | 36px | 14 | 1 |
| 2行 每行 ≤8 字 | `.h1` | 32px（覆写font-size） | 8 | 2 |
| 中标题 | `.h-md` | 40px | 10 | 1 |
| 模块副标题 | `.h2` | 32px | 14 | 1 |
| 品牌大主张 | `.claim` | 40px | 8 | 1 |
| 品牌大数字 | `.num` | 28px | 4 | 1 |

### 2.5 每模块硬限制

基于 940px 模块的内容体可用宽度（≈844px）：

| 场景 | 可用宽度 | 每字宽度 | 最多字/行 | 超限后果 |
|---|---|---|---|---|
| h1 全宽（正文陈述/大主张） | 844px | ~48px(44px+0.05em) | ≤17 字 | 超长换行→标题变 3 行→挤占正文区 |
| h1 两列内（对比列/平行 2 列） | ~382px | ~48px | ≤7 字 | 换行→标题高度翻倍→图片被压下 |
| h2 全宽 | 844px | ~36px(32px+0.05em) | ≤23 字 | 超长换行 |
| lead 标签（功能名/规格） | 844px | ~18px(16px+0.1em) | ≤46 字 | 不需要限制，lead 本身是短标签 |
| body 正文 | 844px | ~16px(14px+line-height) | ∞ | 自动换行 |

### 2.6 最小可读字号（移动端安全）

详情页是 HTML 网页，手机小屏上同样需要保护：

| 角色 | 当前字号 | 安全下限 | 规则 |
|---|---|---|---|
| 正文（body） | 14px | **≥13px** | 小于 13px 手机上看不清正文字 |
| 脚注（meta） | 12px | **≥11px** | 已经是系统最小，不再新增更低级别 |
| 标签（sub/lead） | 16px | **≥14px** | 当前值安全 |

---

## 三、文案类型 × 排版映射表（核心）

**不再按"模块名称"决定排版，按"这条文案是什么信息"决定。**

### 3.1 对比信息（A vs B）

| 特征 | 两个事物被并列比较 |
|------|-------------------|
| 排版 | 两列等宽 `gap:40px`，中间 `border-right` 分隔 |
| 对照方 | `lead`（颜色手动改为 muted，见下方示例） |
| 优势方 | `lead gold` |
| 图片 | 文字在图片正上方，每列独立 |
| 图片占比 | 每列 ~55% 内容体高度（产品图用 `.frame-img.r-4x3 > img`，截图用 `.frame-img.fit-contain.r-4x3 > img`） |
| 文字规格 | 对照方标签 = `lead` + `color:var(--text-muted)`（16px/700/muted），优势方标签 = `lead gold`（16px/700/accent），正文说明 = `body`（14px/400/muted） |

```
┌─ --text-muted ┐  │  ┌─ --accent ┐
│  BEFORE       │  │  │  AFTER        │
│ [BEFORE]      │  │  │ [AFTER]       │
└───────────────┘  │  └───────────────┘
```

**最小内容量**：≥ 2 对 BEFORE/AFTER
不够 → 切换为 3.9 正文陈述

**匹配到的文案：** BEFORE/AFTER、普通水解角蛋白 vs HFAG 角蛋白、普通护发精油 vs 韩方五谷、某方面对比

### 3.2 平行列表（多个平等项）

| 特征 | N 个同等重要的条目，无层级关系 |
|------|-------------------------------|
| 排版 | 网格均匀排列 |
| 2 列 | 左右等宽，间距 40px |
| 3 项 | 3 行左文右图（带图标的 3 项可用三等分网格） |
| 4 项 | 2 列 × 2 行，同 2 列规则 |
| 文字 | 纯标签用 `body`（安静），重要标签用 `lead gold` |
| 配图 | 图片在文字上方 |
| 图片占比 | 3 项每行 ~80%（`.frame-img.r-4x3`），4 项每格 ~55%（`.frame-img.r-1x1`），2 列每列 ~60%（`.frame-img.r-4x3`） |
| 文字规格 | 功能标签 = `lead`（16px/700/main），说明文字 = `body`（14px/400/muted），3 项方案的类别名用 `sub`（16px/500/accent） |

**情感语义：** SVG accent 图标（`--accent`）只用于正面表达（优势/功能）。痛点/负面内容用图片网格替代 SVG，或用 muted 色（`--text-muted`）简化图标。

```
2项/4项（正面）:                2项/4项（负面/痛点）:
┌───┐ ┌───┐                    ┌────┐ ┌────┐
│图 │ │图 │                    │[图]│ │[图]│
│标 │ │标 │                    │lead  │lead  │
├───┤ ├───┤                    │body  │body  │
│图 │ │图 │                    └────┘ └────┘
│标 │ │标 │
└───┘ └───┘

3项（正面）:                    4 项可混搭文字+图片：
┌───┐ ┌───┐ ┌───┐              ┌──────┐ ┌──────┐
│SVG│ │SVG│ │SVG│              │[痛点图]│ │[痛点图]│
│金 │ │金 │ │金 │              │标  签 │ │标  签 │
│标 │ │标 │ │标 │              ├──────┤ ├──────┤
└───┘ └───┘ └───┘              │[痛点图]│ │[对比图]│
                                 │标  签 │ │ (图片) │
                                 └──────┘ └──────┘
```

**匹配到的文案：** 分叉毛躁/烫染受损/打结易断/干枯无光 → 4 项，上图下文
专利科技/进口成分/持久留香 → 3 项，SVG + 文字
澳大利亚/法国/德国进口植物 → 3 项，左图右文（Z 字形）

**最小内容量**：
  - 3 项网格：≥ 3 项
  - 4 项网格：≥ 4 项
  - 2 列对比：≥ 2 项
不够 → 数量降一个档次（4 项不够用 2 列、3 项不够用 正文陈述）

### 3.3 标签+说明（一对多）

| 特征 | 一个标签/标题 + 一段说明文字 |
|------|----------------------------|
| 排版 | 左文右图，文字列宽度约 40%、图片列约 60%，间距 40px |
| 标签 | `lead` |
| 说明 | `body` |
| 多项 | 纵向堆叠，间距 20px |
| 配图 | 右侧一列，高度撑满 |
| 图片占比 | 图片列占 60% 宽度，100% 内容体高度（`.frame-img.r-3x4` 纵向撑满，参数表用 `.frame-img.fit-contain`） |
| 文字规格 | 每对中的标签 = `lead`（16px/700/main），说明 = `body`（14px/400/muted）。纵向堆叠间距 20px |

```
┌─ 约40% ─┐  ┌─ 约60% ──┐
│  10S     │  │          │
│  HFAG... │  │  [ 图 ]  │
│  24H     │  │          │
│  刺阿... │  │          │
│  3Day    │  └──────────┘
│  滋养... │
│  0油感   │
│  质地... │
└─────────┘
```

**匹配到的文案：** 10S/24H/3Day/0油感 + 各自说明、超分子促渗/微质体隔膜 + 说明、STEP 01~04 + 描述

**最小内容量**：≥ 4 对"标签+说明"
不够 → 去掉图片列，改用纯文字流排版（3.9 正文陈述）

### 3.4 大主张（数字/感叹型）

| 特征 | 一句话或一个数字，需要视觉突出 |
|------|------------------------------|
| 排版 | 居中独占一行 |
| 文字 | `claim`（40px serif gold）或 `quote`（24px serif gold） |
| 40px | 真正的大数字（15 倍） |
| 24px | 中等大小的短语（0 油感、白色花园） |
| 文字规格 | 数字或短语 = `claim`（font-serif / 40px / 400 / accent），较短短语 = `quote`（font-serif / 24px / 400 / accent）。居中独占一行，不可加副标题 |

**匹配到的文案：** 15 倍轻盈柔顺秀发、0 油感 更轻盈、「白色花园里的天马行空」

**最小内容量**：≥ 1 个数字/短语
不够 → 合并到相邻模块的标题或正文中，不独占模块

### 3.5 标签集合（多个 tag）

| 特征 | 一堆小标签/关键词，流式排列 |
|------|---------------------------|
| 排版 | `line-height:2.4` 自然换行 |
| 文字 | `tag-item` |

**匹配到的文案：** 无酒精/无香精/无激素/无重金属...

**最小内容量**：≥ 4 个标签
不够 → 放进正文中用 `body` 流式排列，不单独成行

### 3.8 特殊卡片

| 特征 | 一个独立区块，需要边框区分 |
|------|--------------------------|
| 排版 | `callout-box`（白底 + 边框 + 居中）|
| 内部文字 | `body` |

**匹配到的文案：** 洗发不当警告框、前调/中调/基调卡片

**最小内容量**：≥ 1 段文字或 ≥ 1 张配图
不够 → 不使用卡片，内容融入正文流

### 3.9 正文陈述

| 特征 | 纯描述性文字，无特殊结构 |
|------|------------------------|
| 排版 | 正常流式排列 |
| 文字 | `body` |

**最小内容量**：≥ 3 段正文（或 ≥ 2 段 + 1 张配图）
不够 → 合并到相邻模块，不独占模块

---

## 四、层级规则（重要）

### 4.1 文字层级铁律

```
h2（主标题）> lead（标签）> body（正文）> meta（脚注）
```

- 正文字号不能比标题大
- 次级标题不能比主标题粗/大/显眼
- 同一模块内，主标题（h2）永远是最大/最重的文字
- 需要用 accent 色突出子项 → 使用 `gold`，但字号必须小于主标题

### 4.2 对比方的改色

对照方需要改成灰色，但系统没有专门的 class，直接写 inline：

```html
<!-- 对照方 -->
<p class="lead" style="color:var(--text-muted);">BEFORE 分叉毛躁</p>

<!-- 产品方 -->
<p class="lead gold">AFTER 顺滑清爽</p>
```

这是全系统唯一允许 inline 覆盖颜色的场景。

### 4.3 平行项数量决定排版

2 项、3 项、4 项的排版不能硬套同一模板：

| 数量 | 排版方案 |
|------|---------|
| **2 项** | 左右两列等宽 |
| **3 项** | 3 行左文右图（每行文字在图左侧） |
| **4 项** | 2 列 × 2 行网格 |

### 4.4 内容密度规则

每个模块的内容填充率不得低于 **75%**（即空白区域不超过模块高度的 25%）。

```
┌─────────────────────┐
│  ████████████████   │  ← 75% 以上被内容占据
│  ████████████████   │
│  ████████████████   │
│  ████████████████   │
│                     │  ← 留白 ≤ 25%
└─────────────────────┘
```

- 内容不足时：增大图片占比、增加一行数据点、或加底部大图（.mod-img）来撑满。**不可用 `.mod-auto` 逃避密度问题**
- 禁止为了填满而加无意义的装饰元素

### 4.5 通用硬规则（不可违反）

以下 3 条不挑场景，任何页面都必须遵守：

1. ❌ 禁止假数据、假百分比、假引用。所有数据和声明必须来源于用户提供的原始文案
2. ❌ 禁止使用 emoji。详情页的装饰使用 `deco-line`、`tag-item`、`callout-box` 等系统 class
3. ❌ 禁止在文案不够时缩小字号。先砍文案、缩短句式、或切换到更高密度的排版类型

### 4.6 交付前自检清单

每次完成一个详情页模块后，输出以下 PASS/FAIL 检查再进入下一个模块：

```
━━━ 自检 — 模块交付 ━━━
[PASS] 展示性文字（标题/主张/引用）用了 serif，功能文字（标签/正文/脚注）用了 sans
[PASS] 颜色层级正确：标题用 --text-main、正文用 --text-muted、脚注用 --text-meta，未错用
[PASS] 同一模块内 h2 是最大/最重的文字
[PASS] 无多余 inline style（仅对比方改色场景允许 inline color），超出内置 class 的布局用 task-scoped CSS block
[PASS] 内容填充率未违反第 4.4 节密度规则
[PASS] 真实图片用了 `.frame-img`，占位图用了 `.img-box` / `.img-fluid`
[PASS] 装饰元素有功能目的：标签用 `.tag-item`、分割用 `.rule` / `.deco-line`，无装饰性斑点/圆圈/渐变
[PASS] 未使用假数据 / emoji / 缩小字号的补救
━━━ 全部通过 ━━━
```

> **退路机制**：当内置 class 确实无法表达某个布局时，允许在 `<head>` 中写一个最小的 task-scoped CSS block，class 名格式为 `page-xxx`（如`.page-m08-grid`）。**禁止使用 inline style 作为替代**。
>
> **退路检查**：写完 task-scoped CSS 后，全文搜索 `.page-` 确认每个 HTML 里用的 class 名都在 `<style>` 中有定义。发现的 dangling class 在提交前补全。

全部 PASS 才能提交最终 HTML。任一 FAIL → 修正后重新检查。

### 4.7 风格身份测试

一个详情页模块只有**全部条件满足**才算真正符合设计系统：

1. ✅ 展示性文字（h1/h2/claim/quote）用了 Noto Serif SC，功能性文字（sub/lead/body/meta）用了 Noto Sans SC
2. ✅ 同一模块内 h2 是最大/最重的文字，未被其他 class 或 inline style 超越
3. ✅ 装饰有功能目的（标签用 `.tag-item`、分割用 `.rule`/`.deco-line`、引用用 `.callout-box`），无斑点/渐变/纹理
4. ✅ 内容填充率 ≥75%（4.4 节），或内容天然不足以填充时用了 `.mod-auto`
5. ✅ 无 inline style 调整间距/字号/颜色（对比方改色是唯一例外），布局超出内置 class 时用了 task-scoped CSS block

如果某个条件不满足，这个模块不是"详情页设计系统"的模块——修正或改用裸 HTML。

### 4.8 反模式

以下是从真实交付中提取的"能渲染成功但其实是错的"案例：

**反模式 A：内联样式代替 class 系统**
```html
<!-- ❌ 错误 -->
<p class="body" style="margin-top:16px;max-width:480px;color:var(--text-muted);">
<p class="claim gold" style="font-size:28px;">65W</p>

<!-- ✅ 正确：间距用 .gap-1-5，字号用 .num，多余 color 去掉 -->
<div class="stack gap-1-5">
  <p class="body" style="max-width:480px;">
  <p class="num gold">65W</p>
</div>
```

**反模式 B：找不到 class 就编 class**
```html
<!-- ❌ 错误 -->
<div class="col" style="flex:2;gap:32px;">

<!-- ✅ 正确：用系统已有的 .stack + 1N gap，special 布局加 task-scoped CSS -->
<div class="stack gap-3" style="flex:2;">
```
或在 `<head>` 中加 ````css .page-m03-lcols { flex:2; display:flex; flex-direction:column; gap:32px; } ```` 再 `<div class="page-m03-lcols">`

**反模式 C：h1 标题固定用 44px 不按长度调整**
```html
<!-- ❌ 错误：9 个字还用了 44px -->
<h1 class="h1">充得快，只是一种本能</h1>

<!-- ✅ 正确：9-14 字用 .h1-sm -->
<h1 class="h1-sm">充得快，只是一种本能</h1>
```

**反模式 D：模块内的装饰线位置混乱**
```html
<!-- ❌ 错误：deco-line 放在内容体中间 -->
<div class="mod-body">
  <p class="body">...</p>
  <div class="deco-line"></div>
  <p class="body">...</p>
</div>

<!-- ✅ 正确：deco-line 放标题区末尾做视觉过渡 -->
<div class="mod-top-c">
  <h2 class="h2">标题</h2>
  <div class="deco-line"></div>
</div>
<div class="mod-body">
  <p class="body">...</p>
</div>
```

---

## 五、模块框架

每个模块由 **标题** + **内容体** 构成，放在一个容器里，容器之间用 1px 细线分割。

### 5.1 基础容器

```css
.mod        { height:940px; display:flex; flex-direction:column; border-top:1px solid var(--line); }
.mod-auto   { height:auto; min-height:940px; display:flex; flex-direction:column; border-top:1px solid var(--line); }
.mod-top-c  { padding:80px 48px 0; text-align:center; }                        /* 标题区 */
.mod-body   { flex:1; padding:24px 48px 48px; display:flex; flex-direction:column; }  /* 内容体 */
.mod-img    { margin:0 48px 48px; min-height:200px;
              display:flex; align-items:center; justify-content:center;
              background:var(--ph-bg); color:var(--ph-text);
              font-size:12px; letter-spacing:0.1em; text-transform:uppercase; }  /* 底部图片 */
```

- 内容物足够撑满 940px 的模块用 `.mod`
- 内容物不适合填满时用 `.mod-auto`（由内容自然决定高度）
- 标题区用 `.mod-top-c`，内容体用 `.mod-body`，底部图片用 `.mod-img`
- 标题区最后一个元素如果是装饰线，其下 margin 与 `.mod-body` 的 padding-top 合并间距，不需要额外调整

### 5.2 布局辅助类

```css
.stack    { display:flex; flex-direction:column; }
.gap-1    { gap:12px; }
.gap-1-5  { gap:16px; }
.gap-2    { gap:24px; }
.gap-3    { gap:36px; }
.gap-4    { gap:48px; }
.gap-5    { gap:64px; }
.grid-3     { display:flex; gap:32px; }
.grid-3-item{ flex:1; text-align:center; }
.grid-2x2   { display:flex; flex-wrap:wrap; gap:40px; }
.grid-2x2-item { flex:1 1 calc(50% - 20px); text-align:center; }
.img-box    { display:flex; align-items:center; justify-content:center; background:var(--ph-bg); color:var(--ph-text); font-size:12px; letter-spacing:0.1em; text-transform:uppercase; }
```

### 5.3 基础结构

```
┌─────────────────────────────────┐  ← border-top: 1px
│  标题（居中，h2）              │  ← 上方留白 80px
│  副标题/装饰线（可选）           │
├─────────────────────────────────┤
│  内容体                          │  ← 文案类型决定排版
│  （文字/网格/对比列/图片...）     │
│                                  │
│  图片（可选）                    │  ← 图片左右/底部各留白 48px
└─────────────────────────────────┘
```

- 标题区上下 padding：80px（文字不贴顶）
- 内容体内部间距：24px 48px
- 图片：不与边缘贴齐，左右 bottom 各留 48px
- 首屏模块顶部无分割线

### 5.4 三种布局

| 布局 | 适合什么文案 | 结构 |
|------|-------------|------|
| **文字 + 图片** | 标签+说明、正文陈述等正文内容，配一张整图做视觉收尾 | 标题 → 文字内容 → 下方整张大图 |
| **纯文字** | 平行列表、图标层、对比列——内容自身已有完整视觉 | 标题 → 文字/网格/对比列，没有尾部大图 |
| **标题区全包 + 图片** | 大主张、特殊卡片——所有文字密度低，一张标题区容纳全部内容 | 标题区（含所有文字）→ 下方整张大图 |

### 5.5 间距规格

| 场景 | 留白 |
|------|------|
| 模块之间 | 1px 细线 `var(--line)` |
| 标题上下 | 80px |
| 内容体左右 | 48px |
| 图片边缘 | 48px（左右 bottom） |
| 两列之间 | 40px |
| 三列之间 | 32px |

---

## 六、图片系统

### 6.1 图片容器

所有真实图片（非占位）用 `.frame-img` 包裹，配合 ratio class 控制宽高比：

```html
<!-- 产品实物图：cover 裁切填满 -->
<figure class="frame-img r-4x3">
  <img src="assets/product.jpg" alt="产品名">
</figure>

<!-- 参数表/截图：contain 完整显示 -->
<figure class="frame-img fit-contain r-4x3">
  <img src="assets/spec.jpg" alt="参数表">
</figure>
```

```css
.frame-img {
  width:100%; display:block; overflow:hidden;
}
.frame-img > img {
  width:100%; height:100%; object-fit:cover; display:block;
}
.frame-img.fit-contain > img { object-fit:contain; }

/* Ratio classes */
.r-16x9  { aspect-ratio:16/9; }   /* 底部大图 */
.r-4x3   { aspect-ratio:4/3; }    /* 对比/平行图 */
.r-1x1   { aspect-ratio:1/1; }    /* 方形图标/网格 */
.r-3x4   { aspect-ratio:3/4; }    /* 标签+说明右侧纵向图 */
```

### 6.2 占位图组件（开发中/待替换用）

```css
.img-fluid { width:100%; display:flex; align-items:center; justify-content:center; background:var(--ph-bg); color:var(--ph-text); font-size:13px; letter-spacing:0.15em; text-transform:uppercase; }
.img-box   { width:100%; display:flex; align-items:center; justify-content:center; background:var(--ph-bg); color:var(--ph-text); font-size:12px; letter-spacing:0.1em; }
```

---

## 七、装饰组件

```css
/* 分割线 */
.rule       { height:1px; background:var(--line); border:0; margin:24px 0; }     /* 通用细分割线 */
.deco-line  { width:40px; height:1px; background:var(--accent); margin:24px auto; }  /* 强调装饰线 */

/* 标签 */
.tag-item    { display:inline-block; padding:6px 16px; border:1px solid var(--line); border-radius:99px; font-size:13px; color:var(--text-muted); margin:4px; }
.tag-wrap    { line-height:2.4; }  /* 多个 tag-item 的容器加此行高 */

/* 卡片 */
.callout-box { background:var(--card-bg); padding:20px; text-align:center; border:1px solid var(--line); }

/* 参数行（规格列表） */
.ledger      { display:flex; flex-direction:column; }
.ledger-row  { display:grid; grid-template-columns:1fr auto; gap:24px; padding:14px 0; border-bottom:1px solid var(--line); align-items:baseline; }
.ledger-label{ font-family:var(--font-sans); font-size:14px; font-weight:400; color:var(--text-muted); }
.ledger-value{ font-family:var(--font-mono); font-size:16px; font-weight:400; color:var(--text-main); text-align:right; }

/* 图标容器 */
.icon-circle { width:120px; height:120px; border-radius:50%; border:1px solid var(--line); display:flex; align-items:center; justify-content:center; margin:0 auto 16px; font-size:28px; color:var(--accent); }

/* === 图标语义规则 === */
/* .icon-circle 的 accent 色只用于正面表达——产品优势、功能亮点、利益点 */
/* 痛点/负面/「BEFORE 方」的图标 → 用 --text-muted 色覆写 color:var(--text-muted) 或直接省略图标 */
```

### 装饰用法规则

**`.rule` — 通用分割线**
- 用途：在模块内容体内部切割两块不同信息，如标签集合和正文之间
- 位置：放在 `.mod-body` 内部两个内容块之间
- 样式：`var(--line)` 灰色 1px，全宽
- 不要用它做模块之间的分割（模块之间已经用 `.mod` 的 `border-top` 分割）

**`.deco-line` — 强调装饰线**
- 用途：在标题区和内容体之间做一个视觉过渡，或在大主张周围做点缀
- 位置：放在 `.mod-top-c` 末尾（标题内容最后一个元素）
- 样式：`var(--accent)` 金色，40px 宽居中
- 它的下 margin 会自动与 `.mod-body` 的 padding-top 合并，不需要手动调间距

**`.tag-item` — 胶囊标签**
- 用途：多个短关键词/规格的流式排列
- 位置：放在 `.mod-top-c` 的标题下方，或 `.mod-body` 内的内容区
- 多个标签放入 `.tag-wrap` 容器以获得正确行高
- 不放 `.callout-box` 内部（卡片内部用 `body` 文字）

**`.callout-box` — 白底卡片**
- 用途：一条需要边框强调的信息（注意事项、亮点总结、保修说明）
- 位置：放在 `.mod-body` 内部
- 最多一屏 3 个，超过 3 个改用 `tag-item` 或 `body` 流式排列
- 内部文字只用 `body` class，不用其他文字 class

**`.icon-circle` — 圆形图标容器**
- 用途：正面功能点的视觉符号（SVG 图标或 emoji 简写）
- 位置：放在 `.grid-3-item` / `.grid-2x2-item` 内部，文字上方
- accent 色只用于正面表达；负面/痛点用 muted 色（加 `.is-negative`）
- 一屏最多 4 个，超过 4 个改用图片网格

**`.ledger` — 参数行**
- 用途："标签+值"的规格列表（重量 150g / 尺寸 80×50mm / 材质 铝合金）
- 位置：放在 `.mod-body` 内部
- 每行格式：左侧 `ledger-label`（sans/14px/muted），右侧 `ledger-value`（mono/16px/main）
- 最少 2 行，最多 8 行

```html
<div class="ledger">
  <div class="ledger-row">
    <span class="ledger-label">重量</span>
    <span class="ledger-value">150g</span>
  </div>
  <div class="ledger-row">
    <span class="ledger-label">尺寸</span>
    <span class="ledger-value">80 × 50 × 28mm</span>
  </div>
  <div class="ledger-row">
    <span class="ledger-label">材质</span>
    <span class="ledger-value">铝合金</span>
  </div>
</div>
```

**`.rule` vs `.deco-line` 选择规则：**
```
只需要一条线来分隔两块内容  → 用 .rule（无品牌感）
需要在标题下方做一个仪式感停顿 → 用 .deco-line（品牌金色）
不确定用哪个 → 用 .rule（更安静，不会过度设计）
```

### 装饰禁止规则（从杂志风搬）
/* ❌ 亮色渐变 —— 装饰只使用 --accent / --line / --text-muted，不用多色渐变 */
/* ❌ 整页网格、点阵、方格纸 —— 不为"看起来更设计"而加背景纹理 */
/* ❌ 装饰性的斑点、圆圈、飘浮元素 —— 每个装饰元素必须有功能目的（标签/分割/图标） */
/* ❌ 文字背后放强背景标记 —— 确保正文可读性，不在 body/lead 下方加底色块 */
/* ❌ 装饰遮挡内容 —— 任何装饰不能盖住文字、图片或关键信息 */
```

---

## 八、完整 CSS（一次性复制到 `<style>`）

以下 CSS 是设计系统所有 class 的完整定义。复制到 HTML 的 `<style>` 中即可使用：

```css
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
body{font-family:var(--font-sans);background:var(--body-bg);color:var(--text-main);-webkit-font-smoothing:antialiased;}
.page{width:790px;margin:0 auto;background:var(--bg);overflow:hidden;}

/* Token */
:root{--text-main:#2B2826;--text-muted:#827A73;--text-meta:#A6A09A;--accent:#B89670;--bg:#FAF8F5;--body-bg:#E0E0E0;--card-bg:#FFFFFF;--line:#E8E2DB;--ph-bg:#EFECE8;--ph-text:#C4BCB4;--font-serif:"Noto Serif SC","Songti SC","STSong",serif;--font-sans:"Noto Sans SC",-apple-system,"PingFang SC","Microsoft YaHei UI",sans-serif;--font-display:"Playfair Display","Noto Serif SC",serif;--font-mono:"IBM Plex Mono",Consolas,"Courier New",monospace;}

/* 文字 —— Serif 展示 */
.h1{font-family:var(--font-serif);font-size:44px;font-weight:400;line-height:1.3;color:var(--text-main);text-align:center;letter-spacing:0.05em;}
.h1-sm{font-family:var(--font-serif);font-size:36px;font-weight:400;line-height:1.3;color:var(--text-main);text-align:center;letter-spacing:0.03em;}
.h-md{font-family:var(--font-serif);font-size:40px;font-weight:400;line-height:1.3;color:var(--text-main);text-align:center;letter-spacing:0.02em;}
.h2{font-family:var(--font-serif);font-size:32px;font-weight:400;line-height:1.4;color:var(--text-main);text-align:center;letter-spacing:0.05em;}
.claim{font-family:var(--font-serif);font-size:40px;font-weight:400;color:var(--accent);text-align:center;letter-spacing:0.05em;}
.num{font-family:var(--font-serif);font-size:28px;font-weight:400;color:var(--accent);text-align:center;letter-spacing:0.03em;}
.pullquote{font-family:var(--font-serif);font-size:32px;font-weight:400;font-style:italic;color:var(--accent);text-align:center;line-height:1.5;}
.quote{font-family:var(--font-serif);font-size:24px;font-weight:400;color:var(--accent);text-align:center;letter-spacing:0.05em;}

/* 文字 —— Sans 功能 */
.sub{font-family:var(--font-sans);font-size:16px;font-weight:500;color:var(--accent);text-align:center;letter-spacing:0.1em;margin-top:16px;}
.sub-muted{font-family:var(--font-sans);font-size:16px;font-weight:400;color:var(--text-muted);text-align:center;letter-spacing:0.1em;}
.lead{font-family:var(--font-sans);font-size:16px;font-weight:700;color:var(--text-main);margin-bottom:8px;}
.body{font-family:var(--font-sans);font-size:14px;font-weight:400;line-height:1.8;color:var(--text-muted);}
.meta{font-family:var(--font-sans);font-size:12px;color:var(--text-meta);text-align:center;margin-top:24px;}

/* 文字 —— Mono 标签 */
.kicker{font-family:var(--font-mono);font-size:13px;font-weight:500;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.22em;margin-bottom:12px;}
.spec{font-family:var(--font-mono);font-size:16px;font-weight:400;color:var(--text-main);letter-spacing:0.02em;}

/* 文字 —— Display 英文 */
.h-sub{font-family:var(--font-display);font-style:italic;font-size:20px;font-weight:400;color:var(--text-muted);}
.en-deco{font-family:var(--font-display);font-style:italic;font-size:24px;font-weight:400;color:var(--accent);}

/* 修饰符 */
.gold{color:var(--accent);font-weight:inherit;}
.text-center{text-align:center;}
.text-left{text-align:left;}

/* 模块系统 */
.mod{height:940px;display:flex;flex-direction:column;border-top:1px solid var(--line);}
.mod-auto{height:auto;min-height:940px;display:flex;flex-direction:column;border-top:1px solid var(--line);}
.mod-top-c{padding:80px 48px 0;text-align:center;}
.mod-body{flex:1;padding:24px 48px 48px;display:flex;flex-direction:column;}
.mod-img{margin:0 48px 48px;min-height:200px;display:flex;align-items:center;justify-content:center;background:var(--ph-bg);color:var(--ph-text);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;}

/* 布局辅助 */
.stack{display:flex;flex-direction:column;}
.gap-1{gap:12px;}.gap-1-5{gap:16px;}.gap-2{gap:24px;}.gap-3{gap:36px;}.gap-4{gap:48px;}.gap-5{gap:64px;}
.grid-3{display:flex;gap:32px;}
.grid-3-item{flex:1;text-align:center;}
.grid-2x2{display:flex;flex-wrap:wrap;gap:40px;}
.grid-2x2-item{flex:1 1 calc(50% - 20px);text-align:center;}
.img-box{display:flex;align-items:center;justify-content:center;background:var(--ph-bg);color:var(--ph-text);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;}

/* 图片容器 */
.frame-img{width:100%;display:block;overflow:hidden;}
.frame-img > img{width:100%;height:100%;object-fit:cover;display:block;}
.frame-img.fit-contain > img{object-fit:contain;}
.r-16x9{aspect-ratio:16/9;}.r-4x3{aspect-ratio:4/3;}.r-1x1{aspect-ratio:1/1;}.r-3x4{aspect-ratio:3/4;}
.img-fluid{width:100%;display:flex;align-items:center;justify-content:center;background:var(--ph-bg);color:var(--ph-text);font-size:13px;letter-spacing:0.15em;text-transform:uppercase;}

/* 装饰 */
.rule{height:1px;background:var(--line);border:0;margin:24px 0;}
.deco-line{width:40px;height:1px;background:var(--accent);margin:24px auto;}
.tag-item{display:inline-block;padding:6px 16px;border:1px solid var(--line);border-radius:99px;font-size:13px;color:var(--text-muted);margin:4px;}
.tag-wrap{line-height:2.4;}
.callout-box{background:var(--card-bg);padding:20px;text-align:center;border:1px solid var(--line);}
.icon-circle{width:120px;height:120px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-size:28px;color:var(--accent);}
.icon-circle.is-negative{color:var(--text-muted);}

/* 参数行 */
.ledger{display:flex;flex-direction:column;}
.ledger-row{display:grid;grid-template-columns:1fr auto;gap:24px;padding:14px 0;border-bottom:1px solid var(--line);align-items:baseline;}
.ledger-label{font-family:var(--font-sans);font-size:14px;font-weight:400;color:var(--text-muted);}
.ledger-value{font-family:var(--font-mono);font-size:16px;font-weight:400;color:var(--text-main);text-align:right;}
```

---

## 九、构建流程

按顺序回答以下问题，每步答案决定下一步的选项。

```
┌────────────────────────────────────────────────┐
│  第一步：情感语义                              │
│  这段文案在表达什么情绪？                       │
│  ├── 正面/优势（功能亮点、利益点、成就）        │
│  └── 负面/痛点（问题、BEFORE 状态、缺陷）       │
│                                                │
│  决定：图标用什么色（accent / muted）            │
└────────────────────┬───────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────┐
│  第二步：信息类型                              │
│  这些文案之间是什么关系？                       │
│  ├── A vs B 被并列对比     → 对比（第 3.1 节） │
│  ├── N 个同等重要的条目    → 平行（第 3.2 节） │
│  ├── 一个标签 + 一段说明   → 标签+说明（3.3 节）│
│  ├── 一句话/数字需要突出   → 大主张（第 3.4 节）│
│  ├── 一堆小标签流式排列    → 标签集合（3.5 节） │
│  ├── 独立区块需要边框区分  → 特殊卡片（3.8 节） │
│  └── 纯描述无特殊结构      → 正文陈述（3.9 节） │
│                                                │
│  决定：用什么排版方案                           │
└────────────────────┬───────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────┐
│  第三步：模块布局                              │
│  内容体下方还有图吗？                           │
│  ├── 有尾部大图    → 「文字 + 图片」布局       │
│  ├── 无尾部大图    → 「纯文字」布局             │
│  └── 全部文字在标题区 → 「标题区全包 + 图片」   │
│                                                │
│  决定：用 .mod（固定940px）还是 .mod-auto       │
└────────────────────┬───────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────┐
│  第四步：选文字类                              │
│  对照方 = lead + color:var(--text-muted)     │
│  产品方 = lead gold                        │
│  功能名/标签 = lead                          │
│  正文/描述 = body                            │
│  最低权重 = meta                             │
│                                                │
│  注意：4.1 铁律——主标题最大、字重不降级、      │
│  不 inline 覆盖字号/颜色/字重                   │
└────────────────────────────────────────────────┘

例：本文 HKH 充电器 M02（痛点）
  情感：负面 → 图片网格，不用 accent 色图标
  类型：4 项平行 → 2×2 网格（3 痛点 + 1 对比图）
  布局：无尾部图 → 纯文字，.mod-auto
  文字：标签用 lead，描述用 body

---

## 十、换肤示例

```css
:root {
  --bg: #F5F7FA;
  --text-main: #1A1A2E;
  --accent: #4A90D9;   /* accent 换色：暖金→科技蓝 */
  --text-muted: #6B7280;
  --line: #D1D5DB;
}
```

---

## 十一、图片规格速查表

占位图（`.img-fluid`）中的文字必须写清楚"这张图放什么"，交付前替换为真实图片。

### 11.1 占位图写作规范

占位图文字必须包含三个要素：**主体对象** + **呈现方式/视角** + **核心信息**。

```
✅ 正确：产品 45° 悬浮渲染 · 芯片结构爆炸图 · 蓝色能量环
✅ 正确：充电曲线图 / 0% → 50% / 15分钟
✅ 正确：磨砂外壳微距特写（不沾指纹）
✅ 正确：左=旧充电器发烫 / 右=用户焦急等待

❌ 错误：产品图
❌ 错误：对比图
❌ 错误：数据图
```

多行内容用 `<br>` 换行，次要说明用 `.page-ph-cap` 或 `.page-hero-caption` 缩小字号展示。

### 11.2 图片角色类型 × 规格映射

以下按详情页中常见的 **图片角色** 组织，不绑定具体产品。写占位文字时套用对应角色的模板。

| 图片角色 | 典型出现场景 | 容器 | 比例 | 占位文字模板 | 替换为真实图后注意 |
|---------|-------------|------|------|------------|----------------|
| **主视觉大图** | 首屏海报位，独立撑满 | `.mod-img` | 自由（flex 撑满） | `产品 [视角/摆放方式] · [背景元素1] · [背景元素2]`<br>`底部：[辅助说明]` | 高精渲染/摄影，裁切以主体为准 |
| **对比图（痛/优势）** | 对比屏，左旧右新 / 左痛右好 | `.frame-img.r-4x3` | 4:3 | `[场景描述] · [核心感受]` 或 `左=[旧] / 右=[新]` | 两图风格统一，色温区分（旧=暖灰，新=冷亮） |
| **透视/拆解图** | 核心科技屏，展示内部结构 | `.frame-img.r-16x9` | 16:9 | `产品 [透视方式] · [内部结构件1] · [内部结构件2]`<br>`caption：[对比说明]` | 需展示对比元素（如传统 vs 新型结构） |
| **场景示意图** | 使用场景、功能示意屏 | `.frame-img.r-16x9` | 16:9 | `[人物/设备] + [动作/状态] · [环境]` | 干净背景，突出产品与动作关系 |
| **特写细节图（×N）** | 材质/工艺屏，N 格网格 | `.frame-img.r-1x1` | 1:1 | `[部位名称]（[拍摄视角]）` | 微距拍摄，每格聚焦一个细节，光影一致 |
| **使用场景图（×4）** | 场景矩阵屏，2×2 网格 | `.frame-img.r-4x3` | 4:3 | `[场景标签]`（简洁，文字在图下方） | 真人场景摄影或高品质合成，氛围感统一 |
| **数据图表** | 实证屏，展示测试数据 | `.frame-img.r-4x3` | 4:3 | `[图表类型] / [关键数据1] · [关键数据2]` | 如截图/参数表需加 `.fit-contain` |
| **产品全家福** | 品牌承诺/购买屏 | `.frame-img.r-16x9` | 16:9 | `[主体] + [配件1] + [配件2] · [摆放方式]` | 平铺或摆拍，配件齐全，光线均匀 |
| **安全/防护示意** | 安全承诺屏 | `.frame-img.r-16x9` | 16:9 | `[防护方式] + [视觉比喻] · 图标排列` | 抽象化视觉表达，配图标矩阵 |
| **端口/接口示意** | 多口功能屏 | `.frame-img.r-16x9` | 16:9 | `[端口类型1] + [端口类型2] + [端口类型3] · [设备名称]` | 特写插口，标注每个口的功率/设备 |

> **通用替换规则**：
> - 实物摄影/渲染图 → `<img>` 用 `object-fit:cover`（默认）
> - 截图/参数表/图表 → `<figure>` 加 `.fit-contain` 子类
> - 删除占位文字，替换为 `<img src="assets/xxx.jpg" alt="...">`

### 11.3 占位图 → 真实图替换模板

```html
<!-- 替换前（占位阶段） -->
<figure class="frame-img r-4x3">
  <div class="img-fluid page-ph-full">产品透视图 · 内部结构件 · 对比传统设计</div>
</figure>

<!-- 真实产品图：cover 裁切填满 -->
<figure class="frame-img r-4x3">
  <img src="assets/product-xray.jpg" alt="产品内部透视结构图">
</figure>

<!-- 截图/参数表/图表：fit-contain 完整显示 -->
<figure class="frame-img fit-contain r-4x3">
  <img src="assets/spec-chart.jpg" alt="性能对比图表">
</figure>

<!-- N 格网格中的单个特写 -->
<figure class="frame-img r-1x1">
  <img src="assets/detail-texture.jpg" alt="外壳磨砂纹理微距特写">
</figure>
```

### 11.4 图片交付检查清单

替换真实图片前确认：

- [ ] 占位文字已完整描述图片内容和视角（主体 + 方式 + 信息点）
- [ ] ratio class 与图片实际宽高比匹配（16:9 大图 / 4:3 平行 / 1:1 方形）
- [ ] 截图/参数表加了 `.fit-contain`，实物图不加
- [ ] 所有 `<img>` 有 `alt` 属性，描述图片内容
- [ ] 多图网格中每张图风格/色调/精度一致
- [ ] 删除空的 `.img-fluid` / `.img-box` 占位容器
