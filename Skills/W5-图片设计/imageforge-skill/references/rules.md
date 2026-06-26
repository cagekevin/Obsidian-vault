# 决策规则（if-then）

> 可执行规则，不是教育原理。每条都是"遇到X→做Y"的决策指令。
> 机制推导见 principles.md（深度参考，非必需）。

---

## R01: 冗余信号稀释有效信号

**IF** prompt中有多于一个同义词修饰同一主体（如"beautiful, gorgeous, stunning"）
**THEN** 只保留最具体的一个，删除其余
**BECAUSE** 注意力是零和资源，同义词占3倍注意力但不增加3倍信息

---

## R02: Generic对抗三层

**IF** 输出"好看但不是我想要的" / prompt无特异性风格词
**THEN** 按优先级依次尝试：
1. 特异性描述（"琥珀色瞳孔"非"漂亮眼睛"）
2. 反常规组合（"蒸汽朋克医疗室"）
3. 风格锚定（具体媒介/年代/流派/作品名）

**IF** 三层都试过仍generic
**THEN** 检查是否特异性描述超出了模型训练分布（太罕见→模型退回已知分布）

---

## R03: 注意力前置

**IF** prompt中主体不在前20词
**THEN** 将主体移到prompt开头
**IF** prompt超过50词
**THEN** 逐条删词验证：去掉它会变吗？不变→删

---

## R04: 一次一个意图

**IF** prompt中存在矛盾描述（冷+暖/远+近/简+繁/暗+亮）
**THEN** 删除矛盾方之一，一条prompt只表达一个画面意图
**BECAUSE** 矛盾梯度导致去噪方向震荡

---

## R05: 颜色-物件绑定

**IF** 模型=SD AND 描述多色多物件
**THEN** 颜色和物件用完整短语（"red hat"非"red, hat"），跨75-token用BREAK
**IF** 模型≠SD（Flux/MJ/GPT Image 2/Ideogram/国产）
**THEN** 用自然语言完整短语即可，无需BREAK
**BECAUSE** 仅CLIP有75-token分组编码导致的颜色污染

---

## R06: 省略=模型接管

**IF** 5个关键维度（主体/风格/构图/光影/配色）任一未描述
**THEN** 显式补充
**BECAUSE** 不描述≠不存在，而是由模型默认分布填充（正面均匀照明/居中构图/高饱和）
**EXCEPTION** Flux中省略≈隐式控制（T5不做概率补充），可利用信息不对称控图

---

## R07: 风格锚定用具体词

**IF** 需要控制风格但只写了模糊词（"beautiful/stunning/retro/artistic/nice style"）
**THEN** 替换为具体锚定，优先级：
1. 具体作品名（"Celeste style"/"DST art style"）
2. 媒介+年代+流派（"1970s silkscreen poster"/"Edo period ukiyo-e"）
3. 视觉特征描述（"chalk pastel on textured paper, visible strokes, rough edges"）

**BECAUSE** 模糊词编码指向宽分布（多种可能），具体词编码指向窄分布（精确匹配）

---

## R08: 精确词>模糊词

**IF** 使用了模糊光照/构图/材质/风格词
**THEN** 替换为精确词：

| 模糊 | → 精确 |
|------|--------|
| dramatic lighting | Rembrandt lighting from upper left |
| beautiful light | soft diffused key light from overhead, warm 3200K |
| good lighting | three-point studio lighting, key from 45° left |
| dark lighting | low-key single source from behind, rim light only |
| good composition | rule of thirds, subject on left third |
| metallic | brushed aluminum / chrome / gunmetal |
| retro style | 1970s silkscreen / NES palette / Art Deco |

**BECAUSE** 精确词在训练数据中与特定视觉模式共现频率高→编码精确→可控

---

## R09: 文字渲染模型选择

**IF** 需要渲染文字
**THEN** 优先级：GPT Image 2（英中文都强）> Ideogram v3（英文强+位置精确）> Seedream 5.0（中文强）
**IF** 必须用SD
**THEN** ControlNet + 预排版文字图

---

## R10: 一致性策略梯度

**IF** 需要跨图片一致性
**THEN** 按需要强度选：
1. 固定风格提示词（弱——仍有随机漂移）
2. 固定种子+参数（中——相同输入→相同输出）
3. 图生图+低重绘幅度0.3-0.5（强——以参考图为锚）
4. ControlNet（很强——像素级约束）
5. 风格LoRA/微调（最强——修改模型本身）

**IF** 批量产出同风格素材 → 方案3（图生图锚定）
**IF** 角色多角度一致性 → Flux四宫格 or 图生图锚定

---

## R11: 加法≠增强

**IF** 想写"add more details"或"enhance quality"或"4K/8K"
**THEN** 不写笼统增强，写具体增强方向
- ❌ "add more details" → 编码为"更多元素"而非"更好看"
- ✅ "sharper texture on bark, more visible grain" → 编码为"在这个方向细化"

---

## R12: 跨模型翻译

**IF** 在模型A中有效的prompt需要用于模型B
**THEN** 不是逐词翻译，而是：理解原prompt的视觉意图 → 用模型B的格式重新表达

| 方向 | 变化 |
|------|------|
| SD → Flux | 词组→自然语言，删"best quality"和负向词，删权重语法 |
| SD → MJ | 词组→描述+参数，负向词→--no，权重→::数值 |
| 任意 → Ideogram | 自然语言→JSON结构化 |
| 任意 → GPT Image 2 | 自然语言描述，参考图用ref_images参数 |
| 任意 → 国产模型 | 直接中文描述，成语/网络用语有效 |

**关键**：翻译的是"视觉意图"不是"文本字面"。先问"这条prompt在原模型中实现了什么视觉效果"，再用新模型的表达方式重述。

---

## R13: 四元组结构化写法

**IF** 用GPT Image 2/对话式模型生图 AND 首次满意率低
**THEN** 用四元组结构组织prompt：[主体]-[属性]-[关系]-[约束]
- 主体：画什么（"a black cat"）
- 属性：主体特征（"with golden eyes, fluffy fur"）
- 关系：主体与场景/其他元素的关系（"sitting on a windowsill"）
- 约束：风格/光影/构图/技术参数（"oil painting style, warm candlelight, centered"）

**BECAUSE** 实测首次满意率72% vs 自由描述31%。结构化prompt降低编码歧义
**边界**：SD/MJ等非对话式模型对四元组结构无额外增益，词组/自然语言各自按原规则

---

## R14: GPT Image 2质量词反效果

**IF** 模型=GPT Image 2 AND prompt包含"高清/8K/杰作/best quality/masterpiece"
**THEN** 全部删除——GPT Image 2的自回归架构没有"质量"训练维度，这些词只增加噪声
**IF** 需要提升视觉质量
**THEN** 写可验证的物理特征而非质量形容词
- ❌ "高清精美" → 无效
- ✅ "Nikon D7000, ISO 1600, 1/60s, slight camera shake" → 注入对应噪点模型
- ✅ "水墨风格，近景石桥青苔斑驳，中景白墙黛瓦倒映水面，远景薄雾山峦，留白40%" → 替代"精美绝伦的江南水乡"

**BECAUSE** 217个失败案例中63%源于质量形容词；强行加"8K"甚至触发安全降级
**边界**：SD/MJ对质量标签有正向响应（有专门训练维度），此规则仅限GPT Image 2

---

## R15: 文字渲染引号规则

**IF** 需要在画面中渲染文字
**THEN** 文字内容必须用引号包裹："Hello World"而非Hello World
**BECAUSE** 引号区分"要渲染的文字"和"描述文字的词"——命中率差30-40%
- ✅ title "SUMMER FESTIVAL" in bold sans-serif
- ❌ title SUMMER FESTIVAL in bold sans-serif（模型可能理解为"夏天节的标题"而非"渲染这几个字母"）
**边界**：GPT Image 2/Ideogram引号效果最显著；SD对引号不敏感（文字渲染能力本身太弱）

---

## R16: GPT Image 2安全降级诊断

**IF** GPT Image 2生图结果"不像想要的版本"（元素缺失/风格被强制调整/质量明显下降）但未报错
**THEN** 这是隐性安全机制——不拒绝但降级输出
**诊断方法**：最小变更定位法——把prompt缩减到主体+风格+场景三要素，逐步加细节，记录触发降级的具体维度
**修复**：对触发维度用抽象/象征/概括替换高度具体的描述
- ❌ "realistic photo of person in [可能触发降级的场景]"
- ✅ "artistic illustration conveying the feeling of [同场景的抽象表达]"
**边界**：隐性降级对"意图结构"更敏感，换措辞可能绕过但同一意图不同措辞效果差异大

---

## R17: 对话式迭代轮次限制

**IF** 用GPT Image 2多轮对话迭代生图
**THEN** 每轮只改1-2个维度，不超过3个；约5-8轮后模型对早期指令记忆衰减
**IF** 超过5轮
**THEN** 重新提及关键特征："记住，人物仍然是蓝色短发、戴眼镜"
**IF** 结果"接近但不完全对"
**THEN** 用"Same X but [具体修改]"句式——比从零重写效率高3-5倍
**边界**：非对话式模型（SD/MJ一次生成模式）不支持此策略

---

## R18: 中英混合写法

**IF** 用GPT Image 2 AND 描述涉及中国文化/抽象概念
**THEN** 主体描述用中文（语义更准确），技术参数用英文（视觉映射更精准）
- ✅ "一只柴犬，shiba inu，穿宇航服，wearing spacesuit，赛博朋克城市，cyberpunk city"
**BECAUSE** GPT Image 2中文语料占比23%（DALL-E 3仅8%），但技术术语训练数据仍以英文为主
**边界**：Qwen-Image等国产模型中文表现优于GPT Image 2，特别是中国文化元素（"靛青色宋制褙子""湘妃竹折扇"）

---

## R19: 批量一致性数值锚点

**IF** 批量产出同风格素材
**THEN** 关键数值：
- 图生图重绘幅度：0.45-0.65（太低不变，太高漂移）
- 种子偏移：±3以内漂移可控，超过5开始明显偏移
- 主体占比：≥30%（视频模型/图生图场景下低于此值主体变糊）
- 固定风格后缀：同一批所有素材最后5-10词完全相同

**BECAUSE** 实测数据：重绘幅度0.45时角色特征保持率92%，0.65时降至76%，0.8时降至41%
**边界**：不同模型的重绘幅度含义不同，这些数值基于SD实测；GPT Image 2无重绘幅度概念，用参考图+对话式迭代替代
