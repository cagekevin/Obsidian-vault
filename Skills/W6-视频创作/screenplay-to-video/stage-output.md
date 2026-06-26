# Stage 输出阶段（Phase 5-8）

**覆盖原 Phase：** Phase 5 (提示词审计) + Phase 6 (故事板合成) + Phase 7 (熔断确认) + Phase 8 (视频合成)

---

## Phase 5: 提示词审计

**产出：** 审计报告（含 🟢/🟡/🔴 标签）
**前提：** 必须先确认所有组的 Phase 4 产出（group{N}_prompt_video.json + group{N}_note.txt）已完成，方可进入本阶段。
**终止条件：** 所有 Critical 项修复，否则不得进入 Phase 6

1. **加载规则**：读取 `roles/role_prompt_auditor.md` + 项目本地的 `configs/audit-rules.json`（审计师从此文件读取具体规则项而非硬编码）。

2. **执行审计**：加载剧本、全局变量、`character_blueprint.md`、Shots JSON 与 Breakdown，逐镜执行三层审计（角色一致性、视觉合理性、单图/垫图确认）。

3. **审计报告与熔断**：输出报告，每条结论标注信心标签：
   - 🟢 已验证（有参考图或规则明确对应）
   - 🟡 中等置信度（有推理依据但需用户确认）
   - 🔴 纯假设（AI 推断，必须人工复查）
   Critical 项必须全部修复才放行。**不通过 = 不得进入下一阶段**。

---

## Phase 6: 故事板合成

**产出：** `prompts/storyboard_data_{N}.json` + `prompts/group{N}_production_board.md`
**终止条件：** `scripts/board_to_video.py` 成功执行

> **故事板不是中间过渡，而是管线中的合成 + 确认 + 垫图三层关键节点**（注意：垫图来源分两阶段，资产垫图始终在 `assets/`，故事板输出到 `images/`）：
> 1. **合成层** → 以 `assets/` 下的角色定妆照、场景概念图、用户提供/网络下载的参考图等作为垫图（通过 `assets_manifest.json` 解析最新版本），按 Agent 的分镜数据拼成一张网格板，输出到 `images/storyboard_N.png`
> 2. **确认层** → 用户看合成图确认镜头布局和构图，未确认熔断锁生效，禁止进入视频阶段
> 3. **垫图层** → 用户确认后，`images/` 下的故事板图成为视频生成的主垫图（`reference_image_paths[0]`），视频模型用它理解场景布局和镜头关系
>
> **数据流概览**：定妆照/场景图 (assets/) → 拼入故事板 (images/) → 确认后垫入视频 (videos/)
>
> **核心原则**：Agent 只做创作决策（镜头怎么走、情绪什么曲线），机械拼装 prompt 格式交给脚本。
>
> **时序说明**：以下流程逐组执行。每完成 Phase 4（产出 `group{N}_note.txt` 后）→ 进入本阶段创建该组的 storyboard_data + production_board → 运行 board_to_video.py 装配 → 用户执行生图命令生成故事板图片 → 进入 Phase 7 熔断确认（用户确认构图满意后）→ 再开始下一组。不在 Stage 创作预创建。**必须先把当前组的图生成并确认后，才能进入下一组。**

1. **读取输入**：读取 `story.md`、`global_vars.md`、`group{N}_note.txt` 以及 `assets/` 目录清单。

2. **Agent 产出结构化数据**：创建两份文件：

   ① **数据层（机器读取）** `prompts/storyboard_data_{N}.json`
   参考模板文件 `templates/storyboard_data_template.json`，字段含义如下：
   - `refs[]` 引用 `assets/` 下的资产名（如 `"char_main_female"`），`scripts/storyboard.py` 自动通过 `assets_manifest.json` 解析为 `latest` 版本
   - 角色描述自动推断：`char_` 前缀的 ref 会自动查找对应 `configs/` 下的角色 config 提取文本描述，无需手动指定

   ② **展示层（人类审阅）** `prompts/group{N}_production_board.md`
   - 与 data JSON 内容一致但人类可读格式，包含详细镜头时序表、灯光曲线图、角色服装标注

3. **AI 执行装配**：运行 `scripts/board_to_video.py`（包含 scripts/storyboard.py 装配 + **🔒 前置硬闸门校验** + 垫图校验 + 视频提示词补全，AI 自动执行，无需用户操作）：
   ```bash
   python scripts/board_to_video.py <项目路径> <组号>
   # 可选：如果有故事板图的 CDN URL 可直接填入视频垫图
   python scripts/board_to_video.py <项目路径> <组号> --board-cdn <CDN_URL>
   ```
   脚本自动完成：
   - **角色描述自动注入**：从 `refs[]` 中 `char_` 前缀的反查 config JSON 提取角色外貌描述
   - **风格令牌动态注入**：从 `prompts/global_vars.json` 读取风格令牌（不硬编码，支持任意风格），无该文件则用兜底令牌
   - **精简 Assembly Prompt 拼装（Visual Hierarchy 优先）**：
     | Section | 内容 | 来源 | 权重 |
     |---------|------|------|------|
     | **S4 故事板网格**（排第一位） | 逐帧"标题. 英文描述" | data `shots[].title/en` | **PRIMARY** — 分配最大面积 |
     | S2 角色参考 | 角色外貌，仅在有 `char_` 垫图时生成 | char config prompt | **SECONDARY** — 侧边缩略图 |
     | S1 顶部方向栏 | 镜头数、调色板、环境 | data JSON 字段 | SUPPLEMENTARY |
     | S3 场景平面图 | 摄像机路径标注（仅当有 camera_path 时） | data `camera_path` | SUPPLEMENTARY |
     | ~~S5-S8 灯光/情绪/音频/摄影~~ 已移除 | 技术信息保留在 JSON 中，不挤占图片空间 | — | — |
     提示词中用 "PRIMARY / SECONDARY / SUPPLEMENTARY" 三级权重代替硬编码百分比，AI 根据内容自动分配布局。
   - **垫图路径解析**：通过 `assets_manifest.json` 自动将 default 路径升级为 `latest` 版本，不依赖 cdn_urls.json
   - 输出 config 至 `configs/storyboard_{N}.json`
   - 同时补全 `group{N}_prompt_video.json` 的垫图 URL

4. **提供生图命令给用户**：
   ```bash
   python run_image_generator.py <项目路径>/configs/storyboard_N.json
   ```
   `run_image_generator.py` 会显示每张垫图的完整路径、文件大小、上传链接，文件缺失时红字报错。

5. **更新 Group 摘要**：在 `configs/group_map.md` 追加该组记录。

---

## Phase 7: 生图与熔断确认

**产出：** `images/storyboard_{N}_v1.png`
**终止条件：** 用户明确确认"构图满意"，未确认前严禁进入 Phase 8

1. **🔒 硬闸门校验（故事板 config）**：`scripts/board_to_video.py` 执行时已自动完成校验。如跳过装配直接修改了 storyboard config，手动补跑：
   ```bash
   python scripts/validate_project.py <项目路径> --type storyboard --group <N>
   ```

2. **🔴 提供生图命令给用户**：`python run_image_generator.py <项目路径>/configs/storyboard_{N}.json -- 3:4 2K`
   （config 由 Phase 6 的 `scripts/storyboard.py` 自动生成，包含完整 prompt + 垫图路径 + project_id）
   **`run_image_generator.py` 自动读取 config 中的 `project_id` 字段，不需要手动传 `--project`。**

3. **展示图片与确认**：故事板图落地至 `images/storyboard_{N}_ar3x4_2K_v1.png`（自动带版本号）。**更新 `assets_manifest.json`** 中 `storyboard_{N}` 的 `latest` 字段指向新版本文件（如果再次迭代出 `_v2`，`latest` 也随之更新），后续 Phase 8 通过 manifest 解析最新版本。展示给用户并严格发问：**"构图满意可以出视频，还是需要调整？"**

4. **局部回滚逻辑**：
   - "调整第 N 组" → Agent 修改对应的 `prompts/storyboard_data_{N}.json` → 重新跑 `scripts/board_to_video.py`（或轻量 `scripts/storyboard.py` 如果只改镜头不走视频） → 重新提供生图命令（脚本自动出 `_v2` 版本）
   - "满意" → 进入 Phase 8。未获满意确认前，禁止执行下一步。

5. **同步与 CDN 记录（可选）**：全组图确认后，同步项目所有图片到本地并记录 CDN URL。后续视频生成时可通过 `--board-cdn` 使用在线垫图更稳定：
   ```bash
   cd skills/工作效率类/W7-API链接/lovart-skill
   # 通过 config 读取 project_id（推荐，不依赖全局状态）
   python sync_lovart_images.py --config {项目路径}/prompts/group{N}_prompt_video.json --output-dir {项目路径}/images --confirm
   # 或通过项目名
   python sync_lovart_images.py --project "{项目名}" --output-dir {项目路径}/images --confirm
   ```

---

## Phase 8: 视频合成与大片落地

**产出：** `videos/group{N}_video_v1.mp4`
**终止条件：** `.video_approved` 熔断锁存在 + 通过 `validate_project.py --type video`

1. **物理熔断解锁**：获取用户明确确认后，在项目目录创建物理解锁锁文件：
   - Windows: `cmd /c copy nul <项目根目录>\.video_approved`
   - macOS/Linux: `touch <项目根目录>/.video_approved`
   此文件是视频脚本的物理熔断锁，未创建则拒绝执行（`run_video_generator.py` 启动时自动检查）。

2. **确认视频配置**：取出 Phase 4 已创建的 `prompts/group{N}_prompt_video.json`，按最终出片需求调整 `aspect_ratio`（通常 9:16）和 `duration`（≤15）。
   - **垫图规则**：`reference_image_paths` 默认只填故事板图（Phase 4 预填，此时图片尚未生成）。**必须通过 `assets_manifest.json` 中 `storyboard_{N}` 的 `latest` 字段解析最新版本路径**，不要写死 `_v1`/`_v2` 版本号（Phase 7 生图后 `latest` 已更新）。**不自动填入角色/场景垫图**，用户需要时自行追加。
   - **视频主垫图 = 故事板图**（`images/storyboard_N_v1.png`）：视频模型通过故事板图理解每个镜头的场景布局、角色位置和构图关系，纯文字描述无法替代。
   - **角色/场景/道具素材作为补充垫图**排在后面（如有需要），而非主垫图。参考模板 `templates/video_prompt_template.json`：
   ```json
   {
     "name": "group3_video",
     "prompt": "从 storyboard_data_N.json 的 shots[].en 浓缩得到的英文画面描述。只写画面内容（角色动作、运镜、光线、情绪），引导句和技术参数由 run_video_generator.py 自动拼接。禁止独立创作不来自 storyboard 的画面。",
     "model": "generate_video_seedance_v2_0",
     "aspect_ratio": "16:9",
     "resolution": "720p",
     "duration": 15,
     "reference_image_paths": [],
     "output_dir": "<项目根目录>/videos/group3_video.mp4"
   }
   ```
   - **Agent 职责**：从 `storyboard_data_N.json` 的 `shots[].en` 浓缩得到英文画面描述 + 设 `duration/aspect_ratio/resolution`
   - **脚本职责**（`board_to_video.py --board-cdn`）：填 `reference_image_paths`
   - **运行时代理**（`run_video_generator.py` 的 `VIDEO_GUIDE`）：自动拼接负面提示词（No text / Sound only / Must match ref...）+ 技术参数前缀（比例/分辨率/时长/模型）+ 垫图说明
   - **单一源头原则**：所有负面提示词仅存放在 `run_video_generator.py` 的 `VIDEO_GUIDE`，不分散到各文件
   - 输出时自动带版本号（如 `group3_video_v1.mp4`）

3. **🔒 硬闸门校验（视频提示词）**：提供视频生成命令前，Agent 必须在本轮先执行：
   ```bash
   python scripts/validate_project.py <项目路径> --type video --group <N>
   ```
   全部 ✅ 通过后才能进入下一步。

4. **提供视频生成命令给用户**（逐组生成）：
   - `python run_video_generator.py <项目根目录>/prompts/group{N}_prompt_video.json --project-dir <项目根目录>`
   - `run_video_generator.py` 自动读取 config 中的 `project_id`，不需要手动传 `--project`

5. **结果交付**：视频落地至 `videos/group{N}_video_v1.mp4`（自动带版本号）。更新 `configs/group_map.md` 中该组视频状态为 ✅。`assets_manifest.json` 自动更新 `latest` 字段。
