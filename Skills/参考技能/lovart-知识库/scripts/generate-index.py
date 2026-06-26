#!/usr/bin/env python3
"""
知识库索引生成器 — 从 catalog.json + 文件系统扫描生成索引。
"""
import os, json, argparse

from catalog import KB_DIR, require_catalog

INDEX_MARKER_START = "<!-- INDEX_AUTO_GENERATED -->"
INDEX_MARKER_END = "<!-- /INDEX_AUTO_GENERATED -->"


def scan_dir(cat: str) -> list:
    d = os.path.join(KB_DIR, cat)
    if not os.path.isdir(d):
        return []
    files = []
    for fname in sorted(os.listdir(d)):
        if not fname.endswith(".md"):
            continue
        if fname in ("README.md", "data_structure.md"):
            continue
        name = fname.replace(".md", "")
        files.append((name, f"{cat}/{fname}"))
    return files


def generate_index() -> str:
    catalog = require_catalog()
    lines = [INDEX_MARKER_START, "", "## 目录索引"]

    for cat_info in catalog["categories"]:
        cat = cat_info["dir"]
        if not cat_info.get("index_in_readme", True):
            continue
        files = scan_dir(cat)
        if not files:
            continue
        label = cat_info.get("label", "")
        desc = cat_info.get("desc", "")
        lines.append("")
        lines.append(f"### {cat} — {label}（{len(files)} 篇）")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")

        fragments = [(n, p) for n, p in files if n.startswith("碎片-")]
        articles = [(n, p) for n, p in files if not n.startswith("碎片-")]

        if articles:
            for name, relpath in articles:
                lines.append(f"- [{name}]({relpath.replace(' ', '%20')})")
        if articles and fragments:
            lines.append("")
            lines.append("  > 碎片（未整理中间态）：")
        if fragments:
            for name, relpath in fragments:
                lines.append(f"- [{name}]({relpath.replace(' ', '%20')})")

    lines.append("")
    lines.append("---")
    lines.append("_上次生成: 运行 `python scripts/generate-index.py` 刷新此索引_")
    lines.append("")
    lines.append(INDEX_MARKER_END)
    return "\n".join(lines)


def update_readme(index_text: str):
    readme_path = os.path.join(KB_DIR, "README.md")
    if not os.path.exists(readme_path):
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if INDEX_MARKER_START not in content or INDEX_MARKER_END not in content:
        return False

    start_idx = content.index(INDEX_MARKER_START)
    end_idx = content.index(INDEX_MARKER_END) + len(INDEX_MARKER_END)
    new_content = content[:start_idx] + index_text + content[end_idx:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ README.md 索引已更新（{sum(1 for c in index_text if c == '-')} 个条目）")
    return True


def rebuild_data_structure(cat: str, cat_info: dict):
    cat_dir = os.path.join(KB_DIR, cat)
    if not os.path.isdir(cat_dir):
        return

    files = sorted(os.listdir(cat_dir))
    md_files = [f for f in files if f.endswith(".md") and f not in ("README.md", "data_structure.md")]
    if not md_files:
        return

    fragments = sorted(f for f in md_files if f.startswith("碎片-"))
    articles = sorted(f for f in md_files if not f.startswith("碎片-"))
    label = cat_info.get("label", "")

    lines = [f"# {cat} — {label}", "",
             "## Purpose", "",
             "KBRetriever 自动索引 — `python scripts/generate-index.py --rebuild` 刷新。", "",
             "**何时搜索**：根据文件名和目录描述判断。", "",
             "## Files", ""]

    if articles:
        lines.append("### 稳定文章")
        lines.append("")
        for f in articles:
            lines.append(f"- `{f}` — {f.replace('.md', '')}")
        lines.append("")

    if fragments:
        lines.append("### 碎片（未整理中间态）")
        lines.append("")
        for f in fragments:
            lines.append(f"- `{f}` — {f.replace('.md', '').replace('碎片-', '')}")

    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    lines.append(f"- 篇数：{len(md_files)} 篇（{len(articles)} 稳定 + {len(fragments)} 碎片）")
    lines.append("- 自动生成，文件变更后运行 `--rebuild` 刷新")

    content = "\n".join(lines) + "\n"
    target = os.path.join(cat_dir, "data_structure.md")
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  📝 {cat}/data_structure.md ({len(md_files)} 篇)")


def do_rebuild():
    catalog = require_catalog()
    print("🔄 重新生成所有 data_structure.md...")
    for cat_info in catalog["categories"]:
        cat = cat_info["dir"]
        if cat == "_meta":
            continue
        rebuild_data_structure(cat, cat_info)
    print()
    index = generate_index()
    if update_readme(index):
        print("✅ 全部更新完成！")


def main():
    p = argparse.ArgumentParser(description="生成知识库索引")
    p.add_argument("--print", "-p", action="store_true", help="只打印，不写文件")
    p.add_argument("--rebuild", "-r", action="store_true", help="重建所有 data_structure.md + 刷新 README")
    args = p.parse_args()

    if args.rebuild:
        do_rebuild()
        return

    index = generate_index()
    if args.print:
        print(index)
    else:
        readme_path = os.path.join(KB_DIR, "README.md")
        has_marker = False
        if os.path.exists(readme_path):
            with open(readme_path, encoding="utf-8") as f:
                has_marker = INDEX_MARKER_START in f.read()
        if has_marker:
            update_readme(index)
        else:
            print("⚠️  README.md 中未找到索引标记。已将索引打印到终端：")
            print()
            print(index)


if __name__ == "__main__":
    main()
