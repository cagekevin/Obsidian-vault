#!/bin/bash
# 扫描 skills/ 目录，自动生成 plugin.json 并检查 README.md 一致性
# 全递归扫描，不再硬编码 bucket 列表

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ERRORS=0

echo "=== 扫描技能目录 ==="

# 全递归扫描所有 S*/W* 目录（含子目录）
declare -a PUBLISHED_SKILLS=()
declare -a ALL_SKILLS=()

while IFS= read -r -d '' skill_dir; do
    sname=$(basename "$skill_dir")

    # 只匹配 S1-xxx / W1-xxx 格式
    if ! echo "$sname" | grep -qE '^[SW][0-9]+-'; then
        continue
    fi

    # 排除未发布桶: 个人专用类, 开发中技能, 已废弃技能
    rel=$(echo "$skill_dir" | sed "s|$ROOT/skills/||")
    bucket=$(echo "$rel" | cut -d'/' -f1)

    # 检查主技能文件
    main_file="$skill_dir/$sname.md"
    if [ ! -f "$main_file" ]; then
        echo "  ⚠  $rel — 缺少主技能文件 ($sname.md)"
        continue
    fi

    rel_path="./skills/$rel"
    ALL_SKILLS+=("$rel_path")

    case "$bucket" in
        个人专用类|开发中技能|已废弃技能)
            # 跳过未发布桶
            ;;
        *)
            PUBLISHED_SKILLS+=("$rel_path")
            ;;
    esac
done < <(find "$ROOT/skills" -type d -print0)

echo ""
echo "=== 生成 plugin.json ==="
PLUGIN_FILE="$ROOT/.claude-plugin/plugin.json"

IFS=$'\n' SORTED_PUBLISHED=($(sort <<<"${PUBLISHED_SKILLS[*]}")); unset IFS

json='{\n  "name": "mattpocock-skills",\n  "skills": [\n'
for ((i=0; i<${#SORTED_PUBLISHED[@]}; i++)); do
    comma=""
    [ $i -lt $((${#SORTED_PUBLISHED[@]}-1)) ] && comma=","
    json+="    \"${SORTED_PUBLISHED[$i]}\"$comma\n"
done
json+='  ]\n}\n'

echo -e "$json" > "$PLUGIN_FILE"
echo "  ✅  plugin.json 已更新（${#SORTED_PUBLISHED[@]} 个技能）"

echo ""
echo "=== 检查 README.md 技能列表 ==="
README_FILE="$ROOT/README.md"
MISSING=()

for skill_rel in "${PUBLISHED_SKILLS[@]}"; do
    sname=$(basename "$skill_rel")
    # 尝试匹配路径
    if ! grep -q "$sname" "$README_FILE" 2>/dev/null; then
        MISSING+=("$skill_rel")
    fi
done

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "  ✅  README.md 技能列表完整"
else
    echo "  ❌  以下技能在 README.md 中缺失："
    for m in "${MISSING[@]}"; do
        echo "     - $m"
    done
    ERRORS=1
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ 检查通过"
else
    echo "❌ 存在不一致，请修复"
fi
