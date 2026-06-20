# Phase 4: 故事板分镜

**产出：** 每组的故事板数据（中文分镜备注 + 每镜图片提示词 + 故事板图提示词）
**终止条件：** 用户确认构图满意，**确认前严禁进入 Phase 5**

> **故事板是管线中的三层关键节点**：
> 1. **创作层** → Agent 做创作决策（镜头怎么走、情绪什么曲线），决定每镜内容
> 2. **垫图层** → 引用 Phase 3 的角色定妆照和场景概念图作为参考垫图
> 3. **确认层** → 用户看完整分镜确认后，这些提示词生成的图片成为视频生成的主垫图

**时序说明：** 以下流程**逐组执行**。每完成一组 → 展示给用户确认 → 下一组。不在 Phase 3 预创建所有组。

---

#### Step 1: 读取输入

读取以下材料：
- `story.md` — 剧本（含 Phase 1 标注的每场冲突 Archetype）
- 风格说明书 — 渲染令牌（Phase 2 产出）
- 角色定妆照提示词 — 了解角色外貌（Phase 3 产出）

#### Step 2: Archetype → 摄像机签名映射（关键）

从 Phase 1 标注的每场冲突 Archetype，确定摄像机签名：

| Archetype | 摄像机签名 |
|-----------|-----------|
| **对决 (Duel)** | 低角度交替拍摄，优势方更低 |
| **对峙 (Confrontation)** | OTS 过肩镜头，权力转换时越过轴线 |
| **审讯 (Interrogation)** | 不对等构图，审问者低角度，受审者推进 |
| **谈判 (Negotiation)** | 对称等量构图，相同景别 |
| **追逐 (Pursuit)** | 距离拉开/拉近，被追者在画面前方 |
| **冲击 (Impact)** | 慢→快→慢，接触点为画面中心 |
| **旅程 (Journey)** | 跟拍/航拍，景物从旁掠过 |
| **氛围 (Atmosphere)** | 极慢推镜头或静止，微变化承载全部 |
| **揭示 (Reveal)** | 摇臂/环绕，摄像机运动控制何时看到主体 |

#### Step 3: 分组与编号

按剧本结构划分自然组。**N 从 1 开始**，一组对应一个独立场景或连续情绪段落。**镜头编号 XX-YY 必须连续递增**（如 01-06、07-11）。

#### Step 4: 每组产出物

每组产出**三份内容**：中文分镜备注 + 每镜独立图片提示词 + 故事板合成提示词

**① 中文分镜备注（替代原版 group{N}_note.txt）**

```markdown
## 第 N 组：[场景名称]

### 分镜备注
- **总情绪：** [该组整体情绪基调]
- **Archetype：** [对决/对峙/追逐/冲击等]
- **摄像机签名：** [低角度交替/OTS过肩/跟拍等]
- **灯光曲线：** [该组内光线从什么变为什么]
- **角色位置：** [每角色在该组中的空间位置]
- **角色服装状态：** [哪个版本的服装，变化路径状态]
```

**② 每镜独立图片提示词（单镜原画用）**

每镜必须包含以下全部字段，**缺一不可**：

```markdown
#### 镜头 XX — [镜头标题] [Ch{N}-Shot{XX}]
**景别：** [极远景/全景/中景/中近景/特写/极特写]
**焦点状态：** [State A 微观细节 / State B 动作交互 / State C 宏大叙事 / State D 宏微融合]
**画面：** [中文描述，角色动作+表情+环境]
**参考垫图：** [引用 Phase 3 资产ID，如 char_main_female_before, scene_01]
**提示词：**
```
[前置: --token-global ... --token-style ... --token-render]
[景别] of [主体动作], [环境细节], [光线/色彩], [构图/视角], [风格], [工具参数]
```
```

**③ 故事板合成提示词（整组总览用）**

每组**必须**生成一张故事板合成图提示词——这是后续视频生成的主垫图：

```markdown
### 第 N 组故事板合成图
**用途：** 将本组所有镜头合成一张网格故事板大图，
        用于视觉确认 + 后续视频生成的主垫图

**布局：** [本组 N 个镜头, 按 2x3 / 3x2 / 竖排等布局排列]

**合成提示词：**
```
Grid storyboard layout with [N] panels arranged in [2x3] grid,
each panel depicting a sequential shot from [场景名称]:
Panel 1 (Wide shot): [镜头1画面浓缩]
Panel 2 (Medium close-up): [镜头2画面浓缩]
Panel 3 (Close-up): [镜头3画面浓缩]
...
Cinematic storyboard style, blue pencil sketch or color key frames,
shot numbers and arrows indicating camera movement,
[风格令牌], [工具参数]
```
```

#### Step 5: 完整分组示例

```markdown
## 第 1 组：深夜便利店门口
**Archetype：** 揭示 (Reveal)
**摄像机签名：** 摇臂/环绕，运动控制何时看到主体

### 分镜备注
- **总情绪：** 孤独→温暖，从冷蓝过渡到暖黄
- **灯光曲线：** 冷白路灯 → 便利店暖光溢出
- **角色位置：** 主角从街道深处走来→停在店门口

#### 镜头 01 — 街道深处走来 [Ch1-Shot01]
**景别：** 极远景
**焦点状态：** State C · 宏大叙事
**画面：** 深夜空旷街道，主角身影极小，从远处走来，路灯拉长影子
**参考垫图：** scene_01（街道夜景概念图）
**提示词：**
```
[--token-global: Pixar 3D animation style, Disney CG animation, RenderMan, ray traced global illumination, claymation feel, appealing silhouette --token-style: Pixar 3D animation style --token-render: RenderMan]
Extreme wide shot of a lone figure walking down an empty late-night street, streetlights casting long shadows, cool blue color temperature, misty atmosphere, distant warm glow from a convenience store sign, cinematic composition, rule of thirds, --ar 16:9
```

#### 镜头 02 — 停步凝望 [Ch1-Shot02]
**景别：** 中景
**焦点状态：** State B · 动作交互
**画面：** 主角停步，抬头看向便利店，暖光照在半边脸上
**参考垫图：** char_main_before（主角定妆照-疲惫版）, scene_01
**提示词：**
```
[--token-global: Pixar 3D animation style, Disney CG animation, RenderMan, ray traced global illumination, claymation feel, appealing silhouette --token-style: Pixar 3D animation style --token-render: RenderMan]
Medium shot of a tired man in gray suit stopping in front of a brightly lit convenience store, warm yellow light illuminating half his face creating dramatic chiaroscuro, cool blue fill on the shadow side, slight rain on his shoulders, realistic skin texture, subsurface scattering, --ar 16:9
```

#### 镜头 03 — 暖光吸引 [Ch1-Shot03]
**景别：** 特写
**焦点状态：** State A · 微观细节
**画面：** 主角的眼镜反射着店内暖光，眼神从疲惫变得柔和
**参考垫图：** char_main_before
**提示词：**
```
[--token-global: Pixar 3D animation style, Disney CG animation, RenderMan, ray traced global illumination, claymation feel, appealing silhouette --token-style: Pixar 3D animation style --token-render: RenderMan]
Extreme close-up of eyeglasses reflecting warm convenience store light, tired eyes behind glass transitioning to soft warmth, rain droplets on lenses catching neon refraction, shallow depth of field, Peach Fuzz skin texture, Subsurface Scattering on skin, --ar 16:9
---
```

### 第 1 组故事板合成图
**布局：** 3 个镜头竖排排列
**提示词：**
```
Grid storyboard layout with 3 panels arranged vertically:
Panel 1 (Extreme wide): A lone figure walking down empty night street
Panel 2 (Medium shot): Man in suit stopping at convenience store, warm light on face
Panel 3 (Extreme close-up): Eyeglasses reflecting warm store light, eyes softening
Cinematic storyboard style, color key frames with lighting notes,
shot numbers and camera direction arrows, Pixar 3D animation style,
RenderMan, ray traced global illumination, --ar 9:16
```
```

#### Step 6: 渲染令牌注入（关键）

每个提示词**首行必须强制前置**全局渲染令牌，从 Phase 2 风格说明书的渲染令牌模块提取：
- 单镜和故事板合成图都用全局令牌（`--token-global / --token-style / --token-render`）
- 角色镜头不需要追加角色专用令牌（角色令牌只用于 Phase 3 定妆照）
- 不同风格有不同的令牌名，从 Phase 2 输出中原样提取

#### Step 7: 🔒 自检清单

输出每组后必须逐项自检：

| # | 检查项 | ✅❌ |
|---|--------|------|
| 1 | 镜头编号是否连续递增（XX-YY） | |
| 2 | 每镜是否包含所有必需字段（景别/焦点状态/画面/参考垫图/提示词） | |
| 3 | 提示词首行是否前置了全局渲染令牌 | |
| 4 | 参考垫图是否引用 Phase 3 产出的资产 ID（char_*/scene_*） | |
| 5 | 引用的资产 ID 是否在 Phase 3 中确实产出过 | |
| 6 | 同角色在不同镜头中外貌是否一致（服装版本、发色、瞳色） | |
| 7 | Archetype 摄像机签名是否在运镜描述中体现 | |
| 8 | 灯光曲线是否在该组内有连续变化（而非每镜各亮各的） | |
| 9 | 图片提示词中是否没有 `$not` 语法 | |
| 10 | 是否生成了故事板合成图提示词（供视频垫图用） | |

#### Step 8: 熔断确认

**展示给用户确认**。使用二元问题：
> "第 N 组分镜构图满意，可以出视频，还是需要调整细节？"

- **"调整"** → 修改对应镜头的提示词，重新展示
- **"满意"** → 进入下一组，全部完成后进入 Phase 5

**未获用户明确确认前，严禁进入 Phase 5（视频提示词阶段）。**
