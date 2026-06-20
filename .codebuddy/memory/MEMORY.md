# 长期记忆

> 只存 Context/ 五件套覆盖不到的实操细节。
> Context/（profile/goals/brand/style/schema）已定义了身份、目标、风格、工作流，这里不重复。

---

## 技术操作规范

- 改 JSON 字段必须用 replace_in_file 精确替换，禁止用 sed 全局替换
- 改完关键字段用 python 加载 JSON 验证
- 看到错误先分析根因再修复，不要跳过
- 不要"看到我"出错了还继续执行"完整流程"，要先停下来修复
- **做任何判断前必须先查相关文档确认**，不能凭记忆回答。即使用户说"先不要看文件"，也要先说明需要查文档再回答

---

## 环境配置

- Python 包管理使用 `uv`，命令格式 `uv pip install <包名>`
- 记录在 CLAUDE.md 和 README.md 中

---

## 项目路径记录

### HKH 皮卡斯 03 版本
- 皮克斯 3D 动画广告，112 秒，西班牙语旁白
- 路径：/Users/kevin/Documents/AgentSpace/1_Active/HKH皮卡斯03版本/
- 主文档：story.md（11 个镜头）

---

## Obsidian 同步配置备忘

- 同步方式：GitHub + Obsidian Git 插件自动同步
- .gitignore 中 .obsidian/ 只忽略 workspace.json 和 cache
- 插件配置已改为每 10 分钟自动 commit + push，启动时自动 pull
