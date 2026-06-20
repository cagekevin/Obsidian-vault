#!/bin/bash
# 一键同步：扫描技能清单 → commit → push

set -e

VAULT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$VAULT_DIR"

echo "📋 扫描技能清单..."

SKILL_LIST="# 技能清单\n\n"
SKILL_LIST+="> 自动生成于 $(date '+%Y-%m-%d %H:%M')\n\n"

# 遍历大类
for bucket in "$VAULT_DIR/Skills/"*/; do
    bucket_name=$(basename "$bucket")
    SKILL_LIST+="## $bucket_name\n\n"
    
    # 遍历技能子文件夹
    for skill in "$bucket"*/; do
        skill_name=$(basename "$skill")
        # 只显示有 SKILL.md 的
        if [ -f "$skill/SKILL.md" ]; then
            desc=$(head -5 "$skill/SKILL.md" | grep 'description:' | sed 's/.*description: *//')
            SKILL_LIST+="- **$skill_name**"
            [ -n "$desc" ] && SKILL_LIST+=": $desc"
            SKILL_LIST+="\n"
        fi
    done
    SKILL_LIST+="\n"
done

echo -e "$SKILL_LIST" > "$VAULT_DIR/SKILLS.md"
echo "✅ 已生成 SKILLS.md"

echo "📤 推送到 GitHub..."
git add -A
git commit -m "sync: $(date '+%Y-%m-%d %H:%M')" || echo "⏭️  没有变更"
git push
echo "✅ 完成"
