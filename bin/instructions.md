# bin/instructions.md

## 这是什么

环境初始化脚本，首次搭建或重置 vault 机制时使用。

## 脚本清单

| 脚本 | 用途 | 何时用 |
|------|------|--------|
| `setup-vault.sh` | 完整 vault 初始化 | 首次搭建 |
| `setup-mode.sh` | 设置文件路径模式 | 切换 Wiki 组织方式（generic/lyt/para/zettelkasten） |
| `setup-retrieve.sh` | 检索管道初始化 | 建/重建 BM25 索引 |
| `setup-dragonscale.sh` | DragonScale 机制初始化 | 启用地址分配 |
| `setup-multi-agent.sh` | 多 agent 环境 | 多 agent 协作时 |

## 常用操作

```bash
# 重建检索索引
bash bin/setup-retrieve.sh --no-llm

# 切换 Wiki 模式
bash bin/setup-mode.sh --mode generic
```
