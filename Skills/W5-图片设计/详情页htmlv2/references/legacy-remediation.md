# V3 违规 HTML 修复方向（legacy-remediation.md · v1）

> **状态**：v1 · 基于 V3 实际代码 grep 验证
> **配套**：`../SKILL.md` / `typographic-rhythm.md` / `pattern-library.md`
> **适用范围**：未来接手 V3 / 详情页-v2/v3 / 终版 / 重构版 等老产物时，**知道哪些违反 R4 静态优先 / 38 BEM 命名 / 命名空间隔离**

---

## 本文档的定位

**不修老 HTML**（按用户决策），**只沉淀"反模式 → 修法"映射表**。让未来接手人：

1. 知道老产物的违规点（grep 验证）
2. 知道每个违规点对应 PRD v0.5 的哪条铁律
3. 知道怎么改成 v0.5 合规（用 `dp2-` 组件 + 静态优先）

**老产物的命运**：挂在 `examples/_legacy/` 作为反面参考，**不**纳入 v1 skill 的 1 屏范例。

---

## 15 条违规点（按文件 + 行号）

### 违规 1 · CSS 动效 `@keyframes oilShine`

**位置**：`levity-hair-oil-v2/index.html` CSS 第 474-477 行
**违反**：R4 静态优先
**代码**：
```css
@keyframes oilShine {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.oil-drop { animation: oilShine 4s ease-in-out infinite; }
```
**修法**：删 `@keyframes` + `animation`，`.oil-drop` 静态化。3D 抗毛躁效果用 `dp2-step-flow`（模板 2）替代动效。
**对应模板**：模板 2 三节点流程

### 违规 2 · CSS hover transform 缩放

**位置**：`levity-hair-oil-v3/index.html` CSS 第 219 行
**违反**：R4 静态优先（hover 状态仅限颜色 / 边框微调，禁止 transform）
**代码**：
```css
.theme-switcher__dot:hover { transform: scale(1.1); }
```
**修法**：删 `transform: scale(1.1)`，hover 只改 `border-color` 或 `opacity`。

### 违规 3 · JS 主题切换器

**位置**：`levity-hair-oil-v3/index.html` HTML 第 1073-1078 行 + JS 第 1637-1646 行
**违反**：R4 禁止 Tweaks 面板
**代码**：
```html
<div class="theme-switcher">
  <span class="theme-switcher__label">Theme</span>
  <span class="theme-switcher__dot" data-theme="a"></span>
  ...
</div>
<script>
  document.querySelectorAll('.theme-switcher__dot').forEach(...)
</script>
```
**修法**：删 `.theme-switcher` + 整段 JS。主题切换按 PRD §3.1 "启动时手动"——改 `<link href="tokens/...">`。
**对应 PRD**：§3.1 主题选择·启动时手动

### 违规 4 · V3 `.sp` / `.selling-points` 组件 class

**位置**：`levity-hair-oil-v3/index.html` CSS 第 209-353 行 + HTML 第 1097-1113 行
**违反**：38 BEM 命名约束（v0.5 扩到 48，V3 用了 50+ 个非 BEM）
**修法**：用 `dp2-list-row`（模板 1）或 `grid-3` + `icon-circle`（PRD 原有 38 BEM）。
**对应模板**：模板 1 横向列表卡

### 违规 5 · V3 `.hero` 主结构 class

**位置**：`levity-hair-oil-v3/index.html` CSS 第 290-320 行
**违反**：38 BEM 命名（PRD 已有 `.mod--hero` 修饰符）
**修法**：删 `.hero` 全部，Hero 屏用 `<div class="mod mod--hero">` + `mod-top-c` + `mod-img mod-img--hero`。
**对应 PRD**：§3.1.1 主结构 + 屏修饰

### 违规 6 · V3 `.section` / `.section--soft/card/dark` 3 态背景

**位置**：`levity-hair-oil-v3/index.html` CSS 第 42-56 行
**违反**：v0.4 命名空间（v0.5 收编为 `dp2-section-soft/card/dark`）
**修法**：v0.5 收编后，V3 改用 `dp2-section-soft/card/dark`（pattern-library §"屏内 3 态背景"），挂在 `.mod-body` 内子 div，不直接挂 `.mod`。
**对应模板**：pattern-library §"屏内 3 态背景"

### 违规 7 · V3 `.problems` / `.problem` / `.problem__visual` 等

**位置**：`levity-hair-oil-v3/index.html` CSS 第 358-402 行
**违反**：38 BEM 命名
**修法**：4 大问题用 `grid-2x2` + `grid-2x2-item` + `mod-img dp2-mock--square`（PRD 原有 + 模板 7）。
**对应模板**：模板 7 统一占位图 + PRD 原有 38 BEM

### 违规 8 · V3 `.miracle-list` / `.miracle-item` / `.miracle-index` 等

**位置**：`levity-hair-oil-v3/index.html` CSS 第 407-438 行
**违反**：38 BEM 命名
**修法**：用 `dp2-list-row`（模板 1）。
**对应模板**：模板 1 横向列表卡

### 违规 9 · V3 `.dim-flow` / `.dim-node` 三节点

**位置**：`levity-hair-oil-v3/index.html` CSS 第 462-556 行
**违反**：38 BEM 命名
**修法**：用 `dp2-step-flow` + `dp2-step-node`（模板 2）。
**对应模板**：模板 2 三节点流程

### 违规 10 · V3 `.tech-vs` / `.tech-vs__card--gold/--gray` 双卡

**位置**：`levity-hair-oil-v3/index.html` CSS 第 561-588 行
**违反**：38 BEM 命名
**修法**：用 `dp2-card-compare` + `dp2-card-compare__card--gold/--gray`（模板 3）。
**对应模板**：模板 3 颜色对比双卡

### 违规 11 · V3 `.compare-board` / `.board-card.competitor/brand-ours` 重叠卡片

**位置**：`levity-hair-oil-v3/index.html` CSS 第 904-972 行
**违反**：38 BEM 命名 + R3 排版可改铁律不改（用了 `direction: rtl` 翻转）
**代码**：
```css
.board-card.competitor { width: 44%; ... }
.board-card.brand-ours { width: 58%; margin-left: -4%; ... }
```
**修法**：用 `dp2-card-overlap` + `dp2-card-overlap__card--them/--us`（模板 4）。`direction: rtl` 翻转保留作为模板 4 的子技巧（不改 `transform` / `animation`）。
**对应模板**：模板 4 重叠卡片

### 违规 12 · V3 `.stats-bar` / `.stats-bar__item/val/sep` 数据条

**位置**：`levity-hair-oil-v3/index.html` CSS 第 443-457 行
**违反**：38 BEM 命名
**修法**：用 `dp2-data-strip` + `dp2-data-strip__item/val/sep`（模板 5）。
**对应模板**：模板 5 数据条

### 违规 13 · V3 `.extracts` / `.extract` / `.extract__orb` 顶部小圆卡

**位置**：`levity-hair-oil-v3/index.html` CSS 第 619-668 行
**违反**：38 BEM 命名
**修法**：用 `dp2-feature-orb` + `dp2-feature-orb__circle/country/name/desc`（模板 6）。
**对应模板**：模板 6 顶部小圆 + 下方白卡

### 违规 14 · V3 `.ph` / `.ph--hero/--wide/--square/--portrait` 占位图

**位置**：`levity-hair-oil-v3/index.html` CSS 第 241-285 行
**违反**：38 BEM 命名
**修法**：用 `dp2-mock` + `dp2-mock--hero/--wide/--square/--portrait` + `dp2-mock__label`（模板 7）。
**对应模板**：模板 7 统一占位图

### 违规 15 · V3 多处 `backdrop-filter` / 散落 `@keyframes`

**位置**：散落在 V3 CSS
**违反**：仅 `@keyframes` 违反 R4（`backdrop-filter` 不是动效，**保留**）
**代码**：
```css
backdrop-filter: blur(4px);   /* 散落 5+ 处 — 保留，真实质感支点 */
@keyframes oilShine { ... }   /* 违规 1 已列 */
```
**修法**：`backdrop-filter` 保留（属 PRD §7.1 真实质感支点）。`@keyframes` 删。

---

## 违规点总览（统计）

| 类型 | 数量 | 占比 |
|---|---|---|
| 38 BEM 命名约束（v0.4 / v0.5 命名空间）| 11 | 73% |
| R4 静态优先（`@keyframes` / `transform: scale` / JS 主题切换器）| 4 | 27% |
| 合计 | 15 | 100% |

**核心判断**：V3 真正"违反"的是**11 个 class 命名**（不是动效）。动效只有 `@keyframes oilShine` + 1 个 `:hover transform: scale` + 1 个 JS 主题切换器（共 3 个硬伤）。

**V3 的"好"不在动效，在巧思**——巧思全部可以静态化收编到 `dp2-` 组件（pattern-library 已沉淀）。

---

## 落地策略（v1 不实修老 HTML）

| 决策 | 理由 |
|---|---|
| ❌ 不动老 HTML 文件 | 改动 50+ 个 class 成本高，且新 BEM 不一定适合老场景 |
| ✅ 沉淀本文档作为"反模式" | 未来接手人 5 分钟看清"哪些不能用" |
| ✅ 老产物挂 `examples/_legacy/` | 与 v1 skill 的 1 屏范例（`examples/hkh-time-capsule/`）隔离 |
| ✅ v1 范例屏 1 用 `dp2-` 组件 | 证明"v0.5 合规 + 设计感好"可以并存 |

---

## 命名空间映射速查（V3 → v0.5）

| V3 旧 class | v0.5 新 class | 模板 |
|---|---|---|
| `.sp` / `.selling-points` | `.dp2-list-row` / `.grid-3` + `.icon-circle` | 模板 1 |
| `.hero` | `.mod .mod--hero` + `.mod-top-c` + `.mod-img .mod-img--hero` | 主结构 |
| `.section` / `.section--soft/card/dark` | `.dp2-section-soft/card/dark` | 屏内 3 态 |
| `.problems` / `.problem` | `.grid-2x2` + `.grid-2x2-item` + `.dp2-mock--square` | 模板 7 |
| `.miracle-list` / `.miracle-item` | `.dp2-list-row` | 模板 1 |
| `.dim-flow` / `.dim-node` | `.dp2-step-flow` + `.dp2-step-node` | 模板 2 |
| `.tech-vs` / `.tech-vs__card` | `.dp2-card-compare` + `.dp2-card-compare__card--gold/--gray` | 模板 3 |
| `.compare-board` / `.board-card` | `.dp2-card-overlap` + `.dp2-card-overlap__card--them/--us` | 模板 4 |
| `.stats-bar` / `.stats-bar__item` | `.dp2-data-strip` + `.dp2-data-strip__item/val/sep` | 模板 5 |
| `.extracts` / `.extract` | `.dp2-feature-orb` + 子元素 | 模板 6 |
| `.ph` / `.ph--hero/wide/square/portrait` | `.dp2-mock` + `.dp2-mock--hero/wide/square/portrait` | 模板 7 |

---

## 版本记录

| 版本 | 变更 | 触发 |
|---|---|---|
| v1 | 15 条违规点 + 命名空间映射速查 | Day 1 v1 skill 化（V3 巧思收编）|
