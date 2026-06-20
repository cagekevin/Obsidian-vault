---
name: 翻译官部署指南
description: 初始化、配置文件、出图流程详细说明。SKILL.md 遇到部署相关问题时查阅此文档。
---

## 完整管线概览

```
① 初始化
   python3 init_project.py [项目目录]
     → 创建 assets/ images/ videos/ output/
     → 创建 Lovart 画布（所有图集中管理）
     → 创建 lovart_config.json（分辨率/模型/比例配置）

② AI 工作（SKILL.md 主流程）
   读 story.md → 提取 Scene → 分组 → 审计 → 写 project.json → export.py

③ 第一阶段：资产参考图
   python3 export_to_lovart.py [项目目录] --type refs
   python3 run_image_generator.py output/lovart_refs.json
     → assets/ref_*.png（角色定妆照、场景概念图）

④ 第二阶段：单帧/故事板图
   python3 export_to_lovart.py [项目目录] --type shots
   python3 run_image_generator.py output/lovart_shots.json
     → images/image_*.png（自动以资产图为垫图）

⑤ 打开画布查看所有图
   https://www.lovart.ai/canvas?projectId={UUID}
```

**两阶段不可逆**：必须先出资产参考图（refs），再出单帧/故事板图（shots）。

---

## 脚本说明

| 脚本 | 用途 | 阶段 |
|------|------|------|
| `init_project.py` | 创建目录 + Lovart 画布 + 配置文件 | 初始化 |
| `export.py` | project.json → output/ 提示词文件 | 翻译导出 |
| `export_to_lovart.py` | output/ 提示词 → Lovart JSON（分 refs/shots） | 图片生成 |

### lovart_project.py（外部依赖）

路径：`skills/工作效率类/W7-API链接/lovart-skill/lovart_project.py`
`init_project.py` 自动调用它创建画布，无需手动操作。

### run_image_generator.py（外部依赖）

路径：`skills/工作效率类/W7-API链接/lovart-skill/run_image_generator.py`
读取 Lovart JSON → 出图 → 自动更新 `assets_manifest.json`。

需要环境变量：`LOVART_ACCESS_KEY` 和 `LOVART_SECRET_KEY`。

---

## lovart_config.json

由 `init_project.py` 自动创建，用户可自行修改。

```json
{
  "project_id": "UUID（自动生成）",
  "refs": {
    "resolution": "1K",
    "aspect_ratio": "4:3",
    "model": "generate_image_gpt_image_2_medium"
  },
  "shots": {
    "resolution": "2K",
    "aspect_ratio": "16:9",
    "model": "generate_image_gpt_image_2_medium"
  },
  "output": {
    "assets_dir": "assets",
    "images_dir": "images",
    "videos_dir": "videos"
  },
  "skip_existing": false
}
```

| 字段 | 说明 |
|------|------|
| `project_id` | Lovart 画布 UUID，`init_project.py` 自动填入 |
| `refs.*` | 资产参考图（角色/场景）的分辨率、比例、模型 |
| `shots.*` | 单帧/故事板图的分辨率、比例、模型 |
| `output.*` | 各类文件的输出目录 |
| `skip_existing` | true 时跳过已生成的图（省积分） |

---

## 完整的出图流程

```bash
# 1. 初始化（新项目只需一次）
cd 翻译官目录
python3 init_project.py /path/to/项目目录

# 2. AI 翻译 → 出提示词
python3 export.py /path/to/项目目录 --html

# 3. 出资产参考图（第一阶段）
python3 export_to_lovart.py /path/to/项目目录 --type refs
python3 run_image_generator.py /path/to/项目目录/output/lovart_refs.json

# 4. 出单帧/故事板图（第二阶段）
python3 export_to_lovart.py /path/to/项目目录 --type shots
python3 run_image_generator.py /path/to/项目目录/output/lovart_shots.json

# 5. 打开画布查看所有图
# （上一步末尾会打印画布 URL）
```

### 跳过已存在的图

在 `lovart_config.json` 中设置：

```json
"skip_existing": true
```

生成前会查 `assets_manifest.json`，已存在最新版的图直接跳过，不消耗积分。

---

## 常见问题

| 问题 | 排查 |
|------|------|
| `init_project.py` 报错 | 检查 `lovart_project.py` 路径是否正确，AK/SK 是否设置 |
| `export_to_lovart.py` 找不到配置 | 确认项目目录下有 `lovart_config.json` |
| 出图时报错"文件不存在" | `--type shots` 在 `refs` 之前运行了——必须先出 refs |
| 垫图没有生效 | 检查 `assets_manifest.json` 中对应 asset 的 `latest` 字段是否正确 |
