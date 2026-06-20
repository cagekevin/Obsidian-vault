#!/usr/bin/env python3
"""
技能初始化工具 — 创建一个新技能的模板目录

用法：
    init_skill.py <技能中文名> --path <目标路径>

示例：
    init_skill.py 我的新技能 --path skills/工作效率类
    init_skill.py 数据导入工具 --path /custom/location

注意：不生成编号前缀，创建后自行改名（如 W8-我的新技能）
"""

import sys
import os
from pathlib import Path


def safe_print(message):
    try:
        print(message)
    except UnicodeEncodeError:
        import re
        clean_message = re.sub(r'[\U0001F300-\U0001F9FF]', '', message)
        print(clean_message.strip())


if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


SKILL_TEMPLATE = """---
name: {skill_name}
description: 模板占位：一句话说明技能用途与触发词，务必以 "Use when" 结尾（示例：Use when user wants to generate images for e-commerce）。
---

# {skill_title}

<what-to-do>

[ TODO: 核心执行流程 ]

</what-to-do>

<supporting-info>

[ TODO: 参考材料、模板、完整示例 ]

</supporting-info>
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 辅助脚本
这是一个示例脚本。替换为实际实现或删除。
"""

def main():
    print("{skill_name} 脚本")
    # TODO: 添加实际逻辑

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} — 参考文档

这是一个占位参考文档。替换为实际内容或删除。

## 适用场景
- 详细 API 文档
- 复杂工作流指南
- 过长不宜放在主文件的参考信息
"""

EXAMPLE_ASSET = """# 示例资源文件

这是一个占位文件。替换为实际的资源文件（模板、图片、字体等）或删除。

## 常见资源类型
- 模板: .pptx, .docx
- 图片: .png, .jpg, .svg
- 字体: .ttf, .otf
- 数据文件: .csv, .json
"""


def init_skill(skill_name, path):
    skill_name = skill_name.strip()
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        safe_print(f"❌ 错误：目录已存在: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        safe_print(f"✅ 创建目录: {skill_dir}")
    except Exception as e:
        safe_print(f"❌ 创建目录失败: {e}")
        return None

    # 创建主文件
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_name
    )
    skill_md = skill_dir / f'{skill_name}.md'
    try:
        skill_md.write_text(skill_content)
        safe_print(f"✅ 创建 {skill_name}.md")
    except Exception as e:
        safe_print(f"❌ 创建主文件失败: {e}")
        return None

    # 创建资源目录
    try:
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example = scripts_dir / 'example.py'
        example.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example.chmod(0o755)
        safe_print("✅ 创建 scripts/example.py")

        ref_dir = skill_dir / 'references'
        ref_dir.mkdir(exist_ok=True)
        (ref_dir / 'api_reference.md').write_text(
            EXAMPLE_REFERENCE.format(skill_title=skill_name))
        safe_print("✅ 创建 references/api_reference.md")

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        (assets_dir / 'example_asset.txt').write_text(EXAMPLE_ASSET)
        safe_print("✅ 创建 assets/example_asset.txt")
    except Exception as e:
        safe_print(f"❌ 创建资源目录失败: {e}")
        return None

    safe_print(f"\n✅ 技能 '{skill_name}' 初始化完成")
    print("\n下一步：")
    print("1. 编辑 SKILL.md 补全 TODO 内容")
    print("2. 按需添加编号前缀（如 W8-{skill_name}）")
    print("3. 清理不需要的示例文件")
    print("4. 注册并运行 skills-init")
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("用法: init_skill.py <技能中文名> --path <目标路径>")
        print("\n示例:")
        print("  init_skill.py 新技能 --path skills/工作效率类")
        print("  init_skill.py 数据导入工具 --path .")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    safe_print(f"🚀 初始化技能：{skill_name}")
    safe_print(f"   位置：{path}")
    print()

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
