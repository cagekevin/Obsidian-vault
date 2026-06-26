"""
manifest_resolver.py — 管线唯一 manifest 解析入口

职责：通过 assets_manifest.json 将 asset key 解析为 latest 文件路径。
策略与 run_image_generator.py / run_video_generator.py 保持一致。

用法:
  from manifest_resolver import resolve, find_key_in_manifest, load_manifest
"""
import json, os, re

# 剥离后缀的正则：比例/分辨率 + 版本号
_STRIP_RE = re.compile(r"_(ar\d+x\d+_\d+[kK]|ar\d+x\d+|\d+[pPkK])$")
_STRIP_VER_RE = re.compile(r"_v\d+$")


def load_manifest(project_dir):
    """加载项目 assets_manifest.json，不存在则返回空 dict"""
    path = os.path.join(project_dir, "assets_manifest.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def resolve(asset_key, manifest, project_dir):
    """通过 manifest 将 asset key 解析为 latest 完整文件路径

    Args:
        asset_key: 资产名（如 "char_main_female" 或带后缀的 "char_main_female_ar4x3.png"）
        manifest: 从 load_manifest() 加载的字典
        project_dir: 项目根目录（用于拼接绝对路径）

    Returns:
        解析后的完整文件路径，或 None
    """
    clean = os.path.splitext(os.path.basename(asset_key))[0]

    # 1) 精确匹配 manifest
    entry = manifest.get(clean, {})
    for field in ("latest", "default"):
        rel = entry.get(field, "")
        if rel:
            full = os.path.join(project_dir, rel.replace("\\", "/"))
            if os.path.exists(full):
                return full

    # 2) 剥比例/分辨率/版本后缀后匹配
    stripped = _STRIP_VER_RE.sub("", clean)  # 先剥 _v1 等版本号
    stripped = _STRIP_RE.sub("", stripped)   # 再剥 _ar3x4_2K 等比例
    if stripped != clean:
        entry = manifest.get(stripped, {})
        for field in ("latest", "default"):
            rel = entry.get(field, "")
            if rel:
                full = os.path.join(project_dir, rel.replace("\\", "/"))
                if os.path.exists(full):
                    return full

    # 3) assets/ 下直接找文件兜底
    for ext in ("png", "jpg", "jpeg", "webp"):
        direct = os.path.join(project_dir, "assets", f"{clean}.{ext}")
        if os.path.exists(direct):
            return direct

    return None


def find_key_in_manifest(key, manifest):
    """在 manifest 中查找 key，返回 latest 路径（不拼接完整路径，用于校验）

    剥离策略：
      1. 原始名 → 2. 剥比例 → 3. 剥版本 → 4. 先剥比例再剥版本
    """
    candidates = [key]

    # 剥比例/分辨率后缀
    s = _STRIP_RE.sub("", key)
    if s != key:
        candidates.append(s)

    # 剥版本号后缀
    s2 = _STRIP_VER_RE.sub("", key)
    if s2 != key:
        candidates.append(s2)

    # 先剥比例再剥版本
    s3 = _STRIP_VER_RE.sub("", s) if s != key else ""
    if s3 and s3 != s:
        candidates.append(s3)

    for name in candidates:
        entry = manifest.get(name, {})
        v = entry.get("latest", "")
        if v:
            return v
    return None


def resolve_latest(ref, manifest, project_dir):
    """带 manifest 解析的垫图文件存在性检查

    先用 find_key_in_manifest 解析 latest 路径，
    如果存在则返回完整路径，否则返回 ref 自身（用于校验脚本的 warn 提示）。
    """
    resolved = find_key_in_manifest(os.path.splitext(os.path.basename(ref))[0], manifest)
    if resolved:
        full = os.path.join(project_dir, resolved.replace("\\", "/"))
        if os.path.exists(full):
            return full
    return ref if os.path.exists(ref) else None
