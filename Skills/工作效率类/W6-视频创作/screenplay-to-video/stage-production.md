# Stage 制作阶段（Phase 2-4）

**覆盖原 Phase：** Phase 2 (视觉定调) + Phase 3 (资产先行) + Phase 4 (分镜细化)

---

## Phase 2: 视觉定调

**产出：** `global_vars.md` + `prompts/global_vars.json` + `configs/audit-rules.json`
**终止条件：** **抛 3 个渲染风格给用户选择 → 必须终止对话**（收到确认后才能进入下一步）

1. **确认方向与加载 Skill**：让用户确认方向，定位风格 name，加载对应的风格 skill（如 `styles/皮卡斯风格动画分镜_*.md`）。

2. **从风格文件提取令牌**：从已加载的风格文件中，提取其定义的所有 `--token-*`（无需拆分 `style/render/shading` 等子类），作为后续输出全局变量的数据来源。所有风格文件的 token 名已统一为 `--token-director` / `--token-lighting` / `--token-camera`（皮卡斯额外保留 `--token-shading-character`）。直接从文件中复制 token 名和值，不要自己改写。

3. **双向解耦输出（Dual-Output 铁律）**：读取 `story.md`，**必须同一轮同时生成**以下两份文件，结构必须始终保持一致：
   - **展示层（人类审阅）**：`<项目>/global_vars.md`。顶部写明风格来源。**必须包含**：第 2 步提取的 `--token-*` 令牌列表、全局色彩脚本、角色几何与材质建档、场景空间与光照档案、状态机定义、跨镜头一致性锁定规则（Consistency Lock）。
   - **数据层（机器读取）**：`<项目>/prompts/global_vars.json`。提取结构化的 Style Tokens + Color Script + State Machine。
     - `tokens`：原样保留风格文件的 `--token-*` key，供手写 config（如单镜 shot JSON、角色定妆照）使用。
     - **`style_tokens`（必填）**：将每个风格文件定义的 `--token-*` 映射为 3 个标准化 key。风格文件现已统一使用 `--token-director` / `--token-lighting` / `--token-camera`，直接抄即可：

       | 写入 key | 对应 `--token-*` |
       |----------|-----------------|
       | `token_director` | `--token-director` |
       | `token_lighting` | `--token-lighting` |
       | `token_camera` | `--token-camera` |

4. **展示给用户确认**。

5. **编译审计规则文件**：从所选风格文件中提取色彩脚本、渲染令牌、状态机规则，写入 `configs/audit-rules.json`（仅含视觉风格相关规则，不含角色设定）。Phase 5 审计师从此文件读取具体规则。

---

## Phase 3: 资产先行

**产出：** `configs/char_*.json` + `configs/scene_*.json`（以及可选 `configs/product_*.json`）
**终止条件：** 用户确认产品/道具资产 + 定妆照全部通过 `python scripts/validate_project.py <路径> --type assets` 校验

1. **加载规则**：读取 `roles/role_art_director.md`。

2. **读取角色蓝图**：从 `configs/character_blueprint.md` 读取每个角色的变化路径，确认需要生成几个版本（通常 before/after 两个，具体维度依剧本定）。

3. **生成双版本配置**：在项目 `configs/` 目录下为每个角色按版本生成逐张 JSON 配置，命名统一为 `char_{id}_before.json`、`char_{id}_after.json`，场景照同理 `scene_1.json`。
   **每个 config 必须填上 `project_id`**（从 `lovart_project.py id "项目名"` 查 UUID），这样不用传 `--project`。
   **关键**：每个 config 的 `prompt` 首行必须强制前置全局渲染令牌（从 `global_vars.md` 的渲染令牌章节提取），令牌不在 prompt 里则 Lovart API 不会应用该风格。参考模板 `templates/character_asset_config_template.json`。

4. **🔒 硬闸门校验（资产 config）**：提供生图命令前，Agent 必须在本轮先执行：
   ```bash
   python scripts/validate_project.py <项目路径> --type assets
   ```
   全部 ✅ 通过后，才能进入下一步。校验失败则 Agent 修复 config 后重跑。

5. **提供生图命令给用户**（config 已自带 `project_id`）：用户自行在终端执行：
   `python run_image_generator.py <项目路径>/configs/char_female_before.json`
   config 中的 `project_id` 会自动定位到正确的 Lovart 项目，不需要传 `--project`。

---

## Phase 4: 分镜细化

**产出：** `prompts/group{N}_prompt_video.json`（垫图暂空） + `prompts/group{N}_note.txt` + （按需）`prompts/group{N}_prompt_shot_*.json`
**终止条件：** 所有组（N=1..n）的 Phase 4 产出全部完成，且单镜 JSON（如有）通过 `validate_project.py --type shots` 校验。未完成全部组前不得进入下一阶段。

1. **读取剧本 Archetype 标注**：从 `story.md` 读取前面标注的每场冲突 Archetype，以及对应的 Camera Signature 映射关系（Duel → 低角度交替 / Confrontation → OTS 轴线交叉 / Interrogation → 不对等构图 / Negotiation → 对称等量）。

2. **写完整视频运动描述 → 写入 prompt 字段**：为当前组写一段完整的英文视频运动描述，从 `storyboard_data.shots[].en` 展开。**直接写入 `group{N}_prompt_video.json` 的 `prompt` 字段**，不压缩。重点在"运动"——镜头怎么移动、画面怎么过渡、视觉怎么流动。

3. **⏸ 熔断询问**：展示完整版给用户，问 **"现在精简吗？"**。用户确认前不得进入下一步。

4. **浓缩为视频 prompt**：用户确认后，将完整描述压缩。原则：去冗余、保持时空连续性、保留关键视觉锚点。不写技术参数（`run_video_generator.py` 自动拼接），不独立创作。用精简版覆盖 `prompt` 字段。

5. **精准物理落地**：按剧本结构划分自然组（N 从 1 开始，一组对应一个独立场景/连续情绪段落，镜头编号 XX-YY 必须连续递增），每组产出必要文件：
   - `prompts/group{N}_prompt_video.json`（视频提示词，必出。**每个 JSON 必须填上 `project_id`**，从 `lovart_project.py id "项目名"` 查 UUID。垫图由 `board_to_video.py` 自动从 manifest 解析最新故事板图，Agent 无需手动填写。模板中的路径占位符会被脚本覆盖）
   - `prompts/group{N}_note.txt`（中文分镜备注说明，必出）
   - `prompts/group{N}_prompt_shot_XX-YY.json`（**按需，仅当用户要求出单镜原画时生成，不影响后续生成合成网格故事板**）— 该组每镜完整生图配置，格式直接兼容 run_image_generator.py，**每个 JSON 必须填上 `project_id`**。参考模板 `templates/shot_config_template.json`：

   > **📌 单镜 JSON 与 storyboard_data JSON 的分工**：
   > - `prompt_shot_XX-YY.json` = **单镜生图配置**，每张图片输出一个独立的单镜画面（如 shot_01.png、shot_02.png），是一份 `run_image_generator.py` 的输入 config
   > - `storyboard_data_{N}.json`（Stage 输出产出）= **故事板大图的结构化数据**，描述一组镜头如何摆进一张合成大图，通过 `scripts/board_to_video.py` 拼装后产出 `configs/storyboard_N.json`，再经 `run_image_generator.py` 生成一张含所有镜头布局的故事板网格图
   > - 前者出**单镜页面**，后者出**整组总览故事板**，两者职责不同、不冲突

   每个镜头 config 必须包含 `name/project_id/prompt/aspect_ratio/resolution/model/output_dir/reference_image_paths`，缺一不可。**关键**：`prompt` 首行必须前置全局渲染令牌（从 `global_vars.md` 提取）。垫图路径从 `assets_manifest.json` 的 `latest` 字段提取最新版本，**不写死 `_vN` 版本号**。

6. **🔒 硬闸门校验（单镜 config）**：如果生成了单镜 JSON，Agent 必须在本轮先执行：
   ```bash
   python scripts/validate_project.py <项目路径> --type shots --group <N>
   ```
   全部 ✅ 通过后才能提供生图命令。校验失败则修复后重跑。
