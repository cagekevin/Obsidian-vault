"""
翻译官 — 公共工具函数

提取自 export.py / export_to_lovart.py / lovart-web.py / init_project.py
"""

import json, os, re, sys, logging
from datetime import datetime


# ── 日志 ──

def setup_logger(name="translator"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


log = setup_logger()


# ── 文件读写 ──

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data, indent=2):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def read_txt(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def fatal(msg):
    log.error(msg)
    sys.exit(1)


# ── 路径 / 命名 ──

def safe_name(name):
    text = str(name or "").strip().lower().replace(" ", "-")
    text = re.sub(r'[\\/:"*?<>|]+', "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "element"


def reference_file_name(el):
    name = el.get("name", "element")
    if el.get("is_background"):
        return f"ref_bg_{safe_name(name)}.txt"
    return f"ref_{safe_name(name)}.txt"


def is_reference(el):
    return el.get("reference", True) is not False


def json_filename_to_element_name(json_filename):
    name = json_filename
    for prefix in ("ref_", "ref_bg_"):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    name = name.rsplit(".json", 1)[0]
    name = name.replace("_", " ")
    return " ".join(w.capitalize() for w in name.split())


def output_dir(project_dir, input_name="project.json"):
    base = os.path.splitext(input_name)[0]
    if base == "project":
        return os.path.join(project_dir, "output")
    style_tag = base.replace("project_", "")
    return os.path.join(project_dir, f"output_{style_tag}")


def style_tag_from_input(input_name):
    base = os.path.splitext(input_name)[0]
    if base == "project":
        return "original"
    return base.replace("project_", "")


# ── 资产引用解析 ──

def resolve_manifest_ref(asset_key, manifest, project_dir):
    """从 manifest 解析 asset_key 的 latest 路径，找不到返回 None"""
    ext = os.path.splitext(asset_key)[0]
    clean = os.path.splitext(os.path.basename(asset_key))[0]
    for name in [clean, ext]:
        entry = manifest.get(name, {})
        for field in ("latest", "default"):
            rel = entry.get(field, "")
            if rel:
                full = os.path.join(project_dir, rel.replace("\\", "/"))
                if os.path.exists(full):
                    return full
    return None


def scan_asset_refs(ref_key, project_dir, assets_dir_name="assets"):
    """扫描 assets/ 下匹配 ref_key 前缀的所有文件（含 _v1, _v2 等），返回最新版本路径"""
    ad = os.path.join(project_dir, assets_dir_name)
    if not os.path.isdir(ad):
        return None
    prefix = ref_key.lower()
    candidates = []
    for f in os.listdir(ad):
        if f.lower().startswith(prefix) and f.lower().endswith((".png", ".jpg", ".jpeg")):
            candidates.append(f)
    if not candidates:
        return None
    def version_key(name):
        m = re.search(r'_v(\d+)', name)
        return int(m.group(1)) if m else 0
    best = max(candidates, key=version_key)
    return os.path.join(project_dir, assets_dir_name, best).replace("\\", "/")


def check_asset_exists(filename, assets_dir):
    basename = os.path.basename(filename)
    target = os.path.join(assets_dir, basename)
    if os.path.exists(target):
        return True, basename
    return False, basename


def list_all_ref_versions(element_name, json_filename, assets_dir):
    if not os.path.isdir(assets_dir):
        return []
    if json_filename:
        prefix = os.path.splitext(json_filename)[0]
        return [f for f in sorted(os.listdir(assets_dir))
                if f.lower().endswith((".png", ".jpg", ".jpeg")) and f.startswith(prefix)]
    return []


def extract_appearance(prompt_text):
    for marker in ("APPEARANCE:", "ENVIRONMENT:"):
        pattern = rf"{re.escape(marker)}\s*\n(.*?)(?=LAYOUT\s)"
        m = re.search(pattern, prompt_text, re.DOTALL)
        if m:
            return m.group(1).strip()
    return prompt_text.strip()


def load_config(project_dir):
    config_path = os.path.join(project_dir, "lovart_config.json")
    if os.path.exists(config_path):
        return load_json(config_path)
    return {}


# ── QC 共享 ──

def get_all_scenes(data):
    groups = data.get("storyboard_groups", [])
    scenes = []
    for g in groups:
        scenes.extend(g.get("scenes", []))
    return scenes, groups


def get_elements(data):
    return data.get("elements", [])
