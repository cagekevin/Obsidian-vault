## 多触发词
支持多个触发词，用 `/` 分隔或通配符
- `hkh-product` 和 `hkh-social` 可以同时存在
- 触发词冲突时，系统根据上下文优先匹配

## Skill 嵌套与组合
通过 workflow 或 common skill 机制实现：
```
HKH 品牌主控 Skill
  ├─ hkh-background-skill → 生成背景图层
  ├─ hkh-product-skill    → 生成产品主体  
  ├─ hkh-text-skill       → 生成文字排版
  └─ hkh-effects-skill    → 添加光影效果
      输出：合成后的最终图像
```

**继承机制**：子 Skill 可通过 `parent_skill` 字段继承主 Skill 配置
```python
{
    "name": "HKH Product",
    "trigger_word": "hkh-product",
    "parent_skill": "hkh-master",   # 继承主 Skill
    "scene": "product"
}
```

## API 管理
```http
# 创建
POST /api/v1/skills
# 版本管理
POST /api/v1/skills/{id}/versions
# 回滚
POST /api/v1/skills/{id}/rollback  {"to_version": "1.0.0"}
# 获取版本历史
GET /api/v1/skills/{id}/versions
```

## Skill Pipeline 实际案例
用户输入一句话 → 自动完成全套品牌物料：
```
"为 HKH 春季发布会生成营销物料"
→ 调用 hkh-master-skill（主控）
→ 并行调用：hkh-poster / hkh-social / hkh-ppt
→ brand-compliance-skill 检查
→ 打包输出
→ 总耗时 ~30 秒
```
