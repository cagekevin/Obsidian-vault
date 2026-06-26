# 游戏素材

## 判定条件

路由到此场景的信号：
- 关键词：图标/精灵/像素/游戏素材/UI元素/asset/sprite/icon/pixel/item/道具/装备/tileset/瓦片/建筑/道具/怪物/spritesheet
- 场景特征：需要精确形状控制+风格一致性+可批量复制的视觉素材，而非单幅艺术画作
- 典型请求："画个血瓶图标"/"做一套像素风物品图标"/"像素风角色精灵"/"3D游戏资产"

---

## 子场景路由

游戏素材内部再按素材类型分路径，不同类型prompt策略差异巨大：

| 信号 | → 子场景 | → 使用模板 |
|------|---------|-----------|
| icon/图标/物品/道具/装备/武器/药水/宝箱 | 道具图标 | 模板A（UI图标） |
| sprite/角色/人物/NPC/敌人/怪物/Boss | 角色精灵 | 模板B（像素精灵）+ B.6动画 |
| building/house/建筑/小屋/商店/铁匠铺/酒馆 | 建筑Sprite | 模板C（建筑） |
| tile/tileset/地形/瓦片/草地/水面/地面/地砖 | 地形瓦片 | 模板D（Tileset） |
| tree/plant/树/灌木/花/蘑菇/植被/自然物 | 植被自然 | 模板E（植被） |
| VFX/特效/光效/slash/爆炸/烟雾/粒子/魔法弹 | 特效VFX | 模板F（特效） |
| UI/button/血条/HUD/物品栏/对话框/面板/边框 | UI界面元素 | 模板G（UI元素） |
| background/parallax/天空/远景/视差/背景层 | 背景视差层 | 模板H（Parallax背景） |
| spritesheet/多帧/动画帧/走跑跳攻击帧 | 动画帧 | 模板B.6 + I（动画工作流） |
| 3D模型/glb/低模/灰模/游戏模型 | 3D资产 | 模板J（3D灰模中转） |

**交叉场景**：一次请求多类素材（如"一套小镇素材包"）→ 用资产表法（模板K）一次性规划，再分批次生成。

---

## 模型选择

### 像素风模型推荐（关键决策，2026-06核查更新）

像素风游戏素材**不要**用通用对话模型直接生成——通用模型输出的是"像素风格插画"，边缘带抗锯齿、色块不锐利、光影是渲染出来的，不是真像素资产。必须使用专用像素模型/LoRA/工具。

**本地模型（开源，RTX 4060可跑）**：

| 模型/LoRA | 基座 | 触发词/用法 | 权重 | CFG | Steps | 显存 | 最适合 |
|-----------|------|------------|------|-----|-------|------|--------|
| **⭐ Limbicnation/pixel-art-lora** | FLUX.2-klein-4B (Apache 2.0) | `pixel art sprite, game asset, transparent background, SPR1TE8` | 默认 | 1.0 | 4步 | **8GB** | **2026本地新基线首选**，4步最快，支持16-bit/32-bit/chibi |
| **Z-Image-Turbo + tarn59 pixel LoRA** | Z-Image-Turbo 6B (Apache 2.0) | 含pixel art/8-bit/16-bit/sprite | 0.6–1.0 | 4–5 | 8步 | 16GB | 快速原型迭代（~2秒/张RTX4070），i2i偏弱 |
| skormino Pixel Art LoRA **v8.0**（⚠️不是v6.3） | Illustrious | `masterpiece, pixpix, 8-bit, pixel_art`，CLIP Skip=2 | 1.0 | 3.5–5 | 20–28 | 8GB | 日系二次元像素/JRPG风；⚠️"pixpix"与旧SD1.5模型触发词重名 |
| nerijs/pixel-art-xl | SDXL | 无特殊，含"pixel"即可 | 1.0–1.2 | 7.5/1.5(+LCM) | 25-30/8(+LCM) | 8GB | SDXL生态最稳（2026已被FLUX.2-klein分流，降级可选） |
| Muertu XL 像素世界 V1.3 | SDXL（中文社区） | 中文prompt友好 | 0.8 | 7 | 20 | 8GB | 哩布哩布在线/中文SDXL选项 |
| Qwen-Image-Pixel-Art-LoRA | Qwen-Image-2512 | `Pixel Art`开头强化 | 0.8–1.2 | 默认 | 20 | 云端 | 中文prompt友好，云端使用 |
| pixelsprite v1.0 | Flux.1 Kontext | chibi sprite（见B.1） | 默认 | 默认 | 默认 | 16GB | 图生图转像素（参考图改像素），坎公骑冠剑风Q版 |
| 8bitdiffuser/pixpix v4.0 | SD1.5 | `8-bit pixel_art pixpix`（⚠️重名） | 0.8–1.0 | 7–9 | 20–28 | 4GB | 纯正8-bit复古大颗粒（SD1.5老旧，仅风格化保留） |

**已淘汰**：~~SD_PixelArt_SpriteSheet_Generator~~（SD1.5 checkpoint 2025-01停更）、~~Pixie-Spritesheet-48~~（无法确认存在）。

**在线工具（生产级）**：

| 工具 | 核心能力 | 价格 | 推荐度 |
|------|---------|------|--------|
| **⭐ PixelLab (pixellab.ai)** | 双模型、4/8方向角色旋转、骨架动画、Wang tileset、等距瓦片、inpaint、导出精灵表；**Aseprite插件+MCP server** | 免费40次；$12–$50/月 | ⭐⭐⭐⭐⭐ 2026年像素生产标杆 |
| Sprite AI (sprite-ai.art) | 16×16–128×128精灵专用，内置编辑器，导出Unity/Godot | $5–$24/月 | ⭐⭐⭐⭐ 小分辨率精灵高效 |
| Retro Diffusion | Aseprite内嵌老牌扩展，三模型（Plus/Tile/Animation） | $65一次性/$20Lite; Web $5/月起 | ⭐⭐⭐⭐ Aseprite内嵌最成熟 |
| 即梦AI | 中文云端快速出图，非游戏专用 | 免费/会员 | ⭐⭐ 中文零门槛概念参考，非生产主力 |

**MCP/Aseprite集成（2026 vibe coding新趋势）**：willibrandon/pixel-mcp、Dizzd/aseprite-extension-mcp、PixelLab MCP——让Cursor/Claude Code直接操作Aseprite，边写代码边出素材。

**推荐三级工作流**：
1. 快速原型：Z-Image-Turbo + tarn59 LoRA（8步）
2. 本地高质量：FLUX.2-klein-4B + Limbicnation pixel-art-lora（4步，8GB显存）
3. 生产级资产：PixelLab（$12+/月）+ Aseprite插件 + MCP，出8方向/动画/tileset，导出引擎可用精灵表

### 非像素游戏素材模型选择

| 素材类型 | 首选模型 | 备选 | 说明 |
|---------|---------|------|------|
| 扁平矢量图标 | Recraft V3/V4 | GPT Image 2 | Recraft矢量输出最干净，适合UI图标 |
| 3D风格游戏概念 | Flux 2 Pro | GPT Image 2 | Flux空间理解最强 |
| 赛璐璐/二次元角色 | GPT Image 2 | Seedream 5.0 | GPT Image文字渲染强但清理化house style |
| 中文界面/中文字体 | Seedream 5.0 | Ideogram v3 | 中文渲染是国产模型强项 |
| 3D资产灰模参考 | GPT Image 2 / Flux | — | 只做参考不需要精确像素 |

**降级链**：专用像素模型 > SD+LoRA > 通用对话模型（仅风格参考级别，不做资产）

### 内置工具 image_generate 的局限

- 底层模型未公开（扣子内置更可能是Seedream系列），无法选择模型/CFG/步数/负向词
- 输出分辨率固定（1728×2304或2848×1600自适应）
- **像素风只能到风格参考级别**——硬边不保证、色块可能有抗锯齿、无法锁色板
- 用途：定风格参考、探索方向、给后续SD本地生成提供锚定图

---

## Prompt组装

### 像素风Prompt五层公式（所有像素素材通用基础）

```
[风格触发词/位深] + [主体描述] + [视角/动作/状态] + [技术约束(分辨率/调色板/描边)] + [艺术参考/游戏类型]
```

中文拆解：
```
[pixel art/16-bit/像素风]，[一个XXX]，[视角/姿势]，
[硬边缘/无抗锯齿/16色调色板/扁平上色]，[SNES/Stardew Valley/Celeste风格]
```

**风格触发词优先级表**（按权重从高到低）：

| 层级 | 关键词 | 用途 |
|------|--------|------|
| 基础触发 | `pixel art`, `pixel style`, `((pixel style:1.5))` | 必带，括号权重强化 |
| 位深年代 | `8-bit`, `16-bit`, `32-bit` | 控制像素块大小（8-bit颗粒最大） |
| 平台参考 | `NES`, `SNES`, `Game Boy`, `GBA`, `Genesis` | 锁调色板和分辨率 |
| 游戏参考（最精准） | `in the style of Stardew Valley`, `Final Fantasy VI aesthetic`, `Celeste modern pixel`, `Zelda: A Link to the Past`, `Chrono Trigger`, `Shovel Knight`, `Hyper Light Drifter`, `Eastward` | 直接锚定具体游戏视觉 |
| 技术约束（去AI味） | `no anti-aliasing`, `hard edges`, `sharp pixels`, `flat shading`, `clean outlines`, `limited palette`, `pixel perfect`, `dithering` | 必须带，否则AI默认出软边缘 |
| 视角 | `top-down view`, `side view`, `isometric`, `front view`, `orthographic` | 必须写清，视角错了全部错 |

**采样器/参数通用建议**：
- SDXL + LCM LoRA：LCMScheduler，8步，CFG 1.5（最快迭代）
- SD 1.5 像素：Euler a / DPM++ 2M Karras / UniPC，20-30步，CFG 7-9
- 像素风禁用高CFG（>10），会过度锐化出杂色；推荐CFG 5-7更干净
- 像素风禁用：photorealistic lighting / lens flare / depth of field / bokeh / bloom / gradient / smooth shading

---

### 模板A：UI图标 / 道具图标

**最适合AI生成的素材类型**——尺寸小、单主体、纯色背景，成功率最高。

#### A.1 道具图标通用公式（SDXL Pixel Art XL）

```
pixel, [item name with material/color/state], centered,
[dark/transparent/white] background, retro game style
Negative: 3d render, realistic, blurry, gradient, anti-aliasing, text, watermark
```

示例：
- `pixel, red health potion bottle, centered, dark background, retro game style`
- `pixel, wooden treasure chest, isometric view, warm colors, clean edges`
- `pixel, golden key with ornate design, centered, dark background`
- `pixel, iron sword with leather grip, side view, transparent background`

#### A.2 8-bit道具模板（TavernCrowd风格，强剪影优先）

设计原则：强剪影>细节、颜色作信息、3-6色/道具、1px留白、白色高光代表玻璃反光。

```
An 8-bit pixel art [item type], [material/color/key feature],
[gameplay role context], limited color palette, bold silhouette,
clean pixel edges, transparent background, retro game item icon
```

**武器类示例**：
- 铁剑：`An 8-bit pixel art iron short sword, simple steel blade with leather-wrapped grip, basic starter weapon, metallic gray with brown handle, limited 5-color palette, bold silhouette, transparent background`
- 木盾：`An 8-bit pixel art wooden shield, simple starter equipment, wood grain texture in limited colors, iron boss in center, beginner adventurer gear, classic RPG item`
- 弓：`An 8-bit pixel art bow and arrow, wooden longbow, ranger equipment, simple but effective design, adventure game staple`

**药水/消耗品示例**：
- 生命药水：`An 8-bit pixel art health potion, classic red liquid in round flask, glowing slightly, heal HP item, cork stopper, simple but essential`
- 魔法/灵能药水：`An 8-bit pixel art mana potion, dark cyan/teal liquid in tall vial, magical shimmer effect, restore spiritual energy item`
- 食物：`An 8-bit pixel art baked flatbread, golden brown toasted surface, simple staple food, warm earthy beige and brown tones`

**宝物/材料示例**：
- 宝箱：`An 8-bit pixel art treasure chest, wooden with iron bands, slightly open showing warm glow, classic dungeon reward, iconic loot container`
- 金币：`An 8-bit pixel art gold coin, simple circle with shine effect, currency item, collectible treasure, fundamental RPG element`
- 水晶碎片：`An 8-bit pixel art glowing crystal shard, dark cyan jagged geometric shape, subtle inner glow, magical relic material`

#### A.3 图标组批量生成（保一致性秘诀）

**一次生成一组图标而非单张**，否则风格必飘。固定风格描述+排列要求：

```
pixel art game item icon set, [N] items arranged in a grid on pure [dark/transparent] background,
evenly spaced with clear gaps between items, same scale and style for all items,
16-bit SNES RPG style, [size]x[size] pixel resolution per item scaled with nearest neighbor,
hard sharp pixel edges, zero anti-aliasing, flat solid colors with no gradients,
no soft shadows, no blur, limited [N]-color palette, thick 1-pixel dark outline on each item,
clean readable silhouettes.

[Item 1 description]
[Item 2 description]
...

Style references: Stardew Valley, Final Fantasy VI item icons.
NO 3D, NO photorealism, NO gradients, NO text, NO watermarks.
```

**秘诀**：锁定风格关键词（色板、描边粗细、光影方向、参考游戏）每次重复，只换主体词。

#### A.4 简约线性图标（UI按钮/功能图标）

```
pixel art icon, flat design, [16/32]x[16/32] pixels, [white/colored] on [transparent/dark] background,
clean edges, sharp pixels, no anti-aliasing, minimalist, high contrast,
a simple [icon_subject] icon, readable at small size, clean consistent style
Negative: blurry, messy, gradient, detailed background, realistic, 3d, shaded, complicated
```

---

### 模板B：像素精灵（角色/NPC/敌人/怪物）

#### B.1 单帧角色基础公式（SDXL Pixel Art XL最稳）

```
pixel, a [class/type] character [equipment/attire description],
[view] view, [pose], transparent background,
[32/48/64]x[32/48/64] style, retro game sprite,
limited palette, hard pixel edges, flat shading
Negative: 3d render, realistic, blurry, photograph, multiple characters, anti-aliasing, gradient
```

示例：
- `pixel, a warrior character with sword and shield, side view, idle stance, transparent background, 48x48 style, retro game sprite`
- `pixel, slime monster bouncing, front view, green translucent, simple shape, 32x32 style`
- `pixel, female blacksmith NPC with apron and hammer, front view, idle pose, transparent background, 48x48 style, warm earth tones`

**视角关键词映射**：

| 游戏类型 | 视角 | 关键词 |
|---------|------|--------|
| 平台跳跃/横版 | 侧面 | `side view, profile` |
| RPG对话/立绘 | 正面 | `front view, facing camera` |
| Zelda/顶视ARPG | 俯视 | `top-down view, overhead` |
| 经典JRPG | 3/4斜俯 | `three-quarter view, angled top-down` |
| 策略/模拟经营 | 等距 | `isometric pixel art, 2:1 perspective` |

**尺寸规格参考**：

| 用途 | 推荐尺寸 |
|------|---------|
| UI图标/拾取物 | 16×16 |
| NPC/普通敌人 | 32×32 |
| 主角/精细NPC | 48×48 |
| Boss/大型敌人 | 64×64 到 128×128 |

#### B.2 DALL·E 3友好三档位

```
[8/16/32]-bit pixel art character sprite, [front/side] view,
[character description], transparent background,
[32/64/128]x[32/64/128] suitable, [NES/SNES/modern indie] game style,
detailed pixel work, centered composition, game asset
Negative: 3d, realistic, blurry, anti-aliasing
```

#### B.3 Qwen中文角色（国产模型友好）

```
Pixel Art, top-down perspective, 16-bit JRPG style, vibrant colors,
clean outlines, consistent lighting from above,
[角色描述]，[动作/姿态]，[细节修饰]
```

风格锚定词必须每条prompt重复，保证系列角色一致性。

#### B.4 角色一致性工作流（关键）

同一游戏多个角色必须保持画风一致，推荐流程（Python/PIL半自动）：
1. 选定一个角色作为"风格锚"，反复调试到满意
2. 固定seed + 固定LoRA权重 + 固定风格后缀
3. 用img2img以锚定图为参考生成其他角色（denoising strength 0.6-0.7）
4. 用rembg去背景后PIL统一调色板
5. Aseprite中微调对齐

#### B.5 敌人/BOSS

```
pixel, [enemy type] monster/enemy, [color/feature description],
[view] view, [action/pose: idle/attacking/chasing],
transparent background, [size]x[size] style, game sprite,
[menacing/cute/creepy/eldritch] mood, limited palette
```

敌人设计原则：用颜色和剪影快速传达威胁等级——绿色普通/红色精英/紫色Boss；圆形可爱/尖刺危险/扭曲腐化。

#### B.6 多方向/动画精灵表

见模板I（动画帧/SpriteSheet工作流）。

---

### 模板C：建筑Sprite

#### C.1 顶视/等距建筑（RPG小镇最常用）

```
pixel, [building type], [top-down/isometric/three-quarter] view,
[exterior wall material], [roof type/color],
[door/window/chimney/sign details], [small surroundings decor],
[64x64/96x96/128x128] style, 16-bit RPG game sprite, transparent background,
clean edges, flat shading, hard pixel outline, consistent top-left lighting
Negative: 3d render, perspective distortion, blurry, front view, side view, photorealistic
```

**示例：铁匠铺**
```
pixel, blacksmith workshop building, three-quarter top-down isometric view,
rough stone walls with dark brown wooden beams, dark red sloped tile roof,
stone chimney with small light gray smoke, large wooden double door with iron bands,
anvil and water barrel visible outside,
96x96 style, 16-bit SNES RPG game sprite, transparent background,
clean edges, flat shading from top-left, dark brown outline, warm earth tones
Negative: 3d render, perspective distortion, front view, photorealistic
```

**示例：小酒馆**
```
pixel, cozy tavern building, three-quarter isometric view,
plaster walls with dark brown half-timber framing, dark brown thatched/slate roof,
hanging wooden sign (simple beer mug shape), windows with warm yellow glow,
wooden door with lantern beside, small bench outside,
96x96, 16-bit cozy RPG sprite, transparent background, warm color palette
```

**示例：普通民居小屋**
```
pixel, small residential cottage house, three-quarter isometric view,
light beige plaster walls with brown wooden beam trim, warm reddish-brown sloped tile roof,
small stone chimney with light smoke, dark brown wooden front door centered,
two small square windows with warm yellow light, wooden front step, small green bushes,
64x96 style, 16-bit RPG game sprite, transparent background,
clean sharp pixel edges, hard 1-pixel dark outline, flat solid colors, top-left flat shading,
cozy lived-in feel, well-maintained not ruined
Negative: 3d render, photorealism, perspective distortion, front facade view, bloom
```

**示例：帐篷**
```
pixel, traveler's camping tent, top-down view, canvas fabric in [color],
wooden entrance poles, small campfire in front,
48x48, 16-bit RPG sprite, transparent background, simple clean design
```

#### C.2 正面立面建筑（横版平台/城镇背景层）

```
pixel art, [building type], front facade view, side-scroller platformer style,
[architectural style and materials], [door/windows/roof/shop sign details],
16-bit, [palette description], clean pixel edges, no anti-aliasing,
isolated on transparent background
```

#### C.3 大型建筑/遗迹入口

```
pixel, large [ruins/temple/gatehouse/ancient structure],
[isometric/top-down] view, dark stone construction with [cracks/moss/vines/geometric patterns],
[architectural details: pillars/arch/stairs/geometric patterns],
[lighting: torch glow/ethereal cyan light from cracks],
[128x128/larger] style, 16-bit RPG game sprite, transparent background,
dramatic lighting, limited muted palette with accent glow color
```

---

### 模板D：Tileset瓦片（地形/地面/墙壁/道路）

**瓦片是像素游戏AI生成最麻烦的素材**——单块好生成，但拼接会有"暗角"问题（AI会给每块瓦片加阴影边缘），prompt修不了，必须后处理偏移补缝。

#### D.1 单块地形瓦片（基础模板）

```
pixel, [surface type] tile [with small scattered details],
top-down view, seamless tileable game texture,
flat even lighting, uniform color distribution,
16-color palette, [NES/SNES/Game Boy optional],
no corner darkening, no vignette, no edge shadow
```

填充示例：
- 草地：`pixel, grass tile with small evenly scattered grass tufts, top-down view, seamless tileable, green 16-color palette, no edge darkening`
- 水面：`pixel, water tile with small ripples evenly scattered, top-down view, seamless tileable, blue and cyan wave pattern, 16 colors`
- 沙地：`pixel, sand tile with tiny pebbles, top-down view, seamless tileable, warm yellow-orange desert palette`
- 石板路：`pixel, cobblestone tile with scattered stones, top-down view, seamless tileable, gray stone 16-color palette`
- 木板：`pixel, wooden plank floor tile with wood grain, top-down view, seamless tileable, warm brown tones`
- 地牢石：`pixel, dungeon stone tile with cracks and moss, top-down view, seamless tileable, dark gray brown palette`
- 遗迹石砖：`pixel, ancient geometric carved stone tile, top-down view, seamless tileable, dark gray black with faint cyan geometric pattern lines`

瓦片适配等级：
- **AI生成优秀**：有机纹理（草/泥土/沙/雪/熔岩/水）
- **AI生成良好**：半结构化（鹅卵石/砖/石板/木板）
- **AI生成勉强**：方向性瓦片（道路/河流）
- **不适合一次生成**：完整Wang/Blob自动瓦片集（需逐块生成+手工组装autotile）

#### D.2 硬核Autotile（HEX色锁+自动转角）

```
Mandatory Role: You are a precision 2D pixel art spritesheet engine.
Generate a 32x32 Tileset Spritesheet in a 1024x1024 grid.
Each 32x32 cell must be an independent functional game tile.
ABSOLUTELY NO black divider lines or borders between tiles.
Tiles must touch edge-to-edge with 100% pixel continuity.

Perspective: Top-down 90-degree orthogonal view, no parallax, no tilt
Pixel Density: 2x2 macro-pixel block clusters (effective 16x16 per tile)
Anti-Aliasing: Zero, sharp 1px aliased step, no blur, no transparency gradients
Lighting: Flat ambient, NO directional sunbeams or long shadows
NO vignetting, NO corner darkening, NO edge shadows

Color Palette (HEX LOCKED): STRICTLY ONLY [HEX color list]. No #000000 pure black, no outside colors.

Tile Content (Autotile Logic):
- Row 1: 4 variations of Core Tile (seamless, low-frequency details)
- Row 2: Edge Tiles - Tile A transitioning to transparent/B (top/bottom/left/right)
- Row 3: Corner Tiles - 90-degree inner/outer corner transitions

Style: [style description], 16-bit retro console aesthetic,
minimalist texture to prevent obvious tiling patterns
```

#### D.3 整套地形资产表（Givros"乐高法"）

见模板K资产表工作流。

**重要：暗角（Vignetting）问题**
AI生成tileset几乎必然给每个瓦片四周加暗角/阴影，导致拼接时出现网格线。解决方案：
1. prompt里反复强调`NO vignetting, NO edge darkening, NO corner shadows, flat even lighting`
2. 后处理：在Aseprite里将瓦片边缘1-2像素手动偏移/羽化，手工做seamless
3. 终极方案：不用AI一次出整张tileset，而是AI出纹理参考→手工在Aseprite里绘制瓦片

---

### 模板E：植被/自然物

#### E.1 顶视树（Tileset兼容）

```
pixel, a [tree type: oak/pine/palm/apple/dead] tree, top-down view,
[season/color: green summer/autumn orange/snowy/dead],
[fruit/drops if any], subtle shadow beneath to ground circle,
64x64 style, 16-bit RPG sprite, transparent background,
clean edges, limited [N]-color [green-brown/etc] palette
Negative: blurry, 3d render, perspective, roots visible from above
```

#### E.2 侧视树（横版/装饰）

```
pixel art deciduous tree, side view, thick brown trunk,
full green canopy with lighter highlights, small shadow at base,
16-bit, clean pixel edges, limited 12-color green-brown palette,
transparent background, no anti-aliasing
```

#### E.3 灌木/花/草/蘑菇/小石

```
pixel, [plant type], top-down view, [color/size description],
[states: blooming/withered/growing], small subtle shadow,
16x16 or 32x32, 16-bit game sprite, transparent background,
clean pixel edges, limited palette
```

尺寸分档建议：
- 小草/花/蘑菇：16×16
- 灌木/大石/树桩：32×32
- 树（树冠覆盖一个瓦片）：64×64或更大
- 大型特色树/Boss场景树：128×128+

---

### 模板F：特效VFX（攻击/魔法/粒子/爆炸）

特效一般用透明背景+多帧spritesheet。AI单帧能出效果，但动画帧一致性需要手工调整。

#### F.1 单帧特效

```
pixel art VFX sprite, [effect type: slash/hit/explosion/fireball/magic/smoke],
[color: red/orange fire / blue cyan magic / white slash],
transparent background, 48x48, 16-bit game effect,
glowing pixel clusters, particle dots, bloom effect done with color ramps not blur,
clean edges, no anti-aliasing
```

元素特效关键词表：

| 元素 | 颜色 | 形态关键词 |
|------|------|-----------|
| 火 | 橙/红/黄 | flame, ember, sparks, rising |
| 冰/水 | 蓝/青/白 | shard, frost, ripple, splash |
| 雷 | 黄/白/紫 | lightning bolt, jagged line, spark |
| 风/气 | 白/浅青 | swirl, wind line, curved streak |
| 暗/蚀 | 紫/黑/品红 | miasma, tendril, corruption, drip |
| 灵/圣 | 金/白/青 | glow, radiating line, orb, beam |
| 物理slash | 白/浅灰 | arc, slash line, impact star |

#### F.2 魔法投射物

```
pixel art [element] projectile spell, [shape: orb/bolt/arrow],
[color] with trailing particle effect, moving [direction] facing right,
transparent background, 32x32, 16-bit game sprite, clean edges
```

---

### 模板G：UI元素（血条/HUD/物品栏/按钮/对话框）

#### G.1 HUD元素（血条/饱食度/状态条）

```
pixel art game UI [element: health bar/hunger bar/stamina bar],
[orientation: horizontal/vertical], [size: width x height],
[colors: red for HP / orange for hunger / green for stamina],
[empty frame + filled portion],
16-bit game UI, clean pixel edges, transparent/black background,
no anti-aliasing, readable at small scale
```

#### G.2 物品栏/面板/边框

```
pixel art game inventory panel UI frame,
dark wood/brown leather texture with golden border trim,
[N]x[M] grid of square item slots,
16-bit RPG UI style, clean pixel edges, cohesive warm color palette
```

#### G.3 按钮组（批量生成保一致性秘诀）

一次生成一组按钮，风格锁定后重复使用：
```
一组游戏UI按钮图标，统一风格：[按钮1]/[按钮2]/[按钮3]/[按钮4]，
[填充颜色]填充，[描边颜色]粗描边[N]px，[圆润/方形/像素]风格，
[光泽/哑光]质感，透明背景，128x128px每按钮，像素风UI
```

秘诀：每次都带相同风格词（颜色、描边粗细、质感），只换按钮内容。

#### G.4 对话框/文字框

```
pixel art RPG dialogue text box,
dark blue/black semi-transparent background with thin white border,
[N] lines of placeholder pixel text area, small [triangle/arrow] indicator at bottom,
16-bit game UI, clean pixel edges, 4:3 aspect ratio frame
```

#### UI颜色语义参考

| 状态 | 颜色 |
|------|------|
| 生命/危险/敌 | 红 |
| 魔力/灵能/冷 | 青/蓝 |
| 体力/自然/安全 | 绿 |
| 饱食/温暖/友方 | 橙/黄 |
| 经验/升级/稀有 | 金/紫 |
| 毒/蚀/异常 | 紫/毒绿 |
| 普通/中性UI | 棕/灰/米白 |

---

### 模板H：背景/Parallax视差层

视差背景一般分3-4层（天空/远山/近景建筑/前景装饰），每层单独生成，靠滚动速度差制造深度。

#### H.1 远景天空/山

```
pixel art [time: day/sunset/night] [biome: plains/mountain/desert/forest] landscape background,
[layer: sky with clouds / distant mountain silhouette / far forest],
side-scrolling view, 16-bit, wide panoramic,
[color palette: warm sunset / cool blue night / bright day],
clean pixel edges, no anti-aliasing, NO objects in playable area
```

#### H.2 通用视差公式（PromptAnvil法）

按变量填充：
```
pixel art [era] [biome] parallax background layer, [time of day], [weather],
[layer position: sky/mid/near/foreground], [landmarks],
side view, 16-bit, [width]px wide, clean pixel edges, limited palette
```

变量表：
- era：medieval / post-apocalyptic / ancient ruins / sci-fi
- biome：forest / desert / mountain / plains / coast / underground cave
- time：dawn / noon / sunset / night / overcast
- weather：clear / foggy / rain / snow / sandstorm
- landmarks：castle silhouette / ancient arch ruins / windmill / water tower

**层分离技巧**：每层背景单独生成，保持相同时间和天气但不同距离，色饱和度随距离递减（远景灰蓝，近景饱和）。

---

### 模板I：动画帧 / SpriteSheet 工作流

**AI一次出整张可用spritesheet的成功率低**（帧间不一致/动作不流畅），这是像素游戏AI辅助的最大难点。推荐工作流按可靠性排序：

| 方法 | 可靠性 | 说明 |
|------|--------|------|
| **1. 单帧生成+Aseprite手工补帧** | 最稳 | AI出key frame，手工补in-between |
| **2. SD_PixelArt_SpriteSheet四方向专用模型** | 较稳 | 前缀触发词+256x256，主要是idle/walk/run |
| **3. DALL·E 3整sheet生成** | 一般 | 需要详细描述每行每列帧数，适合简单动作 |
| **4. 专用工具链（SpriteSheet Pipeline插件/Anima）** | 较新 | 社区工具，需验证 |
| **5. img2img逐帧+seed固定** | 可试 | 固定seed，逐帧微调姿态 |

#### I.1 DALL·E 3骑士精灵表模板

```
Create a pixel art hero [class] for a 2D [top-down/side-scrolling] game.
Show a sprite sheet with [N] rows: idle (4 frames), walk (6), [attack/jump/hurt (3-6 frames each)].
Consistent 1-pixel dark outline, flat cel shading, no anti-aliasing,
clean separation between frames (6px gutters). View: [side/top-down] profile.
Pixel grid: [32/48]x[32/48] per frame.
Palette: [N] colors max ([color description]).
Background: transparent PNG. No label text.
Canvas: 1024x1024.
```

#### I.2 8方向顶视角色模板（Roguelike类）

```
Design a top-down pixel [class] with 8-direction facing (N, NE, E, SE, S, SW, W, NW),
idle and walk (4 frames each per direction).
Pixel grid: 32x32 per frame. Palette: 10 colors (muted greens/browns).
Outline: 1-pixel dark outline. No anti-aliasing. Transparent background.
Keep character centered in each cell.
```

#### I.3 动画关键词库

| 动作 | 英文描述 |
|------|---------|
| 待机idle | breathing bob, subtle idle, gentle sway |
| 走walk | walking cycle, legs alternating, arms swinging |
| 跑run | running sprint, fast stride, leaning forward |
| 攻击attack | attacking pose, [weapon] swing, strike arc |
| 跳跃jump | jumping arc, mid-air pose, tuck/extend |
| 受伤hurt | hurt flash, recoil, knocked back |
| 死亡death | death pose, fallen, dissolve particles |

---

### 模板J：3D资产灰模中转

text-to-3D对形状描述理解弱——"倒三角"可能生成"坑坑洼洼的石头"。先出灰模参考图，再图生3D。

```
[object description], pure black background, grayscale, isometric view,
no color, no lighting, no shadow, 1:1 ratio, 3D render,
neutral gray material, clean geometry
```

减面目标：大型场景<5万面，中型道具1-3万面，小型精细5千-1万面。

---

### 模板K：资产表批量规划法（Givros工作流）

独立开发者验证过的高效流程——先在prompt里规划完整资产表，分批生成：

```
Global requirements for all sheets:
pure white/transparent background, all assets fully separated with clear spacing,
consistent scale, clean organization by category,
no overlapping, no UI, no text, no realistic rendering,
minimal details, clean shapes, no noise,
[统一风格描述：pixel art / 16-bit / palette / 参考游戏等]

Sheet 1 - Terrain/Water/Path assets:
[grass tiles, sand tiles, water tiles, dirt path tiles, wooden bridges, fences, rocks, flower bushes]

Sheet 2 - Buildings/Props/Nature:
[cottages, shop buildings, barns, trees, street lamps, wells, barrels, crates, haystacks]

Sheet 3 - Characters/Animals:
[player character (front walk frames), NPCs, cow, chicken, cat]
```

**工作流**：
1. 列出完整资产清单（什么图、什么分辨率、几个变体），Excel或Markdown表格
2. 按类别分成多个Sheet（每Sheet不超过10个物件）
3. 每次生成一个Sheet，所有物件共享同一套Global requirements
4. 生成后用rembg批量去背景，裁切单个素材
5. Aseprite中修整、统一调色板、对齐网格

独立开发者用此流程1-2天可出一整套小镇素材。

---

## 风格锚定速查表

用具体游戏名锚定比抽象描述精确得多：

| 想要的风格 | 写这个 | 不写这个 |
|-----------|--------|---------|
| 暖色独立像素（Celeste/蔚蓝） | `Celeste style, pastel colors, modern indie pixel` | `retro indie pixel style` |
| NES复古（铲子骑士） | `Shovel Knight inspired, NES palette, 8-bit` | `old school pixel` |
| 16-bit暖色（星露谷） | `Stardew Valley aesthetic, cozy 16-bit` | `cute pixel, farming game style` |
| 暗黑童话/手绘（饥荒DST） | `Don't Starve Together style, Tim Burton-esque, ink sketch, rough edges` | `dark creepy style` |
| 毛糙手绘像素（风来之国Eastward） | `Eastward / Pixpil style, rough hand-drawn pixel, earthy palette, thick outlines` | `retro pixel RPG` |
| 霓虹复古像素（赛博朋克/HLD） | `Hyper Light Drifter aesthetic, neon accents, dark palette, detailed pixel` | `cyberpunk pixel` |
| 扁平轻渐变（现代UI） | `game icon institute flat design` | `modern clean icon` |
| 低多边形等距（Tunic/Cocoon） | `Tunic isometric low-poly pixel, geometric shapes, soft pastel` | `cute 3D pixel` |
| 高清2D像素（八方旅人HD-2D） | `HD-2D style, Octopath Traveler, 3D environments with 2D sprites` | `3D pixel RPG` |
| 硬核动作像素（渎神/Blasphemous） | `Blasphemous gothic pixel art, dark religious aesthetic, detailed pixel` | `dark fantasy pixel` |

---

## 跨场景通用后缀（万能复制段）

**英文版（SD/MJ通用）**：
```
hard sharp pixel edges, zero anti-aliasing, flat solid colors,
no gradients, no soft shadows, no blur, no bloom, no photorealism,
limited color palette, thick 1-pixel dark outline, clean readable silhouette
```

**中文版（国产模型用）**：
```
硬边像素，零抗锯齿，纯平色块，无渐变，无柔边阴影，无模糊，
无光晕，无写实感，限色调色板，1像素粗深色描边，剪影清晰
```

---

## 通用负面提示词库

### SDXL / SD 1.5 通用负面模板（去AI味）

```
3d render, realistic, photograph, photorealistic, blurry, soft, smooth,
anti-aliased, anti-aliasing, gradient, smooth gradients, smooth shading,
high resolution, detailed texture, noise, noisy background, watermark,
text, signature, logo, jpeg artifacts, lowres, cropped, out of frame,
bad anatomy, deformed, disfigured, extra limbs, missing limbs, mutation,
multiple characters, frame, border, vignetting, edge darkening
```

### 问题→针对性负面词

| 问题 | 加这些 |
|------|--------|
| 边缘模糊/非像素感 | `anti-aliasing, soft edges, blurry, smooth` |
| 3D塑料感 | `3d render, realistic, rendered, cgi, octane render, unreal engine` |
| 渐变/光影过度 | `gradient, photorealistic lighting, lens flare, depth of field, bokeh, bloom` |
| 多余噪点/纹理 | `noise, noisy, detailed texture, grain, film grain` |
| 出现文字水印 | `text, watermark, signature, logo, username, letters` |
| 肢体畸形（角色） | `bad anatomy, extra limbs, missing limbs, mutated, deformed hands, extra fingers` |
| 色彩过多/过饱和 | `too many colors, oversaturated, high contrast hdr` |
| 瓦片暗角/拼接问题 | `vignetting, corner darkening, edge shadows, darkened edges` |
| 背景不纯净（图标/精灵） | `complex background, detailed background, busy background` |

### Midjourney参数

```
--no realistic, smooth, gradient, 3d, photoreal, blurry
--style raw          # 必加，关闭自动美化
--s 50-150           # 低stylize保持像素约束
```

### 国产模型（即梦/可图/通义/豆包）中文负面词

```
不要文字，不要水印，不要签名，不要模糊，不要渐变，不要抗锯齿，
不要3D感，不要写实风格，不要多余细节，不要噪点，不要晕影
```

---

## 后处理工作流（关键）

AI生成像素素材后，**必须**经过后处理才能用。工具链：

| 环节 | 工具 | 作用 |
|------|------|------|
| 去背景 | rembg / remove.bg | PNG透明化 |
| 像素修整 | Aseprite（付费）/ Piskel（免费在线）/ LibreSprite | 修正AI边缘、对齐网格、统一调色板 |
| 调色板统一 | pngquant / Aseprite调色板功能 | 所有素材限到同一色板 |
| 瓦片拼接检查 | Tiled地图编辑器 | 检查autotile是否seamless |
| SpriteSheet打包 | TexturePacker / Aseprite | 打包成游戏引擎可用的图集 |
| 压缩 | pngquant / oxipng | PNG无损压缩减小体积 |

**瓦片暗角修复流程**：
1. 在Aseprite中打开AI生成的瓦片
2. 复制瓦片到4个方向偏移（Offset by X/Y by tile size）
3. 检查拼接缝，用clone stamp工具修复
4. 取32x32中心区域作为seamless瓦片

**5大AI味陷阱与解药**：

| AI味 | 原因 | 解药 |
|------|------|------|
| 软边缘/抗锯齿 | 通用模型默认bilinear采样 | 像素LoRA + `no anti-aliasing` + 后处理nearest neighbor缩小 |
| 渐变/柔和光影 | AI默认shading不是flat | `flat shading, no gradients, solid colors` + Aseprite手工修 |
| 过度细节/噪点 | AI默认加texture | `minimal details, clean shapes, limited palette` + pngquant减色 |
| 形状不准 | 文本空间理解有限 | 参考图+img2img / ControlNet Canny线稿 / 手工修正关键形状 |
| 风格漂移（批量） | 每张独立采样 | 固定seed + 统一风格词 + img2img锚定 |

---

## 诊断路由

| 观察到 | 可能原因 | 修复动作 |
|--------|---------|---------|
| 像素边缘模糊/有抗锯齿 | 通用模型出像素风 | 换专用像素LoRA；prompt加`hard edges, no anti-aliasing`；后处理nearest neighbor缩小到真像素尺寸再放大 |
| 瓦片拼接有暗角/网格线 | AI给每块瓦片加边缘阴影 | prompt加`no vignetting, no edge darkening, flat lighting`；后处理offset修补 |
| 一套图标风格不统一 | 批量生成风格漂移 | 固定seed+统一风格词+一组生成+图生图锚定；最后Aseprite统一调色板 |
| 角色sprite肢体畸形 | SD人体理解+小尺寸双重问题 | 先128-256尺寸生成再nearest缩到64；或用OpenPose ControlNet；后处理手工修正关键部位 |
| spritesheet帧间不一致 | AI独立处理每帧 | 不指望一次出sheet；AI出key frame手工补帧；或用SD_PixelArt_SpriteSheet专用模型 |
| 图标过度细节/不像游戏素材 | 堆了"ultra detailed/high quality" | 删画质增强词，图标不需要过度细节；加`minimal, clean silhouette, limited palette` |
| 食物/日常物品跑偏成金币/曲奇 | AI对round golden联想固化 | 精确材质描述+加负面词`no coin, no cookie, no gold`；或用参考图 |
| 3D形状偏差 | text-to-3D空间理解弱 | 先灰模参考图再图生3D；或用ControlNet Depth |
| 风格与游戏不搭 | 风格锚定太笼统 | 用具体游戏名锚定（见风格速查表） |
| 手绘/粗糙风变干净 | GPT Image 2/内置模型house style | 描述具体视觉特征不写风格标签：`rough chalk texture, visible strokes, jagged edges` |

---

## 场景必检项

```
□ 素材类型已确定？（图标/角色/建筑/瓦片/植被/特效/UI/背景/动画/3D）
□ 模型选择合适？（像素素材必须用专用LoRA或SD像素模型；非像素素材按类型选）
□ 视角写清了？（top-down/side/isometric/front 选错全错）
□ 风格锚定具体？（具体游戏名或年代+平台，不是"retro/cute"）
□ 技术约束带齐？（硬边缘/无抗锯齿/限色板/平涂/正确尺寸）
□ 批量需求已确认？（是否需要一致性策略：一组生成/seed固定/锚定图img2img）
□ 负面提示词按素材类型加了针对性项？（瓦片加暗角/角色加畸形/图标加背景词）
□ 后处理计划明确？（Aseprite修整/调色板统一/瓦片补缝/打包）
```
