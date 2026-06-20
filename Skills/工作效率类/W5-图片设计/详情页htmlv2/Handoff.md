# Handoff · 详情页 HTML 2 Skill · v0.5.4.1

> **本文件作用**：skill 的"工作记忆"。每次读 skill 都自动看到 v0.5.4.1 完整状态。
> 主 memory（`.codebuddy/memory/`）只存"全局方法论 + 用户偏好"，不重复 skill 详情。

---

## 1. v0.5.4.1 完整状态

**版本**：v0.5.4.1（2026-06-14）
**Skill 路径**：`skills/工作效率类/W5-图片设计/详情页htmlv2/`
**W5 路由引用**：`skills-lock.json` W5.description（v0.5.4.1）

### 1.1 17 项自动化自检（#1-#17）

| # | 检测 | 版本 |
|---|---|---|
| 1 | 无 emoji 字符 | v0.5.1 |
| 2 | 无 `<br>` 后 1-2 字孤儿 | v0.5.1 |
| 3 | 无 inline `transform: scale/rotate` | v0.5.1 |
| 4 | 无 `<script>` 标签 | v0.5.1 |
| 5 | 无 `@keyframes` / `animation` | v0.5.1 |
| 6 | 无 `.theme-switcher` | v0.5.1 |
| 7 | 无 V3 违规 class（旧 7 个）| v0.5.1 |
| 8 | 无 CSS `transform: scale/rotate` | v0.5.1 |
| 9 | `.mod` 含 `min-height: 940px` | v0.5.1 |
| 10 | 无 V3 违规 class（新 14 个）| v0.5.3 |
| 11 | 屏宽必须 790px | v0.5.4 |
| 12 | 衬线 font-variation SOFT 80-100 | v0.5.4.1 |
| 13 | R8-1 屏间 bg 必变（≥ 2 态或 ≥ 1 次 dp2-section）| v0.5.4.1 |
| 14 | 自由排版区 ≥ 500px | v0.5.4.1 |
| 15 | R1 必含主标 + body（display-* + class="body" + <h1>）| v0.5.4.1 |
| 16 | brand-spec.md 必填 8 字段 | v0.5.4.1 |
| 17 | 4 维定位完整 | v0.5.4.1 |

### 1.2 8 个屏布局模板

| # | 模板 | 用途 | BEM |
|---|---|---|---|
| 1 | 横向列表卡 | 4 大功效 / 用户评价 | `.dp2-list-row` |
| 2 | 三节点流程 | 1D/2D/3D / 4 步按摩 | `.dp2-step-flow` + `.dp2-step-node` |
| 3 | 颜色对比双卡 | 双蛋白 / 3 人群 | `.dp2-card-compare` |
| 4 | 重叠卡片 | 28 天无效退款 vs 赠品 | `.dp2-card-overlap` |
| 5 | 数据条 | 临床数据 / 累计数据 | `.dp2-data-strip` |
| 6 | 顶部小圆卡 | 6 大植萃 | `.dp2-feature-orb` |
| 7 | 统一占位图 | 任何占位图 | `.dp2-mock` 4 个比例修饰符 |
| 8 | 非对称图文环绕 | 0 添加 / 成分安全 | `.dp2-wrap-block` + `.dp2-wrap-block__line` |

**BEM 总数**：50 类 51 个（v0.4 38 + v0.5 10 + v0.5.3 2）
**BEM 修饰符**：12 个

### 1.3 核心铁律（8 条）

1. **每行 ≥ 3 字**（断行后含末行）
2. **Emoji 必须去掉**
3. **原文护栏**：所有正文必须来自用户文案
4. **字号给两套方案让用户选**（不擅自决定）
5. **强制分批 checkpoint**（A 批 / B 批 / C 批）
6. **资产隔离铁律**（梳子/滴管/粒子/光斑等未列入 Theme Bundle 禁用）
7. **强制断句符协议**（用户给 `|` → AI 替换 `<br>`）
8. **R9-1 格式塔间距**（组件内 `<` 组件间）

---

## 2. 8 步流程（强制分批）

### A 批（步骤 0-4）· 规划批
- Step 0 · 验真（brand-spec.md 8 字段）
- Step 1 · 复制模板 + 选主题
- Step 2 · 4 维定位（目的/用户情绪/内容类型/视觉锚点）
- Step 3 · 选排版模板（8 模板）
- Step 4 · 空间预算

**⏸️ 硬性 checkpoint 1**：AI 停下等用户"继续"

### B 批（步骤 5-7）· 生成批
- Step 5 · 文字 class 分配
- Step 6 · 配图规划
- Step 7 · 排版美感收口

**⏸️ 硬性 checkpoint 2**：前 3 屏先输出等用户回看

### C 批（步骤 8）· 收口批
- Step 8 · 自检（17 项自动化 + 24 项人工）

---

## 3. 关键文件位置

```
skills/工作效率类/W5-图片设计/详情页htmlv2/
├── SKILL.md          v0.5.4.1 · 17 项自检清单 + 8 步流程
├── PRD.md            v0.5.3 · 50 BEM + 12 修饰符
├── template.html
├── tokens/
│   └── theme-pilgrim-dawn.css
├── references/       5 文件
│   ├── content-grid.md        栅格/字号/间距/R9-1 格式塔
│   ├── typographic-rhythm.md  断行/Few-Shot/断句符
│   ├── pattern-library.md     8 模板 + 资产隔离
│   ├── self-check.md          24 项操作清单
│   └── legacy-remediation.md  V3 违规修复
├── examples/
│   └── hkh-time-capsule/       范例屏 1（14/17 PASS 反面教材）
├── scripts/
│   └── dp2-self-check.cjs     17 项自动化
└── Handoff.md         ← 本文件
```

**跑自检**：`node scripts/dp2-self-check.cjs <项目目录>/`

---

## 4. 范例项目状态

### 4.1 HK v0.5.3 项目（v0.5.4.1 验证用）

**位置**：`Temp/详情页 HTML2/hk-time-reverse-v0.5.3/`
**状态**：屏 1-3 已写（B 批前 3 屏）· 17/17 PASS ✅
**Theme Bundle**：7 个允许元素 + 11 个禁用元素
**断句符决策**：13 屏主标全部 A 方案（display-xl 44px 1 行排 / 屏 1 B 方案 display-xxl 60px）
**待办**：屏 4-12 待写（B 批后续）

### 4.2 HK 范例屏 1（v0.5 时代）

**位置**：`skills/.../详情页htmlv2/examples/hkh-time-capsule/`
**状态**：14/17 FAIL（按"页面不动"原则保留为反面教材）

---

## 5. 已砍项（用户已确认不做）

- ❌ **Dribbble 5 维评分卡**（主观，无客观标准）
- ❌ **自由区计算公式**（自检 #14 已自动化检测 padding-top ≤ 200px）
- ❌ **模板 9 `.img-fluid` 真实资产接入路径**（用户说"不重要，跳过"）
- ❌ **html-to-png 导出脚本**（"从 V1 拿过来改"——未做）
- ❌ **桶 C #9 优先级 / 成功指标**（业务级）
- ❌ **桶 C #11 30 分钟 12 屏验证**（流程优化，非护栏）

---

## 6. 下一件事（用户说"准备收尾"）

按重要性：
- **A**：跑 HK v0.5.3 屏 4-12（B 批后续，~12 屏用模板 1/2/3/4/5/8 + 屏 12 模板 8 第一次实战）
- **B**：跑 v0.5.4.1 新项目（新品牌验证全规则）
- **C**：老产物挂 `examples/_legacy/`（levity-v2/v3 + HK v0.5 老产物归档）
- **D**：直接收尾（HK v0.5.3 屏 1-3 已能代表 skill 跑通）

回 A / B / C / D。

---

## 7. 版本历史

| 版本 | 关键变更 | 触发 |
|---|---|---|
| v0.4 | 38 个 BEM class 定稿 | W5 v1 整合 |
| v0.5 | +10 个 `dp2-` 组件 + R8 3 态背景 + 7 模板 | V3 巧思收编 |
| v0.5.1 | +5 项自检（emoji/断行/字号方案/原文护栏）+ §3.5/3.6/3.7 | 用户点出"原文护栏" |
| v0.5.2 | +断句符协议 + Few-Shot + 强制分批 + 资产隔离 + R9-1 | 外部专家 4 个优化方向 |
| v0.5.3 | +模板 8 `.dp2-wrap-block` + R10-1 V3 class 检测 | 用户点出"布局模板盲区" |
| v0.5.4 | +R10-2 屏宽 790px 护栏（自动化 #11）| 用户点出"宽度固定 790" |
| **v0.5.4.1** | **+6 项 PRD 漏护栏 R10-3 ~ R10-8（#12-#17）**| **用户点出"PRD 还有哪些没注意" + "影响视觉"分类** |
