#!/bin/bash
# sync.sh — 扫描 S/W 编号技能 + Tools，生成 SKILLS.md 和 TOOLS.md
set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$VAULT_DIR"
SKILLS_DIR="$VAULT_DIR/Skills"
TOOLS_DIR="$VAULT_DIR/Tools"

log_info()    { echo "   ℹ️  $1"; }
log_success() { echo "   ✅ $1"; }
log_warn()    { echo "   ⚠️  $1"; }
log_error()   { echo "   ❌ $1"; }

# =====================================
# 1. 扫描 S/W 编号技能
# =====================================
echo "📋 扫描技能清单..."

# 提取编号信息：目录名如 "W5-图片设计" → prefix=W, num=5, name=图片设计
scan_skills() {
    find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -type d | sort | while IFS= read -r d; do
        local fname=$(basename "$d")
        if echo "$fname" | grep -qE '^[SW][0-9]+-'; then
            local prefix=$(echo "$fname" | sed 's/^\([SW]\)[0-9]*\-.*/\1/')
            local num=$(echo "$fname" | sed 's/^[SW]\([0-9]*\)\-.*/\1/')
            local name=$(echo "$fname" | sed "s/^[SW]${num}\-//")
            local bucket=$(basename "$(dirname "$d")")
            echo "${prefix}|${num}|${name}|${bucket}|${d}"
        fi
    done | sort -t'|' -k1,1 -k2,2n
}

ALL_SKILLS=$(scan_skills)
SKILL_COUNT=$(echo "$ALL_SKILLS" | grep -c '|' || echo 0)

# 按大类分组输出
gen_skill_list() {
    local last_bucket=""
    echo "# 技能清单\n"
    echo "> 自动生成于 $(date '+%Y-%m-%d %H:%M')\n"
    
    echo "$ALL_SKILLS" | while IFS='|' read -r prefix num name bucket path; do
        [ -z "$prefix" ] && continue
        if [ "$bucket" != "$last_bucket" ]; then
            echo "\n## $bucket\n"
            echo "| 编号 | 名称 |\n|------|------|"
            last_bucket="$bucket"
        fi
        echo "| $prefix$num | $name |"
    done
}

SKILL_LIST=$(gen_skill_list)
echo -e "$SKILL_LIST" > "$VAULT_DIR/SKILLS.md"
log_success "SKILLS.md（$SKILL_COUNT 个技能）"

# =====================================
# 2. 自动生成缺失的路由 SKILL.md
# =====================================
gen_missing_skill_md() {
    local generated=0
    find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -type d | sort | while IFS= read -r dir; do
        local dir_name=$(basename "$dir")
        if ! echo "$dir_name" | grep -qE '^[SW][0-9]+-'; then continue; fi

        local prefix="${dir_name:0:1}"
        local rest="${dir_name:1}"
        local num="${rest%%-*}"
        local name="${rest#*-}"

        # 已有 SKILL.md 则跳过
        [ -f "$dir/SKILL.md" ] && continue

        # 检查是否有子模块
        local subdirs=()
        while IFS= read -r sub; do subdirs+=("$sub"); done <<< "$(find "$dir" -mindepth 1 -maxdepth 1 -type d | sort)"
        [ ${#subdirs[@]} -eq 0 ] && continue

        local sub_names=()
        for sub in "${subdirs[@]}"; do sub_names+=("$(basename "$sub")"); done
        # 子模块少于 2 个时不需要路由导航（单个 references/ 目录不算子技能）
        [ ${#subdirs[@]} -lt 2 ] && continue

        local sub_list=$(IFS='、'; echo "${sub_names[*]}")

        {
            echo -e "---\nname: $name\ndescription: 路由导航。子模块：${sub_list}。\nmetadata:\n  pattern: pipeline\n---\n"
            echo -e "# $dir_name\n\n<what-to-do>\n\n## 路由表\n\n| 模块 | 路径 |\n|------|------|"
            for sub in "${subdirs[@]}"; do
                local sub_name=$(basename "$sub")
                local md_files=$(find "$sub" -maxdepth 1 -name "*.md" | head -1)
                if [ -n "$md_files" ]; then
                    echo "| $sub_name | \`$dir_name/$sub_name/$(basename "$md_files")\` |"
                else
                    echo "| $sub_name | $dir_name/$sub_name/ |"
                fi
            done
            echo -e "\n</what-to-do>"
        } > "$dir/SKILL.md"

        log_success "自动生成路由: $dir/SKILL.md（${#subdirs[@]} 个子模块）"
        generated=$((generated+1))
    done
    [ "$generated" -eq 0 ] && log_info "无需生成缺失的路由 SKILL.md"
}

gen_missing_skill_md

# =====================================
# 3. 扫描 Tools 生成 TOOLS.md
# =====================================
echo ""
echo "📋 扫描工具清单..."

TOOL_LIST="# 工具清单\n\n"
TOOL_LIST+="> 自动生成于 $(date '+%Y-%m-%d %H:%M')\n\n"
TOOL_LIST+="| 工具 | 类型 | 用途 |\n|------|------|------|\n"

# 扫描 .py 文件
for f in "$TOOLS_DIR"/*.py; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    desc=$(python3 -c "
import ast
try:
    with open('$f') as fh:
        tree = ast.parse(fh.read())
    doc = ast.get_docstring(tree)
    if doc:
        print(doc.strip().split(chr(10))[0].rstrip('.。'))
    else:
        print('Python 脚本')
except:
    print('Python 脚本')
" 2>/dev/null || echo "Python 脚本")
    TOOL_LIST+="| \`$fname\` | Python | ${desc} |\n"
done

# 扫描 .sh 文件
for f in "$TOOLS_DIR"/*.sh; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    desc=$(grep -m1 '^#[^#!]' "$f" 2>/dev/null | sed 's/^#[[:space:]]*//' || echo "Shell 脚本")
    TOOL_LIST+="| \`$fname\` | Shell | ${desc} |\n"
done

# 扫描 .jsx 文件
for f in "$TOOLS_DIR"/*.jsx; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    TOOL_LIST+="| \`$fname\` | JSX | Photoshop 脚本 |\n"
done

# 扫描子目录（工具包）
for d in "$TOOLS_DIR"/*/; do
    [ -d "$d" ] || continue
    dirname=$(basename "$d")
    entry=$(ls "$d/$dirname.py" "$d/main.py" "$d/run.py" 2>/dev/null | head -1 || ls "$d"/*.py 2>/dev/null | head -1 || true)
    desc="工具文件夹"
    if [ -n "$entry" ] && [ -f "$entry" ]; then
        desc=$(python3 -c "
import ast
try:
    with open('$entry') as fh:
        tree = ast.parse(fh.read())
    doc = ast.get_docstring(tree)
    if doc:
        print(doc.strip().split(chr(10))[0].rstrip('.。'))
    else:
        print('工具文件夹')
except:
    print('工具文件夹')
" 2>/dev/null || echo "工具文件夹")
    fi
    TOOL_LIST+="| \`$dirname/\` | 目录 | ${desc} |\n"
done

echo -e "$TOOL_LIST" > "$VAULT_DIR/TOOLS.md"
TOOL_COUNT=$(echo "$TOOL_LIST" | grep -c '| \`' || echo 0)
log_success "TOOLS.md（$TOOL_COUNT 个工具）"

echo ""
echo "✅ 扫描完成"

# 自动生成 Wiki/index.md
echo ""
echo "📖 生成 Wiki/index.md..."
INDEX_FILE="$VAULT_DIR/Wiki/index.md"
{
    echo "# Wiki 页面索引"
    echo ""
    echo "> 由 sync.command 自动生成。每次同步时更新。"
    echo ""
    echo "| 页面 | 类型 | 摘要 |"
    echo "|------|------|------|"
    for page in "$VAULT_DIR/Wiki"/*.md; do
        name=$(basename "$page" .md)
        [ "$name" = "index" ] || [ "$name" = "log" ] || [ "$name" = "instructions" ] && continue
        type=$(grep -m1 '^type:' "$page" 2>/dev/null | sed 's/type: *//' || echo "—")
        desc=$(grep -m1 '^description:' "$page" 2>/dev/null | sed 's/description: *//' || echo "—")
        echo "| [[$name]] | $type | $desc |"
    done
} > "$INDEX_FILE"
WIKI_COUNT=$(grep -c '| \[' "$INDEX_FILE" || echo 0)
log_success "Wiki/index.md（$WIKI_COUNT 个页面）"

# 周日自动生成周复盘 + 校准日志审计（不包含当天）
if [ "$(date '+%u')" = "7" ]; then
    REVIEW_DIR="$VAULT_DIR/复盘"
    mkdir -p "$REVIEW_DIR"
    REVIEW_FILE="$REVIEW_DIR/$(date '+%Y-%m-%d').md"
    if [ ! -f "$REVIEW_FILE" ]; then
        # 扫 8 天不包含今天 = 上周日到这周六
        python3 "$VAULT_DIR/Tools/weekly_review.py" --days 8 --exclude-today --output "$REVIEW_FILE" 2>/dev/null && log_success "周复盘已生成"
        # 校准日志审计
        python3 "$VAULT_DIR/.codebuddy/memory/audit.py" --days 7 --output "$REVIEW_DIR/audit-$(date '+%Y-%m-%d').md" 2>/dev/null && log_success "校准日志审计已生成"
    fi
fi

# 扫描 Clippings/raw/ 未处理文件
echo ""
PENDING=$(python3 "$VAULT_DIR/Clippings/raw/pending.py" --count 2>/dev/null || echo "0")
if [ "$PENDING" != "0" ]; then
    echo "📋 检测到 $PENDING 个未处理的原始资料（Clippings/raw/）"
    echo "   运行: python3 Clippings/raw/pending.py"
else
    echo "📋 Clippings/raw/ 全部已处理"
fi

# Git 推送（双重保险）
echo ""
echo "📤 推送到 GitHub..."
cd "$VAULT_DIR"
git add -A
git commit -m "sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || echo "⏭️  无变更"
git push 2>&1 || echo "⚠️  Git 推送失败（可能是网络问题）"
echo "✅ 同步完成"
