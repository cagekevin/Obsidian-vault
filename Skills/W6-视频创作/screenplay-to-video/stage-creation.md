# Stage 创作阶段（Phase 0-1）

**覆盖原 Phase：** Phase 0 (阵地初始化) + Phase 1 (剧本编剧)

---

## Phase 0: 阵地初始化

**产出：** 空目录结构 + `assets_manifest.json` + Lovart 项目
**终止条件：** 目录创建完成 + manifest 准备就绪 + Lovart 项目已注册

1. **阵地创建**：询问用户项目名，按 SKILL.md 中「产出目录树」结构创建空文件夹：
   - macOS: `mkdir -p ~/Documents/AgentSpace/1_Active/{项目名}/{prompts,configs,assets,images,videos}`
   - Windows (cmd): `mkdir "G:\AgentSpace\1_Active\{项目名}\prompts" "G:\AgentSpace\1_Active\{项目名}\configs" "G:\AgentSpace\1_Active\{项目名}\assets" "G:\AgentSpace\1_Active\{项目名}\images" "G:\AgentSpace\1_Active\{项目名}\videos"`
   - Windows (PowerShell): `mkdir G:\AgentSpace\1_Active\{项目名}\{prompts,configs,assets,images,videos}`

2. **创建资产版本索引**：在项目根目录创建 `assets_manifest.json`，初始内容为空对象 `{}`。后续各阶段产出文件后自动/手动填入记录。字段定义如下（完整模板参考 `templates/manifest_template.json`）：

3. **创建 Lovart 项目**：调用 W7 统一项目管理创建专属 Lovart 项目，所有该视频项目的生图/生视频线程都在此项目下，实现项目隔离。

   ```bash
   cd skills/工作效率类/W7-API链接/lovart-skill
   python lovart_project.py init "{项目名}"
   ```

   成功后会在 `projects.json` 注册映射，生成的 UUID 就是这个视频项目所有图片/视频的归属。

   **后续所有 config JSON 中都要带上 `project_id`（= 这个 UUID）**，这样 `run_image_generator.py`、`run_video_generator.py`、`sync_lovart_images.py` 都能自动定位到正确的 Lovart 项目，无需手动传 `--project`。
   
   查 UUID 的方法：`python lovart_project.py id "项目名"` → 输出 `9a55effc-0847-...`

   ```json
   {
     "资产ID（如 char_female_before）": {
       "config": "生成该资产使用的 config 路径（如 configs/char_female_before.json，没有则为空字符串）",
       "default": "初始产出路径（如 assets/char_female_before.png）",
       "latest": "最新版本路径（如 assets/char_female_before_ar4x3.png，由脚本自动更新）"
     }
   }
   ```

   脚本（`scripts/storyboard.py`、`scripts/board_to_video.py`、`run_image_generator.py`、`run_video_generator.py`）均通过此文件解析最新版本。脚本出图/出视频后自动更新 `latest` 字段。

---

## Phase 1: 剧本编剧

**产出：** `story.md` + `configs/character_blueprint.md`
**终止条件：** 用户二元确认剧本 + 角色蓝图定稿

1. **动态加载规则**：读取 `../俄语详细剧本/SKILL.md`（该文件会自动拉起 methodology.md、style-rules.md、workflow.md 及整套编剧行为框架）。

2. **剧本输出要求**：按俄语规则生成剧本（一个版本+分析）。经过二元问题确认。

3. **精准物理落地**：定稿写入 `story.md`。

4. **角色设定确认与变化路径规划**：从剧本提取角色清单，逐角色与用户确认核心设定（人种、发色、瞳色、标志性服装），并**提前规划每个角色的完整变化路径**（如"衰老暗沉→饱满发光"、"素颜→精致妆容"、"日常→盛装"等，具体维度依据剧本定）。确认结果写入 `configs/character_blueprint.md`，为后续资产生成提供双版本依据。

5. **全维度剧本审计**：剧本定稿后加载 `roles/role_screenwriter.md`，读取其"剧本审计清单"章节（第 4 节 A-D 全部子节），逐组逐场景执行审计。将审计结果标注到 `story.md` 对应场景下，并写入后续 Archetype 标注供 Phase 4 使用。
