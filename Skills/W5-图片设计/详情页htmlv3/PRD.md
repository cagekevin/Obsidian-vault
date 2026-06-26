# 详情页 HTML v3.1 · PRD

> **核心目标**：1 张产品图（必填）→ 3 种输出（HTML / 瀑布流长图 / 生图 Prompt）
> **核心架构**：`brand-spec.json` 驱动一切；文案与视觉彻底解耦；脚本渲染，拒绝大模型乱改代码
> **核心价值**：比 v2 简单（25 BEM · 4 模板 · 1 主题）、比 v2 严谨（解决多态数据与 AI 幻觉）、全自动化输出
> **版本**：v3.1（2026-06-14）
> **范例**：HKH Bakuchiol VC-IP Cistus Revitalizing Facial Oil

---

## 1. 设计原则（v3.1 核心架构升级）

| 维度 | v2 (旧) | v3.1 (当前) |
| --- | --- | --- |
| 画布 | 790×940 | **720px 定宽 + `min-height` 弹性高度**（拒绝死锁） |
| 屏数 | 12 | **8** |
| BEM class | 48 类 | **25 类**（砍 50%） |
| 布局模板 | 8 | **4**（hero / list / compare / closing） |
| 主题 | 3 个可选 | **1 个**（朝圣黎明 · 默认） |
| 视觉隔离 | 无 | **强制解耦**（`text_exact` 供人读，`visual_description` 供机器生图） |
| 流程 | 8 步 3 批 | **6 步 2 批**（70% 脚本化） |
| 自动化自检 | 17 项 | **12 项**（新增字数防爆、转化词拦截、Prompt 污染阻断） |
| 输出物 | HTML | **HTML + 拼接长图 + 8 段纯净 Prompt** |
| 脚本参与 | 0% | **70%（4/6 步）** |
| 叙事护栏 | 无 | **claim seed 追溯链**（来自 DetailFlow） |
| 返修引导 | 自检只报 PASS/FAIL | **revision routing**（来自 DetailFlow） |

**关键架构变更**：
- 砍 4 维定位（v3 只用 claim seed + 文案，更轻量）
- 用 `brand-spec.json` 替代 `brand-spec.md`（结构化 + 可校验）
- 脚本 `render.cjs` 一次性出 3 种输出
- `screens[*]` 强制 `text_exact` + `visual_description` 双字段并列

### 1.1 弹性高度策略（替代死板的 aspect-ratio）

**致命 Bug 修复**：旧版强制 `aspect-ratio: 9/21` 会导致字少的屏幕出现巨大空洞，字多的屏幕文字溢出。
**v3.1 策略**：使用**弹性最小高度（Fluid min-height）**。

* `.mod { width: 100%; max-width: 720px; min-height: 1680px; height: auto; }`
* 允许内容自然向下撑开。Playwright 截图时依靠 `fullPage: true` 自动截取真实高度，随后无缝拼接为完美长图。

### 1.2 比例切换（9:21 默认 / 9:16 可选 — 兼容保留）

**v3.1 仍支持 2 种比例，在 brand-spec.json 中指定，但不再依赖 `aspect-ratio`，而是通过 `min-height` + 截图策略实现**：

```json
"style": {
  "ratio": "9:21"   // 默认 · 电商长图首选
  // 或
  "ratio": "9:16"   // 可选 · 移动端优先
}
```

**两种比例的适用场景**：

| 比例 | 尺寸 | 适用 | 推荐 |
|---|---|---|---|
| **9:21** | 720×1680 min-height | 淘宝/京东/拼多多 详情页长图 | ✅ v3.1 默认 |
| **9:16** | 720×1280 min-height | 移动端 H5 页面、品牌官网 | 备选 |

**切换原理**：
- `.mod { min-height: <比例对应值>; max-width: 720px; }` — 改 CSS 变量
- 8 屏布局结构完全不变（只改最小高度）
- 长图 PNG 尺寸自动跟着改
- prompt 中 `ratio: 9:21` 同步替换

**不允许混用**（每个项目只能选一个比例）。

**自动校验（Step 4 Fail Fast）**：
- `ratio` 字段必须 ∈ {`9:21`, `9:16`}
- 非法值（如 `"1:1"` / `"16:9"`）→ **立即中断**，报 `Error: style.ratio 必须为 9:21 或 9:16，当前值: "1:1"`

---

## 2. 输入路由（2 个分支）

**用户必填**：至少 1 张产品图（无图直接退出）

```
                ┌──────────────────────┐
                │  用户必填：产品图     │  ← 无图 = 退出
                └──────────┬───────────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
        【路由 A】                 【路由 B】
        有文案（用户提供）         极简输入（1 图 + 至少 3 个核心声明）
              ↓                         ↓
        AI 生成 brand-spec.json   AI 基于 Claim Seeds 扩写 8 屏文案
        + 补 visual_description        + 合规铁律（禁捏造/禁医疗词）
              ↓                         ↓
        Step 1 直接进行            回问用户确认
                                       ↓
                                  路由 A 路径
```

### 2.1 路由 A · 精确输入（用户指定文案）

**触发**：用户提供 8 段文案（每段含主标+副标+body）+ 至少 1 张产品图

**操作**：
1. 接收产品图 + 文案
2. AI 将文案转化为 `brand-spec.json`，补齐英文画面描述（`visual_description`），核心字段用户填，可选字段 AI 推断
3. 进入 Step 1

**成功**：8 段文案完整 + brand-spec.json 必填字段齐全
**失败**：文案缺屏 / JSON 缺字段 / 字段值含 banned 词

### 2.2 路由 B · 极简输入（AI 合规辅助）

**触发**：用户仅提供 **1 张产品图 + 至少 3 个核心声明（Claim Seeds，如：维C、提亮、敏肌可用）**。

**操作**：
1. AI 严格基于给定的 Claim Seeds，扩写 8 屏展示页文案。
2. **合规铁律**：**绝对禁止** AI 凭空捏造任何化学成分、专利名称或临床数据；禁止使用医疗词汇（抗皱/治愈等）。
3. AI 生成 `brand-spec.json`（含 8 屏草稿文案 + claim seed），并回问用户确认。
4. 用户回"OK"或修改 → 进入 Step 1。

**AI 推断的边界**：
- ✅ 可推断：品类、目标人群、3-4 claim seed、8 段主标/副标/body
- ❌ 不可推断：临床数据、认证、奖项、检测报告、精确参数
- ❌ 不可推断：医疗词（抗皱/抗衰/祛斑/祛痘/治愈）

**草稿标注**：JSON 字段标 `"ai_inferred": true`，提示用户复核

---

## 3. 核心架构：brand-spec.json

**v3.1 用 JSON 替代 markdown 文档**，核心原因：
- 字段可校验（缺字段 = FAIL）
- 字段可复用（HTML 和 prompt 都从 JSON 读）
- 字段可改（1 处改动 → 8 屏自动同步）

### 3.1 强一致性的 JSON 结构（修复多态陷阱）

**致命 Bug 修复**：旧版 `list` 模板的 items 数据结构不统一，会导致渲染脚本崩溃。v3.1 强制所有 `list` 模板的 `items` 必须遵循统一键值对：`{"mark", "title", "desc"}`。

### 3.1.0 文案与视觉解耦（隐喻陷阱防护 · 强制）

**架构铁律**：`screens[*]` 必须**同时**存在两个独立字段，**任何一屏缺 `visual_description` = Fail Fast 中断**。

| 字段 | 用途 | 流向 | 风险 |
|---|---|---|---|
| `text_exact` | **人**看的营销文案（中文、含修辞） | HTML 排版、UI 标签 | 直接喂给图像模型 → 灾难 |
| `visual_description` | **机器**看的画面描述（英文、画面、镜头） | 生图 prompt 拼接 | 缺它 = prompt 退化为中文文案 |

**为什么必须解耦**：图像生成模型是字面派（Literal），不是文学家。

- ❌ 错误：`text_exact.headline = "像给皮肤一次深呼吸"` 直接喂给模型 → 画面生出一个张大嘴巴呼吸的人
- ❌ 错误：`text_exact.headline = "一滴, 三道温和抗老链路"` → 画面画出三条发光的电线或马路
- ✅ 正确：`visual_description = "A macro of a single golden oil droplet resting on a pristine white Cistus petal, soft morning light, ultra-clear, minimalist, evokes ritual and quiet luxury."` → 画面是一滴油在花瓣上

**`visual_description` 写法约束**：
1. 必须是**完整英文句子**，而非中文译稿
2. 必须含 **subject（主体） + lighting（光位） + lens/composition（镜头/构图） + mood（情绪） + palette hint（色调暗示） + banned-aware（远离 banned 词）**
3. **禁止使用** `text_exact` 中的中文修辞（深呼吸 / 链路 / 一滴 / 仪式感 / 4 周见变化 等）
4. 长度建议 50-120 词（过短信息不足，过长模型会抓不住重点）
5. 单屏出现人脸时**必须避坑**：默认"no people / no hands / no faces"（除非用户明确要求）

**Fail Fast 校验**（Step 2 加入）：
- `screens[*].visual_description` 字段缺失 → 立即中断 `Error: Screen 03 缺 visual_description · at validate-seeds.cjs · fix: 在 screens.03 补一段 50-120 词的英文画面描述`
- `visual_description` 命中 banned 词 → 立即中断（避免闭环：写文案时禁用，喂图时也禁用）
- `visual_description` 含中文 → 立即中断

**AI 写 `visual_description` 的工作流**（路由 B / 路由 A 均可）：
1. 读 `text_exact` → 抓**画面锚点**（屏 03 = 三道链路 → 三个胶囊）
2. 读 `style.photography / lighting / lens / mood` → 套**风格前缀**
3. 读 `theme_bundle.allowed` → 挑**视觉元素**
4. 读 `banned` → 主动**避开** banned 视觉（如 stock photo feel、cartoon）
5. 用英文拼成 1 段，**不译中文文案**

**HKH 范例（屏 03）对照**：
```json
{
  "text_exact": { "headline": "一滴, 三道温和抗老链路" },
  "visual_description": "Three crystal-clear golden oil capsules arranged in a vertical column on a slab of raw white Cistus rock-rose, each capsule glowing softly with one hero ingredient inside, side directional warm light, shallow depth of field, no hands, no numbers, no text, ultra-clean laboratory editorial aesthetic."
}
```

#### 3.1.0.a 展示页定位（Showcase Page · 非电商详情）

**v3.1 的核心定位是「展示页 / Showcase Page」，不是「电商详情页 / E-commerce Detail」**。两者根本不同：

| 维度 | 展示页（v3.1 做这个） | 电商详情页（v2 在做） |
|---|---|---|
| 目的 | 品牌叙事、产品呈现、信任建立 | 直接促成下单转化 |
| 收尾 | 品牌信息、价值主张、仪式感 | 价格、优惠、库存、CTA 按钮 |
| 关键词 | 探索 / 体验 / 仪式 / 工艺 | 立即购买 / 加购 / 领券 / 限时 / 库存 |
| 落地页 | 通常外链到品牌官网 / 小程序 | 自带购物车闭环 |

**v3.1 禁用转化词清单**（Hard Banned · `text_exact.*` 任一字段命中即 FAIL）：

```
立即购买 / 立即下单 / 立即查看 / 立即抢购
加购 / 加入购物车 / 加入车队
领券 / 领红包 / 优惠券 / 满减
限时 / 限时特价 / 倒计时 / 错过等
包邮 / 顺丰包邮 / 7 天无理由 / 7 天退换
库存 / 仅剩 / 即将售罄 / 疯抢
正品保证 / 假一赔十
```

**HKH 范例修正对照**：
- ❌ 旧 `screens.01.text_exact.cta = "立即查看"` → 错位（电商标语侵入展示页）
- ✅ 新 `screens.01.text_exact.cta = "了解更多"` → 展示页语气（鼓励继续浏览，不催促转化）
- ❌ 旧 `screens.08.text_exact.cta = "立即购买 → HKH Bakuchiol VC-IP Facial Oil"` → 严重错位（详情页做了电商的事）
- ✅ 新 `screens.08.text_exact.closing = "HKH · Light Edition · 4 周温和抗老 · 写给敏感肌的日常仪式"` → 展示页收尾（品牌落款，无购买引导）

**架构落地**：
- `banned` 字段扩展（默认加载 v3 展示页 banned 集 ∪ 转化词清单）
- Step 2 `validate-seeds.cjs` 加扫：每屏 `text_exact.*` 字段值命中转化词 → **立即中断**报具体屏号+具体词
- Step 6 `self-check.cjs` 加 #9 项：8 屏 text_exact 全扫转化词
- `visual_description` 不受影响（英文，本身不会写"立即购买"）

**展示页允许的 cta 语气**（白名单）：

```
了解更多 / 查看详情 / 继续探索 / 探索工艺
阅读完整故事 / 探索更多 / 关注品牌 / 访问官网
```

**如果用户要做电商详情页**（需求转换）→ 切换到 v2 skill 路径，不要混用 v3.1。

### 3.1 JSON 结构（HKH 范例 — 多态修复版）

```json
{
  "brand": {
    "name": "HKH",
    "product_full": "Bakuchiol VC-IP Cistus Revitalizing Facial Oil (Light Edition)",
    "product_short": "Bakuchiol Facial Oil",
    "category": "面部精华油"
  },
  "style": {
    "photography": "high-end skincare editorial photography, macro details",
    "lighting": "soft directional warm light from upper right 45°",
    "lens": "shallow depth of field with light bokeh",
    "mood": "clinically trustworthy + luxury",
    "palette": {
      "gold": "#C9A876",
      "cream": "#F2E8D9",
      "text": "#2A1F1A",
      "sub": "#8B7B6F"
    },
    "typography": {
      "header": "Playfair Display, Source Han Serif SC",
      "body": "Inter, PingFang SC"
    },
    "ratio": "9:21",
    "modifiers": ["magazine-grade", "commercial photography", "never cartoonish"]
  },
  "banned": ["emoji", "cartoon", "stock photo feel", "抗皱", "抗衰", "祛斑", "治愈"],
  "claim_seeds": [
    {"id": "bakuchiol_replacement", "text": "维 A 之外的温和抗老"},
    {"id": "vc_ip_brightening", "text": "稳态提亮"},
    {"id": "cistus_resilience", "text": "屏障修护"},
    {"id": "light_friendly", "text": "敏肌轻油日用友好"}
  ],
  "theme_bundle": {
    "allowed": ["瓶子", "金盖", "胶囊", "米白底", "金色粒子", "花瓣", "油滴"],
    "banned": ["梳子", "滴管", "粒子(未列)", "光斑", "光环", "能量波纹"]
  },
  "primary_image": "Temp/WecomSave_*.JPG",
  "screens": {
    "01": {
      "template": "hero",
      "background": "mod--hero",
      "claim_seed_back": ["bakuchiol_replacement", "vc_ip_brightening", "cistus_resilience", "light_friendly"],
      "text_exact": {
        "kicker": "HKH · LIGHT EDITION",
        "deco_en": "Bakuchiol · VC-IP · Cistus",
        "headline": "维 A 之外的 4 周温和抗老",
        "subheadline": "HKH × Bakuchiol × VC-IP × Cistus",
        "body": "敏感肌也能用的温和抗老精华",
        "tags": ["敏感肌可用", "4 周紧致淡纹", "胶囊锁鲜"],
        "cta": "了解更多"
      },
      "visual_description": "A single frosted-glass dropper bottle with a golden cap, centered on a pristine ivory backdrop. Soft warm directional light from the upper right at 45 degrees, ultra-macro editorial shot, the golden oil visible through the translucent glass. Shallow depth of field, no text, no hands, no clutter, magazine-grade commercial photography."
    },
    "02": {
      "template": "list",
      "background": "mod--alt-bg",
      "claim_seed_back": ["light_friendly"],
      "text_exact": {
        "kicker": "PAIN POINTS · 4 大痛点",
        "headline": "抗老产品用过不少, 为什么还是没用？",
        "transition": "你的皮肤需要的不是更强, 是更对。",
        "body": "敏感肌抗老, 选对成分比选对浓度重要。",
        "items": [
          {"mark": "icon-circle", "title": "刺痛泛红", "desc": ""},
          {"mark": "icon-circle", "title": "干燥脱皮", "desc": ""},
          {"mark": "icon-circle", "title": "闭口爆痘", "desc": ""},
          {"mark": "icon-circle", "title": "白天反黑", "desc": ""}
        ]
      },
      "visual_description": "Four vertically arranged still-life vignettes on cream linen fabric in soft daylight: a dry flaky skin fragment, a red irritated patch, a clogged-pores close-up, a dull uneven skin-tone swatch. Clinical, editorial, no people, no faces, no text overlays, gentle and empathetic mood."
    },
    "03": {
      "template": "list",
      "background": "mod--alt-bg",
      "claim_seed_back": ["bakuchiol_replacement"],
      "text_exact": {
        "kicker": "MECHANISM · 核心机制",
        "headline": "一滴, 三道温和抗老链路",
        "summary": "3 个成分, 1 条温和链路。",
        "items": [
          {"mark": "1", "title": "Bakuchiol", "desc": "类视黄醇, 刺激仅为 A 醇的 1/10"},
          {"mark": "2", "title": "VC-IP", "desc": "油溶性维 C, 稳定不反黑"},
          {"mark": "3", "title": "Cistus", "desc": "岩玫瑰精萃, 边抗老边修护"}
        ]
      },
      "visual_description": "Three crystal-clear golden oil capsules arranged in a vertical column on a slab of raw white Cistus rock-rose, each capsule glowing softly with one hero ingredient inside, side directional warm light, shallow depth of field, no hands, no numbers, no text, ultra-clean laboratory editorial aesthetic."
    },
    "04": {
      "template": "list",
      "background": "default",
      "claim_seed_back": ["bakuchiol_replacement", "vc_ip_brightening", "cistus_resilience"],
      "text_exact": {
        "kicker": "INGREDIENTS · 成分档案",
        "headline": "三大成分, 各司其职",
        "items": [
          {"mark": "B", "title": "Bakuchiol (补骨脂酚)", "desc": "温和抗老主力, 紧致淡纹"},
          {"mark": "V", "title": "VC-IP (抗坏血酸四异棕榈酸酯)", "desc": "稳态提亮, 匀净肤色"},
          {"mark": "C", "title": "Cistus (岩玫瑰)", "desc": "屏障修护, 舒缓强韧"}
        ],
        "zero_strip": ["0 香精", "0 色素", "0 矿物油", "0 酒精"]
      },
      "visual_description": "Three botanical ingredients in a triptych flat-lay on pale linen: a sprig of fresh Bakuchiol leaves on the left, a single translucent orange VC-IP crystal in the center, a dried Cistus rock-rose flower on the right. Morning side light, editorial still-life, no text, no people, calm and clinical mood."
    },
    "05": {
      "template": "list",
      "background": "default",
      "claim_seed_back": ["light_friendly"],
      "text_exact": {
        "kicker": "USAGE · 使用场景",
        "headline": "一天 3 滴, 早晚都能用",
        "items": [
          {"mark": "时刻 1 · 晨间", "title": "化妆水后", "desc": "2 滴混合面霜"},
          {"mark": "时刻 2 · 通勤", "title": "持妆不搓泥", "desc": "避免反黑"},
          {"mark": "时刻 3 · 夜间", "title": "精华后", "desc": "3 滴按摩全脸"}
        ],
        "tip": "建议先在耳后测试, 敏肌从 1 滴开始。",
        "texture": "流动性金黄液体, 吸收不黏腻。"
      },
      "visual_description": "A serene bathroom counter at golden hour: the HKH dropper bottle beside a folded cream towel, a small ceramic dish, and a sprig of dried rose. Warm window light from the left, a single golden oil droplet suspended mid-air just above the dropper tip, lifestyle editorial, no hands, no people, no text."
    },
    "06": {
      "template": "compare",
      "background": "default",
      "claim_seed_back": ["bakuchiol_replacement", "light_friendly"],
      "text_exact": {
        "kicker": "COMPARE · 跟传统 A 醇比",
        "headline": "4 个不同",
        "rows": [
          {"label": "刺激感", "us": "几乎无", "them": "刺痛脱皮"},
          {"label": "反黑风险", "us": "极低", "them": "白天易反黑"},
          {"label": "敏肌友好", "us": "可用", "them": "不建议"},
          {"label": "日间使用", "us": "可", "them": "限夜间"}
        ],
        "badges": ["温和配方", "不致痘配方", "无动物实验"]
      },
      "visual_description": "A side-by-side split composition: on the left the golden HKH oil bottle under soft warm side light, on the right a generic retinol serum bottle with cooler harsher fluorescent light. Both centered on the same neutral surface, identical framing, no text, no labels visible, product comparison editorial."
    },
    "07": {
      "template": "closing",
      "background": "mod--alt-bg",
      "claim_seed_back": ["cistus_resilience"],
      "text_exact": {
        "quote": "抗老不必急, 像给皮肤一次深呼吸。",
        "notes": [
          {"label": "前调", "text": "清新柑橘, 唤醒"},
          {"label": "中调", "text": "玫瑰岩兰, 安神"},
          {"label": "尾调", "text": "檀香琥珀, 沉静"}
        ],
        "signature": "一滴一仪式, 4 周见变化。"
      },
      "visual_description": "A macro of a single golden oil droplet resting on a pristine white Cistus rock-rose petal. Soft diffused morning light from above, ultra-clear, ultra-minimal, evokes ritual and quiet luxury. Shallow depth of field, no text, no people, painterly and serene."
    },
    "08": {
      "template": "closing",
      "background": "default",
      "claim_seed_back": ["bakuchiol_replacement", "vc_ip_brightening", "cistus_resilience", "light_friendly"],
      "text_exact": {
        "kicker": "FAQ · 还在犹豫？",
        "headline": "这 3 个问题帮你决定",
        "qa": [
          {"q": "敏感肌真的能用吗？", "a": "配方通过温和度测试, 建议先在耳后试用。"},
          {"q": "白天能用吗？", "a": "可以, 不含光敏成分, 注意防晒即可。"},
          {"q": "多久有感觉？", "a": "4 周为一个观察期, 持续使用更明显。"}
        ],
        "badges": ["敏感肌通过测试", "胶囊锁鲜工艺", "每日仪式感"],
        "closing": "HKH · Light Edition · 4 周温和抗老 · 写给敏感肌的日常仪式"
      },
      "visual_description": "The HKH bottle centered on a low pedestal of soft cream draped fabric, surrounded by subtle golden bokeh particles. Gentle uplight from below, dark warm backdrop, premium brand-campaign closing hero shot, no text, no hands, evokes quiet confidence and trust."
    }
  }
}
```

### 3.2 JSON 字段 → HTML 元素映射

```
JSON 字段                      →  HTML 元素
────────────────────────────────────────────────────
brand.name                     →  <title>
style.palette.gold             →  :root { --gold: #C9A876; }
style.typography.header        →  .display-xl { font-family: ...; }
style.ratio                    →  .mod { min-height: <值>; }
screens.01.template="hero"     →  调用 render_template_hero()
screens.01.text_exact.headline →  <h1 class="display-xxl">...
screens.01.text_exact.tags[]   →  循环 <span class="tag-item">
screens.01.claim_seed_back[]   →  <div data-seed="bakuchiol_replacement,...">
screens.01.background          →  <div class="mod mod--hero">
```

### 3.3 JSON → prompt 拼接规则

```
[Style 前缀] = brand + style 字段拼接
  "Style: <style.photography>, <style.lighting>,
   <style.lens>, mood: <style.mood>,
   palette: <palette 4 色>, typography: <typography>,
   ratio: <style.ratio>, modifiers: <modifiers>.
   Banned: <banned 拼接>."

[Content 段] = 单屏的 visual_description 字段（绝不用 text_exact）
  "Screen 01 · hero · claim seed: <claim_seed_back 拼接>
   <visual_description 完整英文段>"

[Full Prompt] = Style 前缀 + Content 段
```

**输出**：`output/prompt_01.txt` ~ `prompt_08.txt`（8 段独立文件）

**反隐喻护栏（必须执行 · 流向级白名单）**：

> ⚠️ **本护栏禁的是"流向"（field → prompt），不是"字段"（field 本身）**。`text_exact.*` 字段在 JSON 里**正常使用**（详情页 HTML 渲染读这些字段来填 DOM），唯一禁的是它们的值被 `render.cjs` 拼到 `prompt_XX.txt` 里。

**流向级白名单**（`ALLOWED_IN_PROMPT`，只有下列字段值可以出现在 prompt 文件里）：
| 字段 | 用途 | 出现位置 |
|---|---|---|
| `claim_seed_back` | 屏 1 必含（叙事追溯标签，让模型知道本屏是"哪条 claim 的延伸"） | 每屏屏头 |
| `visual_description` | 唯一画面来源 | Content 段 |
| `template` | 屏类型标签 | 屏头 |
| `primary_image` | 屏 1 末附产品图引用 | 屏 1 末行 |

**流向级黑名单**（`text_exact.*` 任一字段值）→ 拼 prompt 时命中即 FAIL：

| 字段 | 字段值举例（绝不能进 prompt） |
|---|---|
| `kicker` / `deco_en` | "HKH · LIGHT EDITION" |
| `headline` | "维 A 之外的 4 周温和抗老" |
| `subheadline` / `body` | "敏感肌也能用的温和抗老精华" |
| `tags` / `items` / `rows` | "刺痛泛红" / "1 Bakuchiol ..." |
| `cta` / `closing` / `quote` / `signature` | "了解更多" / "HKH · Light Edition · ..." |
| `tip` / `texture` / `transition` / `summary` / `zero_strip` | "建议先在耳后测试" |
| `qa` / `notes` / `badges` | "敏感肌真的能用吗？" / "敏感肌通过测试" |

**架构落地**（与 §5.2 render.cjs 实现完全一致）：
- ✅ Content 段**只读** `screens[XX].visual_description`
- ❌ 任何 `text_exact.*` 字段值**绝对禁止**进 prompt（HTML 渲染照常用，路径完全解耦）
- ❌ "展示页"细节（cvt 词、电商字段如 `badges`）在 prompt 里也是黑名单（哪怕已经"修正过"展示页语气）
- ✅ 屏 1 必含 `Primary product reference: <primary_image>` 一行

**HKH 屏 03 实际生成示例**（对照看护栏效果）：
```
Style: high-end skincare editorial photography, macro details, soft directional warm light from upper right 45°, shallow depth of field with light bokeh, mood: clinically trustworthy + luxury, palette: warm gold #C9A876 / cream #F2E8D9 / deep brown #2A1F1A / soft taupe #8B7B6F, typography: Playfair Display, Source Han Serif SC for headers, ratio: 9:21 vertical, modifiers: magazine-grade, commercial photography, never cartoonish. Banned: emoji, cartoon, stock photo feel, 抗皱, 抗衰, 祛斑, 治愈.

Screen 03 · list · claim seed: bakuchiol_replacement
Three crystal-clear golden oil capsules arranged in a vertical column on a slab of raw white Cistus rock-rose, each capsule glowing softly with one hero ingredient inside, side directional warm light, shallow depth of field, no hands, no numbers, no text, ultra-clean laboratory editorial aesthetic.
Primary product reference: Temp/WecomSave_03051d2332b350a4b66f69a134e8e1f906.JPG
```

**与手工 prompt 对比**：
- ✅ 风格锚定、构图、元素、文字、禁忌规则全有
- ✅ HTML 改 → JSON 改 → prompt 同步改
- ⚠️ 缺"项目特定情感性描述"（如"this moment feels like a warm exhale"）
- **可达手工 prompt 80-90% 水准**（在用户认真填 style 字段的前提下）

---

## 4. 6 步自动化流程

### Step 0 · 输入与数据抽取 (AI)

**目标**：拿到 1 张产品图 + 核心文案（或 Seeds），AI 严格按照 3.1 结构生成 `brand-spec.json`。

**成功**：
- ✅ 至少 1 张产品图
- ✅ brand-spec.json 必填字段齐全（brand / style / banned / claim_seeds / screens 8 屏）
- ✅ 路由 A：用户确认文案
- ✅ 路由 B：AI 草稿 + 用户回"OK/继续"

**失败**：
- ❌ 无图 → 退出
- ❌ JSON 缺字段 → 列出缺哪几个
- ❌ 路由 B 草稿含 banned 词 → 立即删
- ❌ 路由 B 草稿与产品图明显不符 → 返工

### Step 1 · 初始化项目（脚本 `init-project.cjs`）

**目标**：建项目目录 + 复制模板 + 写 copy.md

**调用**：`node scripts/init-project.cjs <项目名>`

**操作**：
1. 创建 `Temp/<项目名>/` 目录
2. 复制 `template.html` → `index.html`
3. 复制 `tokens/theme-pilgrim-dawn.css` → `tokens/theme.css`
4. 从 brand-spec.json 抽 8 屏 text_exact → `copy.md`

**成功**：
- ✅ index.html 浏览器能打开
- ✅ copy.md 8 段文案完整
- ✅ theme.css 链接正确

**失败**：
- ❌ 模板文件缺失 → 报路径错误
- ❌ copy.md 缺段 → 标红该屏

### Step 2 · 叙事与合规校验（脚本 `validate-seeds.cjs`）

**目标**：校验 claim seed 追溯链 + 转化词拦截 + visual_description 完整性

**操作**：
1. 读 brand-spec.json 的 claim_seeds（2-4 个）
2. 校验 8 屏的 claim_seed_back 字段
3. **校验规则**：
   - 每屏必须有 ≥1 个 seed 追溯（追溯空 = FAIL）
   - 至少 3 屏追溯到同一 seed（叙事主线）
   - 屏 1 必须包含所有 4 个 seed（首屏一次性抛）
4. 校验每屏 `text_exact` 是否含有 **展示页违禁词（立即购买/领券/包邮等转化词）**
5. 校验每屏 `visual_description` 字段是否存在（缺 = Fail Fast 中断）

**成功**：
- ✅ 8 屏追溯齐全
- ✅ ≥ 3 屏追溯到主 seed
- ✅ 屏 1 含全部 4 个 seed
- ✅ 无转化词侵入

**失败**：
- ❌ 某屏追溯为空 → 标红
- ❌ 8 屏追溯分散到 8 个不同 seed → 返工
- ❌ 屏 1 不含全部 seed → 标红
- ❌ `visual_description` 缺失 → 立即中断
- ❌ `text_exact` 含转化词 → 立即中断报具体屏号+具体词

### Step 3 · 模板分配（脚本 `assign-template.cjs`）

**目标**：为 8 屏分配 4 模板中的 1 个，保证相邻不重复。

**操作**：
1. 读 brand-spec.json 的 screens[*].template 字段
2. 校验：4 模板各至少 1 次
3. 校验：相邻屏不用同模板
4. 校验：屏 1 = hero，屏 8 = closing（默认）

**成功**：
- ✅ 8 屏都有 template 字段
- ✅ 4 模板都用了
- ✅ 相邻屏无重复
- ✅ 屏 1/8 默认约束满足

**失败**：
- ❌ 某屏 template 字段缺失 → 标红
- ❌ 4 模板没用全 → 提示
- ❌ 相邻屏同模板 → 提示修改

### Step 4 · 渲染 HTML（脚本 `render.cjs` 阶段 1）

**目标**：JSON → 8 屏 HTML

**调用**：`node scripts/render.cjs <项目名>`

**操作**：
1. 读 brand-spec.json
2. 循环 8 屏，按 template 调对应 render_template_*() 函数
3. 套 25 BEM class
4. 写入 :root CSS 变量（颜色/字体/比例/弹性最小高度）
5. 输出 index.html

**Fail Fast 原则**：遇到 JSON 键值不匹配或结构缺失，脚本**立即中断报错并等待人工修复**，绝对不静默自动补全。

**25 个 BEM class**：
```
主结构 (4)  : .mod .mod--hero .mod--alt-bg .mod--dark-bg
字号 (5)    : .display-xxl .display-xl .display-lg .h1-sm .body
装饰 (4)    : .kicker .deco-en .deco-line .num
布局 (5)    : .stack .gap-1 .gap-2 .grid-2x2 .grid-2x2-item
组件 (4)    : .callout-box .tag-item .ledger .quote
dp2- (3)    : .dp2-mock .dp2-section-soft .dp2-section-dark
```

**成功**：
- ✅ 8 屏 HTML 生成
- ✅ 25 BEM class 全部就位
- ✅ `min-height` 写入 .mod（1680px 或 1280px，看 brand-spec.json style.ratio）
- ✅ font-variation-settings: "SOFT" 80 写入 display-*
- ✅ 背景至少 2 态交替

**失败（Fail Fast · 立即中断）**：
- ❌ 8 屏不全 → **立即中断**，报"screens 缺第 X 屏"
- ❌ BEM class 缺失 → **立即中断**，报"Screen XX 缺 .mod-body 容器"
- ❌ min-height 漏写 → **立即中断**，报"Screen XX .mod 缺 min-height"
- ❌ 8 屏背景全同 → **立即中断**，报"8 屏背景全为 default，无 mod--alt-bg/mod--dark-bg"
- ❌ 屏顺序错乱 → **立即中断**，报"screens 顺序缺 01/02/03/.."
- ❌ template 字段值非法（如 "unknown_template"）→ **立即中断**，报"Screen XX template 必须为 hero/list/compare/closing"
- ❌ JSON 键值不匹配（如 list 模板 items 缺少统一键）→ **立即中断**，报具体结构错误

### Step 5 · Playwright 截图与 Prompt 生成（脚本 `render.cjs` 阶段 2+3）

**目标**：HTML → PNG + HTML → prompt

**操作**：
1. 读 index.html
2. **长图**：playwright headless 截图，每屏 1 张 720px 定宽 PNG（fullPage 自动截取弹性高度）
3. **拼接**：8 张 PNG → 1 张 full_long.png
4. **prompt**：拼接 style 前缀 + screen content → 8 段 txt

**输出**：
```
output/
├── screen_01.png ~ screen_08.png    (720px 定宽，弹性高度)
├── full_long.png                     (拼接好的极长展示图)
└── prompt_01.txt ~ prompt_08.txt     (8 段生图 prompt)
```

**成功**：
- ✅ 8 张 PNG 完整
- ✅ 1 张 full_long.png 完整
- ✅ 8 段 prompt 完整
- ✅ prompt 含 style 前缀 + 屏内容 + banned 词
- ✅ **所有 PNG 字体正确加载（无系统默认字体回退）**
- ✅ **所有 PNG 图片正确显示（无空白图）**

**失败（Fail Fast）**：
- ❌ playwright 未安装 → 报 `npx playwright install` 提示并退出
- ❌ PNG 截图截到一半 → **立即中断**，不重试
- ❌ prompt 缺 style 前缀 → **立即中断**
- ❌ 字体加载超时（>5s）→ **立即中断**，报具体哪个 font-family
- ❌ 图片加载失败（404 / 403）→ **立即中断**，报具体哪个图片 URL

#### 5.1 解决竞态条件的截图机制

**风险**：Playwright 默认 DOM ready 就截图。高级电商页依赖 Web 字体（Playfair Display / Fraunces / Noto Sans SC）和高清占位图。如果不等加载完，截图会出现：
- 字体回退到系统默认（宋体 / Times）→ 排版错乱
- 图片区域一片空白 → 信息缺失

**架构解法**（render.cjs 必须实现的异步钩子）：

```javascript
// 1. 导航 + 设置视口
await page.setViewportSize({ width: 720, height: ratio === '9:21' ? 1680 : 1280 });
await page.goto(`file://${indexHtmlPath}`, { waitUntil: 'networkidle' });

// 2. 浏览器端注入：死等字体和图片加载
await page.evaluate(async () => {
  // 2.1 死等所有 @font-face 加载完成
  await document.fonts.ready;

  // 2.2 显式检查每个字体状态（font.loaded promise）
  const fontFaces = [...document.fonts.values()];
  await Promise.all(fontFaces.map(f => f.loaded));

  // 2.3 死等所有 <img> 的 complete 属性为 true
  const imgs = [...document.images];
  await Promise.all(imgs.map(img => {
    if (img.complete) return Promise.resolve();
    return new Promise((resolve, reject) => {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', () => reject(new Error(`图片加载失败: ${img.src}`)), { once: true });
    });
  }));
});

// 3. 再等 200ms 兜底（防止部分字体 fallback 切换动画）
await page.waitForTimeout(200);

// 4. 截图（取消绝对高度，截取弹性全图）
const buffer = await page.screenshot({ fullPage: true, type: 'png' });
```

**超时保护**（避免死锁）：
- `document.fonts.ready` 总超时 5s → 失败立即报超时
- 单张图片加载超时 3s → 失败立即报哪个图
- 全部超时仍失败 → 中断 render.cjs，**不静默重试**

#### 5.2 Prompt 纯净拼接公式

**3 段式拼接**：

```
[1/3] Style 前缀（从 brand.spec.style 抽 · 必含）
[2/3] Content 段（从 screens.XX.visual_description 抽 · 唯一来源）
[3/3] Banned 收尾（从 banned 抽 · 防止回流 banned 词）
```

**反隐喻护栏（render.cjs 必须硬编码 · 流向级禁用 · 字段级白名单）**：

> ⚠️ **重要澄清：本护栏禁的是"流向"（field → prompt），不是"字段"（field 本身）。**
> - `text_exact.*` 字段在 `text_exact` 节点里**正常使用**（详情页 HTML 渲染、UI 标签）
> - 唯一禁止的：**任何 `text_exact.*` 字段值被读出来写入 prompt 文件**
> - 例：`render.cjs` 读 `screens.01.text_exact.headline` 来渲染 `<h1>` 标签 ✅；`render.cjs` 把 `headline` 拼到 `prompt_01.txt` 里 ❌

```javascript
// Prompt 拼接白名单（流向级白名单 · 字段级精确）
// 只有下列字段值可以出现在 prompt_XX.txt 里
const ALLOWED_IN_PROMPT = new Set([
  'claim_seed_back',       // 屏 1 强制包含，其余可选（叙事追溯标签）
  'visual_description',    // 唯一画面来源
  'template',              // 屏类型标签（hero/list/compare/closing）
  'primary_image'          // 屏 1 末附的产品图引用
]);

// render.cjs 拼 prompt 时的硬编码检查
function buildPrompt(screen) {
  const out = [buildStylePrefix(), ''];

  // 1. 屏头标签
  out.push(`Screen ${screen.id} · ${screen.template} · claim seed: ${(screen.claim_seed_back || []).join(', ')}`);

  // 2. Content 段：唯一来源 visual_description
  if (!screen.visual_description) {
    throw new Error(`Screen ${screen.id} 缺 visual_description · fix: 在 screens.${screen.id} 补一段 50-120 词的英文画面描述`);
  }
  out.push(screen.visual_description);

  // 3. 屏 1 追加产品图引用
  if (screen.id === '01' || screen.id === '1') {
    out.push(`Primary product reference: ${screen._primary_image || ''}`);
  }

  // 4. Banned 收尾
  out.push('');
  out.push(`Banned: ${banned.join(', ')}.`);

  return out.join('\n');
}
```

> **流向上唯一例外**：`render.cjs` 在 Step 4 渲染 HTML 时**不受本护栏约束**——HTML 渲染是另一条代码路径（`buildHtmlElement()`），它会读 `text_exact.*` 全部字段来填 DOM。两路径完全解耦，不共享数据。
>
> 任何 `text_exact.*` 字段值被 `render.cjs` 写入 `prompt_XX.txt` → **立即中断**，不静默剔除。

**Style 前缀模板**：
```
Style: <style.photography>, <style.lighting>, <style.lens>,
mood: <style.mood>, palette: <palette 4 色英文>,
typography: <style.typography.header> for headers, <style.typography.body> for body,
ratio: <style.ratio> vertical, modifiers: <style.modifiers 拼接>.
Banned: <banned 拼接>.
```

**Content 段模板**（**所有 4 种 template 统一走 visual_description，不再按 template 分支**）：
```
Screen <id> · <template> · claim seed: <claim_seed_back 拼接>
<visual_description 完整英文段，一字不改原样输出>
```

**屏 1 额外追加**（仅屏 1）：
```
Primary product reference: <primary_image>
```

**HKH 屏 03 prompt_03.txt 实际产物示例**：
```
Style: high-end skincare editorial photography, macro details, soft directional warm light from upper right 45°, shallow depth of field with light bokeh, mood: clinically trustworthy + luxury, palette: warm gold #C9A876 / cream #F2E8D9 / deep brown #2A1F1A / soft taupe #8B7B6F, typography: Playfair Display, Source Han Serif SC for headers, Inter, PingFang SC for body, ratio: 9:21 vertical, modifiers: magazine-grade, commercial photography, never cartoonish. Banned: emoji, cartoon, stock photo feel, 抗皱, 抗衰, 祛斑, 治愈.

Screen 03 · list · claim seed: bakuchiol_replacement
Three crystal-clear golden oil capsules arranged in a vertical column on a slab of raw white Cistus rock-rose, each capsule glowing softly with one hero ingredient inside, side directional warm light, shallow depth of field, no hands, no numbers, no text, ultra-clean laboratory editorial aesthetic.
```

**prompt 成功标准**：
- ✅ 8 段 txt 全部生成
- ✅ 每段含 Style 前缀（15 行内）
- ✅ 每段含屏 Content（来自 visual_description，5-15 行英文）
- ✅ 每段末含 Banned 收尾（1 行）
- ✅ 屏 1 必含 `Primary product reference: <primary_image>`
- ✅ **prompt 内不出现任何 `text_exact.*` 字段值**（流向级护栏检测 · HTML 渲染不受影响）

**prompt 失败标准**（Fail Fast）：
- ❌ 缺 Style 前缀 → 立即中断
- ❌ 缺 Banned 收尾 → 立即中断
- ❌ **缺 `visual_description` 字段** → 立即中断报哪个屏缺（§3.1.0 护栏）
- ❌ **`visual_description` 含中文**（正则 `[\u4e00-\u9fa5]`）→ 立即中断报具体字符位置
- ❌ **`visual_description` 命中 banned 词**（含主题 bundle.banned + style.banned）→ 立即中断报具体词
- ❌ **`text_exact.*` 字段值被意外写入 prompt 文件**（render.cjs 流向级护栏自检）→ 立即中断报哪个字段名 + 哪段 prompt 被污染
- ❌ **`text_exact.*` 字段值命中 §3.1.0.a 展示页转化词**（`validate-seeds.cjs` 扫）→ 立即中断报具体屏号 + 具体词
- ❌ visual_description 长度 < 30 词或 > 200 词 → 立即中断（信息不足或模型失焦）

### Step 6 · 自动化终检（脚本 `self-check.cjs` · 最后一步）

**目标**：12 项自动化检测 + revision routing

**调用**：`node scripts/self-check.cjs <项目名>`

**12 项检测**（v3.1 在 v3 11 项基础上新增 #1 字数防爆）：

```
1.  字数上限防爆（新增）：主标 > 18字，副标 > 24字 → FAIL（强制删减或降级字号，防破版）
2.  反转化词扫荡（新增）：text_exact 含有"立即购买/加购"等电商催促词 → FAIL（改写为展示页优雅语气）
3.  Prompt 污染检测（新增）：扫描 Prompt 产物，若含有任何中文或修辞 → FAIL
4.  无 emoji 字符
5.  无 <br> 后的 1-2 字孤儿断行
6.  无 <script> 标签注入
7.  无 @keyframes / animation 动效
8.  屏背景至少 2 态交替
9.  Claim seed 8 屏追溯完整
10. JSON 必填字段齐全
11. 字体正确加载无回退
12. 弹性高度 .mod { min-height: 1680px } 生效，未锁死 aspect-ratio
```

**revision routing**（FAIL → 最小修法）：
```
FAIL #1  字数超标  → 删减文案 / 降级字号
FAIL #2  转化词    → 改写为展示页语气（"了解更多" 替代 "立即查看"；"HKH · Light Edition · ..." 替代 "立即购买"）
FAIL #3  prompt 污染 → 检查 render.cjs 是否误读 text_exact.* 写入 prompt
FAIL #4  emoji    → 删 emoji / 改 .icon-circle
FAIL #5  孤儿字    → 调 <br> 位置 / 降字号
FAIL #6  script   → 删 <script>
FAIL #7  animation → 删 @keyframes / animation
FAIL #8  背景      → 加 mod--alt-bg
FAIL #9  seed 追溯 → 在 brand-spec.json 补 claim_seed_back
FAIL #10 JSON 字段 → 补缺字段
FAIL #11 字体回退  → 修 font-family 加载链 / 加 font-display: swap
FAIL #12 弹性高度  → .mod 补 min-height，移除 aspect-ratio
```

**成功**：12/12 PASS + self-check-report.md 生成

**失败**：按 revision routing 最小修改

---

## 5. 8 屏叙事结构（v3.1 推荐标准）

| 屏号 | 叙事定位 | 映射模板 | 核心动作 |
| --- | --- | --- | --- |
| **01** | 品牌身份 | `hero` | 抛出所有 4 个 Claim Seeds，建立高奢定调。 |
| **02** | 痛点共鸣 | `list` | 用 `icon-circle` 的 items 陈列 4 大痛点。 |
| **03** | 核心机制 | `list` | 用 `num` 的 items 拆解生效原理（如 3 道链路）。 |
| **04** | 成分档案 | `list` | 用字母 Initial (如 B/V/C) 拆解核心配方。 |
| **05** | 真实场景 | `list` | 描述早、中、晚的使用时刻与肤感。 |
| **06** | 真实对比 | `compare` | "我们"与"传统竞品"的 4 维度优劣对比卡片。 |
| **07** | 仪式感 | `closing` | 留白极简排版，带出香调或质地特写。 |
| **08** | 转化收尾 | `closing` | FAQ 答疑，给出优雅的品牌落款（代替购买按钮）。 |

**推荐叙事映射表**：

```
屏 1  · 品牌身份
       模板: hero
       4 claim seed 全部抛
       claim_seed_back: [all_4]

屏 2  · 痛点共鸣
       模板: list (4 项)
       追溯到 light_friendly（敏肌痛点）
       claim_seed_back: [light_friendly]

屏 3  · 核心机制
       模板: list (3 步骤)
       追溯到 bakuchiol_replacement
       claim_seed_back: [bakuchiol_replacement]

屏 4  · 成分档案
       模板: list (3 成分)
       追溯到 3 个 seed（多线展开）
       claim_seed_back: [bakuchiol, vc_ip, cistus]

屏 5  · 真实场景
       模板: list (3 时刻)
       追溯到 light_friendly
       claim_seed_back: [light_friendly]

屏 6  · 真实对比
       模板: compare (4 行)
       追溯到 bakuchiol + light_friendly
       claim_seed_back: [bakuchiol, light_friendly]

屏 7  · 仪式感
       模板: closing (3 香调)
       追溯到 cistus_resilience
       claim_seed_back: [cistus_resilience]

屏 8  · 转化收尾
       模板: closing (3 答疑 + CTA)
       4 seed 全部回顾
       claim_seed_back: [all_4]
```

---

## 6. 核心目录与输出物交付

```text
Temp/<Project_Name>/
├── index.html                   # 渲染完的展示页 HTML
├── copy.md                      # 8 段文案母版（供人工审校）
├── tokens/theme.css             # 朝圣黎明 (唯一默认主题)
└── output/
    ├── screen_01.png ~ 08.png   # 720px 定宽的无缝切片
    ├── full_long.png            # 拼接好的极长展示图
    └── prompt_01.txt ~ 08.txt   # 干净、隔离、解耦的生图咒语
```

## 7. 4 个核心脚本

```
scripts/
├── init-project.cjs       # Step 1  建项目 + 复制模板 + 写 copy.md
├── validate-seeds.cjs     # Step 2  校验 claim seed 追溯链 + 转化词 + visual_description 完整性
├── assign-template.cjs    # Step 3  校验模板分配（4 各 1 + 相邻不重复）
├── render.cjs             # Step 4+5  渲染 HTML + 截 PNG + 拼 prompt
└── self-check.cjs         # Step 6  12 项自动化检测
```

**render.cjs 是核心**（~200 行代码），3 段式：
1. 读 brand-spec.json
2. 循环 8 屏，套 4 个模板函数（hero / list / compare / closing）
3. 输出 HTML + 调 playwright 截图 + 拼 prompt

**总耗时**：~10 秒（脚本主导，AI 退到 Step 0/2/3 的校验辅助）

---

## 8. 验收标准（v3.1 完成定义）

v3.1 算完成必须满足：
- [ ] 6 步流程独立跑通（脚本一键 + AI 校验）
- [ ] 8 屏 HTML 在浏览器打开流畅
- [ ] 8 屏 720px 定宽 PNG 完整（弹性高度，非锁死 9:21）
- [ ] 1 张 full_long.png 完整
- [ ] 8 段 prompt 完整且含 style 前缀
- [ ] 12 项自动化自检全 PASS
- [ ] 25 个 BEM class 全用上
- [ ] 4 个模板各至少 1 次
- [ ] 1 个主题（朝圣黎明）作为默认
- [ ] HKH 范例项目跑通
- [ ] brand-spec.json 驱动一切
- [ ] list 模板 items 键值统一（{mark, title, desc}）
- [ ] 弹性高度策略生效（未锁死 aspect-ratio）
- [ ] 文案/视觉解耦护栏生效（visual_description 缺 = 中断）
- [ ] 展示页转化词拦截生效

---

## 9. 决策锁定清单

- ✅ 弹性高度策略（min-height 替代 aspect-ratio，解决 9:21 高度死锁）
- ✅ 比例 9:21（720×1680 min-height）默认 / 9:16（720×1280 min-height）可选
- ✅ 屏数 8
- ✅ 主题 1 个（朝圣黎明）
- ✅ claim seed 2-4 个
- ✅ 脚本化 70%（4/6 步）
- ✅ 自检放最后（Step 6）
- ✅ 4 维定位砍掉（用 claim seed + 文案）
- ✅ brand-spec.json 替代 brand-spec.md
- ✅ prompt 双层结构（JSON 字段 + 屏内容拼接）
- ✅ HKH 作为 v3.1 范例项目
- ✅ **Fail Fast 原则**：脚本不静默补全，缺什么立即中断报错
- ✅ 比例切换在 brand-spec.json 的 style.ratio 字段控制
- ✅ **Playwright 竞态条件防护**：死等字体 + 图片加载后才截图，不静默重试
- ✅ **Prompt 3 段式拼接**（Style 前缀 + Content 段 + Banned 收尾）
- ✅ **文案/视觉解耦（反隐喻陷阱）**：详见 §3.1.0 ——
  - `screens[*]` 强制并列 `text_exact`（人） + `visual_description`（机器）双字段
  - 缺 `visual_description` = Fail Fast 中断
  - 拼 prompt 时**流向级白名单**：`ALLOWED_IN_PROMPT = ['claim_seed_back', 'visual_description', 'template', 'primary_image']`（屏 1）
  - 拼 prompt 时**流向级黑名单**：所有 `text_exact.*` 字段值（HTML 渲染路径**不受影响**，两路径解耦）
  - HKH 8 屏已补 `visual_description` 范例
- ✅ **展示页定位（非电商详情页）**：详见 §3.1.0.a ——
  - v3.1 做的是「Showcase Page / 品牌展示页」，不是「E-commerce Detail / 电商详情页」
  - 转化词黑名单（硬禁用）：立即购买/立即下单/立即查看/立即抢购/加购/加入购物车/领券/优惠券/满减/限时/倒计时/包邮/顺丰包邮/7 天无理由/库存/仅剩/即将售罄/正品保证/假一赔十
  - 展示页 cta 白名单（语气）：了解更多 / 查看详情 / 继续探索 / 探索工艺 / 阅读完整故事 / 关注品牌 / 访问官网
  - HKH 已修正：屏 01 cta "立即查看" → "了解更多"；屏 08 改品牌落款
  - 落地：Step 2 `validate-seeds.cjs` 加扫转化词 → 立即中断；Step 6 `self-check.cjs` 加 #2 项全扫
  - 例外：若用户明确要做电商详情页 → 切回 v2 skill 路径，不混用 v3.1
- ✅ **List 数据结构多态陷阱修复**：所有 `list` 模板的 `items` 统一键值对 `{mark, title, desc}`
- ✅ **Route B AI 幻觉合规铁律**：绝对禁止捏造成分/专利/临床数据；禁止医疗词
- ✅ **字数防爆**：自检 #1 项，主标 > 18 字 / 副标 > 24 字 → FAIL 并降级

---

## 10. 版本历史

| 版本 | 关键变更 | 触发 |
|---|---|---|
| v0.5.4.1 | v2 完整版（48 BEM + 17 自检 + 8 步 3 批） | 2026-06-14 |
| v3 draft | JSON 驱动 + 砍 50% + 3 种输出 | 用户提出 v3 |
| **v3.1** | **弹性高度修复 + 多态数据修复 + Route B 合规加固 + 字数防爆 + 12 项自检** | **用户要求升级** |
