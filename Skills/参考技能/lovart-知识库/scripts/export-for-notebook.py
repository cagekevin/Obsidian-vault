#!/usr/bin/env python3
"""
【Layer 3 - 合并导出】
知识库合并导出 → 一键拖入 NotebookLM
- 从 catalog.json 读取分类目录（仅导出标记为 export: true 的目录）
- 按顺序合并为单个文件
- 用 hash 记录已合并版本，不重复输出
"""
import os, hashlib, json

from catalog import KB_DIR, require_catalog

HASH_FILE = os.path.join(KB_DIR, ".export_hash.json")
OUTPUT = os.path.expanduser("~/Desktop/lovart-知识库全量.md")


def get_export_cats(catalog: dict) -> list:
    return [c["dir"] for c in catalog["categories"] if c.get("export", False)]


def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    catalog = require_catalog()
    CATS = get_export_cats(catalog)

    # 计算所有文件的 hash
    current = {}
    for cat in CATS:
        d = os.path.join(KB_DIR, cat)
        if not os.path.isdir(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.endswith(".md"):
                continue
            if fname in ("README.md", "data_structure.md"):
                continue
            fpath = os.path.join(d, fname)
            current[f"{cat}/{fname}"] = file_hash(fpath)

    # 读上次记录
    previous = {}
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE) as f:
                previous = json.load(f)
        except (json.JSONDecodeError, IOError):
            previous = {}

    # 比较：完全一致则跳过（包括添加和删除）
    if current == previous:
        print("✅ 无变更，跳过合并（上次内容一致）")
        return

    # 合并输出
    total = 0
    with open(OUTPUT, "w", encoding="utf-8") as out:
        out.write("# Lovart 知识库全量\n\n")
        for cat in CATS:
            d = os.path.join(KB_DIR, cat)
            if not os.path.isdir(d):
                continue
            out.write(f"\n---\n# {cat}\n\n")
            for fname in sorted(os.listdir(d)):
                if not fname.endswith(".md"):
                    continue
                if fname in ("README.md", "data_structure.md"):
                    continue
                fpath = os.path.join(d, fname)
                with open(fpath, encoding="utf-8") as f:
                    content = f.read().strip()
                out.write(f"\n## {fname.replace('.md','')}\n\n{content}\n\n")
                total += 1

    # 记录 hash
    with open(HASH_FILE, "w") as f:
        json.dump(current, f, indent=2)

    change_type = "新增或删除" if len(current) != len(previous) else "内容变更"
    print(f"✅ 已合并 {total} 篇（{change_type}）→ {OUTPUT}")
    print("   📌 直接拖这个文件进 NotebookLM")


if __name__ == "__main__":
    main()
