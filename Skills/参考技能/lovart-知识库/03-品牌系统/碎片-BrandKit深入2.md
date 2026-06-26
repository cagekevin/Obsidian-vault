# Lovart 拼图碎片 — Brand Kit 深入：API/版本/导出

## API 管理（完整 REST API）
- 创建：`POST /api/v3/brand-kits`
- 更新：`PATCH /api/v3/brand-kits/{kit_id}`
- 上传资产：`POST /api/v3/brand-kits/{kit_id}/assets`（Logo/颜色/字体/指南）
- 查询：`GET /api/v3/brand-kits/{kit_id}`
- 列表：`GET /api/v3/brand-kits`
- 删除：`DELETE /api/v3/brand-kits/{kit_id}`
- SDK：Node.js/Python

## 版本管理（变体聚类）
- 不是传统版本号，而是变体（variants）
- 每个变体有时间限定（valid_from / valid_until）
- 可创建季节性变体（spring_2024 / summer_2024 等）
- 历史引用仍可用

## 多品牌切换
- Workspace 隔离：不同工作空间管理不同品牌
- 显式指定：`brand_kit_id` 参数
- 请求头：`X-Default-Brand-Kit`
- 运行时切换：替换 kit_id 即可全局更新风格

## 导出导入
**导出格式：** full_package（完整包）、pdf_guide（指南）、json_config（配置）
**导出内容：**
```
morning-light-brand-kit.zip
├── assets/
│   ├── logos/ (svg + png 多倍率)
│   ├── colors/ (ase + css变量)
│   └── fonts/ (字体文件 + 授权)
├── templates/ (社交/名片/PPT模板)
├── brand-guidelines.pdf
└── brand-kit-config.json  ← 可导入
```

**导入来源：** Figma / Adobe CC / Sketch / Canva / 手动 JSON

## Skill vs Brand Kit 对比

| 特性 | Skill | Brand Kit |
|------|-------|-----------|
| 核心作用 | 定义生成规则和模板 | 定义品牌视觉资产 |
| API 管理 | ✅ 完整 REST | ✅ 完整 REST |
| 版本控制 | 版本号+回滚 | 变体聚类+时间限定 |
| 导出导入 | ✅ JSON | ✅ JSON+资产包 |
| 联合使用 | Skill 引用 brand_kit_id 作为约束条件 |
