# scripts/instructions.md

## 这是什么

Wiki 底层脚本，支持检索、索引、锁定、地址分配等机制。**AI 不直接操作这些脚本，按 Wiki skills 的指引调用。**

## 脚本清单

| 脚本 | 用途 | 调用方式 |
|------|------|---------|
| `allocate-address.sh` | DragonScale 地址分配 | `bash scripts/allocate-address.sh`（分配）/ `--peek`（查看下一个）/ `--rebuild`（重建） |
| `wiki-lock.sh` | 文件级写锁 | `bash scripts/wiki-lock.sh acquire <path>` / `release <path>` |
| `wiki-mode.py` | 文件路径路由 | `python scripts/wiki-mode.py route <type> "<name>"` / `get` / `set <mode>` |
| `detect-transport.sh` | 传输方式检测 | `bash scripts/detect-transport.sh` |
| `retrieve.py` | BM25 检索 | `python scripts/retrieve.py "<query>" --top 5` |
| `bm25-index.py` | BM25 索引构建 | `python scripts/bm25-index.py build` |
| `contextual-prefix.py` | 分块 + 上下文前缀 | `python scripts/contextual-prefix.py --all` |
| `rerank.py` | 语义重排（需 ollama） | 被 retrieve.py 自动调用 |
| `tiling-check.py` | 语义查重（需 ollama） | `python scripts/tiling-check.py --report <path>` |
| `boundary-score.py` | 边界评分 | 辅助工具 |
| `baseline-v16.py` / `benchmark-runner.py` | 检索基准测试 | 测试用 |

## 重建索引

新增 Wiki 页面后，跑 `bash bin/setup-retrieve.sh --no-llm` 重建 BM25 索引。
