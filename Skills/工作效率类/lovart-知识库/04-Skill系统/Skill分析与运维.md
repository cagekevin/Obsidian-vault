## 版本历史
- 保留最近 5-10 个版本，更旧的自动归档或删除
- 每个版本可查看变更记录和回滚

## 更新对运行中任务的影响
- **快照机制**：正在进行的生成任务锁定调用时的版本
- 当前任务完成后才应用新版本
- 不中断正在运行的工作流

## 使用统计 API
```http
GET /api/v1/skills/{id}/analytics/invocations?range=30d
GET /api/v1/skills/{id}/analytics/version-comparison?versions=v1.0,v1.1
```

返回数据：
- 调用次数（invocations）
- 成功率（success_rate）
- 平均延迟（avg_latency_ms）
- 用户评分（user_rating）

## 异常检测
自动检测成功率骤降等异常，给出可能原因和建议操作

## 成本分析
| 成本项 | 说明 |
|-------|------|
| 生成成本 | 按调用次数 × 单价 |
| 存储成本 | 参考图 + 历史输出 |
| 计算成本 | GPU 使用时间 |

## 第三方集成
监控：Datadog、Grafana、阿里云监控
告警：Slack、企业微信、钉钉
BI：Tableau、Power BI、Metabase

## 导出格式
CSV（原始数据）、JSON（结构化）、PDF（可视化报告）、Webhook（实时事件流）
