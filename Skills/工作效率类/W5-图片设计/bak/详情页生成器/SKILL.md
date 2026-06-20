---
name: 详情页生成器
description: 详情页原子骨架拼装与样式解耦主控。支持基于[视觉锚点+文字排版]的双元素弹性骨架组装（Node A），以及全局设计令牌与骨架结构的深度解耦拆解（Node B）。Use when user wants to create, update, design an e-commerce detail page, structure website components, or maintain layout templates.
metadata:
  pattern: inversion+generator+pipeline+tool-wrapper
  category: 设计
---

# 电商详情页模块化生成器 (双主控完全体 V3.0)

## 核心路由控制 (Route Hub)
**在会话开始时，必须严格根据意图，分流进入以下两个独立运作的 Node 核心，严禁发生逻辑混淆：**
- ➔ **意图：写详情页/排版/根据卖点出方案/根据文案构思页面** ➔ 锁定进入 **`[Node A：详情页智能组装生产线]`**
- ➔ **意图：拆解爆款/记录排版/添加新样式/丰富或更新积木库** ➔ 锁定进入 **`[Node B：模块化组件库维护]`**

---

## 🧭 [Node A：详情页智能组装生产线]

### 核心协议：全局画布基因级编译
**Node A 启动时，无条件隐式读取以下两部分作为最高真相源。生成最终结果时，必须将全局视觉基因无缝缝合至双元素骨架中，严禁在组件内部硬编码色彩、字号与字重：**
1. **全局设计令牌（Theme-Palette）**：加载唯一全局样式库 `详情页生成器/references/theme-palette.md`（控死全局背景色彩、大/小标题字号字重级差、核心点缀色及点缀元素特征）。
2. **双元素弹性骨架（Component Mesh）**：全量扫描 `详情页生成器/assets/components/` 目录下由[视觉锚点]与[文字排版]构成的无色相弹性积木。

<what-to-do>
### 标准作业程序 (SOP)

#### 步骤 1 — 原始资料多维审计与文案重力核对 (Audit & Check)
1. **执行静默吞噬**：全量阅读并解构桌上的所有原始材料（产品粗文案、卖点、受众）。
2. **执行文本层级清点**：严格清点原始文案中包含哪些层级（是否有【核心数据】、【大标题】、【副标题/正文说明】），判定文案的总重力（长篇大论还是极简短句）。
3. **执行期望主体推演**：根据产品类目与本屏卖点，自动推导本屏的绝对主角（如：讲成分则锁定 `#成分意象`，讲数据则锁定 `#数据面板`）。

#### 步骤 2 — 动态降维与双元素骨架智能匹配 (Smart Triage)
1. **双轴标签打捞**：前往 `详情页生成器/assets/components/` 目录，通过[视觉锚点标签]与[文字排版标签]交叉匹配最完美的骨架（如同时命中 `#成分意象` 与 `#横向三列阵列`）。
2. **文案重力拦截（重路由机制）**：**若选中的复杂阵列骨架需要填充 3 组数据，但用户只输入了 1 句话，强制抛弃当前复杂骨架，退回并重新匹配极简排版骨架（如单行大标题），绝对禁止保留大面积空洞或擅自扩写。**

#### 步骤 3 — 全局基因注入与单屏空间全自动化输出（Batch Production）
采用 `batch` 模式，将【全局设计令牌】的物理数值，无缝灌注到【双元素弹性骨架】的结构坑位中。

**分批续写机制：**
若 N > 6 屏，分多次生成：
- 第1批：生成前 6 屏
- 后续批次：基于已有结果续写，附加指令"补充要求：这是续写生成。请生成新的 X 屏，不要重复之前的内容与角度。"
- 每批输出后执行 Checkpoint 确认 → 方可进入下一批
- 全部完成后一次性展示全案

**强制输出格式模板：**
```markdown
### 📺 第 [N] 屏：[本屏核心卖点/功能]

**🎨 [UI 结构轨] (全局视觉基因缝合排版)**
- [画布背景]：调用全局 [Theme-Palette: Canvas_Bg_Style] (如：浅蓝到白线性渐变)
- [核心视觉锚点]：[读取当前组件 Frontmatter 中的 visual_anchor 属性]
  - ➔ 空间占比：[anchor_scale]
  - ➔ 边缘约束：[anchor_edge]
- [信息文本排版]：[读取当前组件 Frontmatter 中的 typography_layout 属性]
  - ➔ *[抗干扰门禁]*：(静默判定) 若 visual_anchor 为 `#材质微距` 或 `#模特场景` 等复杂实景，强制为下方的文字群组叠加 [Theme-Palette: 半透明/毛玻璃 UI 底板]，确保文本绝对清晰可读。
  - ➔ [挂载: Deco/点缀元素]：(具体文案) | 样式：调用全局 [Theme-Palette: Deco_Font_Style]
  - ➔ [挂载: 主标题/H1]：(具体文案) | 样式：调用全局 [Theme-Palette: H1_Size_Weight]
  - ➔ [挂载: 信息群组/Repeater]：(按骨架群组结构填入确切文案) | 样式：调用全局 [Theme-Palette: Body_Size_Color]
- *[幽灵消除日志]*：(静默打印：简述因无文案而被彻底隐藏并收拢负空间的图层)
- *[文字渲染约束]*：(静默约束) 主文案优先 4-12 字，副文案优先 8-22 字；文案短句化，避免生图乱码；禁止水印及随机字母。

**📸 [ImageFX 图像轨] (视觉锚点物理特征锁死)**
- **ImageFX Prompt**：
An 8k resolution, photorealistic commercial product photography for an e-commerce detail page. The overall lighting, environment tone, and contrast completely follow [Inject: theme-palette.md 全局主题环境与点缀色趋势].

[Inject IF visual_anchor == "#产品本尊"]: "The composition features the main product. 若参考图只有产品白底图/棚拍图，允许自由重建使用场景（模特手持/使用中/环境展示），但产品外观（形状、颜色、材质、LOGO）必须与参考图完全一致。禁止复制参考图的原始背景。Maintain strict negative space based on [anchor_edge], leaving an absolutely clean area for typography."
[Inject IF visual_anchor == "#材质微距"]: "CRITICAL EXCLUSION: ABSOLUTELY NO PRODUCT BOTTLES OR PACKAGING. The entire canvas is a full-bleed macro shot of product texture (e.g., splashing water, creamy smear). Textures must fade smoothly into a flat low-contrast gradient under the typography zone."
[Inject IF visual_anchor == "#模特场景"]: "A high-end beauty editorial shot of a model [用户指定的动作，如：脸部涂抹特写]. Natural, glowing skin texture. Maintain substantial negative space on the designated side for typography overlay."
[Inject IF visual_anchor == "#成分意象"]: "A clean, studio light setup of floating premium [用户指定的成分意象，如叶片/水滴]. Isolated on a seamless solid background color of [Inject: 全局背景色], rendered as a cutout asset suitable for Float-Composite design."
[Inject IF visual_anchor == "#数据面板"]: "CRITICAL EXCLUSION: NO PHOTOGRAPHY AT ALL. Render a pure UI container layout with ultra-sharp vector lines, geometric data charts, and scientific typography grids."

CRITICAL SEAMLESS CONSTRAINT: Ensure the top and bottom borders of the canvas smoothly fade into a solid background color matching the global theme palette to allow for seamless vertical stacking.

PRODUCT CONSISTENCY LOCK: The product shape, color, material, and logo must be IDENTICAL across ALL screens based on the product reference image. Do NOT alter product appearance between screens.

```

#### 步骤 4 — 资产落盘与看板闭环 (Sync & Close)

全案输出完毕后，静默执行无缝连招：

1. **执行文档落盘**：将整套分屏详情页方案（含合并后的提示词）保存至本地项目目录：`.scratch/designs/产品名-detail-page.md`。
2. **执行看板同步**：直接读取并修改项目根目录下的 `kanban.html` 源码，将对应的卡片推进到 `已完成 (Done)` 状态。


---

### 标准维护程序 (SOP)

#### 🏁 步骤 1 — 更新全局基因库 (操作 `references/theme-palette.md`)

从参考图中剥离并更新唯一全局设计令牌，严禁将其污染至独立骨架组件中：

1. **[Typography 字体级差系统]**：提取全局统一的 `H1`、`H3`、`Body`、`Deco` 的比例与字重对比（重黑/纤细），并判定字体风格策略（科技无衬线 / 自然宋体 / 传统楷体）。
2. **[Color & Element 色彩与点缀系统]**：提取唯一的画布背景色（如渐变方向）、核心主色、高光点缀色，以及标志性的微观物理点缀元素（如悬浮粒子、特定的细线框）。

#### 🏁 步骤 2 — 创建无色相双元素骨架 (操作 `assets/components/*.md`)

新建标准弹性骨架文件。**组件内部严禁出现任何具体色彩、字体名或绝对像素值（如20px间距），强制使用群组/嵌套语法记录阵型。**

**骨架结构提取要求：**

1. **[视觉锚点 (Visual Anchor)] 提取**：
* 查主体：判定画面主角（`#产品本尊` / `#材质微距` / `#成分意象` / `#模特场景` / `#数据面板`）。
* 定边界：记录其空间占比 `anchor_scale`，并判定边缘约束 `anchor_edge`（硬边缘需避让 / 透明可穿插）。


2. **[文字排版 (Typography Layout)] 提取**：
* 查阵型：是 `#居中独白`、`#左重右轻` 还是 `#多列阵列`？
* 找容器与规律（深度集群扫描）：若存在重复的图文组合，必须定义为 `[Group: Repeater]` 并记录精确的阵列数（如 1排3列）。



#### 🏁 步骤 3 — 同步标签索引并闭环 (操作 `assets/tags-index.md`)

读取根目录 `assets/` 下的 `tags-index.md`，将新建组件的路径及双轴标签严格追加至对应的表格下，完成注册并向人类报告。


---

### 1. 写作风格与语法约束 (Style Guide)

* 整个技能文件必须无条件采用祈使句与不定式语法（动词先行）。
* 使用绝对客观的指导式语言，严禁出现第二人称指代（如"你"、"您"）。

### 2. 资产目录树规范与 Frontmatter 标准示例

```text
skills/工作效率类/W5-图片设计/
├── 详情页生成器.md                 # 本主控文件
├── references/
│   └── theme-palette.md          # 【全局设计令牌】控死背景色、字号级差、点缀元素
└── assets/
    └── components/               # 【无色相双元素骨架积木库】
        └── B2-成分意象三列阵列.md   # 示例文件如下

```

**组件文件 Frontmatter 强制规范示例：**

```markdown
---
type: component
tags: ["#中段核心", "#成分解析"]
visual_anchor: "#成分意象"          # 画面主角类型
anchor_scale: "局部占位 40%"        # 主角视觉重量
anchor_edge: "透明可穿插"          # 边缘避让规则：允许文字在Z轴轻微重叠

typography_layout: "#左侧多列阵列"   # 文字排版阵型
text_hierarchy: "H1 + H3 + Body"   # 本阵型所需确切文本层级
---
# 骨架空间与约束规范
- **排版结构布线 (DOM Tree)**：
  - `[挂载: 全局 Deco_Style]` ➔ 充当画面视觉边缘点缀，若无文案则隐藏。
  - `[挂载: 全局 H1_Size_Weight]` ➔ 承载核心成分名，左对齐。
  - `[Group: 卖点阵列区 / Repeater - 1排3列]` ➔ 用于处理具体的成分功效。
    - `[挂载: 全局 H3]` ➔ 特征小标题。
    - `[挂载: 全局 Body]` ➔ 详情正文。

```

### 3. 钢铁红线与高频犯错拦截（防呆防错集成门禁）

| 核心维度 / 场景 | AI 高频易错倾向 | 强制性拦截与唯一性规范要求 |
| --- | --- | --- |
| **全局视觉统一性** | 容易在生成不同屏时，私自更改字体大小级差或混用不同的点缀色组合。 | ➔ **硬性门禁：在当前全案生成中，每一屏的 H1/H3/Body 字号字重比例、点缀色必须严格锁定 `references/theme-palette.md` 下的唯一全局令牌，确保整页视觉高度内聚，严禁变脸。** |
| **输入端绝对收敛 (0 扩写)** | 遇到需要多组内容的复杂阵列骨架，但用户文案极简（如只有1句话）时，习惯自行"脑补"扩写或瞎编英文来填满排版。 | ➔ **硬性门禁：用户输入的文案是唯一真理！绝对禁止增删、扩写或"润色"原始文案。若文案体量不足以支撑当前排版阵型，强制触发动态降维，退回重新匹配极简骨架。** |
| **幽灵消除与空间收拢** | 当局部缺失某一非核心文本层级（如缺副标题）时，直接打印占位符，或者留下奇怪的巨大空白漏洞。 | ➔ **硬性门禁：无文案即无图层。** 彻底抹除未分配文案的层级后，其余文本图层必须**向上或向下物理收拢负空间**，由系统自动重算紧凑度，严禁排版视觉松散。 |
| **视觉锚点边缘越界** | 当视觉锚点设定为"实体硬边缘（如产品瓶身、数据面板）"时，文字排版依然侵入或遮挡主体。 | ➔ **硬性门禁：必须无条件服从组件设定的 `anchor_edge` 物理红线。若为实体硬边缘，在输出排版方案时必须强制写明安全避让指令，确保文本可读性。** |
| **产品外观一致性** | 不同屏之间产品颜色、材质、形状发生漂移。 | ➔ **硬性门禁：所有屏的 ImageFX Prompt 尾部必须追加 PRODUCT CONSISTENCY LOCK，锁定产品形状/颜色/材质/LOGO 在所有屏中严格一致。** |

## 5 大内容设计模式速查摘要 (Google ADK)

* **`tool-wrapper`**：监听关键词 → 动态加载 `references/` 规矩 → 按规则执行。
* **`generator`**：按步骤加载 style-guide 和 template → 填空式输出结构化文档。
* **`reviewer`**：加载 checklist → 审计代码/文本 → 按级别评分并输出建议。
* **`inversion`**：执行硬性逻辑防线 → 连续追问获取全约束 → 最终进行综合。
* **`pipeline`**：执行串行工作流 → 锁死每一步的 Checkpoint 确认 ➔ 方可向下推进。
