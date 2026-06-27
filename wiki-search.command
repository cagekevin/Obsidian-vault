#!/bin/bash
# wiki-search.command — 双击运行，在 Obsidian 中搜索 Wiki
# 需要 obsidian-local-rest-api 插件（已安装）

set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 弹窗输入问题
QUERY=$(osascript -e 'Tell application "System Events" to display dialog "Wiki 搜索" default answer "" with title "🔍" buttons {"取消", "搜索"} default button 2' -e 'text returned of result' 2>/dev/null || echo "")

if [ -z "$QUERY" ]; then
  exit 0
fi

# 启动 ollama（如果需要）
if ! curl -fsS --max-time 1 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  ollama serve &>/dev/null &
  sleep 2
fi

# 跑检索
RESULT=$(python3 "$VAULT_DIR/scripts/retrieve.py" "$QUERY" --top 5 2>/dev/null)

# 解析结果生成 Markdown
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
OUTPUT="# Wiki 搜索结果：${QUERY}\n> 搜索时间：${TIMESTAMP}\n\n"

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('candidates', []):
    path = c.get('page_path', '').replace('\\\\', '/')
    score = c.get('rerank_score', 0)
    snippet = c.get('snippet', '')
    print(f'### [{score:.2f}] {path}')
    print()
    print(f'{snippet}')
    print()
" | while IFS= read -r line; do
  OUTPUT+="$line\n"
done

# 写入临时笔记
NOTE_PATH="$VAULT_DIR/Wiki搜索结果.md"
echo -e "$OUTPUT" > "$NOTE_PATH"

# 在 Obsidian 中打开（通过 URL scheme）
open "obsidian://open?vault=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$VAULT_DIR'))")&file=Wiki搜索结果"
