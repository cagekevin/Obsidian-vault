#!/bin/bash
# sync.sh — 扫描 S/W 编号技能 + Tools，生成 SKILLS.md 和 TOOLS.md
set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$VAULT_DIR"
SKILLS_DIR="$VAULT_DIR/skills"
TOOLS_DIR="$VAULT_DIR/Tools"

log_info()    { echo "   ℹ️  $1"; }
log_success() { echo "   ✅ $1"; }
log_warn()    { echo "   ⚠️  $1"; }
log_error()   { echo "   ❌ $1"; }

# =====================================
# 1. 扫描 S/W 编号技能
# =====================================
echo "📋 扫描技能清单..."

# 扫描 skills/ 下所有目录（排除 参考技能/），不要求编号
scan_skills() {
    find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d ! -name "参考技能" | sort | while IFS= read -r d; do
        local name=$(basename "$d")
        echo "${name}|${d}"
    done
}

ALL_SKILLS=$(scan_skills)
SKILL_COUNT=$(echo "$ALL_SKILLS" | grep -c '|' || echo 0)

# 核心技能一个表
gen_skill_list() {
    echo "# 技能清单\n"
    echo "> 自动生成于 $(date '+%Y-%m-%d %H:%M')\n"
    echo "## 核心 Skill（AI 直达）\n"
    echo "| 名称 | 说明 |"
    echo "|------|------|"
    echo "$ALL_SKILLS" | while IFS='|' read -r name path; do
        [ -z "$name" ] && continue
        echo "| $name | |"
    done
    echo ""
    echo "## 参考技能（\`skills/参考技能/\` 下，按需查阅）"
    echo ""
    echo "包含 S 系列、W0-W3/W7/W9、baoyu、编码准则等。不常用，需要时 AI 去目录里找。"
}

SKILL_LIST=$(gen_skill_list)
# 追加 Wiki 知识管理自定义技能（不被自动扫描覆盖）
SKILL_LIST+="\n## Wiki 知识管理\n\n| 触发词 | 说明 | 入口 |\n|--------|------|------|\n"
SKILL_LIST+="| \`整理知识库\` / \`整理wiki\` / \`整理到wiki\` / \`整理raw\` / \`ingest\` | 把 Clippings 里的资料吸收到 Wiki 知识库 | \`Wiki/skills/ingest.md\` |\n"
SKILL_LIST+="| \`检查wiki\` / \`看看wiki健康吗\` / \`检查知识库健康\` / \`lint\` | Wiki 健康检查（孤儿/死链/过期等） | \`Wiki/skills/lint.md\` |\n"
SKILL_LIST+="| \`看看知识库的...\` / \`从知识库查看...\` / \`query\` | 从 Wiki 知识库查询 | \`Wiki/skills/query.md\` |\n"
SKILL_LIST+="| \`把这个保存到知识库\` / \`save\` | 存档当前对话到 Wiki | \`Wiki/skills/save.md\` |\n"
echo -e "$SKILL_LIST" > "$VAULT_DIR/SKILLS.md"
log_success "SKILLS.md（$SKILL_COUNT 个技能）"

# =====================================
# 2. 自动生成缺失的路由 SKILL.md
# =====================================
gen_missing_skill_md() {
    local generated=0
    find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d ! -name "参考技能" | sort | while IFS= read -r dir; do
        local dir_name=$(basename "$dir")
        local name="$dir_name"

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

# Wiki/index.md 由 AI 手动维护，不再自动覆盖

# 周日自动生成周复盘 + 校准日志审计（不包含当天）
if [ "$(date '+%u')" = "7" ]; then
    REVIEW_DIR="$VAULT_DIR/复盘"
    mkdir -p "$REVIEW_DIR"
    REVIEW_FILE="$REVIEW_DIR/$(date '+%Y-W%V').md"
    if [ ! -f "$REVIEW_FILE" ]; then
        # 扫 8 天不包含今天 = 上周日到这周六
        python3 "$VAULT_DIR/Tools/weekly_review.py" --days 8 --exclude-today --audit --output "$REVIEW_FILE" 2>/dev/null && log_success "周复盘已生成"
    fi
fi

# Clippings 整理由 AI 按 Wiki/skills/ingest.md 流程处理

# Git 推送（双重保险）
echo ""
echo "📤 推送到 GitHub..."
cd "$VAULT_DIR"
git add -A
git commit -m "sync: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || echo "⏭️  无变更"
git push 2>&1 || echo "⚠️  Git 推送失败（可能是网络问题）"
echo "✅ 同步完成"
