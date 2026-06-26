"""共享 catalog 加载器 — catalog.json 的单一读取入口。

所有脚本通过 `from catalog import load_catalog, KB_DIR` 使用，
消除 5 份重复的 load_catalog() 函数。
"""
import os, json

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
CATALOG_PATH = os.path.join(KB_DIR, "_meta", "catalog.json")


def load_catalog():
    """加载 catalog.json，失败时返回 (None, 错误信息)"""
    if not os.path.exists(CATALOG_PATH):
        return None, (f"❌ 找不到 {CATALOG_PATH}\n"
                      f"   请运行 python scripts/generate-index.py --rebuild 初始化")
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"❌ catalog.json 格式错误: {e}"


def require_catalog():
    """加载 catalog.json，失败时直接退出"""
    catalog, err = load_catalog()
    if err:
        print(err)
        exit(1)
    return catalog


def get_agent_skill_path(kb_dir=None):
    """从 catalog.json 读取 agent_skill.py 的绝对路径"""
    base = kb_dir or KB_DIR
    catalog = require_catalog()
    rel = catalog.get("paths", {}).get("agent_skill", "")
    if not rel:
        print("❌ catalog.json 中未配置 paths.agent_skill")
        exit(1)
    path = os.path.normpath(os.path.join(base, rel))
    if not os.path.exists(path):
        print(f"❌ agent_skill.py 不存在: {path}")
        exit(1)
    return path
