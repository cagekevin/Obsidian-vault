# Phase 3: 角色/场景定妆提示词

**产出：** 每个角色的双版本定妆照提示词 + 每个主场景的概念图提示词 +（可选）产品/道具提示词
**终止条件：** 用户确认所有定妆照和场景图提示词，全部通过自检清单

1. **读取角色变化路径**：从 Phase 1 产出的角色蓝图中，提取每个角色的**变化路径**。
   变化路径决定了需要生成几个版本（通常 before/after 两个版本）：
   - 例如"衰老暗沉→饱满发光" → 生成 `char_X_before`（衰老暗沉）+ `char_X_after`（饱满发光）
   - 例如"素颜→精致妆容" → 生成 `char_X_before`（素颜）+ `char_X_after`（精致妆容）
   - 如果角色无变化路径 → 生成单一版本即可

2. **⚠️ 渲染令牌前置红线（关键）**：
   每个定妆照和场景概念图的图片提示词，**首行必须强制前置全局渲染令牌**。令牌从 Phase 2 的风格说明书的"渲染令牌"模块提取（如 `--token-global` / `--token-style` / `--token-render` 等）。
   - 令牌不在 prompt 里，生图工具不会应用该风格
   - 角色定妆照追加角色专用令牌（如 `--token-shading-character`）
   - 场景/产品图不需要追加角色令牌

3. **生成双版本定妆照提示词**：为每个角色按版本生成定妆照提示词：

```markdown
### [角色ID] - [版本名]
**变化维度：** [该版本对应的变化点，如"胶原蛋白饱满、眼神锐利、妆容精致"]
**垫图用途：** 角色定妆照，供后续所有分镜作为角色参考垫图

**画面：** [角色外貌+全身造型+标志性服装+状态,根据变化路径写]

**提示词：**
```
[前置: --token-global ... --token-style ... --token-render ... --token-shading-character]
[景别] of [主体描述], [动作/表情], [环境/背景], [光线], [色彩], [构图], [风格]
```

**示例：**
```markdown
### char_female_before - 素颜疲惫状态
**变化维度：** 暗沉肤色、黑眼圈、凌乱散发、简约工作服
**垫图用途：** 角色定妆照，供分镜垫图
**画面：** 25岁女性，素颜，黑眼圈，浅蓝色衬衫，头发随意扎在脑后，神情疲惫
**提示词：**
```
[--token-global: Pixar 3D animation style, RenderMan, ray traced global illumination, claymation feel, appealing silhouette --token-style: Pixar 3D animation style --token-render: RenderMan --token-shading-character: Subsurface Scattering, Peach Fuzz micro-details]
Medium full body shot of a tired 25-year-old woman with bare face, dark circles under eyes, light blue work shirt slightly wrinkled, hair loosely tied back, standing against plain light gray background, soft diffused lighting, slightly desaturated cool tones, shallow depth of field, realistic skin texture, 3:4 aspect ratio
```

### char_female_after - 精致容光状态
**变化维度：** 饱满光泽肌肤、精致妆容、利落盘发、质感职业装
**垫图用途：** 角色定妆照，供分镜垫图
**画面：** 25岁女性，精致淡妆，容光焕发，深蓝职业西装，头发利落盘起
**提示词：**
```
[--token-global: Pixar 3D animation style, RenderMan, ray traced global illumination, claymation feel, appealing silhouette --token-style: Pixar 3D animation style --token-render: RenderMan --token-shading-character: Subsurface Scattering, Peach Fuzz micro-details]
Medium full body shot of a radiant 25-year-old woman with natural makeup, glowing skin, dark blue tailored blazer, hair neatly tied up, standing against plain light gray background, warm side lighting, slightly warm color tone, shallow depth of field, sophisticated complexion, 3:4 aspect ratio
```
```

4. **生成场景概念图提示词**：为每个主要场景写一张概念图提示词。场景图不需要追加角色令牌：

```markdown
### scene_01 - [场景名]
**垫图用途：** 场景氛围概念图，供后续分镜作为环境参考垫图
**画面：** [场景空间描述+时间+天气+氛围+关键陈设]
**提示词：**
```
[前置: --token-global ... --token-style ... --token-render]
[宽景] of [场景描述], [时间/光线], [色彩氛围], [关键陈设细节], [风格]
```

**示例：**
```markdown
### scene_01 - 医疗实验室
**垫图用途：** 场景氛围概念图
**画面：** 现代医疗实验室，冷白顶光，不锈钢台面，一排名牌离心机，墙面嵌入式屏幕
**提示词：**
```
[--token-global: Pixar 3D animation style, Disney CG animation, RenderMan, ray traced global illumination --token-style: Pixar 3D animation style --token-render: RenderMan]
Wide angle view of a modern medical research lab, cold white overhead LED lighting, stainless steel countertops reflecting the cool light, row of benchtop centrifuges, wall-mounted monitors, sterilized clinical atmosphere, toy-like 3D aesthetic, --ar 16:9
```
```

5. **（可选）产品/道具提示词**：如果剧本涉及产品或关键道具，追加生成：

```markdown
### product_xxx - [产品名]
**垫图用途：** 产品道具定妆照
**提示词：**
```
[前置：全局令牌]
[产品描述], [材质细节], [光线], [构图], [风格]
```
```

6. **🔒 自检清单**：输出所有提示词后，必须逐项自检，缺一不可：

| # | 检查项 | ✅❌ |
|---|--------|------|
| 1 | 每个角色是否按变化路径生成了对应版本（before/after） | |
| 2 | 提示词首行是否前置了全局渲染令牌 | |
| 3 | 角色定妆照是否追加了角色专用令牌（如 `--token-shading-character`） | |
| 4 | 场景图是否追加了正确的全局令牌，且没有误加角色令牌 | |
| 5 | 同角色在不同版本间的核心特征（发色、瞳色）是否一致 | |
| 6 | 角色名是否与 Phase 1 角色蓝图中的 ID 一致 | |
| 7 | 图片提示词中是否没有 `$not` 语法 | |

**自检全部通过后**，展示给用户确认。用户确认后才进入 Phase 4。
