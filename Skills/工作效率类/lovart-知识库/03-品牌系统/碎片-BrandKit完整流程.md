# Lovart 拼图碎片 — Brand Kit 完整创建流程

## Brand Kit vs Skill 的关系

- **Brand Kit** = 品牌数据存储（颜色/字体/Logo/指南）
- **Skill** = 创作模板（引用 Brand Kit + 提示词模板 + 变量）
- 两者可组合使用：Skill 引用 Brand Kit 的数据来自动填充品牌规范

## HKH Brand Kit 创建 6 步流程

### 第一步：信息收集
收集 HKH 的所有品牌资产：Logo 文件（主/反白/单色/图标）、现有产品图、品牌色值、字体文件、过往设计案例

### 第二步：创建品牌数据库
上传所有品牌资产到平台，系统建立结构化索引

### 第三步：数字品牌规范
在主控台设置各项参数。

### 第四步：配置字体的排版规则
字号层级：H1 48px Bold → H2 32px SemiBold → H3 24px → 正文 16px → 注释 12px
行高 1.5 倍，段间距 1 倍字号

### 第五步：配置视觉风格指南
摄影风格（色调/光线/背景）、插图风格（几何线条/扁平化）

### 第六步：配置品牌语调
语言风格、情感调性、禁用词汇

## Brand Kit 文件结构

```
HKH_Brand_Kit/
├── config.json              # 品牌基础信息
├── logos/                   # Logo 文件
│   ├── primary.png
│   ├── white.png
│   ├── black.png
│   └── icon.png
├── colors/palette.json      # 颜色代码
├── typography/fonts.json    # 字体配置
├── guidelines/
│   ├── photography.md
│   ├── illustration.md
│   └── tone.md
└── templates/               # 预设模板
    ├── social/
    ├── print/
    └── web/
```

## 调用方式

方式一：直接引用
```
使用 HKH 品牌套件生成一张 LinkedIn 封面图
```

方式二：Brand Kit + Skill 组合
```
用 HKH-brand-skill 生成春季招聘海报
```

## Skill 配置文件格式（引用 Brand Kit）

```yaml
skill_name: HKH Brand Skill
trigger_word: hkh-brand
brand_kit_id: hkh_2024

parameters:
  colors:
    primary: "#E53935"
    secondary: "#1A1A1A"
  fonts:
    heading: "Inter"
    body: "Inter"
  logo:
    primary: "{{brand_kit.logos.primary}}"
    safe_space: "25%"

prompt_template: |
  为 HKH 品牌生成{{content_type}}，
  使用品牌主色 {{colors.primary}} 作为强调色，
  字体使用 {{fonts.heading}}，
  风格要求：{{style_keywords}}，
  内容：{{content}}
```
