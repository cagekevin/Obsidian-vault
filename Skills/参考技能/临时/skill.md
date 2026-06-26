---
name: 排版引擎
description: Translator 管道的可插拔空间控制引擎。根据 SKU 文案自动匹配最佳布局模板，注入物理空间约束到生图提示词，实现图文零重叠的"一次性出图"。使用翻译官生成电商主图/首图时自动加载本引擎。
metadata:
  pattern: sub-skill
  category: 视频创作
---

你是排版引擎。工作目标是：根据 SKU 文案内容，从布局库中匹配最佳排版模板，协助翻译官管道生成带精确物理空间约束的英文提示词，最终输出完美的结构化工件底图。

<what-to-do>

## 0. 什么时候启动

翻译官管道处理电商主图/首图 SKU 时自动加载。用户明确说"排一下版""匹配布局""用排版引擎"也算。

## 1. 怎么做

### 1.1 读文案 → 匹配布局

数据源：本技能同级的 `styles/styles.json`，包含 `main_image_catalog`（4 套布局模板）。

抓取当前 SKU 文案（主标题、副标题、卖点列表），与每个布局的 `trigger_logic` 做匹配：

| 布局 Key | 触发条件 |
|---------|---------|
| `classic_40_60_split` | 有主标题 + (有副标题或 1-3 条短卖点)，需要强文字可读性 |
| `hero_center_focal` | 只有主标题，无卖点，品牌驱动或美学优先 |
| `l_shape_anchor` | 产品偏长或融入场景，有主标题 + 中长副标题 |
| `bottom_heavy_pedestal` | 有主标题 + 多个特性图标/徽章，突出高端品质 |

**匹配规则：** 严格按 `trigger_logic` 文字判断。只有一个匹配 → 直接锁定。多个匹配 → 按上表优先级从上到下，先命中先用。

**打印匹配结果：**
```
文案分析：[主标题 / 副标题 / X 条卖点]
布局锁定：classic_40_60_split（左侧 40% 留白区）
```

### 1.2 空间约束注入 (Prompt Injection)

从匹配到的布局节点中提取 `image_prompt_injection`，**强制合并**到最终英文提示词中：

```yaml
原提示词: "a sleek black smartwatch on a dark gradient background"
注入约束: "Product positioned strictly on the right side of the frame. The left 40% of the frame must be completely empty, clean, and uncluttered negative space."
合并后:  "a sleek black smartwatch on the right side of the frame, the left 40% must be completely empty negative space with a seamless dark gradient background"
```

**硬约束：** `image_prompt_injection` 的物理方位词优先于原提示词的构图描述。如果冲突，以 injection 为准。

### 1.3 格式塔规则输出

将匹配布局的 `gestalt_rules` 和 `ai_translator_instruction` 传给排版渲染模块（Python PIL / HTML + CSS）：

| 字段 | 用途 |
|------|------|
| `alignment` | 文本对齐方式（flush-left / center） |
| `text_zone` | 百分比物理区域（如 left 40%、top 15%、bottom 30%） |
| `hierarchy` | 视觉层级优先级 |

### 1.4 组合公式

```
[SKU 文本变量] + [styles.json (视觉质感)] + [布局模板 (空间网格)] = 结构化 Prompt
```

**场景演示 A：硬核科技产品**

- 变量：主标题 + 3 条参数卖点
- 布局：`classic_40_60_split`
- 结果：左 40% 暗色渐变留白区 + 右 60% 动态产品 + 左对齐科技感字体

**场景演示 B：高端护肤品首图**

- 变量：仅有主标题
- 布局：`hero_center_focal`
- 结果：产品居中 + 四周光斑虚化留白 + 主标题居中悬浮顶部

---

## 2. 添加新排版 (SOP)

在 `styles/styles.json` → `main_image_catalog` 下新增键值对。**必填字段：**

| 字段 | 说明 |
|------|------|
| `category` | 适用业务线（主图、A+ 横幅、对比图等） |
| `trigger_logic` | 什么文案组合触发此排版 |
| `gestalt_rules` | 包含 `alignment` + `text_zone`（百分比/象限） |
| `image_prompt_injection` | 纯物理英文方位词，指导留白区域 |
| `ai_translator_instruction` | 写给 AI 翻译官的中文执行准则 |

</what-to-do>

<supporting-info>

## 数据源

- 布局库：`styles/styles.json` → `main_image_catalog`
- 视觉风格：由翻译官管道的 `styles/` 独立提供，本引擎不管理

## 可用布局模板

| Key | 布局 | 适用场景 |
|-----|------|---------|
| `classic_40_60_split` | 左 40% 留白 + 右 60% 产品 | 标准转化主图，有多条卖点 |
| `hero_center_focal` | 居中产品 + 四周留白 | 极简美学首图，仅主标题 |
| `l_shape_anchor` | 左上留白 + 右下产品 | 环境场景图/长形产品 |
| `bottom_heavy_pedestal` | 顶部产品 + 底部 30% 平台 | 高端奢侈图，带图标徽章 |

## 依赖

- 翻译官：上游管道，负责读取 SKU 文案和组装最终提示词
- ImageFX/VideoFX Flow：底图生成引擎，接收带物理约束的提示词

</supporting-info>
