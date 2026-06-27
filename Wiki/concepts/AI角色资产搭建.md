---
type: concept
title: "AI 角色资产搭建"
address: c-000047
status: developing
tags:
  - concept
  - image-generation
  - video-generation
  - character-design
  - prompt-engineering
created: 2026-06-27
related:
  - "[[sources/刺猬星球AI创作系列]]"
  - "[[人感审美与材质重塑]]"
  - "[[AI视频动作设计]]"
  - "[[一致性锚点原则]]"
  - "[[角色锚定]]"
---

# AI 角色资产搭建

AI 短剧/视频的第一步不是直接生成视频，而是先搭建人物资产。一个完整的人物资产至少包含三样东西：人物的脸、人物的发型和妆造、人物的服装和整体轮廓。

---

## 人物资产三件套

不建议只生成一张人物图（信息量不够）。更好的做法是把三张拆开生成，最后再融合：

1. **脸部三视图** — 包含脸部、妆造和发饰
2. **全身三视图** — 固定人物的服装结构
3. **融合输出** — 将前两者融合为稳定的人物锚点

**注意**：不要一开始就追求特别复杂的造型。元素越多，生成视频时越容易崩。真正高级的短剧人物不是元素越多越好，而是**特征要清晰**。比如女主可以固定三个记忆点：高颅顶黑发、金色古风头饰、浅色系长裙。

---

## 男/女角色妆造差异

**男性角色**的妆造重点不在脸上，而在服装和发型。妆面太重容易失去角色本身的质感。男性角色真正撑住气场的三个部分：

- **发型** — 高马尾利落有力量感、半披发清冷疏离、发冠束发端正有家世、凌乱散发受伤疲惫
- **服装** — 盔甲代表将军、劲装代表侠客、长袍代表文人公子、暗纹黑衣代表刺客、宽袖官服代表权臣
- **配饰** — 剑、玉佩、发冠、披风、腰带、护腕、扳指，都能帮助建立身份

示例：
- 少年将军 → 妆造更利落，发型束起，服装有硬挺感
- 病弱公子 → 妆造更干净克制，发型松一点，服装颜色淡一点

**女性角色**需要的更多，不只是服装状态，更要注重面部妆容和发饰。身份、性格和阶层往往靠妆面和发饰传递。需要写清楚的几个方面：
- 服装：颜色、材质、款式、刺绣、层次
- 发型：高髻、低髻、披发、编发、盘发
- 发饰：金步摇、玉簪、珍珠、银饰、花钿
- 妆面：眉形、眼妆、唇色、腮红、妆容完整度
- 状态：端庄、疲惫、刚哭过、刚赴宴、刚逃亡、刚醒来

示例：
- 宫廷贵妃 → 眉眼更精致，有被规矩养出来的贵气
- 落魄千金 → 妆可以有一点残次

**进阶**：妆造不仅要符合身份，还要符合人物当下的状态。同样是贵妃，刚参加完宫宴和刚经历失宠，妆造一定不一样。**身份决定妆造方向，状态决定妆造细节。**

---

## 妆造提示词公式

写角色妆造时，不要只写"好看的脸""精致五官""高级感"。这些词太空泛，AI 很难准确理解。使用以下公式：

> **角色身份 + 服装材质 + 发型发饰 + 面部妆容 + 色彩气质 + 当前状态 + 画面质感**

示例：
```
古风女贵妃，深红色宫装，金线刺绣，发髻高盘，点缀金步摇，
妆面完整，唇色浓郁，眼神平静克制，刚参加完宫宴，柔和光影，细腻质感。
```

这段提示词不只是写了"她是谁"，还写了她穿什么、戴什么、妆容怎样、处在什么状态。

### 男性角色示例

- **清冷侠客**：年轻男性，黑色窄袖劲装，半披长发，银色发扣，衣料有轻微磨损，腰间佩剑，神情疏离，眼神克制，冷色调画面，江湖氛围。
- **世家公子**：年轻男性，月白色长袍，玉冠束发，衣服有浅色暗纹，手持折扇，面容清俊，气质温和疏离，庭院背景，光线柔和。

> 男性角色的写法：**不要急着给脸加妆，要先让服装和发饰说明他的身份。**

### 女性角色示例

- **宫宴贵妃**：深红色宫装，金线刺绣，高盘发髻，金步摇，妆面完整，眼妆精致，唇色浓郁，神情端庄克制，刚参加完宫宴，华丽宫殿背景，柔和灯火。
- **失宠贵妃**：暗红色旧宫装，发髻略微松散，金饰减少，妆面不完整，唇色偏淡，眼神疲惫，坐在冷清宫室中，窗外微光，画面安静压抑。

> 女性角色的写法：**同样的五官，换一套妆造就换了一个角色。** 服装颜色、发型发饰、妆面完整度、当前状态都要写清楚。

---

## 状态决定细节

真正让角色鲜活的，不是"他是谁"，而是"他刚经历了什么"。**身份决定妆造方向，状态决定妆造细节。**

| 角色 | 场景 | 妆造表现 |
|------|------|----------|
| 世家公子 | 刚赴完宴 | 月白长袍、玉冠束发、衣袍整洁，气质温润 |
| 世家公子 | 刚被责罚 | 发冠微乱、衣袖褶皱、外袍颜色更沉，眼神压抑 |
| 大家闺秀 | 春日宴后 | 妆面完整、发饰精致、衣服柔和，端庄温婉 |
| 大家闺秀 | 得知变故 | 发饰减少、唇色变淡、衣裙更素，眼神隐忍 |

---

## 角色"活人感"

人只要活着就一定在顺便做某件事。很多 AI 人物的问题在于虽然长得像人，却没有任何生活状态——这就是"人物待机感"。

**核心公式**：人物 + 正在做的小事 + 下意识反应 + 情绪落点

真正重要的不是动作本身，而是**行为动机**。比如同样是喝咖啡，干喝是摆拍，边看前面边无意识转杯子才像真人。

**多人物**：不要让每个人都在那里表演。不要一个人行动、另一个人反应。多人物提示词的关键不是动作越多越真实，而是人物之间要有**反应**。

> 活人感的具体动作写法（四层动态、对手戏调度）详见 [[AI视频动作设计]]

---

## 微表情三控（视频版）

AI 视频的底层逻辑缺陷：它不懂"克制"。过强的情绪指令（如 "Angry", "Laughing"）会被 AI 每一帧都尝试强化，最终导致"情绪过载"——笑容越张越大直到崩坏，或全程 100% 强度纹丝不动像动态面具。微表情控制不仅是为了真实，更是为了"稳"。

### 方法一：控制情绪强度

**问题**：AI 默认"最大值"。写下 `A girl laughing loudly`，AI 会从第 1 秒到第 5 秒维持 100% 笑容强度，缺乏呼吸感和回落瞬间。

❌ 错误写法（导致油腻感）：
```
Beautiful woman smiling happily at the camera.
```
→ 像拍广告僵硬假笑的模特，笑容没有任何变化。

✅ 正确写法（用微量修饰词替代大情绪词）：
```
A relaxed woman, a faint hint of a smile at the corner of her mouth,
her gaze soft, facial muscles relaxed, no posed feeling.
```

**视频实战对比**：

❌ 反面（只写情绪结果）：
```
The woman is drinking coffee and smiling happily. She is enjoying the morning.
```
→ AI 让人物一直保持杯子在嘴边，脸上挂着僵硬的微笑。

✅ 正面（写动作全过程）：
```
The woman brings the cup to her lips, pauses to smell the aroma,
her eyes close slightly, then she blows gently on the steam before taking a sip.
```
→ 通过物理动作牵动面部肌肉——闻香气时鼻翼翕动、吹气时嘴唇形状变化，自然消除假笑感。

> **填空公式**：[放松/自然的状态词] + [微量修饰词] + [面部肌肉状态] + [无摆拍感]
>
> **填空词库**：relaxed, faint, subtle, gentle, soft, natural, effortless, unposed, slight, mild

### 方法二：动作驱动法

**问题**：只写表情，AI 凭空捏造面部运动。比如写 `Shy woman`，AI 让人物直勾勾盯着镜头然后脸红扭捏，非常恐怖。

**原理**：真实人类的表情是身体动作的"副产品"，不是独立存在的。写动作，AI 根据人体运动学顺带生成表情。

❌ 错误写法（只写表情）：
```
The woman is shy and looking directly at the camera.
She smiles shyly at the viewer. Static head, just facial expression changing.
```
→ 人物死盯着观众挤表情，非常不自然。

✅ 正确写法（动作驱动表情）：
```
She feels shy. She immediately lowers her head to avoid eye contact.
Her eyes look down, nervously glancing to the side.
She tucks her chin, gently biting her lower lip. She dares not look at the camera.
```
→ 用"低头"承接"害羞"，AI 知道她为什么低头，动作更含蓄柔和。

> **填空公式**：[情绪触发] + [身体微动] + [视线转移] + [承接动作]
>
> **填空词库**：lowers head, avoids eye contact, looks down, glances away, tucks chin, bites lip, turns away, shifts weight

### 方法三：动态演变写法

**问题**：给 AI 一个静态描述（如"他很伤心"），AI 不知道第 1 秒和第 5 秒有什么区别，只能死循环。

**原理**：微表情的本质是 Change（变化）。需要在提示词中写入时间轴。

**公式**：Start（起始状态）→ Transition（变化动作）→ End（最终微表情）

**示例**：一个"如释重负"的镜头
```
A close-up of a man's face. He maintains a serious, contemplative expression,
his brow slightly furrowed. He slowly closes his eyes and takes a deep,
visible breath, his shoulders dropping. As he exhales, a faint,
relieved smile slowly forms at the corners of his mouth.
```

- **第一阶段（Start）**：锚定起始帧状态——严肃沉思、眉头微皱
- **第二阶段（Transition）**：闭眼+深呼吸——用物理动作切断严肃情绪
- **第三阶段（End）**：释然微笑——经过深呼吸铺垫，笑容有血有肉

> **填空公式**：[起始状态] + [触发动作/物理变化] + [最终微表情结果]
>
> **填空词库**：maintains...expression → slowly begins to / gradually transitions → faint/slight/subtle smile/expression forms

---

### 微表情词库与脚本库

以下工具库与上述三个方法配合使用，提供可直接调用的词汇和完整脚本。

**情绪降噪词库**（用于方法一——控制强度）：

| 类别 | 词 | 用法 |
|------|----|------|
| 基础降维 | subtle, faint, slight, soft, gentle, mild, delicate | 将情绪强度从 100% 降至 30%，最通用的"去油"前缀 |
| 克制与隐藏 | suppressed, restrained, hidden, masked, held back, understated, reserved | 表现"想动又不敢动"的高级张力 |
| 极微状态 | barely visible, imperceptible, a hint of..., trace of..., in the eyes, ghost of a smile | 用于电影特写，情绪几乎看不见，全靠观众脑补 |
| 时间流逝 | fleeting, brief, gradual, slow-forming, hesitant, intermittent | 给情绪加时间限制，防止表情像面具一样挂在脸上 |
| 状态形容词 | relaxed, neutral, calm, stoic, unbothered, absent-minded, dreamy | 直接描述"松弛"状态，而非情绪 |

**生理反应动作库**（用于方法二——动作驱动）：

| 部位 | 动作 | 对应的情绪 |
|------|------|-----------|
| 嘴部 | biting lower lip, licking lips, pursed lips, trembling chin, jaw clenching, blowing out air, swallowing | 害羞/紧张/犹豫/愤怒/恐惧 |
| 头部与手部 | tucking hair behind ear, scratching back of neck, rubbing eyes, covering mouth, tilting head, shifting weight, dropping shoulders | 尴尬/困惑/疲惫/好奇/放松 |

**眼神演技库**（打破"死盯镜头"的尴尬感）：

| 类型 | 动作 | 用途 |
|------|------|------|
| 动态视线 | avoiding eye contact, darting eyes, looking down, glancing sideways, shifting gaze | 害羞/心虚/顺从/偷看 |
| 眼神状态 | unfocused/zoning out, dilated pupils, squinting, rapid blinking, watery eyes | 放空/心动/怀疑/惊讶/感动 |

**黄金时序脚本**（用于方法三——动态演变写法）：

**脚本 01：心动的瞬间**
```
Starts with a neutral expression, looking around a room.
Suddenly, the gaze locks onto something off-camera.
Pupils dilate visibly, and the blinking slows down.
A soft, unconscious smile slowly spreads across the face.
```

**脚本 02：强行憋笑**
```
The character is trying desperately not to laugh.
Lips are pressed tight together, cheeks are slightly puffed.
Shoulders are shaking slightly.
Finally, they cover their mouth with a hand and look down to hide the amusement.
```

**脚本 03：由期待转为失落**
```
Starts with an expectant, happy face, waiting for news.
Then, looks down at a phone screen. The smile fades rapidly.
The light in the eyes disappears (becomes dull).
Finally, lets out a subtle sigh and looks away blankly.
```

**脚本 04：隐忍的怒火**
```
The character is listening to someone.
Suddenly, the jaw clenches visibly (masseter muscle flexes).
Nostrils flare slightly. Eyes narrow into a cold stare.
Finally, forces a fake, stiff smile to mask the anger.
```

**脚本 05：极度疲惫的苏醒**
```
The character has heavy eyelids, struggling to keep eyes open.
Blinks slowly and deliberately. Rubs eyes with the back of the hand.
Lets out a long, tired yawn, covering mouth. Eyes are watery.
```

---

## AI 捏脸：一个强项两个辅助

AI 捏脸有两种方法：
1. **普通法**：按结构拆成三个层面（骨骼/比例/五官），分别找参考，用画布画出大致五官位置
2. **进阶法**：在可捏脸的工具中根据 AI 建议一步步调整

**核心逻辑**：有些五官单看好看但放一起不一定好看（如狐狸眼配鹰钩鼻像反派巫婆）。最简单的方法是**"一个强项两个辅助"**——以一个五官为核心特征，其余作为辅助配合，避免特征冲突。

**三停五眼**：中庭偏长显成熟有距离感，中庭偏短显甜显亲和。

---

## 常见错误

### 错误一：只写五官，不写身份
只写"精致五官，漂亮脸蛋，高级感"→ 人物可能好看，但没有角色记忆点。正确做法是用妆造公式写清楚身份。

### 错误二：男性角色妆面太重
将军、侠客、侍卫、谋士等角色，重点在服装、发型、配饰和气场，不要过度强调浓妆。

### 错误三：女性角色只写衣服，不写妆面
女性的贵气、清冷、温柔、疲惫、失落，很多时候靠妆面和发饰表现。妆容是否完整、唇色深浅、发髻是否整齐，都会影响角色故事感。

1. **用时间段拆分动作** — 不要把所有人物的动作写在同一句话里。规定具体时间和具体人物，AI 对时间结构的理解比自然语言顺序更清晰
2. **锁定锚定角色** — 修改多人动作时，明确需要修改的角色和被保留的部分
3. **把复杂动作拆成多个阶段** — 动作越复杂人物越容易崩。很多流畅的 AI 视频不是一次生成出来的，而是拆成多个阶段慢慢生成的
