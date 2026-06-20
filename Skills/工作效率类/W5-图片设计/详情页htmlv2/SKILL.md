---
name: 详情页 HTML 2
description: 仿 claud 美学的工程化详情页生成器。在 940px 固定高度的 12 屏画布内做出 claud 级排版美感。Use when user wants to generate a 12-screen product detail page with brand-specific design and zero animation.
metadata:
  pattern: generator
  version: v0.5.4.1
---

# 详情页 HTML 2（v0.5 · v1 skill 化版）

> **状态**：v1 完整版
> **配套文档**：[`PRD.md`](./PRD.md) / [`template.html`](./template.html) / [`references/`](./references/)
> **设计哲学**：在 940px 固定画布内做出 claud 级排版美感。**无动效 · 无 Tweaks · 静态优先**。

---

## 1. 何时触发

**适用场景**（任一满足即触发）：
- 用户给出产品/品牌 + 文案 + 真实资产，要出 12 屏详情页
- 用户要做"高奢向单页详情"，但不要整页滚动叙事（用 W8 claud）
- 用户对结构合规有要求（38 → 48 BEM 命名 + R4 静态优先）

**不适用**：
- 整页滚动落地页 → 用 W8 claud
- 纯结构合规（无设计感要求）→ 用 W5 v1

---

## 2. 8 步流程（每步带目标检测点 + 强制分批输出）

> **v0.5.2 强化 · 强制分批**：LLM 在长上下文中**极易遗忘 BEM 命名 / 排版铁律**。本流程设置**硬性 checkpoint**，AI 必须分批输出，**未经用户确认不得继续**。

| 批次 | 步骤 | 名称 | 输出 | 目标检测点 |
|---|---|---|---|---|
| **A · 规划批** | 0 | 验真 · 抓官网 | `brand-spec.md` + `assets/brand/*` | brand-spec.md 非空 + ≥ 1 张真实资产 + ≥ 3 段真实文案 |
| **A · 规划批** | 1 | 复制模板 + 选主题 | `<项目名>/index.html` + `tokens/<主题>.css` | `<link href="...">` 已修改 + `<title>` 已修改 + tokens 至少 1 个 .css |
| **A · 规划批** | 2 | 4 维定位 | 每屏 4 问答案 | 12 屏每屏都有 4 问答案 + 至少 1 屏 Hero / 1 屏 pull-quote / 1 屏数据 / 1 屏收尾 |
| **A · 规划批** | 3 | 选排版模板 | 排版模板标注 | 12 屏每屏都标注模板 + 至少 1 屏用 v0.5 新增 `dp2-` 组件 |
| **A · 规划批** | 4 | 空间预算 | 预算表 | 12 屏每屏有预算计算 + 全部 ≥ 75% + 标题区不被自由区侵占 |
| ⏸️ **【硬性 checkpoint 1】** | — | 用户确认 A 批 | — | **AI 停下，等待用户回"继续"** |
| **B · 生成批** | 5 | 文字 class 分配 | class 标注 | h1/h2/display 是同屏最大/最重 + 字体严格隔离（Serif 展示 / Sans 功能） + 字号差距 ≥ 2.5x |
| **B · 生成批** | 6 | 配图规划 | `<img src="...">` 标注 | 真实资产优先 + 描述性占位词 + 所有 `<img>` 有 `alt` + 无图片跨越屏边界（R7）|
| **B · 生成批** | 7 | 排版美感收口 | 美感公式验证 | 12 屏字号对比 ≥ 2.5x + 有节奏留白 + Fraunces `font-variation-settings` 启用 + 屏间 3 态背景交替（R8 v0.5）|
| ⏸️ **【硬性 checkpoint 2】** | — | 用户回看 B 批前 3 屏 | — | **AI 停下，输出前 3 屏 + 等用户回"OK 继续"** |
| **C · 收口批** | 8 | 自检 23 项 + 9 项自动化 | `self-check-report.md` + 跑 `scripts/dp2-self-check.cjs` | 8 基础 + 5 风格 + 4 R4 静态 + 6 R5-R8 排版 = **23 项全 PASS** + 脚本 9/9 PASS |

**批次纪律**：
- ❌ **AI 禁止跳过 checkpoint 一次性输出 12 屏**（即便用户给"BC / 继续"）
- ✅ **A 批（步骤 0-4）必须**先单独输出，等用户回"继续 / OK / BC"
- ✅ **B 批（步骤 5-7）前 3 屏先输出**等用户回看，后 9 屏再继续
- ✅ **C 批（步骤 8）跑自动化脚本**输出 self-check-report.md
- 例外：**用户**主动说"一次性出完" → 才允许跳过 checkpoint

---

## 3. 8 条铁律（不可变 · v0.5）

| 编号 | 铁律 | 来源 | v0.5 变化 |
|---|---|---|---|
| R1 | 每屏必须有文字（主标 + 副标 + 至少 1 段 body / lead）| 用户原话 | 不变 |
| R2 | 每屏 940px 固定（超 → `.mod-auto`）| 用户原话 | 不变 |
| R3 | 排版可改，铁律不改 | — | 不变 |
| R4 | 静态优先（无 transition / animation / Tweaks）| v0.2 | 不变 |
| R5 | 排版美感优先（Dribbble ≥8）| v0.3 | 不变 |
| R6 | 主副标屏顶居中 | v0.3 | 不变 |
| R7 | 屏间不可穿插文字/图片 | v0.3 | 不变 |
| R8 | 屏间不可堆叠（背景交替 + 描边）| v0.3 | **v0.5 升级 3 态背景**（`.dp2-section-soft/card/dark`）|

---

## 4. 主题选择（启动时手动 · 无 Tweaks）

编辑 `index.html` 的 `<link>` 标签：

```html
<!-- 朝圣黎明（默认 · 35+女性护肤） -->
<link rel="stylesheet" href="tokens/theme-pilgrim-dawn.css">

<!-- 玫瑰矿泉（冷感编辑） -->
<link rel="stylesheet" href="tokens/theme-rose-mineral.css">

<!-- 黄昏胶囊（暖感奢华） -->
<link rel="stylesheet" href="tokens/theme-dusk-capsule.css">
```

未来扩展：男性风 / 科技风 / 编辑出版 / 现代工具 SaaS（5 项配置：颜色 + 字体 + 间距 + 圆角 + 留白节奏）。

---

## 5. 48 个 BEM 命名空间（v0.5 · PRD §3.1.1）

**主结构（4）**：`.mod` `.mod-auto` `.mod-top-c` `.mod-body`
**屏修饰（3）**：`.mod--alt-bg` `.mod--dark-bg` `.mod--hero`
**图片（5）**：`.mod-img` `.mod-img--hero` `.frame-img` `.img-fluid` `.img-fluid--bg`
**字号（7）**：`.display-xxl` `.display-xl` `.display-lg` `.h1-sm` `.deco-en` `.body` `.meta`
**文字强调（3）**：`.lead` `.lead--gold` `.kicker`
**装饰（6）**：`.num` `.quote` `.rule` `.deco-line` `.icon-circle` `.icon-circle--negative`
**布局（11）**：`.stack` `.gap-1`~`.gap-5` `.grid-3` `.grid-3-item` `.grid-2x2` `.grid-2x2-item` `.page-flex-2`
**组件（7）**：`.callout-box` `.tag-item` `.tag-wrap` `.ledger` `.ledger-row` `.ledger-label` `.ledger-value`
**对齐（2）**：`.text-left` `.text-center`
**`dp2-` 组件（10 · v0.5 新增）**：
- `.dp2-list-row` — 横向列表卡（模板 1）
- `.dp2-step-flow` + `.dp2-step-node` — 三节点流程（模板 2）
- `.dp2-card-compare` + `__card--gold/--gray` — 颜色对比双卡（模板 3）
- `.dp2-card-overlap` + `__card--them/--us` — 重叠卡片（模板 4）
- `.dp2-data-strip` + `__item/--val/--sep` — 数据条（模板 5）
- `.dp2-feature-orb` + `__circle/--country/--name/--desc` — 顶部小圆卡（模板 6）
- `.dp2-mock` + `--hero/--wide/--square/--portrait` + `__label` — 统一占位图（模板 7）
- `.dp2-section-soft/card/dark` — 屏内 3 态背景（R8 v0.5）

**BEM 修饰符（11）**：v0.4 原 7 个 + v0.5 新增 4 个（`.dp2-mock--hero/--wide/--square/--portrait`）

详细规范：[`PRD.md` §3.1.1](./PRD.md)

---

## 6. 7 个屏布局模板（v0.5 新增 · pattern-library）

**写屏前必查** [`references/pattern-library.md`](./references/pattern-library.md)：

| # | 模板 | 适用场景 | 来源 V3 巧思 |
|---|---|---|---|
| 1 | 横向列表卡 | 4 大功效 / 4 大优势 | `.miracle-item` |
| 2 | 三节点流程 | 1D/2D/3D / 3 步仪式 | `.dim-flow` + `.dim-node` |
| 3 | 颜色对比双卡 | 双蛋白 / 普通 vs 高端 | `.tech-vs` border-top 对比 |
| 4 | 重叠卡片 | 为什么选 / us vs them | `.compare-board` 46%/58% 错位 |
| 5 | 数据条 | 99% 数据 / 临床数字 | `.stats-bar` 深棕底浅金 |
| 6 | 顶部小圆卡 | 6 大植萃 / 3 大产地 | `.extract` + `.extract__orb` |
| 7 | 统一占位图 | 所有占位图 | `.ph` + 4 比例修饰符 |

**V3 违规点的修复方向**：见 [`references/legacy-remediation.md`](./references/legacy-remediation.md)

---

## 7. 23 项自检（v0.5 · 与 PRD §Step 8 对齐）

**8 项基础自检**：
- [ ] 1. Serif/Sans 字体隔离
- [ ] 2. 颜色层级（main / muted / meta）
- [ ] 3. h2 是同屏最大文字
- [ ] 4. 无多余 inline style（仅对比方改色允许）
- [ ] 5. 填充率 ≥75%（或 `.mod-auto`）
- [ ] 6. 图片容器用对
- [ ] 7. 装饰有功能目的
- [ ] 8. 无假数据 / Emoji / 缩字号

**5 项风格身份测试**：
- [ ] 1. 展示用 Serif，功能用 Sans
- [ ] 2. h2 是同屏最大/最重
- [ ] 3. 装饰有功能目的
- [ ] 4. 填充率 ≥75%（或 `.mod-auto`）
- [ ] 5. 无 inline style（对比方例外）

**4 项 R4 静态优先护栏**：
- [ ] R4-1 模板 CSS 中无 transition（除 color/background 微调）
- [ ] R4-2 模板 CSS 中无 animation / `@keyframes`
- [ ] R4-3 模板 JS 中无 IntersectionObserver / scroll / setTimeout 动效
- [ ] R4-4 页面无 Tweaks 面板（无 `.theme-switcher` / 主题切换 JS）

**6 项 R5/R6/R7/R8 排版美感护栏**（v0.5）：
- [ ] R5-1 940px 内每屏有设计意图（Dribbble 评分 ≥8 自评）
- [ ] R5-2 字号对比 ≥ 2.5x（同屏内 display/h1 vs body）
- [ ] R5-3 衬线启用 `font-variation-settings`（Fraunces SOFT 80-100）
- [ ] R6-1 主副标在屏顶居中（DevTools 验证 padding-top 80px）
- [ ] **R6-2 无 emoji**（v0.5 新增 · grep `[\u{1F300}-\u{1FAFF}]` HTML 文件 → 0 命中，详见 references/typographic-rhythm.md §3.7）
- [ ] **R6-3 断行无孤儿字**（v0.5.1 强化 · **每一行** ≥ 3 字，含末行；强制 `<br>` 断行；详见 references/typographic-rhythm.md §3.2）
- [ ] **R6-4 标题字号给两套方案**（v0.5 新增 · 不擅自决定；详见 references/typographic-rhythm.md §3.6）
- [ ] **R6-5 正文逐字对齐用户原文**（v0.5 新增 · 不发明 / 不删减 / 不拼接）
- [ ] R7-1 无文字/图片跨越屏边界（DevTools 检查 12 个 `.mod` 高度）
- [ ] **R8-1 屏间 3 态背景交替**（`.dp2-section-soft/card/dark` v0.5 新增）
- [ ] **R9-1 格式塔间距亲密性**（v0.5.2 新增 · 组件内间距 `<` 组件间距；详见 references/content-grid.md（v0.6 待写））
- [ ] **R10-1 无 V3 违规 class 残留**（v0.5.3 新增 · grep `.zero-add-layout` `.list-item-arc` `.product-hero-left/right` `.sp` `.selling-points` 等 V3 违规 class → 0 命中；详见 references/pattern-library.md 模板 8 V3 违规对照表 + references/legacy-remediation.md）
- [ ] **R10-2 屏宽必须 790px**（v0.5.4 新增 · `.mod` 必须 `max-width: 790px`；高 940 宽 790 固定；自动化 #11 项）
- [ ] **R10-3 衬线 font-variation SOFT 80-100**（v0.5.4 新增 · R5-3 强约束；自动化 #12 项）
- [ ] **R10-4 R8-1 屏间 bg 必变**（v0.5.4 新增 · 至少 2 态或 ≥ 1 次 .dp2-section-xxx；自动化 #13 项）
- [ ] **R10-5 自由排版区 ≥ 500px**（v0.5.4 新增 · PRD 风险 §3 强约束；自动化 #14 项）
- [ ] **R10-6 R1 必含主标 + body**（v0.5.4 新增 · 每屏 display-* + class="body" + <h1> 标签；自动化 #15 项）
- [ ] **R10-7 brand-spec.md 必填 8 字段**（v0.5.4 新增 · 品牌/产品/卖点/主题/资产/Theme Bundle/断句符/原文护栏；自动化 #16 项）
- [ ] **R10-8 4 维定位完整**（v0.5.4 新增 · 目的/用户情绪/内容类型/视觉锚点；自动化 #17 项）

**v0.5.1 自动化自检脚本**（推荐 · 替代手动 9 项）：

```bash
# 跑全 9 项自动化检测
node scripts/dp2-self-check.cjs <项目目录>

# 例：node scripts/dp2-self-check.cjs examples/hkh-time-capsule/
```

**9 项检测**：
1. 无 emoji 字符（仅检测真实 emoji 区 1F000-1F1FF）
2. 无 `<br>` 后 1-2 字孤儿
3. 无 inline `transform: scale/rotate`
4. 无 `<script>` 标签
5. 无 CSS `@keyframes` / `animation`
6. 无 `.theme-switcher` 类
7. 无 V3 违规 class（sp / selling-points / miracle-item 等）
8. 无 CSS `transform: scale/rotate`
9. `.mod` 含 `min-height: 940px`

**0 FAIL 为 PASS**。脚本 + 人工 23 项 = **v0.5.1 完整自检**。

---

## 8. 目录结构（v1 落地目标）

```
skills/工作效率类/W5-图片设计/详情页htmlv2/
├── SKILL.md                ← 本文件（完整版）
├── PRD.md                  ← v0.5（38 → 48 BEM + R8 3 态升级）
├── template.html           ← 12 屏骨架（含 48 BEM 定义）
├── tokens/
│   ├── theme-pilgrim-dawn.css
│   ├── theme-rose-mineral.css
│   └── theme-dusk-capsule.css
├── recipes/
│   └── INDEX.md
├── references/
│   ├── content-grid.md        ← 栅格 / 字号 / 间距（v0.5.3 R9-1 格式塔）
│   ├── typographic-rhythm.md   ← 节奏铁律（字号 / 断行 / 字号降级决策）
│   ├── pattern-library.md      ← 8 模板（v0.5.3 +1 非对称图文环绕）
│   ├── self-check.md           ← 24 项操作清单（9 自动化 + 15 人工）
│   └── legacy-remediation.md  ← V3 违规点修复方向
├── examples/
│   └── hkh-time-capsule/       ← 范例屏 1（用 v0.5 skill 重写，屏 5 改 dp2-list-row）
└── scripts/
    ├── dp2-self-check.cjs       ← v0.5.1 自检脚本（9 项自动化检测）
    └── space-budget-calc.cjs    ← 空间预算计算器
```

---

## 9. 范例

`examples/hkh-time-capsule/` — HKH Plant Retinol Time Capsule 12 屏
- 屏 5 改用 `dp2-list-row` 横向列表卡（V3 巧思收编证明）
- 23 项自检全 PASS（屏 1-3 已验证）
- 朝圣黎明主题（默认 · 35+女性护肤）

---

## 10. 详细文档

- 完整 PRD：[`PRD.md`](./PRD.md)
- 屏布局模板（8 模板）：[`references/pattern-library.md`](./references/pattern-library.md)
- 排版节奏参考：[`references/typographic-rhythm.md`](./references/typographic-rhythm.md)
- 栅格/字号/间距系统：[`references/content-grid.md`](./references/content-grid.md)（v0.5.3 新增）
- 24 项自检操作清单：[`references/self-check.md`](./references/self-check.md)（v0.5.3 新增）
- V3 违规点修复方向：`references/legacy-remediation.md`

---

## 11. 版本记录

| 版本 | 变更 | 触发 |
|---|---|---|
| v0.1 | 9 步流程 + 13 项自检 | 初稿 |
| v0.2 | 删动效 + 新增 R4 静态优先 | v0.2 |
| v0.3 | 新增 4 铁律 R5/R6/R7/R8 | v0.3 |
| v0.4 | 38 个 class BEM 命名定稿 | v0.4 |
| **v0.5** | **48 个 BEM（+10 个 `dp2-` 组件）+ R8 3 态背景升级 + 7 模板 + V3 巧思收编 + legacy-remediation** | **v1 skill 化** |
| **v0.5.1** | **+5 项自检（emoji / 断行 / 字号方案 / 原文护栏 / R6-2~6-5）+ typographic-rhythm §3.5 padding 折算 + §3.6 字号降级决策树 + §3.7 emoji 铁律 + PRD R6 原文护栏** | **用户点出"所有正文必须来自用户原文" + "断行 + 字号降级"规则** |
| **v0.5.2** | **+断句符协议 §3.2.1 + Few-Shot §3.6.4 + 强制分批 checkpoint（§2 A/B/C 三批）+ 资产隔离铁律（pattern-library 模板 7 末尾）+ R9-1 格式塔间距自检** | **外部专家 feedback 4 个优化方向** |
| **v0.5.3** | **+模板 8 `.dp2-wrap-block` 非对称图文环绕（V3 `.zero-add-layout` 替代）+ R10-1 V3 违规 class 检测** | **用户点出"布局模板盲区"（HK v0.5 屏 5 改造痛点）** |
| **v0.5.4** | **+R10-2 屏宽必须 790px（自动化 #11 项，v0.5.3 漏护栏）** | **用户点出"宽度固定 790"** |
| **v0.5.4.1** | **+6 项 PRD 漏护栏 R10-3 ~ R10-8（自动化 #12-#17 项）** | **用户点出"PRD 还有哪些没注意到" + "影响视觉"分类** |
| **v0.5** | **48 个 BEM（+10 个 `dp2-` 组件）+ R8 3 态背景升级 + 7 模板 + V3 巧思收编 + legacy-remediation** | **v1 skill 化** |
