#!/usr/bin/env python3
"""
扫描 Clippings/raw/ 下未处理的原始资料。
检测标准：文件末尾是否有 <!-- processed: 标记。

用法:
  python3 pending.py              # 列出所有未处理的文件
  python3 pending.py --count      # 只显示数量
"""
import os
import sys

RAW_DIR = os.path.dirname(os.path.abspath(__file__))
MARKER = "<!-- processed:"

def is_processed(filepath):
    """检查文件末尾是否有处理标记"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # 只检查最后 5 行
            lines = f.readlines()
            for line in lines[-5:]:
                if MARKER in line:
                    return True
        return False
    except Exception:
        return False

def main():
    count_only = "--count" in sys.argv

    pending = []
    for f in os.listdir(RAW_DIR):
        if f == os.path.basename(__file__):
            continue
        filepath = os.path.join(RAW_DIR, f)
        if os.path.isfile(filepath) and not f.startswith("."):
            if not is_processed(filepath):
                pending.append((f, os.path.getsize(filepath)))

    if count_only:
        print(len(pending))
        return

    if not pending:
        print("✅ 所有文件已处理")
        return

    print(f"📋 未处理的文件（共 {len(pending)} 个）：\n")
    for f, size in sorted(pending):
        print(f"  ❌ {f}  ({size/1024:.0f} KB)")

if __name__ == "__main__":
    main()
