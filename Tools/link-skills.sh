#!/usr/bin/env bash
set -euo pipefail

# 扫描 skills/ 下所有 S*/W* 技能文件夹，软链接到 ~/.claude/skills/
# 让 Claude CLI 本地直接使用 /S1、/W1 等斜杠命令

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.claude/skills"

# 如果 ~/.claude/skills 是指向本仓库的软链接，拒绝污染工作副本
if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST" 2>/dev/null || readlink "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST 是指向本仓库的软链接 ($resolved)。" >&2
      echo "请先删除它 (rm \"$DEST\")，再重新运行本脚本。" >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

# 全递归扫描，匹配 S1-xxx/W1-xxx 格式的文件夹
find "$REPO/skills" -type d -maxdepth 5 | while IFS= read -r dir; do
  fname="$(basename "$dir")"

  # 只处理有编号前缀的技能目录
  if ! echo "$fname" | grep -qE '^[SW][0-9]+-'; then
    continue
  fi

  # 排除未发布桶
  case "$(echo "$dir" | sed "s|$REPO/skills/||")" in
    */开发中技能/*|*/个人专用类/*|*/deprecated/*) continue ;;
  esac

  # 检查主文件是否存在
  main_file="$dir/$fname.md"
  if [ ! -f "$main_file" ]; then
    echo "  ⚠ $fname — 缺少主文件，跳过"
    continue
  fi

  target="$DEST/$fname"
  [ -e "$target" ] && [ ! -L "$target" ] && rm -rf "$target"
  ln -sfn "$dir" "$target"
  echo "linked $fname -> $dir"
done

echo ""
echo "完成。Claude CLI 现在可以使用以下斜杠命令："
find "$DEST" -maxdepth 1 -type l | sort | while read -r link; do
  echo "  /$(basename "$link")"
done
