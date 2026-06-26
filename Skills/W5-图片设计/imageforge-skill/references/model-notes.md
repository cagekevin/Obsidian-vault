# 模型速查笔记

> 轻量参考——只记格式、quirk、参数和打通状态。场景经验在各scene文件里，通用原理在principles.md里。

---

## 格式速查

| 模型 | 提示词格式 | 画质词 | 负向词 | 颜色防污 | 文字渲染 |
|------|-----------|--------|--------|---------|---------|
| SD 1.5/XL | 逗号短词组 | 必须 | 必须 | BREAK+下划线+权重 | ❌ |
| Flux 2 Pro/Dev | 自然语言长句 | 不需要 | 不需要 | 不需要 | ~65% |
| MJ V7/V8 | 描述+参数 | 不需要 | --no | ::权重 | <40% |
| GPT Image 2 | 自然语言/对话式 | 不需要 | 不需要 | 不需要 | 99%+英文/高中文 |
| Ideogram v3 | JSON优先/自然语言 | 不需要 | 不需要 | JSON分区 | 90-95%英文 |
| Seedream 5.0 | 自然语言(中文强) | 不需要 | 不需要 | 不需要 | 中文强 |
| Qwen-Image 2.0 | 自然语言 | 不需要 | 不需要 | 不需要 | 中等 |
| Gemini Flash | 自然语言 | 不需要 | 不需要 | 不需要 | 中等 |

---

## 模型Quirk速查

### SD 1.5/XL 特有
- **75-token分组**：CLIP每75 token独立编码，跨组无注意力交互。多色多物件必须用BREAK控制分组
- **权重语法**：`(word:1.1-1.3)` 安全区间，>1.5可能崩坏
- **SD专用语法**：`BREAK` 强制分组 | `[A:B:0.5]` 分步绘制 | `[A|B]` 交替采样 | `A AND B` 融合
- **CFG范围**：7-12（日常7-8，写实8-12，创意5-7，水彩7-8，暗光5.5-7.0）
- **采样器**：DPM++ 2M Karras(日常) / SDE Karras(高质量写实)
- **最佳尺寸**：1.5=512/768, XL=1024（偏离=潜空间分布外）
- **LoRA权重**：0.6-0.8，必须匹配基础模型版本
- **词序**：主体特征→画质/风格→动作/姿态→场景/环境→细节修饰

### Flux 特有
- **汪格尔综合症**：写"one girl"出动漫风→写实图写"girl"不写"one girl"（T5将"one girl"关联动漫）
- **人像油腻**：训练数据磨皮→光滑=好皮肤→加"natural skin texture, visible pores, matte finish"
- **CFG**：Schnell 1-2, Dev 2.5-3.5, +LoRA 3-4
- **采样器**：Euler + simple调度器
- **减法思维**：只写控制内容+风格+构图的词，去掉所有SD时代的画质词
- **柔和控图**：利用"信息不对称"——想俯拍只写地面元素，想仰拍只写天空元素

### MJ 特有
- **审美加工 vs 忠实指令**：`--s 0-1000` 控制强度——低值忠实指令，高值MJ自由发挥
- **`--style raw`**：关闭自动美化——商业摄影/写实场景必须
- **`--no`**：替代SD式负向词
- **`::数值`**：控制多概念视觉占比
- **`--c 0-100`**：混乱度——概念探索用高值
- **`--niji 6`**：切换二次元模型
- **艺术家名直接写有效**——MJ训练数据中名字-风格配对密集
- **参数预设**：商业摄影`--ar 3:4 --s 250 --style raw` | 艺术插画`--ar 2:3 --s 750` | 概念设计`--ar 16:9 --c 70`

### GPT Image 2 特有
- **House style**：干净数字感，artistic/sketchy风格被"清理化"——对粗糙手绘风、暗黑童话风是硬伤
- **对抗house style**：描述具体视觉特征而非风格标签——"chalk pastel on textured paper, visible strokes, rough edges"而非"artistic sketchy"
- **输出分辨率**：1728×2304(3:4) 或 2848×1600(16:9)，自适应不可控
- **对话式迭代**：先出基础图，再要求"把背景换成XX"

### Ideogram v3 特有
- **JSON格式比自然语言精确**——Qwen-VL在结构化标注数据上训练
- **Prompt Builder**：画区域框+填描述→自动生成JSON

### 国产模型（Seedream/Qwen-Image/Gemini Flash）
- **直接用中文**——中文理解比翻译后的英文更精确
- **成语/诗词/网络用语有效**——"烟雨江南"、"赛博朋克风"
- **不需要画质词/负向词**——与Flux/MJ同代

---

## ControlNet 速查

| 类型 | 功能 | 典型场景 | 权重 |
|------|------|---------|------|
| Canny | 精确边缘控制 | UI图标线框→出图 | 0.8 |
| Depth | 深度/空间结构 | 建筑/场景构图 | 0.6-0.8 |
| OpenPose | 人体姿态 | 角色动作控制 | 0.6-0.8 |
| Lineart | 线稿上色 | 线稿→彩色插画 | 0.8 |
| MLSD | 直线结构 | 室内/建筑 | 0.6-0.8 |

- **引导范围**：0.1-0.8 表示前80%步数约束，后20%放开让模型风格化
- **冲突避免**：控制信号方向与提示词一致，负向词不加边缘相关词（如"broken lines"会导致边缘撕裂）

---

## 模型可用性与 API Key 状态（2026-06-14）

### 场景→模型→Key 映射（完整版见 api-calls.md）

| 场景 | 首选模型 | Key变量 | 备选模型 | Key变量 |
|------|---------|---------|---------|---------|
| 角色/人物 | GPT Image 2 | OPENAI_API_KEY | Seedream 5.0 | VOLCENGINE_API_KEY |
| 风景/场景 | Flux 2 Pro | FAL_API_KEY | GPT Image 2 | OPENAI_API_KEY |
| 游戏素材/图标 | Recraft V4.1 | RECRAFT_API_KEY | GPT Image 2 | OPENAI_API_KEY |
| 文字海报/排版 | Ideogram v3 | IDEOGRAM_API_KEY | Seedream 5.0(中文) | VOLCENGINE_API_KEY |
| 风格化/艺术 | GPT Image 2 | OPENAI_API_KEY | Flux 2 Pro | FAL_API_KEY |
| 商业摄影 | Flux 2 Pro | FAL_API_KEY | GPT Image 2 | OPENAI_API_KEY |

**降级链**：首选无Key → 备选 → 任何有Key的可用模型 → 告知用户"当前场景无可用模型，请提供[Key名]"

### 模型API价格速查

| 模型 | 平台 | 价格/张 | 获取Key | 状态 |
|------|------|---------|---------|------|
| GPT Image 2 | OpenAI/packyapi | $0.006-0.211 | platform.openai.com 或 packyapi.com | ✅ 已打通(packyapi中转) |
| Seedream 5.0-lite | 火山引擎 | ~$0.035 | console.volcengine.com | ✅ 已打通(原生API) |
| Ideogram v3 | Ideogram | $0.0375-0.1125 | developer.ideogram.ai | ⏳ 待Key |
| Recraft V4.1 | Recraft | $0.04-0.08 | recraft.ai | ⏳ 待Key |
| Flux 2 Pro | fal.ai | ~$0.03 | fal.ai | ⏳ 待Key |

### 暂不可打通
| 模型 | 原因 | 替代 |
|------|------|------|
| MJ V7/V8 | 无官方API | Flux 2 Pro+MJ风格LoRA |
| Leonardo AI | 需企业订阅 | SD XL+游戏LoRA |
| Adobe Firefly 2 | 需CC企业订阅 | GPT Image 2 |
| SD 1.5/XL | 需本地GPU | 用户RTX 4060+ComfyUI |

### API调用详情
→ 见 `api-calls.md`（端点/认证/参数/代码示例/错误处理）

---

## 内置工具 image_generate 说明

- **底层模型**: 未公开确认❓。扣子是字节产品，内置生图更可能使用 Seedream 系列（4.0/4.5/5.0），非 GPT Image 2
- **输出**: 1728×2304(3:4) 或 2848×1600(16:9)，自适应
- **参数**: prompt / count / ref_images / mode("生图"或"抠图") / file_prefix
- **局限**: 无法选择模型；无CFG/步数/采样器控制；无精确分辨率；无负向词；house style清理化artistic风格；像素风只能到风格参考级别（边缘可能有抗锯齿）
- **通用性考虑**: 不依赖此内置工具，优先使用外部API获得确定模型和可控参数；像素素材生产必须用SD+像素LoRA本地管线，内置工具只做风格探索和参考图

---

## 像素风专用模型/LoRA/工具 速查（v6.1，2026-06更新）

像素风是游戏素材生产的核心场景，通用模型出的是"像素风格插画"而非"真像素资产"。专用模型/LoRA/工具是必需的。

### 本地模型（开源，RTX 4060可跑）

| 模型/LoRA | 基座 | 触发词/用法 | 权重 | CFG | Steps | 显存 | 最适合 |
|-----------|------|------------|------|-----|-------|------|--------|
| **⭐ Limbicnation/pixel-art-lora** | FLUX.2-klein-4B (Apache 2.0) | `pixel art sprite, game asset, transparent background, SPR1TE8` | LoRA默认 | 1.0 | 4步 | **8GB** | **2026本地新基线首选**，4步推理最快，支持16-bit/32-bit/chibi修饰 |
| **Z-Image-Turbo + tarn59 pixel LoRA** | Z-Image-Turbo 6B (Apache 2.0) | prompt含pixel art/8-bit/16-bit/sprite | 0.6–1.0 | 4–5 | 8步 | 16GB | 快速原型迭代（0.78秒/张H800，~2秒RTX4070），i2i偏弱 |
| skormino Pixel Art LoRA **v8.0**（⚠️不是v6.3） | Illustrious（二次元新基座） | `masterpiece, pixpix, 8-bit, pixel_art`，CLIP Skip=2 | 1.0 | 3.5–5 | 20–28 | 8GB | 日系二次元像素/JRPG/塞尔达风；⚠️触发词`pixpix`与旧SD1.5模型名冲突 |
| nerijs/pixel-art-xl | SDXL | 无特殊，含"pixel"即可 | 1.0–1.2 | 7.5/1.5(+LCM) | 25-30/8(+LCM) | 8GB | SDXL生态最稳像素LoRA（2026已被FLUX.2-klein分流，降级为可选） |
| Muertu XL 像素世界 V1.3 | SDXL（中文社区） | 中文prompt友好 | 0.8 | 7 | 20 | 8GB | 哩布哩布在线出图/中文用户SDXL选项 |
| Qwen-Image-Pixel-Art-LoRA | Qwen-Image-2512 | `Pixel Art`开头强化 | 0.8–1.2 | 默认 | 20 | 云端 | 中文提示词友好，云端使用 |
| pixelsprite v1.0 | Flux.1 Kontext（BFL编辑基座） | chibi sprite描述（见scene-game-assets B.1） | 默认 | 默认 | 默认 | 16GB | 图生图转像素（参考图改像素），坎公骑冠剑风Q版 |
| 8bitdiffuser/pixpix v4.0 | SD1.5 | `8-bit pixel_art pixpix`（⚠️注意与skormino触发词重名） | 0.8–1.0 | 7–9 | 20–28 | 4GB | 纯正8-bit复古大颗粒（SD1.5已老旧，仅风格化保留） |

**已淘汰/不推荐**：
- ~~SD_PixelArt_SpriteSheet_Generator~~（SD1.5全量checkpoint，2025-01后无更新，已被在线工具超越）
- ~~Pixie-Spritesheet-48~~（未能在任何主流平台找到权威页面，可能已下架）

### 在线工具（生产级）

| 工具 | 核心能力 | 价格 | 推荐度 |
|------|---------|------|--------|
| **⭐ PixelLab (pixellab.ai)** | 双模型(Pixflux文生+Bitforge风格迁移)、4/8方向角色旋转、骨架动画、Wang tileset、等距瓦片、inpaint、导出精灵表；**Aseprite插件+MCP server** | 免费40次；$12–$50/月 | ⭐⭐⭐⭐⭐ 2026年像素生产标杆 |
| Sprite AI (sprite-ai.art) | 16×16–128×128精灵专用，内置编辑器，导出Unity/Godot | $5–$24/月 | ⭐⭐⭐⭐ 小分辨率精灵高效 |
| Retro Diffusion | Aseprite内嵌老牌扩展，三模型(RD Plus/Tile/Animation) | $65一次性/$20Lite; Web $5/月起 | ⭐⭐⭐⭐ Aseprite内嵌最成熟方案 |
| Gamelabs Studio | 通用2D游戏资产，最高1024×1024/1920×1080，支持MCP | 免费20credits; $5–$50 | ⭐⭐⭐ 大幅面像素场景/Boss |
| 即梦AI (Dreamina/Seedream) | 中文云端快速出图，每日免费额度，非游戏专用 | 免费/会员 | ⭐⭐ 中文用户零门槛快速概念参考，不做资产主力 |

### MCP/Aseprite集成（2026 vibe coding新趋势）

| 项目 | 作用 |
|------|------|
| **willibrandon/pixel-mcp** | Go/MIT，暴露Aseprite画布/图层/调色板/动画/导出全能力给Cursor/Claude Code |
| Dizzd/aseprite-extension-mcp | TypeScript/WebSocket桥接，跨进程控Aseprite |
| PixelLab MCP Server | 在代码编辑器内生成像素资产，配合Aseprite插件形成闭环 |

→ 让AI编码助手直接操作Aseprite，实现"边写代码边出素材"的vibe coding工作流。

### 工作流三级火箭

1. **快速原型/8步迭代**：Z-Image-Turbo + tarn59 pixel LoRA（8步，Apache 2.0）
2. **本地高质量主力**：FLUX.2-klein-4B + Limbicnation/pixel-art-lora（4步，8GB显存，Apache 2.0）
3. **生产级资产**：PixelLab（$12+/月）+ Aseprite插件 + MCP，出8方向角色、动画、tileset，直接导出引擎可用精灵表

### 像素风通用参数/禁用

**像素风必加技术词**：`no anti-aliasing, hard edges, sharp pixels, flat shading, limited palette, pixel perfect, nearest neighbor scaled`
**像素风禁用**：高CFG(>10)、高Steps(>40)、photorealistic/3D render/lens flare/bloom/gradient/depth of field、原生大分辨率(>1024)
**像素风推荐采样器**：DPM++ 2M Karras / Euler a / LCMScheduler(+LCM) / FlowMatch(FLUX)

> 版本核查基准：2026-06-24。模型/LoRA更新频繁，生产前在Civitai/HuggingFace确认是否有新版。
>
> 🔴 **Recraft V4定位修正**：像素非其强项，核心能力是SVG矢量/品牌图标；像素游戏素材不推荐Recraft作为主力。
>
> 🔴 **dotown定位修正**：这是免费像素素材库（提供现成素材下载），不是AI生成工具。
