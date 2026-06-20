---
name: 电商主图
description: Generate high-conversion Chinese e-commerce main product image prompts or reverse-engineer reference images into Theme Bundles. 支持双模引擎：文本输入生成 / 图片上传提取。专为电商主图场景设计，覆盖淘宝、天猫、1688、京东等平台的主图生成需求，支持批量多产品主图生成、卖点排版自动路由、风格匹配与全家桶注入。Use when user needs Taobao, Tmall, 1688, JD main product images, e-commerce prompts, or reverse-engineering reference images. Optimized for codeBuddy.
metadata:
  pattern: pipeline+generator
---

# 电商主图架构师 — 双模引擎

双模触发规则：
- **MODE A [文本输入]:** 用户输入需求 → 激活生成模式
- **MODE B [图片输入]:** 用户上传图片 → 激活提取模式

<what-to-do>

## MODE A: 生成模式

状态默认进入 **[咨询中]**，严格按以下 4 个阶段执行。

### 批量模式指令
若用户输入的是多产品列表（如 10 个产品）：
1. 将同一个 `[Theme Bundle]` 应用到所有产品，禁止切换视觉风格
2. 对每个产品按 Phase 4 的 [Output Formula] 生成一段独立提示词
3. 将所有提示词组装为批量 JSON 配置（`prompts` 数组），保存到 `input/` 目录下
4. 输出批量执行的终端命令

### Phase 1: Controller（无损解析与降噪）
1. **无损提取：** 包含成分、浓度、型号的词块（如"出油因子-99.3%"）原封不动保留，严禁拆分。纯时间/数量词（如"1次"、"1滴"、"KO"）标记为 `{Highlight_Number}` 准备极致放大。
2. **垫图路由无感化 (Blind Image Ingestion)：** 无条件取消任何关于产品物理外观的文本推演与提取。引入强制变量 `{product_image}`（作为用户真实产品图的 URL 占位符），仅聚焦于排版和环境的构建。
3. **容量熔断分配：**
   - **大标题 (Title1):** 最强核心承诺（1 条短句）
   - **副标题 (Title2):** 痛点或支撑点（1 条短句）
   - **底部横幅 (Banner):** 左侧背书/促销，右侧核心成分
   - **信息角标 (Stickers) — 自动路由：**
     - <= 3 个卖点 → 【角标路线】，`Sticker Snippet`（圆标/盾牌/徽章）
     - 4-5 个卖点 → 【清单路线】，`Checklist Snippet`（垂直打钩清单）
     - > 5 个卖点 → 强制降噪至最多 5 项后走清单路线
4. **风格嗅探 (Theme Matching)：** 若用户未显式指定风格，AI 必须基于产品词义（如"保湿"自动匹配"蓝白科技风"）从 `ecommerce-image/references/theme-bundles/` 目录中自动推选一个最匹配的套装，供用户在 Phase 2 确认。

### Phase 2: Verification（确认校验点）
输出结构化方案后**强制停止等待回复**：

> "✅ 视觉架构已生成！请确认排版方案：
> 📍 大标题：{Title1} *(巨幅放大：{Highlight_Number})*
> 📍 副标题：{Title2}
> 📍 展现形式：{角标路线 <=3 / 清单路线 4-5}
> 📍 卖点内容：{Payload_Badges / Payload_Checklist}
> 📍 底部横幅：{Banner 左} → {Banner 右}
> 📦 调用全家桶套装：{匹配的 Theme_xxx}
> 🔗 产品形态：已锁定为 {product_image} 垫图模式，AI提示词将不包含任何产品外形文字描述。
> 是否准确？回复"确认"开始渲染。"
*(CRITICAL: STOP GENERATING HERE. WAIT FOR USER REPLY.)*

### Phase 3: Bundle Assembly（全家桶注入）
用户确认后，加载 `ecommerce-image/references/theme-bundles/` 下对应的 `[Theme Bundle]` 文件。将解析好的数据注入到该套装的 `[Inject: Text]` 槽位中。

**自动路由：**
- 1-3 个卖点 → 注入 `Sticker Snippet`
- 4-5 个卖点 → 注入 `Checklist Snippet`

### Phase 4: Spatial Narrative Output（视觉平衡与结构引擎）

生成最终提示词后，自动构建为可直接执行的 `.json` 配置文件，保存到用户项目 `input/` 目录下（文件名：`[产品名]-[描述]-[模板名]-config.json`）。

**输出文件命名规则：**
```
[产品名]-[描述]_[模板名]_V1.png    ← 首次跑
[产品名]-[描述]_[模板名]_V2.png    ← 同模板改提示词/尺寸
[产品名]-[描述]_[其他模板]_V1.png  ← 换模板（模板名变，版本重置）
```
模板名放在文件名中可一眼识别出处，版本号 `_V1/_V2` 仅对同一模板的迭代计数。防止重复跑图覆盖旧输出。落盘成功后，在对话框提示用户配置文件已就绪，并输出终端命令让用户自行执行。

**聊天界面输出格式：**
1. 在聊天界面中输出最终提示词的连续英文段落（严禁代码块或 UI 缩进，中文用 `""` 包裹）
2. 附上 JSON 配置文件路径和终端执行命令
3. **不直接调用 Lovart API**，用户自行在终端执行命令
4. **输出质量检查清单，逐项标注已通过：**

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | **负空间压缩** | 若 Bundle 背景为浅色/白色系 → padding 压缩至 5-8%，产品占画幅 65-75%；深色/暖色系保持 10-15% |
| 2 | **文案忠实度** | H1 / H2 / 清单项 / 角标文字 / 横幅文字与排版信息 **一字不差** |
| 3 | **Highlight_Number** | 排版信息中标记放大的数字已在 prompt 中处理颜色和 2.5x 倍率 |
| 4 | **配件/特殊元素** | 刮痧板、容量圈等全部在 prompt 中体现，垫图路径已包含 |
| 5 | **模型与比例** | `model`、`aspect_ratio`、`resolution` 满足用户要求，`output_dir` 符合命名规则 |
| 6 | **文字视觉权重** | 标题字号足够大、文字周围内边距最小化以突出文字，与产品形成清晰的视觉主次关系 |

**终端命令：**
```bash
python <skills目录>/工作效率类/W7-API链接/lovart-skill/run_image_generator.py <config.json路径>
```
将 `<skills目录>` 替换为实际 `skills/` 的绝对路径，将 `<config.json路径>` 替换为 JSON 配置文件的实际路径即可执行。无需手动阅读 W7 技能文件。

**JSON 配置文件结构**（符合 `CONFIG.md` 标准 schema）：
```json
{
  "name": "[产品名]-电商主图",
  "prompt": "[Output Formula 生成的完整提示词]",
  "aspect_ratio": "1:1",
  "resolution": "1K",
  "model": "generate_image_gpt_image_2_medium",
  "output_dir": "{项目根目录}/output/[产品名]-主图_V1.png",
  "reference_image_paths": ["G:/项目路径/input/垫图.png"]
}
```

**布局分层逻辑（重力锁死 40/60 分割）：**
1. **结构层 (Banner):** 始终固定在底部边缘，满版或容器同宽，Banner 是画面的"地基"，绝对禁止偏移或滑动。
2. **40/60 垂直动感分割 (Vertical Dynamic Split):**
   - **左侧 40%** — 超密度左对齐排版区。所有文字群、清单容器、徽章必须严格约束在此左列内，贴紧不可见的垂直边界框。右侧边缘须对齐整齐，防止参差不齐的布局。
   - **右侧 60%** — 产品主导区。将产品尽可能放大，使其成为布局的视觉锚点。产品应动态溢出网格，略微叠压左侧排版区的右边缘以营造层次感，消除中间尴尬间隙。
   - **留白重力:** 不要在左右之间平均分散元素。仅在产品和顶部/底部的右后方保留有意的扫风式留白（右上和右下象限），让布局看起来昂贵且经过设计，而非空旷。
3. **模块化容器约束 (Container Modularity):** 所有文字/角标/清单必须渲染为"紧锁的垂直模块化容器"，具有统一的 padding 和内联间距。清单项严格按容器左侧基准线对齐。**严禁**元素像贴纸一样均匀散落在画面各处——必须通过格式塔亲密性原则（Gestalt Proximity）将相关信息紧凑成组，形成可识别的独立区块。

**属性继承规则：**
1. 从当前 Theme Bundle 读取主题色替换 `[Inject: Theme Color]`
2. 将排版信息的文案填入对应 `[Inject: Text]` 槽位
3. **负空间比例以 Output Formula 的 CRITICAL PADDING 为准**，忽略 Bundle Spatial Framework 中可能遗留的百分比数值（向后兼容）。Bundle 只控制留白方位（哪边留白），不控制留白数值（留多少）

**ImageFX 提示词黑话转换规则：**
底层模型对网页前端术语（padding、margin、auto layout）感知较弱，但对摄影构图和物理遮挡关系高度敏感。在最终提示词中必须做以下翻译：

| 不要写 | 要写 |
|--------|------|
| Add margin right | Ultra-wide negative space on the right hemisphere |
| UI container alignment | Tightly clustered graphical overlay, may overlap the main subject by no more than 15% |
| padding between elements | Intentional breathing room with strict physical separation |
| left-aligned text | Text anchored to a rigid left vertical axis |
| element spacing | Text scaled generously with minimal internal padding, ensuring maximum readability |
| container background | A self-contained graphical panel with its own material properties |

**[Output Formula]:**
```text
{product_image} An 8k resolution, photorealistic e-commerce product image featuring the product from the reference link, front view, 5-15 degree tilt, occupying 50-60% of the canvas. The entire composition strictly follows the environment and lighting of [Inject: Theme Bundle's Environment Palette].

CRITICAL ENVIRONMENTAL CONSTRAINT: DO NOT generate any floating objects, particle effects, or props based on the product's functional keywords unless explicitly stated in the Theme Bundle's Environment Palette.

CRITICAL UI CONSTRAINT: All graphical containers, banners, ribbons, and badges must be rendered with strict vector-style geometric precision. Absolute zero organic curves, rough edges, wobbly borders, or painted textures on structural elements.

[Inject IF Layout is Flush-Left (靠左排版)]: "The composition strictly mandates a 40/60 vertical dynamic split. The left 40% is a flush-left typographic zone tightly constrained within an invisible bounding box. All injected UI containers and text must strictly align to the left axis of this zone, maintaining clean, deliberate spacing without random scattering. Each typographic element is generously proportioned with minimal internal padding to maximize text prominence. The right 60% is dominated entirely by the main product. CRITICAL PADDING: Scale the product to ensure at least 10-15% absolute negative space from the top and bottom edges of the canvas. The product slightly overlaps the rightmost edge of the left typographic zone."

[Inject IF Layout is Centered (居中排版)]: "The composition strictly mandates a perfectly symmetrical, centered editorial layout. The main product is anchored dead-center. CRITICAL PADDING: Ensure at least 10-15% absolute negative space from the top and bottom borders. The primary typographic zone is locked directly to the top-center axis. All injected secondary UI containers and badges must align symmetrically along the central vertical axis, maintaining clean, deliberate spacing without random scattering. Maintain massive, balanced negative space framing the outer edges."

[Inject IF Layout is Flush-Right (靠右排版)]: "The composition strictly mandates a 60/40 vertical dynamic split. The left 60% is dominated entirely by the main product. CRITICAL PADDING: Scale the product to ensure at least 10-15% absolute negative space from the top and bottom edges of the canvas. The right 40% is a flush-right typographic zone tightly constrained within an invisible bounding box. All injected UI containers and text must strictly align to the right axis of this zone, maintaining clean, deliberate spacing without random scattering. The product slightly overlaps the leftmost edge of the right typographic zone."

At the [Inject based on Layout: top-left / top-center / top-right], written in a massive, ultra-bold, glowing font is the prominent text "[Inject: Title1]". [Inject IF {Highlight_Number} exists: "Ensure the specific characters '{Highlight_Number}' are rendered 2.5x larger and bolder than the rest of the text, creating a massive visual impact"]. Directly below it, in a slightly smaller clean font, is the text "[Inject: Title2]".

[Inject IF <=3 items: "The completely translated Spatial English Snippet for Sticker Snippet... Rendered as a tightly locked container block with uniform padding and strict internal alignment."].
[Inject IF >3 items: "The completely translated Spatial English Snippet for Checklist Snippet... Rendered as a tightly locked vertical container block with uniform padding and strict internal flush-left alignment."].

[Inject IF user provided Banner text: "The completely translated Spatial English Snippet for the Banner... Ensure it contains the text '{Banner}'." ELSE: SILENTLY OMIT THIS ENTIRE SENTENCE AND ENSURE NO BANNER IS RENDERED].

Negative prompt: ugly, deformed, mutated, twisted product bottle, messy background, watermark, low resolution, cheap 3d render, overlapping text, unnatural lighting, generic typography, scattered text, floating stickers, loose layout.
```

---

## MODE B: 提取模式

用户上传图片时，像资深美术指导一样反向拆解：

**Step 1: 视觉比对**
扫描图片风格，与 `ecommerce-image/references/theme-bundles/` 目录中现有 Theme Bundles 比对：
- 高度相似 → 告知用户"该风格已存在，建议直接使用 [Theme_X]"
- 新风格 → 触发 Step 2

**Step 2: 逆向提取**
无论原图展示角标还是清单，都必须基于该图的**视觉海报设计系统**，同时输出（推演） `Sticker Snippet` 和 `Checklist Snippet`。严禁干瘪的文本描述，必须包含容器底衬、材质与排版阵型。

**缺失推演法则 (Missing Element Inference)：**
提炼的 Theme Bundle 必须是 100% 完整的高可用全家桶。若原图中缺失某一部件（如原图根本没有底部 Banner，或没有 Checklist），严禁留空或写"无"。AI 必须基于已提取的 Typography & Iconography 美学基调，顺延推演出该部件应有的样子补齐坑位。（例如：原图无 Banner，但整体是磨砂玻璃风，则推演出"底部是一条边缘发光的磨砂玻璃质感长条底座"）。

**模板自检清单（每次输出前必须逐条对照，全部通过才可落盘）：**

| # | 检查项 | 通过标准 |
|---|--------|---------|
| 1 | **标题格式** | `### [Theme_命名]（简要风格描述）`，H3 + 括号描述后缀 |
| 2 | **字段格式** | 全部使用 `- **Field:**`（连字符 + 双星号 + 冒号 + 空格），禁止 `* **` |
| 3 | **字段完整性** | 恰好 6 个字段：Environment Palette / Typography Style / Spatial Framework / Sticker Snippet(<=3) / Checklist Snippet(>3) / Banner Snippet |
| 4 | **Typography 分层** | 必须拆分为 H1 / H2 / Deco / Body / Highlight Numbers 五层子字段，每层描述字效与材质，禁止写具体文案 |
| 5 | **Sticker 后缀** | 必须标注 `(<=3 Items)` |
| 6 | **Checklist 后缀** | 必须标注 `(>3 Items)` |
| 7 | **零具体文案** | 全文件禁止出现任何产品实际文案（如"1秒卸全妆"、"纯氨基酸"），仅使用"关键数字"、"重点文字"等泛指标注 |
| 8 | **零留空/零"无"** | 每个字段必须有实质性描述，违反缺失推演法则的顺延补齐 |
| 9 | **Banner 物理材质** | 描述底衬形态、材质、色号趋势、边缘处理（如"斜切边缘的渐变色长条底座"），不是纯文字描述 |
| 10 | **留白重心描述** | Spatial Framework 中必须明确对齐轴（如"严格左对齐"）+ 留白区域方位（如"右上象限留白"）。**禁止出现具体负空间百分比数值（如10-15%）**，留白比例由 Output Formula 的 CRITICAL PADDING 统一控制 |


**输出格式（纯自然语言描述）：**
```text
✅ 已识别：新风格！已为你提取全家桶套装：

#### [Theme_自定义命名]
* **Environment Palette:** [提取环境背景色、光影氛围，为产品预留空间]
* **Layout Skeleton & Negative Space (空间骨架与留白):** [强制提取画面的整体排版网格。必须明确指出：1. 主视觉动线与对齐轴（如"所有文本和角标严格沿着左侧垂直基准线对齐"）；2. 留白重力（如"右侧大面积留白以突出产品"）。此骨架必须在生成时锁定UI元素的活动范围]
* **Typography & Iconography (美术字效与图标质感):** [提取主副标题字效(如金属渐变、3D白玉发光)、小图标材质(如极简线稿、发光圆点)，这是全套主题的美学基调]
* **Sticker Snippet (<=3 Items 阵型):** [基于原图设计语言，推演低负载排版。例如：不只是"角标"，而是"3个左侧对齐的半透明磨砂玻璃卡片，内嵌发光图标"等复杂视觉容器布局]
* **Checklist Snippet (>3 Items 阵型):** [基于原图设计语言，推演高负载排版。例如：不只是"打钩"，而是"右侧4行带有金属分割线的梯度色块矩阵"等复杂视觉容器布局]
* **Banner Snippet:** [提取底部横幅的物理形态与材质，如"带有斜切边缘的渐变色长条底座"]
```

提取完成后，将上述完整的 `[Theme_自定义命名]` 结构化数据以独立文件形式写入 `ecommerce-image/references/theme-bundles/` 目录下（文件名：`[Theme_自定义命名].md`），并更新 `theme-bundles.md` 索引表。完成后向用户反馈库更新成功。

</what-to-do>

<supporting-info>

## Theme Bundle 库

预设组件定义在 `references/theme-bundles.md`，主题全家桶独立存放在 `references/theme-bundles/` 目录下，Phase 3 时动态加载。

**完整 Bundle 清单请查看** [`references/theme-bundles.md`](references/theme-bundles.md)（唯一数据源，禁止在别处重复罗列）。

**新增 Bundle 标准模版**（每个独立 `.md` 文件必须包含）：
```text
#### [Theme_命名]
* **Environment Palette:** [...]
* **Typography Style:** [...]
* **Spatial Framework (空间与留白基准):** [网格对齐方式 + 留白重心]
* **Sticker Snippet:** [...]
* **Checklist Snippet:** [...]
* **Banner Snippet:** [...]
```

</supporting-info>
