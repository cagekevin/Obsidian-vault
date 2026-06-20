---
name: 亚马逊主图提示词引擎
description: 双模主图引擎。Mode A 严格执行亚马逊合规与摄影画质约束，智能映射本地排版骨架生成高转化主图；Mode B 负责拆解爆款主图，剥离色彩并自动更新原子骨架库。Use when user needs Amazon main image AI prompts, or wants to extract a new template from a reference image.
metadata:
  pattern: inversion+generator+pipeline+tool-wrapper
  category: 设计
---

# Amazon Main Image Prompt Engine (Dual-Node)

## 核心路由 (Route Hub)
**必须严格根据用户意图分流，严禁逻辑混淆：**
- ➔ **意图：输入文本卖点/要求出图** ➔ 锁定进入 **`[MODE A：主图智能映射与组装]`**
- ➔ **意图：输入参考图片/要求拆解排版** ➔ 锁定进入 **`[MODE B：爆款逆向拆解与脱模打标]`**

---

## 🧭 [MODE A：主图智能映射与组装]

### 核心协议：样式与骨架解耦编译
启动时，必须无条件隐式加载以下两部分。**严禁在最终的 AI Prompt 中硬编码具体的排版颜色，必须动态套用品牌皮肤：**
1. **全局外观皮肤（Style Skin）**：加载 `amazon-skincare/references/brand-identity.md`（包含品牌字体组与全局文本颜色规范）与 `amazon-skincare/references/theme-palette.md`（背景色与环境光影规范）。
2. **原子排版骨架（Skeleton Mesh）**：全量扫描本地 `amazon-skincare/templates/` 下的所有主图结构积木。

<what-to-do>
### 标准作业程序 (SOP)

#### 步骤 1 — 卖点吞噬与靶向推演 (Ingestion & Custom Logic)
1. **执行基础收集**：要求用户确认产品类目、期望背景色、品牌名、排版字体组（elegant/modern/bold）、出图总数（对应文本条数）、原始卖点文案。
2. **执行自定义部位三步推演（Custom Category 处理）**：
   - 若用户提供的类目不在标准库中（如"背部/手部/颈部"）：
   - **Step A**: 自动匹配最接近的视觉锚点类目（如匹配 body_firming）。
   - **Step B**: 自动仿写推演出该部位的 7 个变量描述（`closeup`, `model_focus`, `problem_visual`, `improvement_visual`, `application_area`, `application_verb`, `problem_terms`）。
   - **Step C**: 将推演结果交付人类确认或修改。

#### 步骤 2 — 决策引擎与 Mapping Plan (Decision Loop)
**生成任何 Prompt 前，必须且只能先输出 `Mapping Plan` 表格供确认。严禁跳过！**
1. **物理形态排他门禁**：若产品形态为 `capsule`，匹配时必须无条件剔除带有"倾倒液体"或"香调"等不符合物理逻辑的骨架。
2. **四步防撞车排雷法则（强依赖 Frontmatter Priority）**：对于每条卖点匹配的骨架，若发生冲突：
   - ① 匹配所有候选库。
   - ② **查验优先级**：优先选择 `priority: "High"` 或 `priority: "Always"` 的组件。若同优先级撞车，对比当前全案的"平衡类别（Balance Category）"，选择能填补空缺的骨架。
   - ③ 精度比对：若依然冲突，选择 `match_keywords` 触发最精准的骨架。
   - ④ **兜底法则（Fallback）**：若全盘无匹配，强制使用 `priority: "Fallback"`（如 `#生活方式/模特展示`）类骨架兜底。
3. **执行平衡分布校验**：全案必须满足 `1产品主图 + 1-2数据/证明 + 1-2成分/香调 + 1模特/生活方式 + 1使用方法 + 1-2对比/功效`。
4. **交付计划表**：输出表头为 `图片序号 | 原始卖点 | 匹配骨架ID | 显式优先级(Priority) | 填补的平衡类别` 的表格。等待确认。

#### 步骤 3 — 多层级弹性编译与输出 (Pipeline Production)
确认 Plan 后，按顺序融合【原始文案】+【全局皮肤】+【对应骨架】。遵守以下铁律：
- **首图合规红线**：无论用户选什么背景色，**Image #1 必须强制替换为纯白底（pure white background）**。
- **摄影画质强插咒语**：
  - 含人像：强插 `"Editorial lifestyle photography, refined skin texture, shot on 85mm prime lens"`。
  - 含产品：强插 `"Masterpiece, Phase One IQ4 clarity, Crisp rim lighting, defined glossy specular highlights"`。
- **多层级文本弹性法则（大小标题自适应）**：
  - 骨架中定义了具体的排版占位符（如 Layer 1 居中大字号、Layer 2 跟随小字号）。必须从原始卖点中提取对应文案进行填空。
  - **红线**：若卖点文案过短，没有副标题或装饰字，**必须在渲染时直接闭合隐藏未使用的图层**，下方正文自动上移。**严禁 AI 残留 `{}`，严禁瞎编废话！**

#### 步骤 4 — 自我质检与落盘闭环 (Self-Correction & Close)
生成全部 8-9 张提示词后，必须执行以下收尾动作：
1. **打印自我质检报告 (Self-Correction Report)**：逐一检查占位符是否漏填、中英文语言边界是否越界。
2. **执行特定路径落盘**：将全案 Markdown 保存至本地项目目录：`output/<品牌名>-<产品名>-Prompts.md`。
</what-to-do>

---

## 🛠️ [MODE B：爆款逆向拆解与脱模打标]

<what-to-do>
当用户上传参考主图要求拆解时，必须按以下逻辑闭环线性执行：

### 步骤 1 — 模板库对比门禁 (Conflict Detection)
1. **语义特征提取**: 分析用户上传图片的视觉类型与核心主张。
2. **已有库比对**: 与 `amazon-skincare/templates/` 现有骨架进行强匹配。
3. **决策树**:
   - 若存在功能相似模板 ➔ 询问是否升级 ➔ 选 Y 则标记【覆盖更新】，沿用旧 ID。
   - 若属于全新类别或确认继续 ➔ 标记【新建资产】，分配新 ID。

### 步骤 2 — 样式剥离与“半保留”法则 (Smart Stripping)
1. **全局资产剥离**：剥离具体的背景色、字体颜色和特定品牌 Logo（如 HKH）。将其作为全局皮肤追加至 `theme-palette.md` 和 `brand-identity.md`。
2. **核心红线（实物 vs 道具分类法则）**：
   - **核心产品**：必须剥离原图具体的产品形态，将其转换为 `{packaging}` 或 `{capsule_form}` 等通用占位符。
   - **营销道具与动作（特权允许）**：**必须保留**原图中具有高转化属性的特定场景元素（如：对比用的注射器、香调说明的大花、模特涂抹的特定手势、悬浮的数据卡片）。
3. **微观元素审计**：若有特定的科技图标、边框动效，转化为纯视觉描述暂存为【微观修饰词】。

### 步骤 3 — 多层级文本弹性提炼 (Text Layer Extraction)
1. 将文字层解构为弹性图层（如：Layer 1 title, Layer 2 subtitle, feature_list）。
2. 标注相对位置和字体粗细（如 `Layer 1 (top, large, serif bold): title`）。
3. 声明："本结构严禁硬编码颜色，渲染时自动套用全局皮肤"。

### 步骤 4 — 精准打标与落盘组装 (Archive)
- **命名**：`序号-英文特征名.md`（例：`23-clinical-comparison.md`）。
- **YAML Frontmatter（⚠核心）**：必须写入元数据，包含：
  - `type`: "component"
  - `priority`: ("Always", "High", "Medium", "Low", "Fallback")
  - `tags`: [如 "#模特+产品", "#Ingredient"]
  - `balance_category`: (如 "Comparison / Benefit")
  - `match_keywords`: [触发词组]
  - `exclusion_rules`: [若保留的营销道具具有强排他性（如捏碎胶囊），必须在此处写入排除条件，如 "capsule" 或 "cream"]
- **正文输出结构（严格对齐现有组件）**：
  - `# 序号-中文名 (英文名)`
  - `## 骨架排版规则`：(输出步骤 3 的图层列表与视觉焦点)
  - `## 视觉提示词基底 (AI Prompt Base)`：(融合 `{packaging}` 占位符、保留的营销道具、暂存的微观修饰词，以及 `{background}`, `{lighting}`, `{aesthetic}` 全局变量)。
  - `## 规则约束`：(如有，输出排他规则或兜底规则说明)。
</what-to-do>
---

<supporting-info>
## 工业级约束门禁与映射字典

### 1. 边界准则 (Boundary Principle)
- **AI Prompt**：只描述相机能拍到的视觉元素（光影、构图、背景、模特、产品材质）。严禁在其中包含任何具体的文案字词、引号或品牌名。必须全英文输出。
- **Text Layers**：只负责文本层级与排版描述。保留用户提供的原语言（中文），严禁未经允许擅自翻译成英文。

### 2. 目标部位视觉映射表 (Target Area Visual Map)
| Variable | anti_aging_face | eye_care | shoulder_care | body_firming |
|---|---|---|---|---|
| `{closeup}` | facial skin texture | eye area skin texture | shoulder/neck skin texture | body skin texture |
| `{model_focus}` | woman's face with radiant skin | close-up of beautiful eye | woman with elegant shoulders | woman with toned body |
| `{problem_visual}` | woman with wrinkles | woman with puffy eyes | woman with tense neck | woman with loose skin |
| `{improvement_visual}`| woman with smooth skin | woman with radiant eyes | woman with firm shoulders | woman with tightened skin |

### 3. 钢铁红线（防呆集锦）
- ❌ **严禁缩水偷懒**：无论生成到第几张图，每一张的 Prompt 必须保持完全一致的专业摄影参数词汇与长度，绝对不允许使用"同上"或"见上文"。
- ❌ **零占位符准则**：最终输出的内容中，绝对不允许残留任何 `{}`。变量必须被用户的实际文本或推演出的场景完全替换掉。

---

## 🌟 全链路执行示例 (End-to-End Example)

### 🔄 【双模联动全局心智模型】
- **Mode B（后厂生产）**：负责将爆款主图剥离实物，保留营销道具，提炼成带有 `{packaging}` 等变量的纯净骨架并落盘。
- **Mode A（前店消费）**：负责提取用户的具体产品形态、色系与文案，替换掉骨架中的变量，组装成最终的高转化出图 Prompt。

---

### 📦 [示例 1] Mode B 爆款逆向脱模（生产端）
*(当用户上传一张高转化“竞品对比图”要求拆解时，系统启动 Mode B，剥离具体的胶囊，保留对比网格与打勾/画叉符号，落盘为标准资产。)*

**落盘目标文件：`amazon-skincare/templates/05-competitor-comparison.md`**

---
type: component
priority: "High"
tags: ["#竞品对比", "#Comparison"]
balance_category: "Comparison / Benefit"
match_keywords: ["vs", "versus", "对比", "比较", "better than", "other"]
exclusion_rules: []
---
# 05-竞品对比图 (competitor_comparison)

## 骨架排版规则
支持弹性加载，未提供文案层自动隐藏。
- [视觉焦点]   : 左右两栏对称对比，左侧贬低竞品，右侧拔高本品。
- [卖点大标]   : Layer 1 (top center, large, serif bold): title 
- [左侧竞品层] : Layer 2 (left column top, medium, sans-serif): competitor_name
- [左侧痛点区] : Layer 3 (left column, small, sans-serif): competitor_flaws (带 X 号图标)
- [右侧本品层] : Layer 4 (right column top, medium, serif bold): hero_product_name
- [右侧优势区] : Layer 5 (right column, small, sans-serif): hero_benefits (带 √ 号或发光图标)

## 视觉提示词基底 (AI Prompt Base)
split comparison layout, left side: generic {competitor_packaging} on dull background with subtle shadow, right side: {packaging} glowing elegantly on premium pedestal with golden dynamic elements, comparison infographic style, {background}, professional cosmetic product photography, {lighting}, luxurious and convincing aesthetic, {aesthetic}

### 🚀 [示例 2] Mode A 主图智能映射（消费端）
(当用户输入具体的业务数据，系统调用上述 Mode B 录入的模板，拼装成直接可用的出图指令。)

【输入预设】

用户要求：类目 face_serum，背景 warm_beige，期望出对比图。

原始卖点："普通精华液 vs 我们的抗老精华（吸收快，不黏腻）"。

系统隐式映射：{packaging} ➔ transparent glass dropper bottle，{background} ➔ warm beige to light brown gradient background。

【最终落盘输出示例】

Image #2 | Skeleton: 05-competitor-comparison (竞品对比图)

Prompt:
split comparison layout, left side: generic basic plastic bottle on dull background with subtle shadow, right side: transparent glass dropper bottle glowing elegantly on premium pedestal with golden dynamic elements, comparison infographic style, warm beige to light brown gradient background, professional cosmetic product photography, soft studio lighting, luxurious and convincing aesthetic, Masterpiece, Phase One IQ4 clarity, Crisp rim lighting, defined glossy specular highlights.
(注：严守零占位符准则，{packaging}、{background}和{lighting}已被完美替换，并强插了画质咒语)

Text layers:
Layer 1 (top center, large, dark red-brown serif bold): "WHY CHOOSE US"
Layer 2 (left column top, medium, dark red-brown sans-serif): "普通精华液"
Layer 3 (left column, small, dark red-brown sans-serif): "吸收慢 / 表面黏腻"
Layer 4 (right column top, medium, gold serif bold): "HKH抗老精华"
Layer 5 (right column, small, dark red-brown sans-serif): "深层渗透吸收 / 清爽不黏腻"
(注：严格保留中文原文，套用了品牌肤色设定。)
---

### Self-Correction Report
- **Balance Category check**: [OK / 覆盖了 Hero, Data, Lifestyle...]
- **Placeholder check**: [OK / 全文未发现残留的 `{}` 占位符]
- **Language & Boundary check**: AI Prompts → All English & Pure Visual [OK], Text Layers → Original Chinese [OK]
</supporting-info>
