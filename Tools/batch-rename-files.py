#!/usr/bin/env python3
"""
批量重命名 — 一次性改名/改后缀/编号

用法:
    python3 tools/rename-batch.py tools/ --prefix "new_"           # 加前缀
    python3 tools/rename-batch.py tools/ --suffix "_v2"            # 加后缀
    python3 tools/rename-batch.py tools/ --ext .md --new-ext .txt  # 改后缀
    python3 tools/rename-batch.py tools/ --number                  # 编号 01_xxx
    python3 tools/rename-batch.py tools/ --dry-run                 # 预览，不动手
"""

import sys
from pathlib import Path


def main():
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        sys.exit(1)

    directory = args[0]
    prefix = ""
    suffix = ""
    ext_filter = None
    new_ext = None
    number = False
    dry_run = False

    i = 1
    while i < len(args):
        if args[i] == "--prefix" and i + 1 < len(args):
            i += 1
            prefix = args[i]
        elif args[i] == "--suffix" and i + 1 < len(args):
            i += 1
            suffix = args[i]
        elif args[i] == "--ext" and i + 1 < len(args):
            i += 1
            ext_filter = args[i]
        elif args[i] == "--new-ext" and i + 1 < len(args):
            i += 1
            new_ext = args[i]
        elif args[i] == "--number":
            number = True
        elif args[i] == "--dry-run":
            dry_run = True
        i += 1

    root = Path(directory)
    if not root.is_dir():
        print(f"❌ 不是目录: {directory}")
        sys.exit(1)

    files = sorted(root.iterdir())
    changes = []
    num_width = len(str(len(files)))

    for idx, f in enumerate(files, 1):
        if not f.is_file():
            continue
        if ext_filter and f.suffix != ext_filter:
            continue

        name = f.stem
        ext = new_ext if new_ext else f.suffix
        num_part = f"{idx:0{num_width}d}_" if number else ""
        new_name = f"{prefix}{num_part}{name}{suffix}{ext}"
        changes.append((f, f.parent / new_name))

    if not changes:
        print("⚠️ 没有匹配的文件")
        return

    print(f"共 {len(changes)} 个文件:")
    for old, new in changes:
        flag = "DRY: " if dry_run else ""
        print(f"  {flag}{old.name} → {new.name}")

    if not dry_run:
        confirm = input("\n确认重命名？(Y/n): ")
        if confirm.lower() in ("", "y", "yes"):
            for old, new in changes:
                old.rename(new)
            print(f"✅ 已重命名 {len(changes)} 个文件")


if __name__ == "__main__":
    main()
