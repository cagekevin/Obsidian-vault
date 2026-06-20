#!/usr/bin/env python3
"""
【整理阶段工具】碎片晋升管线
将 00-钓鱼话术/ 的原始渔获晋升到对应分类目录作为 碎片-*.md。
分类规则从 _meta/catalog.json 读取。
"""
import os, re, json, argparse, shutil, subprocess, sys

from catalog import KB_DIR, require_catalog

RAW_DIR = os.path.join(KB_DIR, "00-钓鱼话术")


def build_keyword_map(catalog: dict) -> dict:
    kw_map = {}
    for c in catalog["categories"]:
        cat = c["dir"]
        kws = c.get("keywords", [])
        if kws:
            kw_map[cat] = "|".join(kws)
    return kw_map


def get_content_categories(catalog: dict) -> list:
    return [c["dir"] for c in catalog["categories"]
            if c["dir"] != "_meta" and c["dir"] != "00-钓鱼话术"]


def suggest_category(name: str, catalog: dict) -> str:
    kw_map = build_keyword_map(catalog)
    for cat, pattern in kw_map.items():
        if re.search(pattern, name, re.I):
            return cat
    return "02-提示与生成"


def list_raw_files() -> list:
    if not os.path.isdir(RAW_DIR):
        return []
    files = []
    for fname in sorted(os.listdir(RAW_DIR)):
        if not fname.endswith(".md") or fname == "data_structure.md":
            continue
        files.append(fname)
    return files


def find_promoted_fragment(raw_name: str, catalog: dict) -> tuple:
    topic = raw_name.replace(".md", "")
    categories = get_content_categories(catalog)

    for cat in categories:
        cat_dir = os.path.join(KB_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue
        # Exact match: 碎片-{topic}.md
        fragment_name = f"碎片-{topic}.md"
        if os.path.isfile(os.path.join(cat_dir, fragment_name)):
            return (cat, fragment_name)
        # Legacy: {topic}.md without 碎片- prefix
        if os.path.isfile(os.path.join(cat_dir, f"{topic}.md")):
            return (cat, f"{topic}.md")
        # Substring match
        for fname in os.listdir(cat_dir):
            if not fname.endswith(".md") or fname == "data_structure.md":
                continue
            if topic in fname or fname[3:-3] in topic:
                return (cat, fname)
    return (None, None)


def do_check(catalog: dict, verbose: bool = False):
    raw_files = list_raw_files()
    if not raw_files:
        print("📭 00-钓鱼话术/ 为空，没有待晋升的原始渔获。")
        return

    promoted = 0
    not_promoted = []

    for raw_name in raw_files:
        cat, existing = find_promoted_fragment(raw_name, catalog)
        if cat:
            promoted += 1
            if verbose:
                print(f"  ✅ {raw_name} → {cat}/{existing}")
        else:
            suggested = suggest_category(raw_name, catalog)
            not_promoted.append((raw_name, suggested))

    print(f"\n📊 晋升状态：{promoted} 已晋升 / {len(not_promoted)} 未晋升")
    print(f"   00-钓鱼话术/ 共 {len(raw_files)} 篇\n")

    if not_promoted:
        print("未晋升的原始渔获（建议分类）：")
        print("-" * 60)
        for raw_name, suggested in not_promoted:
            print(f"  ❌ {raw_name}  → 建议: {suggested}")
        print()
        print("  晋升命令示例：")
        for raw_name, suggested in not_promoted[:3]:
            topic = raw_name.replace(".md", "")
            print(f"    python promote.py --from \"{topic}\" --to {suggested}")
        if len(not_promoted) > 3:
            print(f"    ... 共 {len(not_promoted)} 个待晋升")
        print()
        print("💡 一键晋升所有未晋升的：python promote.py --batch")


def do_promote(topic: str, category: str):
    raw_path = os.path.join(RAW_DIR, f"{topic}.md")
    if not os.path.isfile(raw_path):
        print(f"❌ 找不到 00-钓鱼话术/{topic}.md")
        for fname in os.listdir(RAW_DIR):
            if topic.lower() in fname.lower():
                raw_path = os.path.join(RAW_DIR, fname)
                topic = fname.replace(".md", "")
                print(f"   ↳ 模糊匹配到: {fname}")
                break
        else:
            return False

    target_dir = os.path.join(KB_DIR, category)
    if not os.path.isdir(target_dir):
        print(f"❌ 目标分类目录不存在: {category}")
        return False

    target_name = f"碎片-{topic}.md"
    target_path = os.path.join(target_dir, target_name)

    if os.path.exists(target_path):
        print(f"⏭️  已存在: {category}/{target_name}，跳过")
        return True

    shutil.copy2(raw_path, target_path)
    fpath = os.path.join(KB_DIR, category, target_name)
    print(f"✅ {topic}.md → {fpath}")
    print(f"   📌 原始文件仍在 00-钓鱼话术/{topic}.md")
    print(f"   💡 确认无误后删除，或 --batch --delete 自动清理")
    return True


def do_batch(catalog: dict, auto_delete: bool = False):
    raw_files = list_raw_files()
    promoted_count = 0
    skipped_count = 0

    for raw_name in raw_files:
        cat, existing = find_promoted_fragment(raw_name, catalog)
        if cat:
            skipped_count += 1
            continue

        topic = raw_name.replace(".md", "")
        suggested = suggest_category(topic, catalog)
        raw_path = os.path.join(RAW_DIR, raw_name)
        target_dir = os.path.join(KB_DIR, suggested)
        target_name = f"碎片-{topic}.md"
        target_path = os.path.join(target_dir, target_name)

        if os.path.exists(target_path):
            skipped_count += 1
            continue

        shutil.copy2(raw_path, target_path)
        fpath = os.path.join(KB_DIR, suggested, target_name)
        promoted_count += 1
        print(f"  ✅ {raw_name} → {fpath}")
        if auto_delete:
            os.remove(raw_path)
            print(f"     🗑️ 已删除原始文件")

    print(f"\n📊 批量晋升完成：{promoted_count} 晋升 / {skipped_count} 跳过")

    # 自动触发 rebuild：有晋升就刷新索引
    if promoted_count > 0:
        print("\n🔄 自动触发索引刷新...")
        rebuild_script = os.path.join(os.path.dirname(__file__), "generate-index.py")
        result = subprocess.run([sys.executable, rebuild_script, "--rebuild"],
                                capture_output=True, text=True)
        for line in (result.stdout + result.stderr).split("\n"):
            if line.strip():
                print(f"   {line}")

    if not auto_delete and promoted_count > 0:
        print("💡 原始文件仍保留在 00-钓鱼话术/，确认无误后加 --delete 自动清理")


def main():
    p = argparse.ArgumentParser(description="碎片晋升工具")
    p.add_argument("--from", dest="from_topic", help="原始渔获主题名（不加 .md）")
    p.add_argument("--to", dest="category", help="目标分类目录名（如 03-品牌系统）")
    p.add_argument("--check", action="store_true", help="检查晋升状态")
    p.add_argument("--batch", action="store_true", help="批量自动晋升所有未晋升的")
    p.add_argument("--delete", action="store_true", help="晋升后删除原始文件（配合 --batch）")
    p.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    args = p.parse_args()

    catalog = require_catalog()

    if args.check:
        do_check(catalog, verbose=args.verbose)
    elif args.batch:
        do_batch(catalog, auto_delete=args.delete)
    elif args.from_topic and args.category:
        do_promote(args.from_topic, args.category)
    else:
        p.print_help()
        print()
        print("常用用法：")
        print("  python promote.py --check              # 检查晋升状态")
        print("  python promote.py --batch              # 一键晋升所有")
        print("  python promote.py --batch --delete     # 晋升并清理原始文件")
        print('  python promote.py --from "品牌资产深入" --to "03-品牌系统"')


if __name__ == "__main__":
    main()
