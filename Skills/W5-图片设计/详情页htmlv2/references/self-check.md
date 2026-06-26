# Self-Check · 24 项操作清单 · v0.5.3

> **本文件作用**：把 v0.5.3 散落在多文件的"自检规则"**集中成可勾选清单**，
> 让 AI / 人类在**一屏 5 分钟**内过完 24 项。

---

## 使用方式

```bash
# 1. 跑自动化（9 项，30 秒）
node scripts/dp2-self-check.cjs <项目目录>/

# 2. 过人工清单（15 项，5 分钟/屏）
#    按本文件从 [1] 勾到 [15]

# 3. 写 self-check-report.md（自动生成模板见末尾）
```

**0 失败 + 15/15 勾 = 屏合格**。

---

## 自动化清单（9 项 · v0.5.3）

跑 `node scripts/dp2-self-check.cjs <项目目录>/`：

| # | 检测 | 修法 |
|---|---|---|
| 1 | 无 emoji 字符（仅 1F000-1F1FF 真实 emoji 区）| 删 emoji，改用 `.icon-circle` 或纯文字 |
| 2 | 无 `<br>` 后 1-2 字孤儿 | 加更多字 / 改用 `<br>` 强制断 / 降字号 |
| 3 | 无 inline `transform: scale/rotate` | 改用 `class` + 静态样式 |
| 4 | 无 `<script>` 标签 | 移除外链 / 内联 JS |
| 5 | 无 `@keyframes` / `animation` | 删除，R4 静态优先 |
| 6 | 无 `.theme-switcher` 类 | 删除，R4 禁止 Tweaks |
| 7 | 无 V3 违规 class（旧 7 个）| 见 `legacy-remediation.md` |
| 8 | 无 CSS `transform: scale/rotate` | 删除，R4 静态优先 |
| 9 | `.mod` 含 `min-height: 940px` | 补 R2 940px 固定 |
| 10 | 无 V3 违规 class（新 14 个）| 改用 `dp2-` 组件 |

---

## 人工清单（15 项 · v0.5.3）

### A · 基础（4 项）

#### [1] 940px 屏高
- [ ] DevTools 检查每个 `.mod` 高度 ≥ 940px
- [ ] 不足时加 `min-height: 940px`（已是 #9 自检）

#### [2] 标题区在屏顶居中
- [ ] DevTools 检查 `.mod-top-c` 的 `padding-top` ≥ 80px
- [ ] 检查 `text-align: center`

#### [3] 标题字号合规
- [ ] 屏 1 Hero = display-xxl 72px / 60px
- [ ] 屏 2-12 = display-xl 44px（默认）
- [ ] 标题太长 = display-lg 32px（用户给的两套方案选了）
- [ ] **不擅自决定字号**

#### [4] 无文字/图片跨越屏边界
- [ ] DevTools 检查 12 个 `.mod` 高度
- [ ] 无元素溢出到下一屏

### B · 风格（5 项）

#### [5] 字号对比 ≥ 2.5x
- [ ] 同屏最大字号 / 最小字号 ≥ 2.5
- [ ] 例：display-xl 44px / body 14px = 3.1x ✅
- [ ] 例：display-lg 32px / body 14px = 2.3x ❌（改 h1-sm 36px）

#### [6] 字体隔离（Serif / Sans / Mono）
- [ ] display / h1-sm → Serif
- [ ] body / lead / meta → Sans
- [ ] kicker / deco-en / num → Mono

#### [7] 衬线启用 `font-variation-settings`
- [ ] Fraunces `font-variation-settings: "SOFT" 80, "WONK" 0`
- [ ] DevTools 检查生效

#### [8] 留白节奏（v0.5.3 R9-1 格式塔原则）
- [ ] 组件内间距 `<` 组件间间距
- [ ] 见 `content-grid.md §3.2` 各模板的间距配方
- [ ] 至少 1 对组件满足

#### [9] 屏间独立（v0.5 R8 升级 3 态）
- [ ] 屏间有 `border-top: 1px solid var(--line)` 描边
- [ ] **或** 屏内用 `.dp2-section-soft/card/dark` 3 态背景交替
- [ ] 重音屏（`.dp2-section-dark`）每隔 3-4 屏 1 次

### C · R4 静态优先（3 项）

#### [10] 无 `<script>` 标签（已 #4 自动化）
- [ ] 无外链 / 内联 JS
- [ ] 主题切换器 / 动画 / 表单等**全部静态化**

#### [11] 无 `animation` / `@keyframes`（已 #5 自动化）
- [ ] 无 CSS 动效
- [ ] hover 只改 `color` / `background`

#### [12] 无 Tweaks（主题切换器 / 浮窗 / 弹窗）
- [ ] 无 `.theme-switcher`（已 #6 自动化）
- [ ] 无模态框 / 抽屉 / 浮窗

### D · R5-R8 排版（3 项）

#### [13] 断行无孤儿字（v0.5.1 强化 · 已 #2 自动化）
- [ ] **每一行** ≥ 3 字（含末行）
- [ ] 用 `<br>` 强制断行（不让浏览器自动断）
- [ ] 强制断句符协议（用户用 `|` 标记断点 → AI 1:1 替换 `<br>`）

#### [14] 无 emoji（v0.5.1 · 已 #1 自动化）
- [ ] HTML 中**无**任何 emoji 字符
- [ ] 用户原文含 emoji → 删 emoji 保留正文
- [ ] 不用 emoji 做装饰（改用 `.icon-circle`）

#### [15] 无 V3 违规 class（v0.5.3 新增 · 已 #10 自动化）
- [ ] grep 0 命中 V3 违规 class（14 个）
- [ ] 改用 `dp2-` 组件（详见 `pattern-library.md` 模板 8 V3 违规对照表）

---

## self-check-report.md 模板

跑完 9 项自动化 + 勾完 15 项人工后，**写报告**：

```markdown
# Self-Check Report · <项目名> · v0.5.3

**日期**：YYYY-MM-DD
**跑版本**：v0.5.3（9 项自动化 + 15 项人工 = 24 项）
**结论**：✅ 24/24 全 PASS

## 1. 自动化（9 项）

\`\`\`
✅ 1. 无 emoji 字符
✅ 2. 无 <br> 后 1-2 字孤儿
✅ 3. 无 inline transform: scale/rotate
✅ 4. 无 <script> 标签
✅ 5. 无 CSS @keyframes / animation
✅ 6. 无 .theme-switcher 类
✅ 7. 无 V3 违规 class（旧 7 个）
✅ 8. 无 CSS transform: scale/rotate
✅ 9. .mod 规则含 min-height: 940px
✅ 10. 无 V3 违规 class（新 14 个）
\`\`\`

## 2. 人工（15 项）

### A · 基础
- [x] [1] 940px 屏高
- [x] [2] 标题区在屏顶居中
- [x] [3] 标题字号合规
- [x] [4] 无文字/图片跨越屏边界

### B · 风格
- [x] [5] 字号对比 ≥ 2.5x
- [x] [6] 字体隔离
- [x] [7] 衬线启用 font-variation-settings
- [x] [8] 留白节奏
- [x] [9] 屏间独立

### C · R4 静态优先
- [x] [10] 无 <script> 标签
- [x] [11] 无 animation / @keyframes
- [x] [12] 无 Tweaks

### D · R5-R8 排版
- [x] [13] 断行无孤儿字
- [x] [14] 无 emoji
- [x] [15] 无 V3 违规 class

## 3. 屏级别验证

每屏跑 24 项的子集：
- 屏 1-12：过 [1] [2] [3] [5] [8] [9] [13] [14]
- 屏 2/5/8/11（重音屏）：加 [9] 3 态背景验证

**9/12 屏 PASS**（如某屏 FAIL，标出 + 改）。

## 4. 项目级别验证

- [x] 所有屏共用 1 主题（朝圣黎明 / 玫瑰矿泉 / 黄昏胶囊 / 自定义）
- [x] R8 3 态背景贯穿（soft/card/dark 节奏 3-4 屏 1 次重音）
- [x] 无 inline `style`（除已声明的 `margin-bottom: 16px` 等微调）
- [x] 1 主题 = 1 tokens CSS 文件
```

---

## 历史变更

| 版本 | 变更 |
|---|---|
| v0.5 | 8 基础 + 5 风格 + 4 R4 静态 + 6 R5-R8 排版 = 23 项 |
| v0.5.1 | +5 项自检（emoji / 断行 / 字号方案 / 原文护栏 / R6-2~6-5）→ 28 项 |
| v0.5.2 | +R9-1 格式塔间距 + R10-1 V3 违规 class 框架 → 29 项 |
| **v0.5.3** | **24 项最终版**（合并 + 去重 + 自动化支持）：9 项自动化 + 15 项人工 |
