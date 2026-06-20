# 屏布局模板库（pattern-library.md · v1）

> **状态**：v1 · 基于 V3 7 个巧思 + PRD v0.5 扩 BEM
> **配套**：`../SKILL.md` / `typographic-rhythm.md` / `legacy-remediation.md`
> **适用范围**：详情页 HTML 2 全部 12 屏 · 写屏前必查

---

## 本库用法

每个模板 = 1 段 HTML 片段 + 1 段 CSS 片段 + 适用场景 + 与 PRD §3.1.1 命名空间的对应。

**7 个模板**全部用 v0.5 新增的 10 个 `dp2-` 组件 class（38 → 48 BEM）。

**子元素用 CSS 子代/属性选择器约束**（不展开 BEM 子元素修饰符），控制 class 膨胀。

---

## 模板 1 · 横向列表卡（`.dp2-list-row`）

**适用场景**：4 大功效 / 4 大优势 / 4 大特点（数字+文字 一行一项）
**取代**：原 4 段文字纵向堆叠
**参考来源**：V3 `.miracle-item`

### HTML

```html
<div class="dp2-list-row">
  <span>10</span>
  <small>SECONDS</small>
  <h3>顺滑毛糙</h3>
  <p>HFAG 角蛋白 + 微渗技术 ｜ 深润保湿，抚平营养枯糙毛糙</p>
</div>
```

### CSS

```css
.dp2-list-row {
  display: flex;
  align-items: center;
  gap: var(--s-5);              /* 24px */
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  padding: var(--s-5) var(--s-6); /* 24px 32px */
  box-shadow: var(--shadow-soft);
}
.dp2-list-row > *:first-child {
  font-family: var(--font-display);
  font-size: 28px;
  color: var(--accent);
  font-style: italic;
  font-weight: 600;
  width: 50px;
  flex-shrink: 0;
  line-height: 1;
}
.dp2-list-row > small {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--accent);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  width: 80px;
  flex-shrink: 0;
}
.dp2-list-row > h3 {
  font-family: var(--font-serif);
  font-size: 16px;
  color: var(--text-main);
  font-weight: 600;
  margin: 0;
  width: 110px;
  flex-shrink: 0;
}
.dp2-list-row > p {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
  flex: 1;
  line-height: 1.6;
}
```

### 节奏要点

- 4 项 = 4 个 `.dp2-list-row` 垂直堆叠，gap 16px
- 单项高度 ≈ 80px（4 项 ≈ 320px + 48px gap = 368px）
- 适合"屏内 360-400px 内容区 + 上下标题区 + 屏底图"

---

## 模板 2 · 三节点流程（`.dp2-step-flow` + `.dp2-step-node`）

**适用场景**：1D/2D/3D 流程 / 3 步骤使用仪式 / 渐进式描述
**取代**：原数字陈列 / 纵向 3 段
**参考来源**：V3 `.dim-flow` + `.dim-node`

### HTML

```html
<div class="dp2-step-flow">
  <div class="dp2-step-node">
    <span>1D</span>
    <h3>填补空洞</h3>
    <p>发芯空洞受损<br>发质干枯毛糙</p>
  </div>
  <div class="dp2-step-node">
    <span>2D</span>
    <h3>深入滋养</h3>
    <p>HFAG 角蛋白<br>深入发芯滋养</p>
  </div>
  <div class="dp2-step-node">
    <span>3D</span>
    <h3>重塑光泽</h3>
    <p>修护受损结构<br>秀发顺滑水亮</p>
  </div>
</div>
```

### CSS

```css
.dp2-step-flow {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--s-4);              /* 16px */
  margin: var(--s-6) 0;         /* 32px */
}
.dp2-step-node {
  background: rgba(255, 255, 255, 0.06);
  border: 1px dashed var(--accent-soft);
  border-radius: var(--radius-sm);
  padding: var(--s-4) var(--s-3); /* 16px 12px */
  text-align: center;
}
.dp2-step-node > *:first-child {
  font-family: var(--font-display);
  font-size: 24px;
  font-style: italic;
  font-weight: 600;
  color: var(--accent);
  display: block;
  margin-bottom: 6px;
}
.dp2-step-node > h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main);
  margin: 0 0 4px;
}
.dp2-step-node > p {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  margin: 0;
}
```

### 节奏要点

- 3 节点横向平分（grid 3 列），gap 16px
- 单节点高度 ≈ 110px
- 适合"屏中部 110-130px 内容区"
- **配合 `.dp2-section-dark` 用**（"重音屏"）

---

## 模板 3 · 颜色对比双卡（`.dp2-card-compare`）

**适用场景**：双蛋白对比 / 普通 vs 高端 / 行业 vs 品牌
**取代**：原平等双列
**参考来源**：V3 `.tech-vs` + `.tech-vs__card--gold/--gray`

### HTML

```html
<div class="dp2-card-compare">
  <div class="dp2-card-compare__card dp2-card-compare__card--gold">
    <div class="dp2-card-compare__head">
      <h3>HFAG 角蛋白</h3>
    </div>
    <div class="dp2-card-compare__body">
      采用尖端科技工艺 HFAG 角蛋白，深入发芯，与人体头发高度相融
    </div>
  </div>
  <div class="dp2-card-compare__card dp2-card-compare__card--gray">
    <div class="dp2-card-compare__head">
      <h3>普通水解角蛋白</h3>
    </div>
    <div class="dp2-card-compare__body">
      分子量大带正电荷，受损发丝带负电荷，正负电荷相吸
    </div>
  </div>
</div>
```

### CSS

```css
.dp2-card-compare {
  display: flex;
  gap: var(--s-5);
  margin-top: var(--s-6);
}
.dp2-card-compare__card {
  flex: 1;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  padding: 0;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
}
.dp2-card-compare__card--gold {
  border-top: 3px solid var(--accent);
}
.dp2-card-compare__card--gray {
  border-top: 3px solid #C0B5A7;
}
.dp2-card-compare__head {
  padding: 18px 18px 12px;
  border-bottom: 1px solid rgba(180, 155, 115, 0.2);
  text-align: center;
}
.dp2-card-compare__head h3 {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}
.dp2-card-compare__card--gold h3 { color: var(--accent); }
.dp2-card-compare__card--gray h3 { color: var(--text-muted); }
.dp2-card-compare__body {
  padding: 14px 18px 18px;
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-muted);
}
```

### 节奏要点

- 2 卡等宽（flex 1:1），gap 24px
- 单卡高度 ≈ 160px
- **关键视觉差异**：border-top 颜色（金 vs 灰）= "优劣"信号
- 适合"屏内 200-240px 内容区"

---

## 模板 4 · 重叠卡片（`.dp2-card-overlap`）

**适用场景**：为什么选我们 / 普通 vs 我们的对比
**取代**：原左右两列等分
**参考来源**：V3 `.compare-board` + `.board-card.competitor` (44%) + `.brand-ours` (58%) + `margin-left:-4%`

### HTML

```html
<div class="dp2-card-overlap">
  <div class="dp2-card-overlap__card dp2-card-overlap__card--them">
    <div class="dp2-card-overlap__badge">其他精油</div>
    <div class="dp2-card-overlap__visual">[ 暗淡粘稠滴管 · PHOTO ]</div>
    <ul class="dp2-card-overlap__list">
      <li>油腻感明显</li>
      <li>吸收慢</li>
      <li>含有化学添加剂</li>
    </ul>
  </div>
  <div class="dp2-card-overlap__card dp2-card-overlap__card--us">
    <div class="dp2-card-overlap__badge">我们的精油</div>
    <div class="dp2-card-overlap__visual">[ 黄金透亮精油拉丝 · PHOTO ]</div>
    <ul class="dp2-card-overlap__list">
      <li>滋润力高</li>
      <li>吸收力快</li>
      <li>98% 天然植物精粹</li>
    </ul>
  </div>
</div>
```

### CSS

```css
.dp2-card-overlap {
  display: flex;
  align-items: stretch;
  margin-top: 32px;
  position: relative;
}
.dp2-card-overlap__card {
  border-radius: var(--radius-md);
  padding: 28px 18px 18px;
  position: relative;
  box-shadow: 0 10px 30px rgba(140, 115, 81, 0.18);
}
.dp2-card-overlap__card--them {
  width: 44%;
  background: var(--bg-deep);
  z-index: 1;
  border-radius: var(--radius-md) 0 0 var(--radius-md);
  box-shadow: -5px 8px 20px rgba(0, 0, 0, 0.06);
}
.dp2-card-overlap__card--us {
  width: 58%;
  background: var(--card-bg);
  z-index: 2;
  margin-left: -4%;
  border: 1px solid var(--accent);
}
.dp2-card-overlap__badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  font-weight: 600;
  padding: 5px 18px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}
.dp2-card-overlap__card--them .dp2-card-overlap__badge {
  background: #635345;
  color: var(--text-invert);
}
.dp2-card-overlap__card--us .dp2-card-overlap__badge {
  background: linear-gradient(90deg, var(--accent-deep) 0%, var(--accent) 100%);
  color: var(--text-invert);
}
.dp2-card-overlap__visual {
  aspect-ratio: 4/3;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: var(--card-bg);
  margin-bottom: 12px;
}
.dp2-card-overlap__list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.dp2-card-overlap__list li {
  font-size: 12px;
  margin-bottom: 8px;
  line-height: 1.4;
  display: flex;
  align-items: center;
  padding-left: 16px;
  position: relative;
}
.dp2-card-overlap__card--them .dp2-card-overlap__list li {
  color: var(--text-muted);
}
.dp2-card-overlap__card--us .dp2-card-overlap__list li {
  color: var(--text-main);
  font-weight: 500;
}
.dp2-card-overlap__list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  font-weight: 700;
}
.dp2-card-overlap__card--them .dp2-card-overlap__list li::before {
  content: "✗";
  color: #a1958a;
}
.dp2-card-overlap__card--us .dp2-card-overlap__list li::before {
  color: var(--accent);
}
```

### 节奏要点

- **46%/58% 错位是核心视觉**——`us` 卡在视觉上"压过" `them` 卡
- 容器总高 ≈ 360px
- 适合"屏内 380-420px 内容区"（屏中部最大布局块）

---

## 模板 5 · 数据条（`.dp2-data-strip`）

**适用场景**：99% 数据 / +X% 临床数据 / 核心数字陈列
**取代**：原 3 个数字并列黑底
**参考来源**：V3 `.stats-bar`

### HTML

```html
<div class="dp2-data-strip">
  <div class="dp2-data-strip__item">
    <span>一梳到底</span>
    <span class="dp2-data-strip__val">+99.65%</span>
  </div>
  <span class="dp2-data-strip__sep">|</span>
  <div class="dp2-data-strip__item">
    <span>水润有活力</span>
    <span class="dp2-data-strip__val">+99.01%</span>
  </div>
  <span class="dp2-data-strip__sep">|</span>
  <div class="dp2-data-strip__item">
    <span>修护发芯</span>
    <span class="dp2-data-strip__val">+99.65%</span>
  </div>
</div>
```

### CSS

```css
.dp2-data-strip {
  background: var(--text-main);
  color: var(--text-invert);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: var(--s-4);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.5px;
  margin-top: var(--s-6);
}
.dp2-data-strip__item {
  display: flex;
  align-items: baseline;
  gap: 6px;
  color: var(--text-invert);
}
.dp2-data-strip__val {
  color: var(--accent-soft);
  font-weight: 700;
  font-size: 14px;
}
.dp2-data-strip__sep {
  color: rgba(255, 251, 237, 0.3);
}
```

### 节奏要点

- 单条数据条高度 ≈ 48-56px
- 深棕底 + 浅金字 = "高奢数字"
- **必须**与 `.dp2-section-dark` 配对使用（数据条本身就是深色，但作为"重音元素"出现而非整屏反转）
- 适合"屏内 56-72px 内容区"

---

## 模板 6 · 顶部小圆 + 下方白卡（`.dp2-feature-orb`）

**适用场景**：6 大植萃 / 3 大产地 / 核心成分（每项 1 张圆图 + 国家/标题/描述）
**取代**：原 1×6 列表 / 3 列网格
**参考来源**：V3 `.extract` + `.extract__orb`

### HTML

```html
<div class="dp2-feature-orb">
  <div class="dp2-feature-orb__circle dp2-feature-orb__circle--tea"></div>
  <div class="dp2-feature-orb__meta">
    <span class="dp2-feature-orb__country">AUSTRALIA · 澳大利亚</span>
    <h3 class="dp2-feature-orb__name">山茶籽油 &amp; 霍霍巴籽油</h3>
  </div>
  <p class="dp2-feature-orb__desc">富含丰富的茶多酚，净润养润</p>
</div>
```

### CSS

```css
.dp2-feature-orb {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--card-bg);
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  padding: 18px 18px 12px;
  box-shadow: var(--shadow-soft);
  flex-wrap: wrap;
}
.dp2-feature-orb__circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(180, 155, 115, 0.3);
}
.dp2-feature-orb__circle--tea {
  background: radial-gradient(circle at 40% 30%, #F0E5C0 0%, #B49B73 80%);
}
.dp2-feature-orb__circle--olive {
  background: radial-gradient(circle at 40% 30%, #C8D58A 0%, #6B7A3F 80%);
}
.dp2-feature-orb__circle--rice {
  background: radial-gradient(circle at 50% 50%, #FFFBED 0%, #D4B570 80%);
}
.dp2-feature-orb__meta {
  flex: 1;
}
.dp2-feature-orb__country {
  display: inline-block;
  background: var(--bg-deep);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  letter-spacing: 0.1em;
}
.dp2-feature-orb__name {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 600;
  color: var(--text-main);
  margin: 0;
}
.dp2-feature-orb__desc {
  padding: 0 18px 18px;
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.6;
  margin: 0;
  flex-basis: 100%;          /* 强制换行到第二行 */
}
```

### 节奏要点

- 单卡高度 ≈ 110px
- 3-6 项垂直堆叠，gap 14px
- **关键视觉差异**：顶部 64px 圆 + 圆周发光 = "高奢植萃"信号
- 适合"屏内 360-440px 内容区"

---

## 模板 7 · 统一占位图（`.dp2-mock`）

**适用场景**：所有需要占位图的位置（主图 / 局部图 / 屏底图）
**取代**：V3 之前的 `.img-box` / `.img-fluid` / 各处临时占位
**参考来源**：V3 `.ph` + `ph--hero/--wide/--square/--portrait`

### HTML

```html
<!-- 屏底主图（16/11） -->
<div class="dp2-mock dp2-mock--hero">
  <span class="dp2-mock__label">主产品图<small>双瓶精油 + 白花</small></span>
</div>

<!-- 宽屏图（16/9） -->
<div class="dp2-mock dp2-mock--wide">
  <span class="dp2-mock__label">3D 微观修护示意<small>金色分子链填补发芯空洞</small></span>
</div>

<!-- 方形（1/1） -->
<div class="dp2-mock dp2-mock--square">
  <span class="dp2-mock__label">分叉特写</span>
</div>

<!-- 竖图（3/4） -->
<div class="dp2-mock dp2-mock--portrait">
  <span class="dp2-mock__label">使用前</span>
</div>
```

### CSS

```css
.dp2-mock {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: var(--radius-md);
  background: var(--card-bg);
  border: 1px solid var(--line);
  box-shadow: inset 0 0 30px rgba(255, 251, 237, 0.6);
}
.dp2-mock::before {
  content: "";
  position: absolute;
  inset: 12px;
  border: 1px dashed var(--line);
  border-radius: calc(var(--radius-md) - 6px);
  pointer-events: none;
}
.dp2-mock--hero     { aspect-ratio: 16/11; }
.dp2-mock--wide     { aspect-ratio: 16/9; }
.dp2-mock--square   { aspect-ratio: 1/1; }
.dp2-mock--portrait { aspect-ratio: 3/4; }
.dp2-mock__label {
  position: relative;
  z-index: 2;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-soft);
  background: var(--card-bg);
  border: 1px solid var(--line);
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  text-align: center;
  max-width: 80%;
}
.dp2-mock__label small {
  display: block;
  font-size: 9px;
  color: var(--text-muted);
  margin-top: 2px;
  letter-spacing: 0.1em;
}
```

### 节奏要点

- **统一规范**：所有占位图都用 `.dp2-mock` + 4 个比例修饰符之一
- **不再用** `.img-box` / `.img-fluid` / 临时 div
- 标签居中（V3 改过：不要右上角，要底部居中）
- 适合"任何需要占位图的位置"

### 资产隔离铁律（**v0.5.2 新增 · 防 LLM 脑补**）

> **核心问题**：AI 在填充 `[ 高清女性瀑布发丝光泽图 ]` 这类描述时，**常常自行脑补多余元素**（如梳子、滴管、悬浮粒子、光斑等），导致占位与未来真实资产冲突。

**铁律**（**资产描述必须极度干净**）：

#### 类型隔离

| 占位类型 | 允许的描述 | 严格禁止的描述 |
|---|---|---|
| **环境主图**（背景 / 氛围）| `[ 黑金极简底 ]` / `[ 米色纹理背景 ]` / `[ 金色光晕渐变 ]` | 任何人物字符 / 任何道具 / 任何粒子 |
| **人物主图**（脸 / 手 / 局部）| `[ 35+ 女性右脸 30° 仰视 ]` / `[ 指腹推开精华特写 ]` | 复杂环境背景 / 任何"模糊"装饰元素 |
| **产品主图**（瓶身 / 滴管）| `[ HK 瓶身 45° 悬浮 · 黑金渐变底 ]` | 任何"光斑" / "粒子" / "水雾"等特效词 |

#### 禁用未定义元素（**铁律**）

> AI **禁止**在占位描述中出现以下元素，**除非该元素已被用户列入"主题资产包（Theme Bundle）"**：

- ❌ 功能性道具：梳子 / 滴管 / 刮痧板 / 按摩仪
- ❌ 特效词：悬浮粒子 / 水滴 / 光斑 / 烟雾 / 光环 / 能量波纹
- ❌ 模糊装饰：金色光晕（除非在 Theme Bundle 明确）/ 模糊背景 / 朦胧
- ❌ 假设性细节：双瓶 / 三件套 / 礼盒装（**必须来自用户原文**）

#### 主题资产包（Theme Bundle）规范

如需引入上述元素，**用户必须**先在 `brand-spec.md` 列出 Theme Bundle：

```markdown
## Theme Bundle · HK 逆时焕颜
- 元素 1: 滴管（带金棕色液体）→ 用于"使用仪式"屏
- 元素 2: 金色波纹（3 圈）→ 用于 Hero 屏主图
- 元素 3: 35+ 女性右脸 → 用于"衰老真相"屏
```

**AI 只能在用户列出的元素中挑选**，**不能自创**。

#### 自检（v0.5.2）

写每个 `.dp2-mock` 时，**强制检查**：

1. 描述中是否含 `梳` `滴管` `刮痧` `按摩仪` `粒子` `光斑` `水雾` `光环` `波纹` `光晕` `双瓶` `三件套` `礼盒`？
2. 如含，**回查 brand-spec.md Theme Bundle** 是否列出
3. 未列出 → **改用通用描述**（如 `[ 产品主图 ]` / `[ 氛围背景 ]`）

---

## 模板与 PRD 命名空间对应

| 模板 | 新 class | 关联原有 class | 模板来源 V3 |
|---|---|---|---|
| 1 横向列表卡 | `.dp2-list-row` | `.body` `.h1-sm` | `.miracle-item` |
| 2 三节点流程 | `.dp2-step-flow` `.dp2-step-node` | `.h1-sm` `.body` | `.dim-flow` + `.dim-node` |
| 3 颜色对比双卡 | `.dp2-card-compare` + `--card` + `--card--gold/--gray` | `.h1-sm` | `.tech-vs` |
| 4 重叠卡片 | `.dp2-card-overlap` + `--card` + `--card--them/--us` + `--badge` | `.body` | `.compare-board` |
| 5 数据条 | `.dp2-data-strip` + `--item` + `--val` + `--sep` | （深色，不依赖其他）| `.stats-bar` |
| 6 顶部小圆卡 | `.dp2-feature-orb` + `--circle` + `--country` + `--name` + `--desc` | `.body` | `.extract` + `.extract__orb` |
| 7 统一占位图 | `.dp2-mock` + `--hero/--wide/--square/--portrait` + `--label` | （独立）| `.ph` |

---

## 屏内 3 态背景（`.dp2-section-soft/card/dark`）

v0.5 新增，配合 R8 升级用。

### 用法

```html
<div class="mod mod--alt-bg">
  <div class="mod-top-c">标题区</div>
  <div class="mod-body">
    <div class="dp2-section-card">  <!-- 屏内 3 态背景区 -->
      <!-- 任意内容 -->
    </div>
  </div>
</div>
```

### CSS

```css
.dp2-section-soft { background: var(--bg-soft); }
.dp2-section-card { background: var(--card-bg); }
.dp2-section-dark {
  background: linear-gradient(180deg, var(--text-main) 0%, #5C4A35 100%);
  color: var(--text-invert);
}
.dp2-section-dark .h1-sm,
.dp2-section-dark h2,
.dp2-section-dark h3 { color: var(--text-invert); }
.dp2-section-dark .body { color: rgba(239, 230, 216, 0.78); }
.dp2-section-dark .kicker { color: var(--accent-soft); }
.dp2-section-dark .deco-en { color: var(--accent-soft); }
```

### 节奏要点

- **重音位**：每隔 3-4 屏可用 1 次 `.dp2-section-dark` 作"重音屏"（V3 验证过）
- 2 态 `.dp2-section-soft` / `.dp2-section-card` 交替 = R8 屏间独立性
- 1 态 `.dp2-section-dark` = 重音屏（数据 / 主张 / 引言 类屏）

---

## 模板 8 · 非对称图文环绕（`.dp2-wrap-block`）· v0.5.3 新增

> **来源**：HK v0.5 屏 5 改造痛点——"0 添加"屏需要"图左 + 文右 + 行不等高错落"，原 7 模板无解。**新增此模板**避免发明 `.zero-add-layout` / `.list-item-arc` 等违规 class。
>
> **核心场景**：电商详情页**最高频**结构之一——"产品主图 + 多行要点陈列"。

### HTML

```html
<div class="dp2-wrap-block">
  <!-- 左：透明大图（用 .dp2-mock--portrait 占位） -->
  <figure class="dp2-wrap-block__media">
    <div class="dp2-mock dp2-mock--portrait">
      <span class="dp2-mock__label">[ 瓶身 45° 悬浮 · 黑金渐变底 ]</span>
    </div>
  </figure>

  <!-- 右：错落文字（不等高行 + 大小字混排） -->
  <div class="dp2-wrap-block__copy">
    <p class="kicker">ZERO ADDED · 0 添加</p>
    <p class="display-lg">0 添加 · 0 刺激</p>
    <div class="deco-line" style="margin: 16px 0 24px;"></div>

    <div class="dp2-wrap-block__line">
      <span class="dp2-wrap-block__num">01</span>
      <small>ALCOHOL</small>
      <p class="body">无酒精 · 敏感肌友好</p>
    </div>
    <div class="dp2-wrap-block__line">
      <span class="dp2-wrap-block__num">02</span>
      <small>FRAGRANCE</small>
      <p class="body">无香精 · 还原原料本味</p>
    </div>
    <div class="dp2-wrap-block__line">
      <span class="dp2-wrap-block__num">03</span>
      <small>MINERAL OIL</small>
      <p class="body">无矿物油 · 透气不闷痘</p>
    </div>
    <div class="dp2-wrap-block__line">
      <span class="dp2-wrap-block__num">04</span>
      <small>PARABEN</small>
      <p class="body">无对羟基苯甲酸酯 · 温和防腐</p>
    </div>
  </div>
</div>

<!-- 反向：图右文左 -->
<div class="dp2-wrap-block dp2-wrap-block--reversed">
  <figure class="dp2-wrap-block__media">
    <div class="dp2-mock dp2-mock--portrait">
      <span class="dp2-mock__label">[ 用户右脸 30° 仰视 ]</span>
    </div>
  </figure>
  <div class="dp2-wrap-block__copy">
    <!-- ... -->
  </div>
</div>
```

### CSS

```css
.dp2-wrap-block {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 48px;
  align-items: center;
}
.dp2-wrap-block--reversed { grid-template-columns: 1.2fr 1fr; }
.dp2-wrap-block--reversed > figure { order: 2; }

.dp2-wrap-block__media {
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dp2-wrap-block__line {
  display: flex;
  align-items: baseline;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid var(--line);
}
.dp2-wrap-block__line:last-child { border-bottom: none; }

.dp2-wrap-block__num {
  font-family: var(--font-display);
  font-size: 22px;
  color: var(--accent);
  font-style: italic;
  font-weight: 500;
  width: 40px;
  flex-shrink: 0;
}
.dp2-wrap-block__line > small {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--accent);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  width: 100px;
  flex-shrink: 0;
}
.dp2-wrap-block__line > p {
  flex: 1;
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
}
```

### 节奏要点

- **错落行**：行高 14px + 数字 22px + 小字 9px + 正文 13px（4 个字号阶）—— 模拟原图"弧度错落"视觉
- **图：1fr / 文：1.2fr**（图略小）—— 主图不抢文字焦点
- **`.dp2-wrap-block--reversed`**：用 `order: 2` 反向，**不复制 CSS**（避免膨胀）
- **行数**：2-6 行最适合（少于 2 行 = 用模板 1 `.dp2-list-row`；多于 6 行 = 拆 2 屏）
- **适用屏**："0 添加" / "成分安全" / "产品 + 卖点" / "用户 + 体验" / "功效 + 证据"

### 不可用场景

- ❌ 屏 1 Hero（用 `.mod--hero` + 居中布局）
- ❌ 数据屏（用模板 5 `.dp2-data-strip`）
- ❌ 卡片对比屏（用模板 3 `.dp2-card-compare`）
- ❌ 卡片重叠屏（用模板 4 `.dp2-card-overlap`）

### 自检（v0.5.3）

- `dp2-wrap-block__line` 数量 ≥ 2 且 ≤ 6
- `.dp2-wrap-block` 必须包在 `.mod-body` 内（不能直接挂 `.mod`）
- 写 `__media` 必须用 `.dp2-mock`（不能用 `<img>` 真实资产代替 mock 容器，**真实资产替换 mock 内层**）

### V3 违规对照（`dp2-wrap-block` 出现的原因）

| V3 用的违规 class | `dp2-wrap-block` 替代 |
|---|---|
| `.zero-add-layout` | `.dp2-wrap-block` |
| `.list-item-arc` | `.dp2-wrap-block__line`（"弧度"是行不等高，不是 border-radius）|
| `.product-hero-left` + `.product-hero-right` | `.dp2-wrap-block` 1 个容器 + grid 双列 |

---

## 版本记录

| 版本 | 变更 | 触发 |
|---|---|---|
| v1 | 7 个屏布局模板 + 3 态背景用法 | Day 1 v1 skill 化（V3 巧思收编）|
| **v0.5.3** | **+模板 8 `.dp2-wrap-block` 非对称图文环绕**（V3 `.zero-add-layout` / `.list-item-arc` 替代）| **HK v0.5 屏 5 改造痛点** |
