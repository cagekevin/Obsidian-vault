# 电商主图 Theme Bundle 库 — 索引（单一数据源）

每个 Theme Bundle 独立存放于 `theme-bundles/` 目录下。**其他文件引用此索引**，禁止在别处重复罗列。

---
---

## Theme Bundles 清单

| 引用ID | 文件名 | 风格说明 | 适用场景 |
|--------|--------|---------|---------|
| [Theme_院线高保湿] | `theme-bundles/院线高保湿.md` | 蓝白科技风 | 保湿/修复类 |
| [Theme_草本防炸毛] | `theme-bundles/草本防炸毛.md` | 绿白自然风 | 草本/植物类 |
| [Theme_奢养金砖] | `theme-bundles/奢养金砖.md` | 黑金/香槟金风 | 奢养/抗老类 |
| [Theme_清爽医疗红白风] | `theme-bundles/清爽医疗红白风.md` | 红白渐变 + 医疗十字 | 美白/医用类 |
| [Theme_Luxury_GoldCapsule] | `theme-bundles/Luxury_GoldCapsule.md` | 奢华金棕养肤风 | 胶囊/精华油类 |
| [Theme_纯净极简灰白风] | `theme-bundles/纯净极简灰白风.md` | 灰白极简风 | 清洁/基础护肤类 |
| [Theme_淡蓝白金棕_护发精油风] | `theme-bundles/淡蓝白金棕_护发精油风.md` | 淡蓝白天空渐变 + 山茶花造景 | 护发精油类 |
| [Theme_金棕奢养_双圆标版] | `theme-bundles/金棕奢养_双圆标版.md` | 暖金香槟渐变 + 双圆标 | 奢养面霜/洁面类 |
| [Theme_米白奶油_身体乳美白风] | `theme-bundles/米白奶油_身体乳美白风.md` | 米白奶油渐变 + 白玫瑰造景 | 身体乳/美白类 |
| [Theme_米金茶花_卸妆风] | `theme-bundles/米金茶花_卸妆风.md` | 米白乳白渐变 + 茶花造景 | 卸妆类 |
| [Theme_米金奢养_发膜清单风] | `theme-bundles/米金奢养_发膜清单风.md` | 米金渐变 + 垂直打钩清单 | 发膜/密集护理类 |
| [Theme_清新粉金科技风] | `theme-bundles/清新粉金科技风.md` | 粉金科技风 | 彩妆/科技感类 |
| [Theme_清新橘橙活力风] | `theme-bundles/清新橘橙活力风.md` | 橘橙活力风 | 维C/活力类 |
| [Theme_清新绿白_内衣清洁风] | `theme-bundles/清新绿白_内衣清洁风.md` | 清新绿白渐变 + 白玫瑰造景 | 内衣/衣物清洁类 |
| [Theme_清新绿白自然风] | `theme-bundles/清新绿白自然风.md` | 绿白自然风 | 植物/天然类 |
| [Theme_奢华黑金风] | `theme-bundles/奢华黑金风.md` | 黑金奢华风 | 高端/尊享类 |
| [Theme_深棕金岩石_蛋白霜风] | `theme-bundles/深棕金岩石_蛋白霜风.md` | 深棕金渐变 + 岩石造景 + 双徽章 | 蛋白霜/面霜类 |
| [Theme_婷美烟酰胺单瓶] | `theme-bundles/婷美烟酰胺单瓶.md` | 金棕暖调 + 胶囊散落 + 白色清单卡片 | 精华/胶囊类 |
| [Theme_婷美烟酰胺红白模板] | `theme-bundles/婷美烟酰胺红白模板.md` | 红白渐变 + 医疗十字 + 打钩清单 | 美白/精华类 |
| [Theme_医美金棕数据风] | `theme-bundles/医美金棕数据风.md` | 金棕渐变 + 数据卡片 + 双圆徽章 | 美白/功效数据类 |
| [Theme_优雅蓝紫科技风] | `theme-bundles/优雅蓝紫科技风.md` | 蓝紫科技风 | 科技/抗老类 |
| [Theme_尊贵金棕养肤风] | `theme-bundles/尊贵金棕养肤风.md` | 暖米到深棕渐变 + 金棕字效 | 奢养面霜/精华类 |

---

## Bundle 生命周期管理（How to Do）

本索引是唯一数据源。任何增删改名必须同步更新此表，否则 Phase 3 加载会遗漏或报错。

### 如何新增一个 Bundle
1. 在 `theme-bundles/` 下新建 `.md` 文件
2. 文件首行为 `### [Theme_命名]（简要风格描述）`
3. 写入 6 个字段：Environment Palette / Typography Style / Spatial Framework / Sticker Snippet / Checklist Snippet / Banner Snippet
4. **在全量索引表中新增一行**
5. 确认 `ecommerce-image.md` 中无硬编码旧名（已改为引用本索引，一般无需改动）

### 如何删除一个 Bundle
1. 删除 `theme-bundles/` 下对应的 `.md` 文件
2. **在全量索引表中删掉对应行**
3. 确认无其他 Bundle 文件内引用被删除的 `[Theme_xxx]`

### 如何重命名一个 Bundle
1. 修改 `theme-bundles/` 下对应 `.md` 的文件名
2. 修改文件内首行 `### [Theme_新命名]`
3. **在全量索引表中更新"引用ID"和"文件名"两列**
4. 搜索全仓库 `[Theme_旧命名]`，替换为 `[Theme_新命名]`

### 验证清单
- [ ] `theme-bundles/` 目录下文件数量 = 索引表行数
- [ ] 每个 Bundle 文件首行的 `### [Theme_xxx]` 与索引表的引用ID一致
- [ ] 无任何文件残留引用已删除的旧 Theme 名
