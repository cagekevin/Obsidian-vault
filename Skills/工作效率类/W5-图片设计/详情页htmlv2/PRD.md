# PRD：详情页 HTML 2（仿 claud 美学的工程化详情页生成器）

> **代号**：`product-detail-v2`
> **作者**：kevin
> **起草时间**：2026-06-14
> **修订时间**：2026-06-14（v0.4 — 38 个 class BEM 命名定稿）
> **状态**：Draft v0.4（待评审）
> **目标路径**（落地后）：`skills/工作效率类/W5-图片设计/详情页htmlv2/`

---

## 一、为什么做这个 skill（Why）

### 1.1 现状与痛点

| 现有产物 | 满意的地方 | 不满意的地方 |
|---|---|---|
| `W5 详情页 HTML` v1（韩方五谷模板） | 12 屏结构严谨、serif/sans 字体隔离、≥75% 填充率、空间预算先算 | 1. **排版美感不足**（用户原话）——像杂志内页堆卡片<br>2. 屏间容易出现文字穿插<br>3. 缺乏 claud 的 4 维定位 + 品牌专属决策 |
| `W8 基础网页设计` claud | 4 维定位 / 真实资产 / Step 0 验真 / 完整状态 / Pre-delivery Checklist | 是整页滚动叙事，**不是** 12 屏分镜卡片式 |

**核心矛盾**：
> 工程化模板（W5）排版美感不足（用户原话），定制化设计（W8 claud）又无法批量出 12 屏。

**用户原话（核心）**：
> "之前的排版有问题，就是设计感不足，所以才需要学习 claud。"
> "我们的这个的核心在于，如何在 940 像素高以内排版要好看。"

### 1.2 目标

造一个**"工程化的 claud"**——既保留 W5 的 12 屏分镜结构和自检铁律，又继承 W8 claud 的"4 维定位 + 品牌专属决策 + 真实资产"。

**静态优先**（v0.2 加入）：差异化靠 **配色 + 字体 + 真实资产 + 4 维定位** 实现，不靠动效。

**排版美感优先**（v0.3 加入 · 核心目标）：在 **940px 固定高度** 内做出 claud 级别的设计感。

### 1.3 不做什么

- ❌ 不替代 W8 claud（整页落地页用 W8）
- ❌ 不替代 W5 详情页 HTML v1（结构合规场景继续用）
- ❌ **不引入任何动效**（R4 · v0.2）
- ❌ **不加 Tweaks 面板**（R4 · v0.2）
- ❌ **不让屏间出现文字穿插**（R7 · v0.3）
- ❌ **不让屏间文字/视觉堆叠**（R8 · v0.3）
- ❌ 不做后端、不做表单提交、不做购物车
- ❌ 不内嵌第三方组件库

---

## 二、铁律（Must-have · 不能改）

### 铁律 R1 · 每屏必须有文字
每屏（`.mod`）必须**有标题文字**（不允许纯图屏）。包括：
- 主标题（h1 / h1-sm / h2，必有）
- 副标题 / 英文装饰（h-sub，可选）
- 至少 1 段 body / lead（功能性说明）

### 铁律 R2 · 每屏 940px 固定高度
- 每屏 940px（`.mod`，与 W5 v1 一致）
- 内容自然超 940 → 用 `.mod-auto`（W5 v1 自带）
- 内容不足 → 增大图片占比、加大字号或加底部 `.mod-img`，**禁止缩字号**

### 铁律 R3 · 排版可改，铁律不改
- 字体可以换（衬线 + 无衬线组合必选，claud 风格 Fraunces + Inter Tight 可作为可选 token）
- 配色可以换（朝圣黎明 / 玫瑰矿泉 / 黄昏胶囊等都可）
- **R1/R2/R4/R5/R6/R7/R8 不变**

### 铁律 R4 · 静态优先（v0.2）
- **禁止任何形式的动效**：无 CSS transition、无 CSS animation、无 JS IntersectionObserver
- **禁止 Tweaks 面板**
- hover 状态允许，但**仅限颜色 / 边框微调**，**禁止 transform: scale / translate / rotate**
- 页面打开 → 立刻呈现最终状态，**零等待**

### 铁律 R5 · 排版美感优先（v0.3 · 核心）
> "如何在 940 像素高以内排版要好看"

- **940px 内每一像素都要有设计意图**——不是"塞满"，是"好看地排"
- 学习目标：W8 claud 的**屏幕叙事美学**（在固定画布内讲故事）
- 自检新增项："这屏排版拿到 Dribbble / Behance 能否得 ≥8 分"
- 美感来源：**节奏 / 留白 / 字号对比 / 衬线小细节 / 真实质感**（不靠动效）

### 铁律 R6 · 标题区固定在屏顶居中（v0.3）
> "我的主副标题一定是在上面居中的，唯一可动的就是下面"

**结构铁律**（每屏）：
```
┌─────────────────────────────────┐
│        屏 顶（padding-top 80px）    │
│                                  │
│         主标题 h1-sm              │  ← 固定：屏顶居中
│         副标 h-sub / deco-line   │  ← 固定：紧跟主标
│         body / lead              │  ← 固定：标题区收尾
│                                  │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│                                  │
│         自由排版区                 │  ← 可变：以下可自由发挥
│         (body / 图片 / 卡片 / 数字) │
│                                  │
│         底部 mod-img（可选）       │
└─────────────────────────────────┘
```

**不可变**：
- 主标题 / 副标 / body 一定在 `.mod-top-c`（屏顶，padding-top 80px）
- 水平居中
- 字号、字距、衬线小细节可在主题文件中调整

**可变**（自由排版区）：
- 图片比例、位置
- 卡片/网格/对比列的排布
- 数字陈列
- 留白节奏

**禁止**：
- ❌ 标题放到屏中部或屏底
- ❌ 标题区与自由排版区交叉穿插
- ❌ 自由排版区溢出到标题区
- ❌ **页面 HTML 中出现任何 emoji**（v0.5 新增 · 详见 references/typographic-rhythm.md §3.7）
- ❌ **擅自决定大标题字号**（v0.5 新增 · 必须给用户两套方案选，详见 references/typographic-rhythm.md §3.6）
- ❌ **凭"感觉"断行**（v0.5 新增 · 必须用 `<br>` 强制断 + 算 padding，详见 references/typographic-rhythm.md §3.5）
- ❌ **发明 / 删减 / 拼接用户原文**（v0.5 新增 · 所有正文必须来自用户文案或用户明确确认）

**断行 + 字号降级**（v0.5 新增 · 写屏前必走）：
1. 数总字数 → 查 typographic-rhythm §3.1 字号上限表
2. 选 class + 算几行排
3. 算实际内容宽（**屏宽 790px - padding × 2**）
4. 单行可容字数 ≤ 实际宽度
5. 写 `<br>` 强制断行（**不让浏览器自动断**）
6. 验证 typographic-rhythm §3.2 全部 5 条规则（重头在上 / **每行 ≥ 3 字（无孤儿，含末行）** / 标点同行 / 中英不断 / em 不孤立）
7. **如果标题太长，给用户两套字号方案**（A 戏剧 / B 保险），**不擅自动**

### 铁律 R7 · 屏间不可穿插文字（v0.3）
> "每一瓶之间还不能有穿插文字"

**屏边界铁律**：
- 每屏 940px 固定，屏与屏之间有 `.border-top: 1px solid var(--line)` 边界
- 屏 A 的任何元素（文字、图片、装饰）**严禁跨越边界**进入屏 B
- 屏 A 的 `.mod-body` / `.mod-img` 内容**严禁溢出** 940px 高度

**自检**：
- [ ] 浏览器 DevTools 检查 12 个 `.mod` 的高度都是 940px（误差 ±0）
- [ ] 滚动时无任何文字/图片跨越屏边界

### 铁律 R8 · 屏间不可堆叠（v0.3 · "一瓶一瓶"陈列 · v0.5 升级 3 态背景）
> "每一瓶之间必须是相当于一瓶一瓶的"

**视觉独立性铁律**：
- 每屏在视觉上**完全独立**——像货架上一瓶一瓶的化妆品
- 屏 A 与屏 B 之间有**清晰的视觉分隔**（不是空白，是有意识的设计分隔）

**具体做法**（v0.5 升级）：
- 屏与屏之间保持 `border-top: 1px solid var(--line)` 描边（保留 W5 v1）
- 描边颜色用 `--line`（柔和，不刺眼）
- **屏内 3 态背景交替**（v0.5 新增）：`.dp2-section-soft`（`--bg-soft` 浅米）/ `.dp2-section-card`（`--card-bg` 暖白）/ `.dp2-section-dark`（`--text-main` 深棕反转）
- 3 态比 2 态多一个"重音位"——每隔 3-4 屏可用 1 次 `.dp2-section-dark` 作"重音屏"
- **禁止用大幅留白代替描边**（会让屏间"糊在一起"）
- **禁止屏 A 的背景色延展到屏 B**

**反面示例**（禁止）：
- ❌ 屏 A 用大色块延伸到屏 B（破坏独立性）
- ❌ 屏 A 的留白让屏 B"飘起来"（缺乏锚定）
- ❌ 屏 A 和屏 B 共享同一种背景色 + 无描边（视觉上糊在一起）

**正面示例**（推荐）：
- ✅ 屏 A 暖砂米底 + 屏 B 浅米底（`--bg` / `--bg-soft` 交替）+ 描边
- ✅ 屏 A 浅色 + 屏 B 深色（用 `--text-main` 反转 bg）
- ✅ 屏 A 图文 + 屏 B 纯文字（节奏变化）

---

## 三、整体架构（What）

### 3.1 目录结构

```
skills/工作效率类/W5-图片设计/详情页htmlv2/
├── SKILL.md              ← 入口（描述、路由、8 步流程）
├── PRD.md                ← 本文件
├── template.html         ← 12 屏骨架（含默认 :root · 无任何动效）
├── tokens/               ← 主题文件
│   ├── theme-pilgrim-dawn.css   ← 朝圣黎明（默认）
│   ├── theme-rose-mineral.css   ← 玫瑰矿泉
│   └── theme-dusk-capsule.css   ← 黄昏胶囊
├── recipes/              ← 风格配方（来自 W8 claud）
│   ├── INDEX.md
│   ├── editorial-warm.md ← 编辑出版型（Fraunces+Inter Tight, 35+女性）
│   ├── modern-saas.md
│   └── minimalist-pro.md
├── references/
│   ├── content-grid.md       ← 内容栅格 / 留白 / 字号阶梯
│   ├── typographic-rhythm.md ← 排版节奏（v0.3 新增 · 940px 内如何好看）
│   └── self-check.md
├── scripts/
│   └── space-budget-calc.cjs ← 空间预算计算器
└── examples/
    └── hkh-time-capsule/
        ├── index.html
        ├── assets/brand/
        └── brand-spec.md
```

### 3.1.1 Class 命名空间规范（v0.5 · v1 第一刀）

**总则**：本 skill 落地 **50 个 class**（v0.4 38 个 + v0.5 新增 10 个 `dp2-` 组件 + v0.5.3 新增 2 个 `dp2-wrap-block` / `__line`），BEM 命名 + 命名空间隔离。**未来加主题 / 加新组件** 时按此规范。

#### 50 个 class 分组（v0.5.3）

| 分组 | 数量 | 命名 | 用途 |
|---|---|---|---|
| **主结构**（永久不动） | 4 | `.mod` `.mod-auto` `.mod-top-c` `.mod-body` | 940px 屏骨架，永久固定 |
| **屏修饰** | 3 | `.mod--alt-bg` `.mod--dark-bg` `.mod--hero` | BEM 修饰符，挂在 `.mod` 上 |
| **图片** | 5 | `.mod-img` `.mod-img--hero` `.frame-img` `.img-fluid` `.img-fluid--bg` | 主图 / 局部图 / 占位 |
| **字号** | 7 | `.display-xxl` `.display-xl` `.display-lg` `.h1-sm` `.deco-en` `.body` `.meta` | 戏剧性 + 基础 |
| **文字强调** | 3 | `.lead` `.lead--gold` `.kicker` | 副标 / 重音 / 上标 |
| **装饰** | 6 | `.num` `.quote` `.rule` `.deco-line` `.icon-circle` `.icon-circle--negative` | 数据 / 引用 / 装饰 |
| **布局** | 11 | `.stack` `.gap-1`~`.gap-5` `.grid-3` `.grid-3-item` `.grid-2x2` `.grid-2x2-item` `.page-flex-2` | flex / grid 工具 |
| **组件** | 7 | `.callout-box` `.tag-item` `.tag-wrap` `.ledger` `.ledger-row` `.ledger-label` `.ledger-value` | 高阶组件 |
| **对齐** | 2 | `.text-left` `.text-center` | 文字对齐修饰 |
| **`dp2-` 组件**（v0.5 新增） | **10** | 见下表 | V3 巧思收编 |
| **合计** | **50** | | （v0.4 38 类 39 个 + v0.5 新增 10 个 + v0.5.3 新增 2 个 = 51 个 class，50 类） |

#### v0.5 新增 10 个 `dp2-` 组件（v1 第一刀 · 全局最优解版）

> **设计原则**：v1 第一刀只加 10 个**最小组件 class**，**不展开 BEM 子元素修饰符**。子元素用 CSS 子代/属性选择器约束样式，**严格控制 class 膨胀**。后续 v2 按需展开。

| # | class | 用途 | 对应 V3 巧思 | 内部结构（CSS 选择器约束） |
|---|---|---|---|---|
| 1 | `.dp2-list-row` | 横向列表卡（数字+文字 一行一项）| 4 大功效 `.miracle-item` | `> *:first-child` 数字 / `> small` 标签 / `> h3` 标题 / `> p` 描述 |
| 2 | `.dp2-step-flow` | 1D/2D/3D 三节点流程容器 | 3D 抗毛躁 `.dim-flow` | 子节点 `.dp2-step-node`（见 #2b）|
| 2b | `.dp2-step-node` | 单个节点（含 step/title/desc）| 3D 抗毛躁 `.dim-node` | `> *:first-child` 步骤 / `> .h1-sm` 标题 / `> p` 描述 |
| 3 | `.dp2-card-compare` | border-top 颜色对比双卡容器 | 双蛋白 `.tech-vs` | `> *:first-child` 卡片 1 / `> *:last-child` 卡片 2 |
| 4 | `.dp2-card-overlap` | 重叠卡片（46%/58% 错位）容器 | 为什么选 `.compare-board` | `> .dp2-card-overlap__card--them` / `--us` |
| 5 | `.dp2-data-strip` | 深棕底浅金数据条 | 99% 数据条 `.stats-bar` | `> .dp2-data-strip__item` / `> .dp2-data-strip__sep` |
| 6 | `.dp2-feature-orb` | 顶部小圆 + 下方白卡 | 6 大植萃 `.extract` | `> .dp2-feature-orb__circle` / 子元按位置 |
| 7 | `.dp2-mock` | 统一占位图规范 | 统一 `.ph` | 4 个修饰符 `.dp2-mock--hero/wide/square/portrait` + `.dp2-mock__label` |
| 8 | `.dp2-section-soft` | 屏内 3 态背景段（浅米）| V3 `.section--soft` | 挂在 `.mod-body` 内子 div |
| 9 | `.dp2-section-card` | 屏内 3 态背景段（暖白）| V3 `.section--card` | 挂在 `.mod-body` 内子 div |
| 10 | `.dp2-section-dark` | 屏内 3 态背景段（深棕）| V3 `.section--dark` | 挂在 `.mod-body` 内子 div |

#### BEM 修饰符清单（v0.5 · 7 个 → 11 个）

```
v0.4 原 7 个（保留不动）：
.mod--alt-bg           ← 原 .alt-bg（屏间背景交替）
.mod--dark-bg          ← 原 .dark-bg（深色屏）
.mod--hero             ← 原 .page-hero（首屏去上边框）
.mod-img--hero         ← 原 .page-hero-img（首屏主图撑满）
.img-fluid--bg         ← 新增（img-fluid 封面背景变体）
.lead--gold            ← 原 .lead.gold（强调金）
.icon-circle--negative ← 原 .icon-circle.is-negative（负面/痛点灰）

v0.5 新增 4 个（`dp2-` 组件修饰符）：
.dp2-mock--hero        ← mock 16/11 比例变体
.dp2-mock--wide        ← mock 16/9 比例变体
.dp2-mock--square      ← mock 1/1 比例变体
.dp2-mock--portrait    ← mock 3/4 比例变体

总：11 个 BEM 修饰符（v1 第一刀接受此数，v2 不再加新修饰符）
```

#### 命名空间规则

| 规则 | 适用范围 | 示例 |
|---|---|---|
| 主结构（`.mod*`） | **永远不改** | 新主题不改 class 名 |
| 字号 / 排版 | 主结构内可改值，不改 class | 换主题只改 tokens 的 `:root` |
| 装饰 / 布局 | 跨主题可复用 | 男性风 / 科技风共用 |
| **v0.5 新组件** | **`.dp2-` 前缀** | `.dp2-list-row` `.dp2-mock` |
| **未来新组件** | **继续用 `.dp2-` 前缀** | `.dp2-accordion` `.dp2-tab` `.dp2-banner` |

#### 与 W5 v1 / W8 claud / V3 的关系

| 来源 | 关系 |
|---|---|
| W5 v1 的 `.mod .mod-body .frame-img .ledger` 等 | **继承**（不重命名） |
| W5 v1 的 `.alt-bg .dark-bg .page-hero` 等 | **改 BEM**（`.mod--alt-bg` 等） |
| W8 claud 的类 | **不引入**（claud 没有 `.mod` 系统） |
| **V3 的巧思 class**（`.miracle-item` `.dim-flow` 等）| **改 `dp2-` 前缀收编**（不直接复用，避免 50+ 个新 class 污染）|
| 本项目独有 | 用 `dp2-` 前缀命名 |

**自检护栏**：
- 加新 class 必须有注释标明所属分组
- 旧名残留 grep 0 命中（h-sub / page-hero / alt-bg / dark-bg / is-negative / lead gold / zero-add-layout / list-item-arc）
- BEM `--` 修饰符数量 ≤ 12（v0.5.3 接受 12 个，v2 严格不再加）
- v0.4 → v0.5 class 总数变化：38 类 39 个 → **48 类 49 个**（+10 个 `dp2-` 组件）
- v0.5 → v0.5.3 class 总数变化：48 类 49 个 → **50 类 51 个**（+2 个 `dp2-wrap-block` / `__line`）
- v0.5 → v0.5.3 BEM 修饰符变化：11 个 → **12 个**（+1 个 `.dp2-wrap-block--reversed`）

#### v0.5.3 新增 2 个 `dp2-` 组件（模板 8 · 非对称图文环绕）

| # | class | 用途 | 对应 V3 违规 class | 内部结构（CSS 子代约束） |
|---|---|---|---|---|
| 1 | `.dp2-wrap-block` | 非对称图文环绕容器（图 1 列 + 文 1.2 列）| `.zero-add-layout` `.product-hero-left/right` | `> figure` 图 / `> div` 文（`.dp2-wrap-block--reversed` 时 `figure { order: 2 }`）|
| 2 | `.dp2-wrap-block__line` | 错落行（数字 + 标签 + 描述）| `.list-item-arc`（"弧度"本质是行不等高，**不是** border-radius）| `> .dp2-wrap-block__num` 数字 / `> small` 标签 / `> p` 描述 |

**v0.5.3 新增 1 个 BEM 修饰符**：

```
.dp2-wrap-block--reversed  ← 图右文左（默认图左文右）
```

**总 BEM 修饰符数变化**：11 → **12**（v0.5.3 接受此数，v2 严格不再加）

### 3.2 输入 / 输出

**输入**：
- 原始产品文案（中英文）
- 品牌 spec（来自 `.brand-spec.md` 或自动跑 W8 claud Step 0 抓取）
- 目标屏数（默认 12，可 6/9/12/15）
- 风格偏好（`朝圣黎明` / `玫瑰矿泉` / `黄昏胶囊` / 自定义）
- 真实资产路径（可选）

**输出**：
- `<项目名>/index.html`（单文件 HTML，**无动效**）
- `<项目名>/tokens/<主题>.css`
- `<项目名>/brand-spec.md`
- `<项目名>/self-check-report.md`

### 3.3 与 W5 v1 的核心差异（v0.4 更新）

| 维度 | W5 v1 | 详情页 HTML2 v0.4 |
|---|---|---|
| 美学 | 印刷品 · 杂志内页 | **claud 排版美感 · 静态** |
| 排版美感 | 中规中矩 | **核心目标**（R5） |
| 标题位置 | 屏顶（隐含） | **强制屏顶居中**（R6 · 新增铁律） |
| 屏间独立性 | 仅描边 | **描边 + 背景交替**（R8 · 新增） |
| 屏间穿插 | 不强制 | **明确禁止**（R7 · 新增） |
| 动效 | 无 | 无（明确禁止） |
| Tweaks | 无 | 无（明确禁止） |
| 字体 | Noto Serif SC + Noto Sans SC | Fraunces + Inter Tight |
| 配色 | luxe-warm 香槟金（固定） | 3 套品牌主题可换 |
| 4 维定位 | 无 | 强制每屏先答 4 问再写 |
| 字号阶梯 | h1/h1-sm/h2 (44/36/32) | 新增 display-xxl/xl/lg（48-96/40-64/32-48） |
| **class 命名** | 自由命名 | **38 个 BEM 命名定稿**（v0.4） |
| **命名空间** | 无 | **未来新组件用 `dp2-` 前缀**（v0.4） |

---

## 四、工作流（8 步 · 仿 claud 改造 · 无动效 · 排版美感优先）

> 每一步都有**目标检测点**（必须满足才能进下一步）。v0.3 新增 4 个 R5/R6/R7/R8 排版美感护栏。

---

### Step 0 · 验真（Step 0 from W8 claud）

**目标**：在动手前确定品牌真实性，绝不假数据

**步骤**：
1. 用户给出产品/品牌名 → WebSearch 抓官网
2. 提取：定位、产品名、文案、配色倾向、字体倾向、Logo/产品图
3. 生成 `<项目名>/brand-spec.md`
4. 抓取真实图片到 `<项目名>/assets/brand/`

**目标检测点**：
- [ ] brand-spec.md 存在且不为空
- [ ] 至少 1 张真实资产已下载
- [ ] 至少 3 段真实文案已记录

---

### Step 1 · 复制模板 + 选主题

**步骤**：
1. `cp template.html <项目名>/index.html`
2. `cp tokens/theme-pilgrim-dawn.css <项目名>/tokens/`
3. 改 `<link rel="stylesheet" href="">` 为对应主题
4. 改 `<title>` 为「产品名 · 品牌主张」

**主题选择**：
- `朝圣黎明`（pilgrim-dawn）— 暖砂米 + 岩蔷薇粉 + 圣地亚哥金
- `玫瑰矿泉`（rose-mineral）— 冷白 + 灰玫瑰 + 苔藓绿
- `黄昏胶囊`（dusk-capsule）— 奶油 + 焦糖 + 琥珀金

**目标检测点**：
- [ ] `<项目名>/index.html` 已创建
- [ ] `<项目名>/tokens/` 至少 1 个 .css
- [ ] `<link href="...">` 已修改
- [ ] `<title>` 已修改

**禁止**：自己写 `<style>` 块

---

### Step 2 · 4 维定位问题（仿 W8 claud Step 3a）

**目标**：每屏的"为什么"必须在写之前定下来

每屏写之前回答：
1. **叙事角色**：Hero / 过渡 / 数据 / pull-quote / 收尾？
2. **观看距离**：手机 30cm / 笔记本 1m / 投影 10m？
3. **视觉温度**：quiet / energized / authoritative / warm？
4. **容量检查**：内容是否装得下 940px？

**目标检测点**：
- [ ] 12 屏每屏都有 4 个问题答案
- [ ] 至少 1 屏是 Hero、至少 1 屏是 pull-quote、至少 1 屏是数据、至少 1 屏是收尾

---

### Step 3 · 选排版模板（继承 W5 v1 + 新增 2 类）

**原有 7 类**（保留）：对比 / 平行列表 / 标签+说明 / 大主张 / 标签集合 / 特殊卡片 / 正文陈述

**新增 2 类**（claud 风格，**无动效**）：
- **Hero 海报**：kicker + 英文装饰 h-sub + h1-sm + body + 3 标签 + 底部主图（mod-img 撑满）
- **Pull-quote 大主张**：h1-sm（≤14 字）+ pullquote italic 32px + body + 主图

**最小内容量**（不够就降级）：
- 标签+说明：≥4 对
- 平行列表：2/3/4 项
- 大主张：≥1 个
- 标签集合：≥4 个
- 特殊卡片：≥1 段

**目标检测点**：
- [ ] 12 屏每屏都标注了排版模板
- [ ] 至少 1 屏是新增的 claud 风格屏

---

### Step 4 · 空间预算（先算后写） · v0.3 升级

**目标**：每屏 ≥75% 填充率，**禁止写完再改**

**新增 R6 强制规则**（v0.3）：
- 标题区（mod-top-c）固定 80px 起始 + 主标 + 副标 + body
- 自由排版区 = 940 - 标题区 - body padding - mod-img
- 标题区不可压缩，不可被自由区侵占

**预算表样例**：
```
【空间预算】屏 01（R6 强制）
├── 标题区（固定·屏顶居中）
│   ├── padding-top 80px
│   ├── h1-sm 36px
│   ├── h-sub 20px
│   ├── deco-line 25px
│   ├── body 50px
│   └── 小计 ≈ 211px
├── 自由排版区（可变）
│   ├── mod-body padding 72px
│   ├── 内容（标签 3 个）≈ 50px
│   └── 小计 ≈ 122px
├── 底部 mod-img（撑满）≈ 607px
└── 合计 ≈ 940px ✅
```

**目标检测点**：
- [ ] 12 屏每屏都有预算计算
- [ ] 全部 ≥75%
- [ ] 标题区不被自由区侵占

---

### Step 5 · 文字 class 分配（继承 W5 v1 + 新增 claud 字号阶梯）

**新增字号阶梯**：

| class | 字号 | 字体 | 用途 |
|---|---|---|---|
| `display-xxl` | clamp(48, 8vw, 96) | Fraunces | Hero 主屏（仅屏 1） |
| `display-xl` | clamp(40, 5.5vw, 64) | Fraunces | 屏 2-3 大标题 |
| `display-lg` | clamp(32, 4vw, 48) | Fraunces | 屏 4-12 子标题 |
| `h1-sm` | 36px | Noto Serif SC | 屏内主标题 |
| `lead` | 16px | Noto Sans SC | 副标 / 卖点 |
| `body` | 14px | Noto Sans SC | 正文 |
| `meta` | 12px | Noto Sans SC | 脚注 |

**R6 强制**：display-* / h1-sm 一律在屏顶居中，**不可下移**

**目标检测点**：
- [ ] 同屏内 h1/h2/display 是最大/最重的文字
- [ ] 字体严格隔离（Serif = 展示 / Sans = 功能）
- [ ] 字号差距 ≥ 2.5x

---

### Step 6 · 配图规划（继承 W5 v1 + claud 真实资产优先）

**优先级**：
1. **真实资产** → `<img src="assets/brand/xxx.jpg">`
2. **诚实占位** → `.img-fluid` + 描述性占位词
3. **AI 假图** → ❌ 禁止

**容器**：
- 主图（屏底）→ `.mod-img`（撑满）
- 局部图 → `.frame-img r-{4x3|16x9|1x1}`
- 占位 → `.img-fluid`

**R7 强制**：所有图片必须完整在 940px 内，**严禁跨越屏边界**

**目标检测点**：
- [ ] 真实资产优先
- [ ] 描述性占位词
- [ ] 所有 `<img>` 有 `alt` 属性
- [ ] **无图片跨越屏边界**（R7）

---

### Step 7 · 排版美感收口（v0.3 重写 · 替代原动效章）

**目标**：在 940px 固定高度内做出 claud 级别设计感

**三大支点**（替代 v0.2 的差异化支点）：

#### 7.1 排版节奏（核心）
> "如何在 940 像素高以内排版要好看"

- **字号阶梯**：同屏内字号对比 ≥ 2.5x（h1-sm 36px vs body 14px）
- **留白比例**：标题区与自由区之间保留 40px 节奏留白
- **衬线小细节**：Fraunces 启用 `font-variation-settings: "opsz" 144, "SOFT" 80-100` 让衬线柔化
- **数字陈列**：核心数据用 Playfair Display 斜体或大字号 Sans Mono 居中
- **网格**：12 栏 / 24px 间距（保留 W5 v1 grid-3 / grid-2x2）

**claud 美感公式**（v0.3 沉淀）：
```
美感 = 字号对比 × 留白节奏 × 衬线细节 × 真实质感 × 屏间独立性
```

#### 7.2 配色支点
- 主色 / 辅色 / 强调色严格 3 色
- 灰度 6 级派生
- 主题文件只覆盖 `:root` 颜色变量

#### 7.3 真实资产支点
- 每屏至少 1 张真实图
- 描述性占位词
- Logo 必须真实

#### 7.4 屏间独立性（v0.3 · R8 强制）
- 屏 A 与屏 B 背景色交替（`--bg` / `--bg-soft` / 偶尔用 `--text-main` 反转）
- 屏间保留 1px 描边（`border-top: 1px solid var(--line)`）
- **禁止用大幅留白代替描边**
- **禁止屏 A 背景色延展到屏 B**
- **禁止屏 A / 屏 B 视觉堆叠**（即"糊在一起"）

**目标检测点**：
- [ ] 12 屏字号对比 ≥ 2.5x
- [ ] 12 屏有节奏留白（不挤压也不空洞）
- [ ] Fraunces 启用 `font-variation-settings`
- [ ] 屏间背景色有变化（不全用同一种 bg）
- [ ] 屏间有清晰描边分隔（R8）
- [ ] 真实资产 ≥ 3 张被引用

---

### Step 8 · 自检（v0.3 · 23 项）

**8 项基础自检**（与 W5 v1 一致）：
- [ ] 1. Serif/Sans 字体隔离
- [ ] 2. 颜色层级（main / muted / meta）
- [ ] 3. h2 是同屏最大文字
- [ ] 4. 无多余 inline style（仅对比方改色允许）
- [ ] 5. 填充率 ≥75%（或 .mod-auto）
- [ ] 6. 图片容器用对
- [ ] 7. 装饰有功能目的
- [ ] 8. 无假数据 / Emoji / 缩字号

**5 项风格身份测试**：
- [ ] 1. 展示用 Serif，功能用 Sans
- [ ] 2. h2 是同屏最大/最重
- [ ] 3. 装饰有功能目的
- [ ] 4. 填充率 ≥75%（或 .mod-auto）
- [ ] 5. 无 inline style（对比方例外）

**4 项 R4 静态优先护栏**：
- [ ] R4-1 模板 CSS 中无 transition（除 color/background 微调）
- [ ] R4-2 模板 CSS 中无 animation
- [ ] R4-3 模板 JS 中无 IntersectionObserver / scroll / setTimeout 动效
- [ ] R4-4 页面无 Tweaks 面板

**6 项 R5/R6/R7/R8 排版美感护栏**（v0.3 新增）：
- [ ] R5-1 **940px 内每屏有设计意图**（Dribbble 评分 ≥8 自评）
- [ ] R5-2 **字号对比 ≥ 2.5x**（同屏内 display/h1 vs body）
- [ ] R5-3 **衬线启用 `font-variation-settings`**（Fraunces SOFT 80-100）
- [ ] R6-1 **主副标在屏顶居中**（DevTools 验证 padding-top 80px）
- [ ] R7-1 **无文字/图片跨越屏边界**（DevTools 检查 12 个 .mod 高度）
- [ ] R8-1 **屏间有清晰描边分隔 + 背景色有变化**（不全用同一种 bg）

**目标检测点**：
- [ ] 8 + 5 + 4 + 6 = 23 项全部 PASS

---

### Step 9 · 输出 + 范例沉淀

**输出**：
- `<项目名>/index.html`
- `<项目名>/tokens/`（主题）
- `<项目名>/brand-spec.md`
- `<项目名>/assets/brand/`
- `<项目名>/self-check-report.md`（23 项）

**可选导出**：
- `node scripts/html-to-png.cjs <项目名> --split` → 12 张 PNG
- `node scripts/html-to-png.cjs <项目名>` → 1 张长图

**范例沉淀**：
- 跑完的项目复制到 `examples/<品牌名>/`

---

## 五、风险与开放问题（Risks & Open Questions）

| # | 问题 | 建议 |
|---|---|---|
| 1 | 940px 固定内做出"claud 级美感"难度高 | 学习目标定在 Dribbble 8 分而非 9 分；提供 **typographic-rhythm.md** 参考 |
| 2 | R6 标题固定在屏顶，限制了排版自由度 | 自由区够大（≥ 500px），仍可做卡片/网格/对比列 |
| 3 | R7/R8 屏间独立性会让 12 屏整体感弱化 | 用 **配色 / 字体 / 真实资产** 三件套维系整体感（与 claud 一致） |
| 4 | R8 背景色交替会不会让屏 A/B 突兀 | 用 `--bg` / `--bg-soft` 微差（视觉连贯），偶尔用 1 屏 `--text-main` 反转做"重音" |
| 5 | 无动效下"claud 美感"打折扣 | 不打折扣——claud 的核心不是动效，是 **4 维定位 + 真实资产 + 衬线小细节 + 留白节奏** |
| 6 | 静态页面无 Tweaks，用户怎么调样式 | 编辑 `tokens/<主题>.css` 改 `:root` 变量（与 W5 v1 一致） |
| 7 | 与 W5 v1 长期共存还是替代 | 建议共存——v1 适合纯结构合规，v2 适合品牌叙事 |

---

## 六、验收标准（Acceptance Criteria · v0.3）

- [ ] 用户给任意品牌 + 文案，能在 30 分钟内出 12 屏详情页
- [ ] 12 屏**排版美感** ≥ 8/10（Dribbble 自评）
- [ ] 自检 23 项（8 + 5 + 4 + 6）100% 通过
- [ ] 真实资产优先，无 AI 假图
- [ ] 0 动效（grep 验证）
- [ ] 0 Tweaks 面板
- [ ] **R6 主副标在屏顶居中**（DevTools 验证 12 屏）
- [ ] **R7 屏间无文字/图片穿插**（DevTools 验证 12 屏）
- [ ] **R8 屏间有描边分隔 + 背景色交替**（DevTools 验证 12 屏）
- [ ] 至少 1 个完整范例（HKH Time Capsule）已落地

---

## 七、PRD 检查清单

- [x] 1. **目标**（Why）
- [x] 2. **铁律**（R1-R8）— 含 v0.3 新增 R5/R6/R7/R8
- [x] 3. **架构**（What）
- [x] 4. **工作流**（How）— 8 步
- [x] 5. **风险与开放问题**（Risks）
- [x] 6. **验收标准**（Acceptance · 23 项）
- [ ] 7. **优先级 / 排期**（待用户敲定）
- [ ] 8. **成功指标**（待用户敲定）

---

## 八、版本变更记录

| 版本 | 变更 |
|---|---|
| v0.1 | 初稿：9 步流程 + 13 项自检，含动效章 |
| v0.2 | 删动效 + 新增 R4 静态优先：8 步 + 17 项自检（8+5+4） |
| v0.3 | **新增 4 铁律 R5/R6/R7/R8**：8 步 + 23 项自检（8+5+4+6）<br>核心目标更新："在 940px 固定内做出 claud 级排版美感"<br>Step 7 重写为"排版美感收口"<br>差异化支点新增"排版节奏"为第一支点<br>claud 美感公式：美感 = 字号对比 × 留白节奏 × 衬线细节 × 真实质感 × 屏间独立性 |
| **v0.4** | **38 个 class BEM 命名定稿**：新增 §3.1.1 "Class 命名空间规范"<br>重命名 4 个（.h-sub→.deco-en, .alt-bg→.mod--alt-bg, .dark-bg→.mod--dark-bg, .page-hero→.mod--hero, .page-hero-img→.mod-img--hero, .is-negative→.icon-circle--negative, .lead.gold→.lead--gold）<br>新增 1 个（.text-left）<br>未来新组件用 **`dp2-` 前缀**（如 .dp2-accordion）<br>Day 1 验证屏 1 通过 R5-1 自评（节奏统一 24 倍数） |

---

## 九、下一步

1. **PRD 评审**：v0.4 是否通过？哪条要改/加/删？
2. **优先级敲定**：哪些 Step 必须 v1 就有
3. **进入实施**：建 `skills/工作效率类/W5-图片设计/详情页htmlv2/` 目录，按 8 步落地
4. **跑通 HKH 范例**：用本 PRD 重写 HKH Time Capsule 12 屏

---

> **本 PRD 已完整可执行。等待你评审。**
