#!/usr/bin/env python3
"""
目录生成器 — 为长 markdown 文件生成章节目录

用法:
    python3 tools/markdown-toc.py 文档.md               # 生成目录
    python3 tools/markdown-toc.py 文档.md --max-level 2  # 只到二级标题
    python3 tools/markdown-toc.py 文档.md --write        # 直接插入文件头部
"""

import sys
import re
from pathlib import Path


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(1)

    filepath = args[0]
    max_level = 6
    write_mode = False

    if "--max-level" in args:
        idx = args.index("--max-level")
        max_level = int(args[idx + 1]) if idx + 1 < len(args) else 6
    if "--write" in args:
        write_mode = True

    p = Path(filepath)
    if not p.exists():
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)

    content = p.read_text(encoding="utf-8")
    lines = content.split("\n")
    toc_lines = ["## 目录\n"]
    in_code_block = False

    for ln, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        m = re.match(r'^(#{1,%d})\s+(.+)$' % max_level, line)
        if not m:
            continue

        level = len(m.group(1))
        title = m.group(2).strip()
        anchor = title.lower().replace(" ", "-").replace(":", "").replace("。", "")
        indent = "  " * (level - 1)
        toc_lines.append(f"{indent}- [{title}](#{anchor})")

    toc = "\n".join(toc_lines) + "\n"

    if write_mode:
        # 查找第一个标题后的位置插入
        insert_pos = 0
        for i, line in enumerate(lines):
            if re.match(r'^# ', line):
                insert_pos = i + 2
                break
        new_content = "\n".join(lines[:insert_pos]) + "\n" + toc + "\n" + "\n".join(lines[insert_pos:])
        p.write_text(new_content, encoding="utf-8")
        print(f"✅ 目录已写入: {filepath}")
    else:
        print(toc)


if __name__ == "__main__":
    main()
