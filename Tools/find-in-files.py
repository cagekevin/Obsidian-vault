#!/usr/bin/env python3
"""
文件搜索 — 代替 grep / 逐文件读，批量搜索关键词，显示匹配位置

用法:
    python3 tools/find-in-files.py "关键词" 路径/         # 搜索路径下所有文件
    python3 tools/find-in-files.py "关键词" 路径/ --ext md # 只搜 .md 文件
    python3 tools/find-in-files.py "关键词" --ignore node_modules
"""

import sys
import re
from pathlib import Path


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    keyword = None
    search_path = "."
    ext_filter = None
    ignore_dirs = {".git", "node_modules", "__pycache__", ".codebuddy", ".cursor", "venv"}

    i = 0
    while i < len(args):
        if args[i] == "--ext" and i + 1 < len(args):
            i += 1
            ext_filter = args[i]
        elif args[i] == "--ignore" and i + 1 < len(args):
            i += 1
            ignore_dirs.add(args[i])
        elif args[i].startswith("--"):
            pass
        elif keyword is None:
            keyword = args[i]
        else:
            search_path = args[i]
        i += 1

    if not keyword:
        print("❌ 请指定搜索关键词")
        sys.exit(1)

    root = Path(search_path)
    if not root.exists():
        print(f"❌ 路径不存在: {search_path}")
        sys.exit(1)

    total = 0
    matched_files = 0

    for f in root.rglob("*"):
        if any(ign in f.parts for ign in ignore_dirs):
            continue
        if not f.is_file():
            continue
        if ext_filter and not f.suffix.lstrip(".") == ext_filter.lstrip("."):
            continue

        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        lines = text.split("\n")
        matches = []
        for ln, line in enumerate(lines, 1):
            if keyword in line:
                idx = line.index(keyword)
                start = max(0, idx - 20)
                end = min(len(line), idx + len(keyword) + 20)
                snippet = ("..." if start > 0 else "") + line[start:end] + ("..." if end < len(line) else "")
                matches.append(f"  L{ln:>4}  {snippet}")

        if matches:
            matched_files += 1
            print(f"\n📄 {f.relative_to(root)} ({f.stat().st_size//1024}KB)")
            for m in matches:
                print(m)
            total += len(matches)

    print(f"\n共 {total} 处匹配，分布在 {matched_files} 个文件")


if __name__ == "__main__":
    main()
