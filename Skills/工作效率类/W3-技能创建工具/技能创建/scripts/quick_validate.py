#!/usr/bin/env python3
"""
技能快速校验工具 — 检查技能文件结构是否符合项目规范
支持中文命名（W3-技能名.md、S6-技能名.md、技能名.md）和英文命名（SKILL.md）

用法：
    quick_validate.py <技能目录>
"""

import sys
import re
from pathlib import Path


def find_main_file(skill_dir):
    """找到技能主文件，兼容多种命名方式"""
    # 优先找 *.md（排除 templates/ references/ 等目录下的）
    for f in skill_dir.iterdir():
        if f.is_file() and f.suffix == '.md':
            return f
    # 也可能就叫 SKILL.md
    sk = skill_dir / 'SKILL.md'
    return sk if sk.exists() else None


def validate_skill(skill_path):
    skill_path = Path(skill_path)

    # 检查主文件
    main_file = find_main_file(skill_path)
    if not main_file:
        return False, "未找到 .md 主文件"

    content = main_file.read_text(encoding='utf-8')

    # 检查 YAML frontmatter
    if not content.startswith('---'):
        return False, f"缺少 YAML frontmatter（{main_file.name}）"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Frontmatter 格式错误"
    frontmatter = match.group(1)

    # 检查必要字段
    if 'name:' not in frontmatter:
        return False, "缺少 'name' 字段"
    if 'description:' not in frontmatter:
        return False, "缺少 'description' 字段"

    # 提取 name
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        if not name:
            return False, "name 为空"

    # 提取 description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        desc = desc_match.group(1).strip()
        if '<' in desc or '>' in desc:
            return False, "description 不能包含尖括号（< 或 >）"

    return True, f"✅ {main_file.name} — 校验通过"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python quick_validate.py <技能目录>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
