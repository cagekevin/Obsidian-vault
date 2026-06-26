# brand-spec.json 完整模板

> 这是一个**带说明的模板**。每个字段都标注了：该填什么、可选值有哪些、去哪里查参考。
> **不要直接复制使用**，按说明逐字段填入你自己的项目数据。

---

## 顶层字段

```json
{
  "brand": {
    "name": "品牌英文名，如 HKH",
    "product_full": "产品完整名称，如 Bakuchiol VC-IP Cistus Revitalizing Facial Oil (Light Edition)",
    "product_short": "产品简称，如 Bakuchiol Facial Oil",
    "category": "品类，如 面部精华油"
  },

  "theme": "主题名，选一个，见下方 [可选主题]",
  "claim_seeds": [
    {"id": "唯一标识", "text": "核心声明文本"},
    {"id": "...", "text": "..."}
  ],

  "style": {
    "height_mode": "fixed 或 auto（见下方 [高度模式]）",
    "ratio": "9:21 或 9:16（见下方 [比例]）",

    "photography": "摄影风格描述，进 Prompt",
    "lighting": "光位描述，进 Prompt",
    "lens": "镜头描述，进 Prompt",
    "mood": "情绪描述，进 Prompt",
    "palette": {
      "accent": "强调色（装饰线条/标签/徽章）",
      "bg_alt": "交替背景色",
      "text": "主文字色",
      "sub": "次级文字色"
    },
    "typography": {
      "header": "标题字体",
      "body": "正文字体"
    },
    "modifiers": ["修饰词，进 Prompt"]
  },

  "banned": ["全局禁用词，画面和文案都不能出现"],
  "theme_bundle": {
    "allowed": ["画面中允许出现的道具"],
    "banned": ["画面中禁止出现的道具"]
  },
  "primary_image": "产品图路径",

  "screens": {
    "01": { "template": "hero", ... },
    "02": { "template": "list", ... },
    "...": "屏数自由增减，01 必须 hero，末屏必须 closing"
  }
}
```

---

## 可选主题（theme）

| theme | 风格 | 对应 CSS | palette 参考（accent / bg_alt / text / sub） |
|-------|------|----------|---------------------------------------------|
| `pilgrim-dawn` | 朝圣黎明 / 暖色杂志 | `theme-pilgrim-dawn.css` | #C5A26B / #F4EFE3 / #2A1F1A / #7A6E67 |
| `lyrical-ocean` | 诗意深海 / La Mer 风 | `theme-lyrical-ocean.css` | #C5A46D / #EBF0ED / #1A2623 / #7A8B86 |
| `parisian-chic` | 巴黎先锋 / 高定海报 | `theme-parisian-chic.css` | #D4A373 / #F8F8F8 / #000000 / #666666 |
| `dark-nexus` | 暗夜星云 / Vercel 科技 | `theme-dark-nexus.css` | #FF6363 / #0A0A0A / #EDEDED / #888888 |
| `swiss-industrial` | 瑞士工业 / 极简秩序 | `theme-swiss-industrial.css` | #E2231A / #F4F4F4 / #111111 / #5C5C5C |
| `apothecary-folio` | 药剂师文库 / 文学收藏 | `theme-apothecary-folio.css` | #7A4623 / #F0EDE4 / #1B1B1B / #7A8470 |
| `data-ink` | 数据时报 / 学术权威 | `theme-data-ink.css` | #D0021B / #F7F7F7 / #121212 / #666666 |
| `brutalist` | 野兽派 / 反设计 | `theme-brutalist.css` | #FF3D00 / #F5F4F0 / #000000 / #000000 |
| `mid-century` | 世纪中叶 / 60年代海报 | `theme-mid-century.css` | #D9A441 / #3D6E70 / #1A1A18 / #7A725F |
| `cupertino` | 加州白皮书 / Apple 风 | `theme-cupertino.css` | #0071E3 / #F5F5F7 / #1D1D1F / #86868B |
| `data-terminal` | 极客终端 / 金融面板 | `theme-data-terminal.css` | #FFA02F / #11172A / #E8ECF4 / #5E6680 |

> **配色规范**：`style.palette` 中的颜色会拼入生图 Prompt。必须与所选 theme 的配色一致。

---

## 高度模式（height_mode）

| 值 | 效果 |
|----|------|
| `"fixed"` | 每屏固定高度（9:21 = 1680px，9:16 = 1280px），内容超长时溢出 |
| `"auto"` | 自适应内容高度，内容撑多高就多高 |

## 比例（ratio）

| 值 | 尺寸 | 适用场景 |
|----|------|----------|
| `"9:21"` | 720×1680 min-height | 电商长图详情页（默认） |
| `"9:16"` | 720×1280 min-height | 移动端 H5 页面、品牌官网 |

---

## 每屏结构（screens）

| 字段 | 必填 | 说明 |
|------|------|------|
| `template` | 是 | `hero` / `list` / `compare` / `closing` / `editorial` / `focus` |
| `background` | 是 | `"default"` / `"mod--alt-bg"` / `"mod--hero"` |
| `claim_seed_back` | 是 | 该屏追溯到的 claim_seed id 列表，屏 01 必须包含全部 |
| `text_exact` | 是 | 该屏文案（人看的），见下方字段 |
| `visual_description` | 是 | 纯英文画面描述 30-120 词，**不能含中文** |

### text_exact 可选字段

| 子字段 | 适用模板 | 说明 |
|--------|----------|------|
| `kicker` | 所有 | 简短标签 |
| `deco_en` | 所有 | 英文装饰文字，字间距自动展开，如 "E D I T I O N" |
| `headline` | 所有 | 主标题，≤18 视觉字 |
| `subheadline` | hero | 副标题，≤24 视觉字 |
| `body` | hero / list | 正文 |
| `tags` | hero | 标签数组 |
| `items` | list | 列表项，key 按需求自定（无预设结构） |
| `rows` | compare | 对比行，key 按需求自定 |
| `qa` | closing | FAQ 问答对 |
| `quote` | closing | 引语 |
| `notes` | closing | 注解列表 |
| `badges` | compare | 徽章数组 |
| `zero_strip` | list | 零添加声明数组 |
| `tip` | list | 小贴士 |
| `texture` | list | 质地描述 |
| `closing` | closing | 品牌落款（末屏必填） |
| `signature` | list / closing | 签名金句 |

---

## visual_description 写法指南

**什么是 visual_description**：纯英文的物理画面描述，喂给生图模型用。
**绝对不能**：把 `text_exact` 的中文文案直接翻译或原样喂给模型（会导致画面出现文字、人脸乱入等灾难）。

### 写法规范

1. 完整英文句子，非中文译稿
2. 必须含 **subject（主体） + lighting（光位） + lens/composition（镜头/构图） + mood（情绪） + palette hint（色调暗示）**
3. 禁止使用 `text_exact` 中的中文修辞
4. 长度建议 50-120 词
5. 默认 `no people / no hands / no faces`（除非用户明确要求）

### 示例对照

❌ 错误：`text_exact.headline = "像给皮肤一次深呼吸"` → 模型画出张大嘴巴呼吸的人
❌ 错误：`text_exact.headline = "一滴，三道温和抗老链路"` → 模型画出三条发光的电线

✅ 正确：
```json
{
  "text_exact": { "headline": "一滴，三道温和抗老链路" },
  "visual_description": "Three crystal-clear golden oil capsules arranged in a vertical column on a slab of raw white Cistus rock-rose, each capsule glowing softly with one hero ingredient inside, side directional warm light, shallow depth of field, no hands, no numbers, no text, ultra-clean laboratory editorial aesthetic."
}
```

---

## 常见问题排查

### check.cjs 报错对照

| 报错 | 原因 | 修复 |
|------|------|------|
| `brand.name 缺失` | JSON 缺字段 | 补齐 brand-spec.json |
| `屏 01 缺少 seed` | 首屏未包含所有 claim_seed | 补全 `claim_seed_back` |
| `无主线 seed（≥3 屏）` | 叙事过于发散 | 让至少 1 个 seed 贯穿 3 屏以上 |
| `含转化词 [立即购买]` | 展示页混入电商词 | 改写为展示页语气 |
| `缺 visual_description` | 文案与视觉未解耦 | 补纯英文画面描述 |
| `visual_description 含中文` | 画面描述写了中文 | 必须纯英文 |
| `屏 X 与上屏同模板` | 相邻屏用了相同模板 | 换模板（closing 除外） |
| `屏 01 必须 hero` | 首屏模板不对 | 改为 hero |
| `末屏必须 closing` | 最后一屏模板不对 | 改为 closing |
| `HTML 含 Emoji` | 页面里有 emoji | 删除或用图标代替 |
| `HTML 含 CSS 动效` | 有 @keyframes/animation | 删除动效 |
| `所有屏背景相同` | 8 屏全是 default 背景 | 加 mod--alt-bg |
| `screen_X.png 未生成` | render 没跑完 | 重跑 render.cjs |
| `screen_X.png 过小` | 该屏内容可能为空 | 检查 JSON 数据 |
| `prompt_X.txt 含中文` | Prompt 被污染 | 检查 render.cjs 是否误读 text_exact |

### 渲染效果不理想

- **字体未加载**：检查网络或 `template.html` 的 font link
- **图片空白**：检查 `primary_image` 路径是否正确
- **排版错乱**：检查 `headline` 是否超 18 字
- **主题不对**：检查 `theme` 字段是否写对
