# Lovart 拼图碎片 — Prompt工程

## 话术

你在生成图片时，怎么写 prompt？你是怎么把用户的一句话需求，扩展成详细的图片生成 prompt 的？你的 prompt 结构是什么、每部分写什么、怎么确保画面质量和风格准确？把完整的 prompt 构建流程讲出来。

## 回复

我来详细讲解我的图片生成 Prompt 构建流程。
---
## 我的 Prompt 构建流程
### 第一步：理解用户意图
从用户的一句话需求中提取核心要素：
- **主体**（Subject）：画面主要是什么
- **动作/状态**（Action）：主体在做什么
- **场景/环境**（Setting）：在哪里发生
- **风格/氛围**（Style/Mood）：什么视觉风格、情绪
- **技术规格**（Technical）：尺寸、比例、分辨率等
### 第二步：结构化扩展
我将 Prompt 分为以下几个层次，逐层构建：
```
[主体描述] + [细节刻画] + [场景环境] + [光影氛围] + [风格修饰] + [技术参数] + [质量强化词]
```
#### 1. 主体描述（Subject）
- 明确主体是什么（人物/物体/场景）
- 包含数量、姿态、表情、服装等关键特征
- **原则**：具体、可视觉化
#### 2. 细节刻画（Details）
- 材质、纹理、装饰元素
- 颜色搭配
- 特殊标志或特征
#### 3. 场景环境（Environment）
- 背景类型（室内/室外/抽象）
- 景深关系（前景、中景、背景）
- 环境元素（家具、自然元素、建筑等）
#### 4. 光影氛围（Lighting & Atmosphere）
- 光源类型（自然光/人工光/混合光）
- 光线方向（侧光、逆光、顶光等）
- 时间氛围（清晨、黄昏、夜晚）
- 色调倾向（暖色、冷色、对比度）
#### 5. 风格修饰（Style）
- 艺术风格（写实、油画、赛博朋克、极简等）
- 参考艺术家或流派
- 渲染方式（3D渲染、摄影、插画等）
#### 6. 技术参数（Technical）
- 相机视角（特写、广角、鸟瞰等）
- 焦距效果（景深、虚化）
- 构图方式（对称、三分法、引导线等）
#### 7. 质量强化词（Quality Boosters）
- 高画质关键词：masterpiece, best quality, highly detailed, 8k, ultra-detailed
- 专业摄影词：professional photography, sharp focus, cinematic lighting
---
## 实际案例演示
**用户输入**：「一只橘猫在窗台上晒太阳」
**我的构建过程**：
| 层次 | 内容 |
|------|------|
| 主体 | A fluffy orange tabby cat |
| 细节 | with soft fur, green eyes, relaxed posture, slightly chubby body |
| 场景 | sitting on a wooden windowsill, vintage-style room, potted plants nearby |
| 光影 | warm afternoon sunlight streaming through the window, golden hour glow, soft shadows |
| 风格 | photorealistic, cozy domestic atmosphere |
| 技术 | close-up shot, shallow depth of field, bokeh background |
| 质量 | masterpiece, best quality, highly detailed, 8k resolution |
**最终 Prompt**：
> "A fluffy orange tabby cat with soft fur and green eyes, sitting relaxed on a wooden windowsill in a vintage-style room with potted plants nearby. Warm afternoon sunlight streaming through the window creating golden hour glow and soft shadows. Photorealistic style with cozy domestic atmosphere. Close-up shot with shallow depth of field and bokeh background. masterpiece, best quality, highly detailed, 8k resolution."
---
## 确保质量和风格准确的方法
### 1. **关键词权重**
- 将最重要的元素放在 Prompt 前面
- 使用具体描述而非抽象概念
### 2. **负面 Prompt（Negative Prompt）**
同时构建排除项，避免不想要的元素：
> "blurry, low quality, distorted, deformed, ugly, duplicate, watermark, text, logo"
### 3. **参考图像锚定**
当用户提供了参考图时：
- 分析参考图的实际视觉特征（颜色、材质、光影）
- 提取可验证的视觉描述
- 在 Prompt 中明确说明要保留/借鉴的元素
### 4. **风格一致性检查**
- 确认所有描述词在风格上是统一的（不会同时出现"写实"和"卡通"）
- 光影描述与时间/场景逻辑一致
### 5. **尺寸/比例映射**
- 将用户的自然语言（如"手机壁纸"）转换为具体参数
- 确保 aspect_ratio 或 target_size 符合使用场景
---
## 核心原则总结
| 原则 | 说明 |
|------|------|
| **具体优于抽象** | "金色阳光"比"好看的光"更有效 |
| **层次清晰** | 主体→环境→光影→风格，逻辑递进 |
| **忠实用户意图** | 不擅自添加用户没要求的元素 |
| **视觉可验证** | 每个描述词都能在脑中形成画面 |
| **技术参数明确** | 尺寸、比例、分辨率必须精确映射 |
这个流程确保我能将简单的一句话需求，转化为模型能准确理解和执行的结构化 Prompt，同时保持对用户原始意图的忠实度。
