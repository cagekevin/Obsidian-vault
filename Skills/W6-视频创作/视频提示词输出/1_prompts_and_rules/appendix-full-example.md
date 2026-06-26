# 附录：完整输出示例

> 当用户说"帮我做一个小短片，一个职场人在深夜便利店的故事"：

**Phase 1 — 剧本：**
```markdown
# 深夜便利店

## 故事概述
加班到深夜的上班族走进便利店，在关东煮的热气和店员的问候中，找到一瞬间的治愈。

## 角色
- **主角**：30岁男性，灰色西装略皱，深棕发，黑框眼镜，疲惫→释然
- **店员**：25岁女性，白色制服，温暖微笑

## 剧本

### 场景 1：深夜街道 — 疲惫
**Archetype：** 揭示 (Reveal)
**摄像机签名：** 摇臂/环绕，运动控制何时看到主体
主角独自走在空旷的街道上，路灯把他的影子拉长。手机屏幕亮着未读消息。

### 场景 2：便利店门口 — 犹豫
**Archetype：** 氛围 (Atmosphere)
**摄像机签名：** 极慢推镜头
主角在门口停住，暖光从玻璃门溢出，犹豫是否进去。

### 场景 3：店内 — 温暖
**Archetype：** 旅程 (Journey)
**摄像机签名：** 跟拍/平移
主角走进店内，店员微笑问候，关东煮的热气升腾。
```

**Phase 2 — 视觉风格说明书：**
```markdown
## 视觉风格说明书

**风格来源：** 真实电影纪实风

**角色建档：**
| 角色ID | 面貌骨相 | 强制锚点 | 严密穿搭 |
|--------|---------|---------|---------|
| char_main | 30岁亚洲男性 | 黑框眼镜、微乱发型 | 深灰西装+白衬衫 |
| char_clerk | 25岁亚洲女性 | 齐肩发、温暖眼神 | 白色制服 |

**视听令牌：**
| 令牌 | 值 |
|------|-----|
| `--token-director` | David Fincher |
| `--token-lighting` | 5600K Cool White + Warm Fill |
| `--token-camera` | 35mm Film Grain, Octane Render |
```

**Phase 3 — 定妆提示词：**
```markdown
### char_main_before - 疲惫状态
**变化维度：** 暗沉肤色、西装起皱、眼镜微斜
**垫图用途：** 角色定妆照，供分镜垫图
**提示词：**
```
[--token-director: David Fincher --token-lighting: 5600K Cool White --token-camera: 35mm Film Grain]
Full body portrait of a tired 30-year-old Asian man in wrinkled gray suit, loosened tie, black glasses slightly askew, standing against dark urban background, cool overhead light casting deep shadows, desaturated skin tone, realistic stubble texture, 35mm film grain, --ar 3:4
```

### scene_01 - 深夜街道
**垫图用途：** 场景氛围概念图
**提示词：**
```
[--token-director: David Fincher --token-lighting: 5600K Cool White --token-camera: 35mm Film Grain]
Wide angle view of an empty late-night street, wet asphalt reflecting streetlights, cool blue color temperature, misty atmosphere, distant warm glow from a convenience store, high contrast shadows, cinematic noir mood, --ar 16:9
```
```

**Phase 4 — 分镜提示词：**
```markdown
## 第 1 组：深夜便利店门口
**Archetype：** 揭示 (Reveal)
**摄像机签名：** 摇臂/环绕

### 分镜备注
- **总情绪：** 孤独→温暖，从冷蓝过渡到暖黄
- **灯光曲线：** 冷白路灯 → 便利店暖光溢出

#### 镜头 01 — 走近 [Ch1-Shot01]
**景别：** 极远景
**焦点状态：** State C · 宏大叙事
**画面：** 深夜空旷街道，主角身影极小从远处走来
**参考垫图：** scene_01
**提示词：**
```
[--token-director: David Fincher --token-lighting: 5600K Cool White --token-camera: 35mm Film Grain]
Extreme wide shot of a lone figure walking down empty late-night street, streetlights casting long shadows, cool blue, misty atmosphere, distant warm glow from store sign, rule of thirds, --ar 16:9
```

#### 镜头 02 — 犹豫 [Ch1-Shot02]
**景别：** 中景
**焦点状态：** State B · 动作交互
**画面：** 主角停步，暖光半边脸，冷蓝填充
**参考垫图：** char_main_before, scene_01
**提示词：**
```
[--token-director: David Fincher --token-lighting: 5600K Cool White --token-camera: 35mm Film Grain]
Medium shot of a tired man stopping in front of convenience store, warm yellow light on half his face, cool blue fill on shadow side, chiaroscuro lighting, realistic skin texture, --ar 16:9
```

### 第 1 组故事板合成图
**布局：** 2 个镜头竖排
**提示词：**
```
Grid storyboard with 2 panels vertical:
Panel 1 (Extreme wide): Lone figure on empty night street
Panel 2 (Medium): Man at convenience store, warm light on face
Cinematic storyboard, color key frames, David Fincher style, 35mm film grain, --ar 9:16
```
```

**Phase 5 — 视频提示词：**
```markdown
## 第 1 组视频
**推荐时长：** 12s
**垫图建议：** 用第 1 组故事板合成图作为视频垫图
**提示词：**
```
缓慢推进镜头，深夜空旷街道上，一个西装男子从远处走来，路灯下拉长影子，冷蓝调，逐渐接近暖光便利店，画面从冷蓝过渡到暖黄
```

## ✅ 项目完结 — 深夜便利店
| Phase | 产出 | 数量 |
|-------|------|------|
| Phase 1 | 剧本 + 角色蓝图 | 1 份 |
| Phase 2 | 视觉风格说明书 | 1 份 |
| Phase 3 | 角色定妆照 + 场景概念图 | 2 条 |
| Phase 4 | 分镜提示词 + 故事板合成图 | 1 组 |
| Phase 5 | 视频提示词 | 1 组 |
```
