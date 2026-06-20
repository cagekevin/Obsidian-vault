# 海报生成 2 层管线 + 图像反推 Skill

基于 [ComfyUI-dapaoAPI](https://github.com/paolaoshi/ComfyUI-dapaoAPI) 工作流精简，保留完整系统提示词。

## 能力

此 CLI 提供三种模式，对应原工作流的三个核心节点：

| 模式 | 对应原节点 | 输入 | 输出 |
|------|-----------|------|------|
| `generate` | dapao_ecommerce_node.py | 文本需求 | 最终英文 Prompt（JSON） |
| `generate --two-pass` | CR Text任务说明 + Gemini + 第2层 | 文本需求 | 分析稿 + 最终 Prompt |
| `reverse` | Gemini 图像反推 | 图片 + 风格模板 | 图像详细描述 |

## 用法

### 前置

```bash
pip install requests
set LLM_API_KEY=sk-你的密钥
```

### 生成海报提示词

```bash
# 快捷单层
python poster.py generate --auto "产品类型：粉底液，卖点：遮瑕持久，风格：简约 Ins 风，数量：5"

# 双层（先分析需求稿，再生成最终 Prompt）
python poster.py generate --two-pass --auto "产品类型：粉底液，卖点：遮瑕持久，风格：简约 Ins 风，数量：5"

# 交互模式
python poster.py generate
```

### 图像反推

```bash
# 列出可用风格模板
python poster.py reverse --list-styles

# 使用12维度极致强化模板反推图片
python poster.py reverse photo.jpg --style "提示词风格-12维度极致强化"

# 使用电影质感模板
python poster.py reverse photo.jpg --style "提示词风格-电影质感"
```

反推结果自动保存到 `output_reverse_<文件名>.md`。

## 管线架构

```
┌─ 文本模式 ──────────────────────────────────────┐
│ 用户需求 → 第1层(需求理解) → 第2层(电商大师) → JSON Prompt │
└─────────────────────────────────────────────────┘
┌─ 图像反推模式 ──────────────────────────────────┐
│ 图片 + 风格模板 → Gemini分析 → 详细描述 → output.md  │
└─────────────────────────────────────────────────┘
```

## 设计风格（21种）

简约 Ins 风、高级奢华、科技感、清新自然、国潮风、活泼撞色、极简工业风、梦幻唯美、亚马逊风格、赛博朋克、复古怀旧、日式和风、北欧极简、波普艺术、莫兰迪色系、暗黑哥特、未来主义、新中式、酸性设计、孟菲斯风格、Y2K千禧风

## 提示词风格（prompt/ 文件夹）

6种：详细、电影质感、JSON、标签、简单、12维度极致强化
