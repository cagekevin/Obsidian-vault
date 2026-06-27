---
type: concept
title: "AI Camera Movements"
complexity: beginner
domain: video-generation
aliases:
  - "AI 运镜提示词"
  - "运镜手法"
created: 2026-06-23
updated: 2026-06-24
tags:
  - concept
  - video-generation
  - prompt-engineering
status: developing
related:
  - "[[Visual Description First Principle]]"
  - "[[AI打光五法]]"
  - "[[AI光源提示词模板库]]"
sources:
  - "https://www.bilibili.com/video/BV1xBjW6pEym"
---

# AI Camera Movements

AI 视频生成中常用的运镜手法提示词。讲故事并不需要大量运镜，许多优秀电影仅用硬切，也能达到很好效果。

---

## 基础运镜

### 推镜 (Push In)
镜头向主体前进，营造靠近、发现或压力的视觉感受。

### 拉镜 (Pull Out)
镜头从远景拉至主体特写，用于强调细节或突出情绪。

### 摇镜 (Pan)
摄影机左右或上下转动，用于展示环境或跟随运动。

### 移镜 (Dolly)
机位横向或纵向移动，常用于跟随主体或在空间穿行。

### 横移 (Truck)
镜头平行于主体侧移动，展示场景或制造动态感。

### 升降镜 (Pedestal)
摄影机垂直运动，创造从地面到高处的视角转换。

### 环绕镜 (Orbit)
围绕主体旋转拍摄，全方位展示其形态与状态。

### 变焦推拉 (Zoom)
通过焦距变化改变主体大小，快速强调画面焦点。

---

## 动态与情绪运镜

### 手持抖动 (Handheld)
人为制造晃动感，常用于模拟纪实或紧张氛围。

### 甩镜 (Whip Pan)
镜头快速从一个目标摇到另一个，制造转场冲击力。

### 主观镜头 (POV)
模拟角色视点，让观众代入视角体验事件。

### 无人机航拍 (Aerial Drone)
从空中俯瞰，展现宏大场景或独特地貌风貌。

### 光学变焦 (Optical Zoom)
不移动机位，通过镜头焦距改变放大或缩小画面。

### 前跟镜 (Follow Front)
镜头跟随运动主体前方拍摄，强调其前进方向与目的。

### 侧跟镜 (Follow Side)
镜头与运动主体平行侧移，展现其行进姿态。

### 过肩镜 (Over the Shoulder)
越过角色肩膀拍摄对话对象，营造对话现场感。

### 荷兰角 (Dutch Angle)
倾斜镜头制造失衡感，常用于表达不安或紧张情绪。

---

## 角度与视角

### 低角度 (Low Angle)
从下往上仰拍主体，使其显得高大、威严或具压迫感。

### 高角度 (High Angle)
从上往下俯拍主体，使其显得渺小、孤独或被审视。

### 鱼眼视角 (Fisheye)
使用广角镜头产生夸张畸变，营造奇幻或扭曲感。

### 旋转镜 (Spin)
镜头自身旋转，制造眩晕感或视角转换的戏剧效果。

### 鸟瞰顶拍 (Bird's Eye View)
从正上方垂直向下拍摄，获得平面化或几何化构图。

---

## 进阶运镜技巧

### 遮挡渐显 (Reveal)
利用前景物体部分遮挡画面，增加层次感与神秘感。

### 穿越镜头 (Fly Through)
镜头穿过缝隙或物体，创造进入新空间的过渡感。

### 拉焦切换 (Rack Focus)
改变焦点，使画面前后景依次清晰，引导注意力。

### 子弹时间 (Bullet Time)
多机位环绕慢拍摄，冻结时间展示动作细节。

### 贴地穿越 (Low Glide)
镜头极低角度掠过地面，营造高速或危机临场感。

### 螺旋上升 (Spiral Up)
镜头围绕主体旋转并上升，常用于英雄出场或宏大揭示。

### 环绕下降 (Spiral Down)
镜头围绕主体旋转并下降，常用于悬念营造或场景结束。

### 低视角街 (Low Street Level)
在较低角度拍摄街道或人群，模拟行人或近距离观察视角。

### 跟随推进 (Follow Push)
边跟随运动主体边向前推进，强化追逐感或运动的紧张感。

### 低弧绕行 (Low Arc Orbit)
以低弧度弧形轨迹环绕主体，增加动感与视觉新鲜感。

---

---

## 英文提示词速查（Seedance 词汇表）

> 来源：第三方整理的 Seedance 2.5 提示词指南（非官方）。写提示词时直接复制这些英文词到 prompt 中。

### 基础运镜

| 你想要的效果 | 提示词里写 |
|------------|-----------|
| 镜头靠近主体 | `slow push in` / `dolly in` |
| 镜头拉远 | `pull back` / `dolly out` |
| 横向滑动 | `tracking shot left/right` |
| 镜头升高 | `crane up` / `boom up` |
| 镜头降低 | `crane down` / `boom down` |
| 跟着主体走 | `steadicam follow shot` |
| 围绕主体旋转 | `orbit shot` / `360 arc` |
| 快速甩过去 | `whip pan left/right` |
| 固定不动 | `static shot` / `locked off camera` |

### 角度

| 你想要的效果 | 提示词里写 |
|------------|-----------|
| 俯拍 | `bird's eye view` / `top-down` |
| 低角度 | `worm's eye view` / `low angle` |
| 手拿晃动感 | `handheld camera` |
| 平滑滑行 | `gimbal shot` |
| 焦点切换 | `rack focus to subject` |

### 进阶运镜

| 你想要的效果 | 提示词里写 |
|------------|-----------|
| 无人机航拍下降 | `aerial drone descending` |
| FPV 穿越 | `FPV drone fly-through` |
| 子弹时间 | `matrix bullet time` |
| 变焦推拉（眩晕效果） | `dolly zoom` / `vertigo effect` |
| 快速变焦 | `crash zoom` |
| 缓慢变焦 | `slow zoom in/out` |
| 甩镜头模糊 | `panning blur` |
| 微抖动 | `micro-jitter` |

## 灯光词汇表

> **一个灯光关键词 > 十个形容词。** 如果生成的画面看起来"平"，先换灯光词，不要改主体描述。

| 你想要的感觉 | 提示词里写 |
|------------|-----------|
| 暖色电影感 | `golden hour cinematography` |
| 黄昏/黎明 | `magic hour` / `blue hour` |
| 夜景暖光 | `tungsten practical lighting` |
| 戏剧感/神秘 | `chiaroscuro lighting` |
| 影棚干净 | `soft box three-point lighting` |
| 赛博朋克 | `neon-drenched night scene` |
| 纪录片自然光 | `natural available light` |
| 恐怖片底光 | `harsh under-lighting` |
| 美妆/时尚 | `butterfly lighting` |
| 阴天户外 | `diffused cloudy daylight` |
| 逆光轮廓 | `rim lighting` / `backlighting` |
| 体积光（上帝光） | `volumetric lighting` / `god rays` |
| 高调/明亮 | `high-key lighting` |
| 低调/暗调 | `low-key lighting` |
| 电影青橙调 | `cinematic teal and orange` |
| 黑白 noir | `noir high contrast black and white` |
| 老胶片 | `nostalgic vintage film` |
| 发光梦幻 | `ethereal glowing light` |

---

## Connections

- 运镜描述属于[[视觉描述优先原则]]的一部分，要用具体的视觉语言，而不是抽象形容词
- 选择运镜时遵循[[描述比重原则]]，重要的运镜多描述，次要的少描述
- 灯光词的使用印证了[[摄影语言锚定质感]]——用具体的摄影术语替代抽象形容词
- AI 生成视频时，运镜提示词要克制，不要同时用太多运镜手法
