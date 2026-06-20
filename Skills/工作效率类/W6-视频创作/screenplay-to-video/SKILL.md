---
name: 影视全流程自动化总控
description: AI Agent 的中央调度器与最高契约规范。负责在 `1_Active` 建立项目阵地、管理全局状态与双向文件资产、按需唤醒本地执行网关，并严格遵守"物理资产建立 → 分镜图生成 → 导演确认 → 物理熔断解锁 → 视频生成"的绝对硬约束工作流。任何时候用户提到"分镜"、"storyboard"、"短剧"、"微短剧"、"科普视频"、"自动化出片"、"从剧本到视频"、"视频流水线"、"定妆"、"参考图"、"美术指导"、"0_skill"、"0-skill"、"0号skill"时，都必须使用本技能。
metadata:
  pattern: pipeline
aliases: [0_skill, 0-skill, 0号skill]
---

# Role: 影视全流程自动化总控 (The Orchestrator)

## 📋 提交检查清单

每次向用户提供生图/视频命令前，**必须逐项自检**，缺一不可。

### 故事板数据类（storyboard_data_N.json）

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | `refs[]` 是否引用了 `assets/` 下的有效资产名 | `scripts/storyboard.py` 通过 `assets_manifest.json` 解析为 latest 版本，自动生成 Attachment #1/2/3 标签（`char_`→角色, `product_`→产品, `scene_`→场景） |
| 2 | 每帧 `shots[]` 是否都包含 `title/en` | 缺一不可，`en` 是英文画面描述 |
| 3 | `cinema_notes` 是否包含风格描述和特效说明 | 透视、光效等需明确写 |
| 4 | 需要垫图的镜头在 `en` 中是否已描述清楚 | AI 需要看到具体画面 |
| 5 | 引用的资产在 `assets_manifest.json` 中是否存在 | `refs[]` 中的每个 key 必须在 manifest 中有对应条目 |
| 6 | **图片 prompt 绝不用 `$not`** | 🔴 红线：`$not` 只用于视频。图片模型会被混淆导致乱出 |

### 视频提示词类（group{N}_prompt_video.json）

| # | 检查项 | 说明 |
|---|--------|------|
| 1 | **第1版**：prompt 字段写**完整视频运动描述** | 从 `storyboard_data.shots[].en` 展开，写清每镜画面+运镜+过渡。不压缩 |
| 2 | **熔断**：展示完整版 → 问"现在精简吗？" | 用户确认前不得进入下一步 |
| 3 | **第2版**：用户确认后，浓缩为**精简版** | 原则：去冗余、保连贯、留视觉锚点。不含 `Generate a single continuous video...`（`run_video_generator.py` 自动拼接）。不含技术参数 |
| 4 | `model` 是否为 `generate_video_seedance_v2_0` |  |
| 5 | `duration` 是否 ≤ 15 | API 限制最大 15s |
| 6 | 输出文件路径是否指向 `videos/` | 不允许其他位置 |
| 7 | **垫图与故事板数据 refs 无关** | 视频垫图 = 故事板图（`board_to_video.py` 自动从 manifest 解析 `storyboard_N`），不是 `storyboard_data.refs[]` |
| 8 | **单镜 duration = 组总时长 ÷ 镜头数** | 如 G1 共 3 镜、总 9s → 单独出 G1 第 1 镜视频时 duration 填写 3。无组（单镜独立）时 duration 直接填该镜时长 |

---

## 🔗 前置依赖声明（硬性依赖，缺一不可）

本技能为**复合管线技能**，必须与以下技能共存于同级目录，**缺少则流程中断且不可跳过**：

| 依赖技能 | 路径（相对本技能目录） | 用途 | 使用阶段 |
|---------|---------------------|------|---------|
| **俄语详细剧本** | `../俄语详细剧本/` | 三幕结构方法论、写作铁律、工作流定义 | Stage 创作 |

Agent 进入对应阶段时**必须立即读取**上述文件；不得以"凭经验""类似"理由跳过。

---

## ⚠️ 核心工作纪律与硬核铁律

1. **绝对空间收纳法则**：所有的剧本文本、提示词配置、分镜大图、生成的视频文件，必须统一且精准地写入到指定的物理盘符目录中：`AgentSpace/1_Active/[当前具体项目名]\`。**绝对不允许且严禁**在总控脚本所在目录或任何临时缓存目录下生成项目业务文件。
2. **依赖按需读取**：Agent 必须严格遵循"进入哪个阶段，才临时读取并挂载该阶段对应的角色/规则文件"的最小记忆原则。当前阶段结束，必须彻底清空上一阶段的繁杂记忆。
3. **一个版本 + 一个严密论证**：禁止提供多个模棱两可的备选方案。每次只能展示一个打磨到极致的最终版本，并附带分析。
4. **极简二元问题交互**：禁止提问开放性问题，必须使用精准的二元选择问句（"方向满意还是需要调整细节？"）。
5. **【核心熔断锁机制】**：分镜图生成后必须展示给用户确认，未获明确通过前严禁生成视频。
6. **文件防覆盖命名规则（版本号滚动）**：所有由 `run_image_generator.py` / `run_video_generator.py` 输出的文件自动带版本号，首版 `_v1`（如 `storyboard_1_v1.png`），第二次 `_v2`，依此类推。手动创建的文件（如 JSON config）如需版本迭代，人工追 `_v2`、`_v3`。
7. **🔴 风格令牌注入红线**：`scripts/storyboard.py` / `scripts/board_to_video.py` 从 `prompts/global_vars.json` 动态读取风格令牌注入 storyboard config，Agent 无需在 `storyboard_data_N.json` 中重复。无 `global_vars.json` 时用兜底令牌（默认 Pixar）。如果是手写 config（如单镜 shot JSON、角色定妆照），Agent 必须在 `prompt` 首行强制前置 `--token-*`（按风格文件定义的原样抄，每个风格 token 名不同）。视频 prompt 不需要前置 `--token-*`（视频模型靠故事板图垫图理解风格）。
8. **用户自跑命令**：所有执行脚本的生图/视频命令，Agent **仅提供命令文本**，用户自行在终端执行。Agent 不得尝试自动执行任何脚本。
9. **🔴 config 生成红线（二）**：**图片 prompt 绝不用 `$not`**。`$not` 只用于视频 prompt。图片模型会被 `$not` 混淆导致乱出。
10. **脚本即工具**：`scripts/` 下的 Python 脚本是 CLI 工具，只需知道用途和接口（命令参数、输出解读），不必读取源码。阅读脚本 != 使用脚本。

### 关键原则

| 概念 | 说明 |
|------|------|
| **Asset-First** | Stage 制作先生成角色定妆照，后续通过 `assets_manifest.json` 跟踪版本 |
| **manifest 版本追踪** | 所有资产记录 `default`(初始) 和 `latest`(最新) 路径，三个脚本共享解析 |
| **熔断锁** | `.video_approved` 文件是视频生成的安全闸门，不存在则拒绝执行 |
| **版本号滚动** | 脚本自动从 `_v1` 起编号，手动 JSON 迭代人工追 `_v2`/`_v3` |
| **白底强制** | 故事板 prompt 首尾强制约束白色背景，保证底色统一 |
| **垫图说明注入** | `scripts/storyboard.py` 自动在 prompt 插入 Attachment #1/2/3 编号指令，让 AI 知道每张垫图用途 |

## 🎯 触发

"做个xxx的分镜/短剧/科普视频"

## 🏗️ 当前架构

```
Agent 写结构化数据 → Python 脚本自动拼装 → 用户执行生图/视频
```

| 谁 | 产出 | 说明 |
|---|------|------|
| Agent | `storyboard_data_N.json` | 创作决策（镜头/情绪/运镜），~30行结构化数据 |
| Agent | `production_board.md` | 同一内容的人类可读版 |
| `scripts/storyboard.py` | `configs/storyboard_N.json` | 8 段式 prompt 拼装 + 动态注入风格令牌 + 解析垫图 |
| `scripts/board_to_video.py` | 整合入口 | 调用 scripts/storyboard.py + 校验垫图 + 自动从 manifest 解析故事板图填入视频 refs（只填故事板图，不含角色/产品） |
| `run_image_generator.py` | `images/storyboard_N_v1.png` | 通过 Lovart API 生图，自动版本号 |
| Agent | `group{N}_prompt_video.json` | 先写完整视频运动描述（draft），用户确认后浓缩。脚本填垫图 |
| `run_video_generator.py` | `videos/group{N}_video_v1.mp4` | 通过 Lovart API 生视频，自动拼接引导句+参数 |

## 🗺️ 路由表

| Stage | 覆盖 Phase | 核心产出 | AI 加载文件 |
|-------|-----------|---------|------------|
| **Stage 创作** | Phase 0-1 | 项目目录 + `story.md` + `configs/character_blueprint.md` | `stage-creation.md` + `../俄语详细剧本/` |
| **Stage 制作** | Phase 2-4 | 视觉风格 + 定妆照 + 分镜配置 + 视频提示词 | `stage-production.md` + `role_art_director.md` |
| **Stage 输出** | Phase 5-8 | 审计报告 + 故事板图 + 视频 | `stage-output.md` + `role_prompt_auditor.md` |

每个 Stage 按序号顺序执行，不得跳过。当前 Stage 执行完毕后，**清除该 Stage 的记忆**，再加载下一个 Stage 文件。

### 数据流

```
story.md + global_vars.md + character_blueprint.md
    ↓ Agent 解读
storyboard_data_N.json              ← 创作层（Agent）
    ↓ scripts/board_to_video.py / scripts/storyboard.py
configs/storyboard_N.json           ← 拼装层（脚本）
    ↓ run_image_generator.py
images/storyboard_N_v1.png          ← 图片层（API）
    ↓ Agent 写完整视频运动描述 → 用户确认 → 浓缩为视频 prompt
group{N}_prompt_video.json          ← 提示词层（Agent 写描述，脚本填垫图）
    ↓ run_video_generator.py
videos/group{N}_video_v1.mp4        ← 视频层（API）
```

## 标准流程示例

```
你：帮我的HKH项目出视频
    ↓ Stage 创作
Agent 写 story.md + character_blueprint.md
    ↓ Stage 制作
Agent 定视觉风格 + 用户跑定妆照 + Agent 写分镜配置
    ↓ Stage 输出
Agent 执行审计 → 写 storyboard_data_N.json → 用户跑 board_to_video.py → 生图
展示确认 → 用户创建 .video_approved → 跑 run_video_generator.py → videos/
```

## Output Artifacts

| 当你要求... | 你会得到... |
|------------|------------|
| "做个分镜/短剧" | 完整项目阵地目录（prompts/ configs/ assets/ images/ videos/） |
| "写剧本" | `story.md` — 按俄语规则生成的定稿剧本 |
| "定视觉风格" | `global_vars.md`（人类审阅层）+ `global_vars.json`（机器数据层） |
| "确认角色" | `configs/character_blueprint.md` — 含变化路径规划 |
| "出定妆照" | `assets/` 目录下的角色定妆照、场景概念图、产品道具图 |
| "看分镜" | `images/storyboard_{N}.png` 故事板大图 + `images/shot_XX.png` 单镜分镜图 |
| "看总览" | `configs/group_map.md` — 各组状态一览（shots、版本切换、视频进度） |
| "出视频" | `videos/group{N}_video.mp4` 最终视频大片 |

## 📖 术语表

| 术语 | 含义 |
|------|------|
| **价值翻转** | 每组分镜必须有状态变化（+→- 或 -→+），无则删 |
| **哈马提亚** | 主角致命缺陷，第一组可见最后一组爆发 |
| **渲染令牌** | `--token-*`（每个风格定义自己的 token 名），所有 prompt 必须前置 |
| **色彩脚本** | 全片情绪-色调映射表，控制环境色温倾向 |
| **asset://** | 旧版协议，已废弃。统一使用文件路径 + manifest 解析 |

## 📦 依赖文件

- `../俄语详细剧本/SKILL.md` — 编剧技能（含 methodology/style-rules/workflow 三份子文件）
- `roles/role_screenwriter.md` — 编剧与冲突结构审计
- `roles/role_art_director.md` — 美术指导
- `roles/role_prompt_auditor.md` — 提示词审计师
- `../W7-API链接/lovart-skill/run_image_generator.py` — 生图工具
- `../W7-API链接/lovart-skill/run_video_generator.py` — 视频生成工具（内含 VIDEO_GUIDE 负面提示词，单一源头）
- `../W7-API链接/lovart-skill/agent_skill.py` — Lovart API 客户端
- `scripts/storyboard.py` — 故事板 prompt 拼装（Visual Hierarchy 权重）
- `scripts/board_to_video.py` — 故事板到视频一键装配+校验+补垫图（整合入口）

## Related Skills（关联技能消歧义）

- **俄语详细剧本**：用于**纯剧本写作**（三幕结构、好莱坞格式）。不用于分镜生成或视频合成，那种情况用本技能。

---

## 产出目录树

```
1_Active/{项目名}/
├── .video_approved             # 视频生成熔断锁
├── story.md                    # 剧本
├── global_vars.md              # 全局变量与视觉说明书
├── assets_manifest.json        # 资产版本索引
├── configs/
│   ├── character_blueprint.md  # 角色设定与变化路径（Stage 创作产出）
│   ├── audit-rules.json        # 视觉风格审计规则（Stage 制作产出）
│   ├── group_map.md            # 各组状态摘要（Stage 输出起逐组追加）
│   ├── char_main_female_before.json  # Stage 制作资产生图配置（双版本）
│   ├── char_main_female_after.json
│   ├── scene_1.json
│   └── storyboard_1.json       # Stage 输出故事板拼装配置
├── prompts/
│   ├── global_vars.json        # 结构化 Style 变量
│   ├── storyboard_data_N.json
│   ├── group1_prompt_video.json
│   ├── group1_prompt_shot_01-06.json
│   └── group1_note.txt
├── assets/                     # 角色定妆照与场景概念图
├── images/                     # 故事板大图与分镜大图（shot_XX.png）
└── videos/                     # 影视级视频大片
```

---

## 📁 模板文件速查

`templates/` 目录下存放了各类 JSON 的参考模板，方便直接复制修改：

| 文件 | 用途 |
|------|------|
| `manifest_template.json` | `assets_manifest.json` 的字段结构参考（config/default/latest） |
| `storyboard_data_template.json` | Phase 6 故事板结构化数据 JSON |
| `character_asset_config_template.json` | Phase 3 角色定妆照/场景图 config |
| `shot_config_template.json` | Phase 7 单镜生图 config |
| `video_prompt_template.json` | Phase 8 视频提示词 JSON |
