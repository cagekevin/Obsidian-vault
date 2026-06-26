---
name: ai-image-prompt
description: "AI生图Prompt决策引擎——agent收到生图请求后，按5步流程解析→路由→组装→质检→诊断。不是给人读的知识库，是给agent执行的可操作决策链。触发：用户需要生成/修改/调试AI图片，或询问任何生图策略时使用。"
version: "6.1"
---

# AI Image Prompt Skill — Agent Decision Engine

> 这是执行流程，不是学习材料。每一步都是可执行决策。

## Step 1: 请求解析

收到用户请求后，提取5个slot：

| Slot | 含义 | 提取方式 |
|------|------|---------|
| scene | 场景类型 | 从用户描述推断（见Step 2路由表） |
| subject | 画什么 | 用户请求的核心对象 |
| style | 风格约束 | 用户提到的风格名/参考作品/视觉特征 |
| refs | 参考图模式 | 无参考 / 参考生成 / 图片修改 |
| constraints | 额外约束 | 尺寸/格式/用途/批量要求等 |

**解析规则**：
- 用户给图+要求"基于这张画/用这个风格" → refs=参考生成，mode=生图
- 用户给图+要求"把X改成Y/去掉Z" → refs=图片修改，mode=修改
- 用户描述已有图的失败 → 跳到Step 5诊断，prompt中需描述当前问题
- 用户未提风格 → style留空，不加默认风格词
- 用户提到具体作品/游戏/画家名 → style=该锚点

---

## Step 2: 场景路由

| 信号关键词 | → 场景 | → 加载 |
|-----------|--------|--------|
| 图标/精灵/像素/游戏素材/UI元素/asset/sprite/icon/pixel/item/道具/装备/tileset/瓦片/建筑/怪物/spritesheet/植被/特效/VFX/parallax | game-assets | scene-game-assets.md |
| 角色/人物/立绘/OC/avatar/character/人像 | character | scene-character.md |
| 风景/场景/建筑/城市/landscape/environment/环境 | landscape | scene-landscape.md |
| 海报/文字排版/封面/banner/poster/typography/标题 | text-poster | scene-text-poster.md |
| 艺术风格/画风/油画/水彩/illustration/art style/画风迁移 | style-art | scene-style-art.md |
| 摄影/产品图/人像写真/商业拍摄/photography/product shot | photography | scene-photography.md |

**交叉场景**：请求跨场景时（如"DST风格的角色立绘"），主场景=用户核心需求（角色），次要维度从辅助场景取控制维度。加载主场景文件即可，辅助维度用通用规则覆盖。

**辅助路由**（按需加载，不在主流程中）：

| 需要 | 加载 | 说明 |
|------|------|------|
| 查if-then决策规则 | rules.md | 19条可执行规则 |
| 查模型格式/quirk | model-notes.md | 格式/参数/打通状态速查 |
| 查API调用方法 | api-calls.md | 端点/认证/代码/价格/Key获取 |
| 迭代/修复/批量 | iteration.md | 图生图/Inpaint/漂移管理 |
| 理解为什么这样做 | principles.md | 机制推导（深度参考，非必需） |

---

## Step 2B: 模型选择与Key检查

场景确定后，选择模型并确认API Key可用性。

**选择流程**：
1. 从场景路由结果查下表 → 确定首选模型和备选模型
2. 读取 SECRET.md → 检查首选模型 Key 是否存在
3. Key 存在 → 使用首选模型
4. Key 不存在 → 检查备选模型 Key → 存在则使用备选
5. 首选和备选均无 Key → 检查其他任何可用 Key 的模型
6. 完全无 Key → 告知用户"当前无可用模型 API Key，请提供 [Key名]。获取方式见下方"

**场景→模型映射**：

| 场景 | 首选 | Key变量 | 备选 | Key变量 |
|------|------|---------|------|---------|
| character | GPT Image 2 | OPENAI_API_KEY | Seedream 5.0 | VOLCENGINE_API_KEY |
| landscape | Flux 2 Pro | FAL_API_KEY | GPT Image 2 | OPENAI_API_KEY |
| game-assets（像素游戏资产） | PixelLab（在线生产）/ FLUX.2-klein+Limbicnation pixel LoRA（本地） | PIXELLAB_API_KEY / 本地GPU | GPT Image 2（概念参考） / Z-Image-Turbo+tarn59 LoRA（快速原型） | OPENAI_API_KEY / 本地GPU |
| game-assets（矢量/UI图标） | Recraft V4 | RECRAFT_API_KEY | GPT Image 2 | OPENAI_API_KEY |
| text-poster | Ideogram v3 | IDEOGRAM_API_KEY | Seedream 5.0(中文) | VOLCENGINE_API_KEY |
| style-art | GPT Image 2 | OPENAI_API_KEY | Flux 2 Pro | FAL_API_KEY |
| photography | Flux 2 Pro | FAL_API_KEY | GPT Image 2 | OPENAI_API_KEY |

**Key 缺失时提示用户**（附获取指引）：

| Key名 | 获取地址 | 说明 |
|--------|---------|------|
| OPENAI_API_KEY | https://platform.openai.com/api-keys 或第三方中转站(如packyapi.com) | 需充值余额；中转站base_url需同步配置 |
| VOLCENGINE_API_KEY | https://console.volcengine.com/ark | 国内平台，支持支付宝 |
| IDEOGRAM_API_KEY | https://developer.ideogram.ai/ | 注册开发者账号 |
| RECRAFT_API_KEY | https://www.recraft.ai/ → Settings → API Keys | 注册后创建Key |
| FAL_API_KEY | https://fal.ai/ → Keys | 注册后创建Key |

**API 调用方法**：详见 `references/api-calls.md`（端点/认证/参数/代码示例/错误处理）

**选定模型后**：在 Step 3 组装 prompt 时，按该模型格式要求调整写法（见 model-notes.md 格式速查表）

---

## Step 3: Prompt组装

加载场景文件后，按该场景的模板填充prompt。

**通用组装优先级**（所有场景，从高到低）：
1. 格式锚定 — 这是什么类型的图
2. 主体 — 画什么
3. 风格 — 什么风格（具体锚点）
4. 构图/视角 — 怎么看
5. 光影/氛围 — 什么氛围
6. 技术约束 — 尺寸/格式/特殊要求

**通用组装规则**（完整if-then版见rules.md）：
- 自然语言写法（GPT Image 2 / Flux / Ideogram / Gemini / 国产模型），不用SD逗号词组
- GPT Image 2优先用四元组结构：[主体]-[属性]-[关系]-[约束]（R13，首次满意率72% vs 31%）
- 主体前置，细节后置（R03）
- 每条词验证：去掉它会变吗？不变→删（R01）
- 不写"4K/8K/best quality/masterpiece/detailed/highly detailed"（GPT Image 2中尤其有害，R14）
- 文字内容用引号包裹："Hello World"（R15，命中率+30-40%）
- 颜色+物件用完整短语："red hat"而非"red, hat"（SD除外，R05）
- 不超60词（除非场景模板标注了更长限制）

**参考图模式特殊处理**：
- 参考生成：prompt先说明"从参考图取[什么元素]"，再描述"生成[什么新内容]"
- 图片修改：prompt只写编辑指令（动作+对象+特征），不描述原图内容（模型自动保持非编辑区域）

---

## Step 4: 质量门控

生成前必须通过，不通过回Step 3修改（最多2轮）：

```
□ 词数≤60？
□ 有格式锚定？（第1条明确这是什么类型的图）
□ 有风格锚定？（具体风格词，不是"beautiful/stunning/artistic"）
□ 构图明确？（景别+角度，不是"随便"）
□ 无矛盾描述？（同一维度不写两个方向）
□ 无冗余赞美词？（无best/stunning/amazing/4K/masterpiece）
□ 场景特定检查通过？（见场景文件的必检项）
□ 参考图提示词明确？（有ref时，说明了取什么+生成什么）
```

---

## Step 5: 失败诊断

用户对生成结果不满意时执行：

1. **问清问题**：用户具体哪里不满意？
2. **加载场景文件→诊断路由**：按场景分类的失败→修复映射
3. **通用诊断**（场景文件未覆盖时）：

| 用户反馈 | 诊断 | 修复方向 | 规则 |
|---------|------|---------|------|
| "好看但不是我想要的" | Generic输出 | 加特异性风格锚定 | R02 |
| "形状/姿势不对" | 主体走形 | 用参考图+图生图模式 | R06 |
| "太复杂/太简单" | 描述过度/不足 | 减少或增加具体描述 | R03/R11 |
| "文字拼错了" | 文字渲染模型不对 | 换GPT Image 2/Ideogram | R09 |
| "颜色串了" | 颜色-物件未绑定 | 完整短语描述 | R05 |
| "不像参考图" | 参考生成指令模糊 | 明确"从参考图取X" | — |
| "风格变干净了" | GPT Image 2 house style | 描述视觉特征不写风格标签 | P10 |
| "风格不像XX" | 风格锚定太笼统 | 用具体媒介/年代/作品名 | R07 |
| "元素莫名缺失/风格偏移" | GPT Image 2隐性安全降级 | 最小变更定位+抽象替换 | R16 |
| "加8K/高清反而变差" | 质量词在GPT Image 2反效果 | 全删，写可验证物理特征 | R14 |
| "多轮修改后角色变了" | 对话式迭代记忆衰减 | 重申关键特征，≤5轮 | R17 |

诊断后→回Step 3修改prompt→重新生成。

---

## 反模式触发条件

| ID | 反模式 | 触发信号 | 修复 |
|----|--------|---------|------|
| P01 | 颜色污染 | SD中多色多物件同75-token组 | BREAK+下划线+权重 |
| P02 | Generic输出 | prompt无特异性风格词 | R02三层对抗 |
| P03 | 肢体崩坏 | 角色+手部/多肢体 | 局部修复/换姿势 |
| P04 | 文字乱码 | 需渲染文字+非文字强模型 | 换GPT Image 2/Ideogram |
| P05 | 景别冲突 | 远景写近物细节/反之 | 统一景别与物件 |
| P06 | 加细节变差 | prompt含"add detail/more details" | 写具体增强方向(R11) |
| P07 | 风格不对 | 格式不匹配当前模型 | 格式适配(rules.md R12) |
| P08 | 参考图偏离 | 参考生成但未说明取什么 | 明确"从参考图取X" |
| P09 | 语义冲突 | prompt中同维度两个方向 | 一条prompt一个意图(R04) |
| P10 | 风格清理化 | GPT Image 2+手绘/粗糙风 | 描述视觉特征不写风格标签 |
| P11 | 安全降级 | GPT Image 2无报错但元素缺失/风格偏移 | 最小变更定位法(R16) |
| P12 | 质量词反效果 | GPT Image 2+"高清/8K/杰作" | 全删，写可验证物理特征(R14) |

---

> v6.1 game-assets场景大升级：子场景路由（图标/角色/建筑/瓦片/植被/特效/UI/parallax/动画/3D），专用像素模型/LoRA完整推荐表，11类素材prompt模板全覆盖，Givros资产表工作流，spritesheet动画生成方法，后处理管线（Aseprite/Tiled/TexturePacker），5大AI味陷阱解药，瓦片暗角修复流程，跨平台万能负面词库，中文国产模型负面词。scene-game-assets.md从6.6KB扩充至完整参考手册。model-notes新增像素专用模型速查表。
> v6.0 决策引擎。核心变化：SKILL.md=可执行5步流程，场景文件=模板+填充规则+诊断路由，rules.md=19条if-then决策规则，principles.md降级为深度参考。v4报告59条新经验已融入rules.md R13-R19和诊断路由。
