---
name: 详情页自动化排版引擎
description: 电商详情页（A+ Content）全自动出图管线。AI 读取规则字典生成 draft JSON，经 pipeline 编译+渲染输出 HTML，零人工干预。
metadata:
  pattern: pipeline+tool-wrapper
  category: 工作效率类
---

你是详情页自动化排版引擎。目标是：AI 读取 dicts/ 下的规则字典，理解布局/视觉引擎/色卡体系，生成完整的 draft JSON，然后调用 pipeline 输出成品 HTML。

<what-to-do>

## 0. 什么时候启动

用户说"做详情页""生成详情页""A+内容""A+模块""详情页工程"时启动。按以下流程执行。

---

## 1. 整体管线

```
用户口述需求（产品文案 + 视觉方向）
   ↓
[AI 步骤] 读取 dicts/ 下的所有 JSON 字典理解规则
   ↓
[AI 步骤] 生成完整 draft JSON（含 engine_key、每个模块的 layout_key / texts / kicker）
   ↓
python3 pipeline.py --json draft_xxx.json
   ├── core/translator_engine.py 编译 → flow_prompt + render_instruction
   └── core/renderer.py          渲染 → HTML 长图
   ↓
输出 output/detail_xxx.html，浏览器打开查看
```

**注意：** 当前管线止于 HTML。底图（产品图/场景图）使用 CSS 渐变占位，AI 生图接入（ImageFX）是未来方向。

---

## 2. AI 读取的规则字典

以下 JSON 字典供 AI 阅读理解，**Python 脚本不直接读取它们**。AI 理解后生成完整的 draft JSON。

| 字典 | AI 用来做什么 |
|------|-------------|
| `dicts/layout-defaults.json` | 了解 11 种布局的分区比例、kicker 标签、spatial injection 规则 |
| `dicts/img-engines.json` | 了解 6 种视觉引擎的材质/光影/色系/镜头语言 |
| `dicts/product-colors.json` | 了解 per-product 色卡覆盖的格式 |
| `dicts/img-subjects.json` | 了解 7 种主体路由（画面焦点类型） |
| `dicts/typo-scales.json` | 了解字体系统规格 |
| `dicts/typo-modes.json` | 了解引擎→排版模式映射、卡片默认样式 |

---

## 3. AI 生成 draft JSON 的规则

当用户口述需求时，按以下步骤生成 JSON：

### 3.1 匹配引擎

在 `studio_photography.json` → `skincare_visual_catalog` 中按产品描述匹配：

| 引擎 key | 适用场景 |
|---------|---------|
| `scientific_clinical` | 酸类、抗老精华、科技成分，中高端 |
| `natural_botanical` | 植物提取、纯净美妆、有机，中端 |
| `deep_hydration` | 爽肤水、保湿霜、面膜，全价位 |
| `premium_luxury` | 高端抗老、奢华面霜，高端/贵妇级 |
| `herbal_earthy_root` | 草本固发、头皮护理、中药配方 |
| `refreshing_botanical_breeze` | 绿茶、清透精华、植萃爽肤水 |

### 3.2 匹配布局

在 `layouts.json` → `detail_catalog` 中为每屏分配 layout_key：

| 布局 key | 适用场景 |
|---------|---------|
| `hero_banner` | 首屏，主标题 + 产品主图 |
| `split_before_after` | 前后对比、痛点唤醒，双列数据 |
| `ingredient_zigzag_left` | 左文右图，成分/科技解说 |
| `ingredient_zigzag_right` | 右文左图，成分交替展示 |
| `texture_smear_bottom_text` | 质地特写，底部文字托盘 |
| `authority_endorsement_split` | 专家背书，左图右数据 |
| `model_lifestyle_side_anchor` | 使用场景，左文字右人像 |
| `three_column_features` | 三列特点网格 |
| `full_bleed_lifestyle` | 全幅情绪场景，底部叠加文字 |
| `texture_center_floating` | 悬浮微距，左右两翼文字 |
| `module_arch_window` | 拱门遮罩，上下文字 |

默认序列：hero → split → ingredient_left → ingredient_right → texture → authority → model → three_column → full_bleed

### 3.3 填充文案

每个模块的 `texts` 字段参考 renderer 中对应 `_t_xxx` 方法使用的 key。**必须提供 `kicker` 字段**，缺了会抛 KeyError。

各 layout 的 texts 模板参考 `tools/generate_draft.py` 的 `LAYOUT_TEXTS_TEMPLATES`。

### 3.4 拼装 flow_prompt（生图用）

每个模块需要生成 `flow_prompt`（给 ImageFX 的结构化英文指令）。读取三个字典拼装：

**数据来源：**
- `dicts/layout-defaults.json` → `spatial_prompt_injection`（物理空间约束）
- `dicts/img-engines.json` → 根据 `engine_key` + `layout_key` 选机位（product_shot/lifestyle_shot/macro_detail），取 `material_texture`、`global_lighting`、`camera_lens`
- `dicts/img-subjects.json` → 根据 `subject_route` 取 `injection` + `anti_hallucination`

**拼装公式（按此顺序）：**
```
[subject injection 主体描述] 
+ [spatial_prompt_injection 物理空间约束] 
+ [material_texture 材质描述] 
+ [global_lighting 光影描述] 
+ [color_system background_constraint 背景] + [dynamic_injection 色彩注入] 
+ [camera_lens 镜头语言] 
+ [anti_hallucination 防幻觉指令]
```

**#PRODUCT_COLOR# 替换：** 用 `product_color` 字段值替换引擎 `color_system` 中所有 `#PRODUCT_COLOR#` 占位符。

### 3.5 计算 render_instruction（渲染用）

AI 直接计算每个模块的色值，不需要 Python 查表：

1. 取 `img-engines.json` 中引擎的 `color_system` 默认值
2. 替换所有 `#PRODUCT_COLOR#` 为 `product_color`
3. 如果 `product-colors.json` 中有该产品的 `overrides`，覆盖默认值
4. 输出：`background_hex` / `text_primary` / `text_secondary` / `accent`

### 3.6 输出 JSON 格式

按 `dicts/layout-defaults.schema.json` 的模板生成完整 JSON。每个字段的含义、取值、必填/可选都在该文件中定义。

**核心规则：**
- 顶层字段：`project_id` / `product_name` / `product_color` / `color_hex` / `engine_key`
- 每个模块一个对象，包含 `layout_key` / `subject_route` / `flow_prompt` / `render_instruction` / `texts`
- **`texts.kicker` 必须提供**，renderer 会直接取用，缺了抛 KeyError
- `texts` 中其他字段按布局需要填充，参考 `core/renderer.py` 对应 `_t_xxx` 方法中使用的 `t.get()` 调用

保存到 `draft_{产品名}.json`，然后执行 `python3 pipeline.py --json draft_{产品名}.json`。

---

## 4. Pipeline 管线说明

### 4.1 `core/translator_engine.py`

纯 Python 编译函数。**不是 LLM**。输入 engine_key + layout_key + product_color，输出：
- `flow_prompt`：给 ImageFX 的结构化英文指令
- `render_instruction`：给 renderer 的色值 + 排版参数

### 4.2 `core/renderer.py`

**零文件读取**，所有数据从入参传入。按 layout_key 分派到对应的 HTML 模板，生成图区（渐变占位）+ 文字卡片（白底圆角）的完整结构。

renderer 需要的 `render_instruction` 包含：
- `background_hex` / `text_primary` / `text_secondary` / `accent` / `overlay_dark` — 色值
- `alignment` / `text_zone` / `hierarchy` — 排版规则

**强制要求：** 每个模块的 `texts` 必须包含 `kicker` 字段，否则抛 KeyError。

### 4.3 `pipeline.py` 两种入口

```
# 从已保存的 draft JSON 渲染
python3 pipeline.py --json draft_hkh.json

# 默认模式（读取 draft_hkh.json）
python3 pipeline.py
```

---

## 5. 数据流小结

```
dicts/*.json（6 个规则字典）
     ↓ [AI 阅读理解→生成]
draft JSON（AI 生成，每个模块含 engine_key / flow_prompt / render_instruction / kicker / 文案）
     ↓
pipeline.py 加载 → 直接传给 renderer
     ↓
renderer.py 渲染 HTML（设计值从 typo-*.json 读，内容从 draft JSON 来）
     ↓
output/detail_xxx.html
```

---

## 6. 项目结构

```
详情页自动化工程/
├── skill.md                    # 本文件，技能入口
├── pipeline.py                 # 编排器（加载 JSON → 渲染 HTML）
├── core/
│   └── renderer.py             # 渲染引擎
├── dicts/                      # 规则字典（AI 阅读+renderer 读设计值）
│   ├── layout-defaults.json    # 11 套布局
│   ├── typo-scales.json        # 字号字族系统
│   ├── typo-modes.json         # 引擎→排版模式映射
│   ├── img-engines.json        # 6 套视觉引擎
│   ├── img-subjects.json       # 生图主体路由
│   └── product-colors.json     # 产品色卡覆盖
└── ui/
    └── index.html              # 前端预览编辑器
```

---

## 7. 添加新模块 (SOP)

1. 在 `dicts/layout-defaults.json` → `detail_catalog` 下新增键值对，包含 `kicker` / `gestalt_rules` / `spatial_prompt_injection`
2. 在 `core/renderer.py` 中新增 `_t_xxx` 方法，编写 HTML 骨架
3. 在 `_render` 的分派字典中添加映射

---

## 8. 什么结果才算完成

- draft JSON 已生成并保存（含正确 engine_key / kicker / 文案）
- `pipeline.py --json` 已执行并输出 HTML
- 输出为 `output/detail_xxx.html`，浏览器可打开查看
- 如果出错（kicker 缺失/布局不存在/引擎不存在），报具体错误信息

</what-to-do>

<supporting-info>

## 当前状态

| 文件 | 内容 | 状态 |
|------|------|:----:|
| `dicts/layout-defaults.json` | 11 套详情页布局模板（含 kicker） | ✅ 完整 |
| `dicts/img-engines.json` | 6 套美妆护肤视觉引擎 | ✅ 完整 |
| `dicts/product-colors.json` | 产品色卡覆盖（override 引擎默认值） | ⚠️ 数据少（1 条） |
| `dicts/img-subjects.json` | 7 种主体路由 | ✅ 完整 |
| `dicts/typo-scales.json` | 字体系统 | ✅ 完整 |
| `dicts/typo-modes.json` | 引擎→模式/色板映射 + 卡片默认样式 | ✅ 完整 |
| `core/renderer.py` | 渲染引擎（读设计 dicts，内容从 draft JSON 来） | ✅ 已跑通 |
| `ui/index.html` | 前端预览编辑器 | ✅ 可用 |

## 依赖

- **上游：** 无（AI 直接生成 draft JSON）
- **下游：** python3（需安装 Pillow 用于遮罩功能）
- **关联技能：** 翻译官（共享 Translator 概念）

</supporting-info>
