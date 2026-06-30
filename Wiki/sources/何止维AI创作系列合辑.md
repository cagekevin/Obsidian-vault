---
type: source
title: "何止维 AI 创作系列合辑"
status: ingested
tags:
  - source
  - image-generation
  - video-generation
  - prompt-engineering
  - methodology
  - hezhiwei
created: 2026-06-30
updated: 2026-06-30
related:
  - "[[AI底层机制与高级控制]]"
  - "[[人感审美与材质重塑]]"
  - "[[AI视觉语法体系]]"
  - "[[AI氛围与色彩控制]]"
  - "[[AI镜头语言进阶]]"
  - "[[AI 生图决策规则]]"
  - "[[何止维]]"
source: "B 站 UP 主何止维 12 个视频转录稿"
---

# Source: 何止维 AI 创作系列合辑

> B 站 UP 主：**何止维**
> 时间跨度：2026-03-23 ~ 2026-06-16
> 核心定位：AI 图片/视频提示词底层方法论，不讲操作讲逻辑

## 视频列表

| 日期 | 标题 | 核心主题 |
|------|------|---------|
| 2026-03-23 | 避免无效抽卡 | 知识诅咒：你默认 AI 知道的东西，AI 根本不知道 |
| 2026-03-23 | 一步错步步错 | 生图两段式：信息版→情绪版，先锁内容再上影调 |
| 2026-03-23 | 翻遍B站材质提示词 | PBR材质、粗糙度、菲涅尔、AO、GI、高光滚降专业术语 |
| 2026-03-28 | 氛围感提示词直接拿去用 | 氛围不是堆砌，是控制；体积光/丁达尔/粒子效果 |
| 2026-04-06 | AI总是看不懂你的提示词 | 提示词修正思路：强磁、歧义修正、删高干扰动作 |
| 2026-04-11 | 提示词没有执行顺序 | 权重竞争机制：模型不是流程图 |
| 2026-04-14 | 电影级构图提示词 | foreground framing、partial body、asymmetrical balance |
| 2026-05-10 | 首尾帧梦境转场 | 首尾帧核心机制、四步控制法 |
| 2026-05-21 | 电影感布光手把手带练 | 电影感布光分析：光影情绪、明暗秩序 |
| 2026-05-28 | 电影感布光提示词这样写 | 布光专业术语：high side back light、soft front fill |
| 2026-06-05 | 光是怎么影响视觉情绪的 | 光线情绪设计：顶光压迫感、弱补光保留细节 |
| 2026-06-16 | 一个提示词瞬间提升质感 | 低长调影调控制：low-key + high contrast |

## 核心方法论提炼

### 一、提示词底层机制

**1. 知识诅咒** — AI 不懂你脑子里默认知道的东西。你写"机甲"，AI 不知道那是机甲还是外星人还是怪物。必须把"你觉得 AI 应该知道"的部分显式写出来。**解法**：将你能理解的抽象概念换成 AI 能理解的具体形象定义。

**2. 权重竞争（非执行顺序）** — 提示词没有执行顺序，只有权重竞争。模型不是流程图，不会按顺序执行。提示词的结果只被5点影响：
- 词本身够不够强（双手合十跪拜=强，克制自然=弱）
- 词是否容易视觉化（抬头=易视觉化，虔诚=抽象）
- 词之间会不会重组冲突（背对镜头看向前方+看到表情=冲突）
- 训练数据里哪种组合更常见
- 参考图的影响

**3. 修正思路** — AI 更擅长执行显性动作，不擅长补全隐性逻辑。修正三步：
- 删高干扰动作（强动作会牺牲身体朝向和头部逻辑）
- 修正强磁（把抽象词换成具体动作）
- 明确动作歧义（"参拜"→"拜佛"）

### 二、生图流程

**4. 信息版→情绪版两段式** — 先做信息版（平光可读性最高，所有细节看得清），再做情绪版（影视化布光、影调氛围、色彩风格）。**核心规则**：内容锁死之后再上影调，不要在情绪版上修改内容。如果要换完全不同的光影风格，回到信息版重做。

### 三、布光与影调

**5. 低长调（low-key + high contrast）** — 影调不是滤镜。低长调以暗部为画面基底，同时保留完整调域跨度，通过局部高光、深黑位、暗部细节和中间调层次形成强烈而受控的明暗组织。代表作品：七宗罪、银翼杀手2049、沉默的羔羊、蝙蝠侠。

**6. 电影感布光分析** — 电影感布光不是为了照明，而是为了表达故事的情绪与思想。核心是分析光的方向、强度、色温、软硬，以及它们如何塑造情绪。

### 四、材质控制

**7. PBR材质术语库** — 材质提示词的核心不是堆"金属质感""高级感"，而是用专业术语精确描述材质属性：
- **PBR材质** — 基于物理的渲染材质，让材质和光的关系更像真的
- **粗糙度** — 表面反光是锐利还是发散（不是摸起来差不扎手）
- **菲涅尔效应** — 越斜越容易反光（裸铁没反光，清漆层产生菲涅尔）
- **AO（环境光遮蔽）** — 缝隙阴影强调，结构夹角处通常更暗
- **GI（全局光照）** — 光照到物体后还在环境里反弹
- **高光滚降（specular rolloff）** — 高光从亮到不亮过渡是否自然，没有会像塑料

### 五、风格控制

**8. 三维渲染二维感** — 皮克斯风格去 AI 感的核心。保留三维的体积感（脸部结构、皮肤反光、衣服褶皱、真实灯光），同时加入二维绘画的处理（夸张表情、手绘纹理、色块、非真实比例）。用3D技术做2D审美。

### 六、构图

**9. 构图术语库**：
- **Foreground framing（前景遮挡构图）** — 前景遮挡物不是装饰，而是为主体服务
- **Partial body framing（局部构图）** — 切掉部分身体让信息更集中
- **Asymmetrical balance / negative space（非对称平衡/留白）** — 双主体关系+大量留白塑造孤静情绪
- **Center composition / near symmetrical balance（中心对称构图）** — 表达公平、平衡、秩序感

### 七、光线与情绪

**10. 光线情绪设计** — 光线不只照亮画面，更塑造情绪：
- 顶光（top light）：强化皮肤纹理皱纹，塑造压迫感与危险
- 弱补光（weak frontal fill）：只保留最低限度细节，不要死黑
- 边缘高光（rough edge highlights）：区别于精致棚拍感的脏硬粗糙高光

### 八、氛围控制

**11. 氛围不是堆砌** — 氛围感不是加的越多越好，而是越有控制越高级。核心元素：high contrast（明暗对比）、volumetric smoke/fog（体积光/空气介质）、cinematic lighting（有情绪有重点的光）、sparks（粒子效果点到为止）。

### 九、首尾帧控制

**12. 首尾帧四步思维模型** — 详见 [[AI首尾帧控制]]。核心：首尾帧的机制是最短路径，你的提示词就是为 AI 重新定义最短路径。

## 关键洞察

- 何止维的底层方法论与刺猬星球系列高度互补——刺猬星球偏操作技巧，何止维偏底层逻辑
- 所有方法论都指向同一个核心：**AI 不是理解文字，而是在竞争性地抓取信号**
- 专业术语（cinematic lighting、PBR、low-key 等）是比抽象形容词更有效的提示词

---

## 完整提示词原文

以下为各视频中出现的可直接使用的提示词原文，一字不差。

### 低长调影调（来自《都来学！一个提示词瞬间提升AI画面质感》）

动作犯罪片：
```
Low-key lighting, high contrast, deep shadows,
volumetric beams cutting through darkness,
urban night setting, gritty texture, cinematic mood.
```

高端男性香水广告：
```
Low-key lighting with controlled highlights,
smooth specular rolloff on glass surfaces,
deep blacks with subtle reflection details,
luxurious and understated atmosphere.
```

### 材质提示词（来自《翻遍整个B站，这绝对是讲的最好的材质提示词撰写逻辑》）

材质升级提示词（带约束，不改原有画面设计）：
```
PBR materials, physically-based rendering,
roughness variation, mixed roughness surfaces,
subtle Fresnel reflections,
ambient occlusion in structural crevices,
global illumination, bounced light,
smooth specular rolloff, natural highlight falloff,
surface wear with logical dirt accumulation,
micro-surface details, realistic material transitions.
```

### 电影感布光（来自《电影感布光提示词这样写》）

```
Cinematic lighting, high side back light,
volumetric beams, soft front fill,
rough edge highlights, warm and cool color contrast,
atmospheric haze, dramatic shadow distribution,
cinematic color grading.
```

### 皮克斯去AI感（来自《皮克斯风格去除AI感》）

```
Pixar-style character, 3D rendering with 2D aesthetics,
cinematic lighting, volumetric atmosphere,
semi-realistic materials, hand-painted textures,
exaggerated expressions, film-level composition,
not toy-like, not overly polished.
```

### 构图提示词（来自《小白也能做出高级氛围感AI画面》）

前景遮挡构图：
```
Cinematic shot, foreground framing with blurred elements,
partial obstruction creating depth and peeking perspective,
subject in the gap between foreground elements,
soft focus on foreground, sharp on subject.
```

局部构图：
```
Partial body framing, close crop on upper body,
mechanical arm entering from top-left, sword cutting across,
another hand at bottom-right holding the hilt,
strong diagonal lines, dynamic tension.
```

非对称平衡与留白：
```
Asymmetrical composition, negative space,
large sky and cloud area, small figure in the frame,
tree and figure as dual subjects, sense of solitude,
calm and quiet mood.
```

中心对称构图：
```
Center composition, near symmetrical balance,
subject at center axis, equal visual weight on both sides,
dark background with soft out-of-focus lights,
formal, orderly, ceremonial atmosphere.
```

### 光线情绪（来自《光是怎么影响视觉情绪的》）

顶光压迫感：
```
Top light from upper right, hard light cutting down,
deep shadows in eye sockets, neck, and collar,
strong skin texture and wrinkles, rough edge highlights,
weak frontal fill to retain minimum detail,
oppressive, dangerous, gritty atmosphere.
```

### 氛围感（来自《如何让AI视频更有电影感？这些氛围感提示词直接拿去用》）

```
Cinematic lighting, high contrast,
volumetric smoke or fog, atmospheric haze,
particle effects (sparks, dust motes),
directional light cutting through darkness,
deep shadows with detail, controlled highlights,
cinematic mood, not poster-like, not overdone.
```
