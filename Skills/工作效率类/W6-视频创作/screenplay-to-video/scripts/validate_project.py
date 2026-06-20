#!/usr/bin/env python3
"""
validate_project.py — 管线硬闸门校验脚本

所有图片/视频生成前，必须先通过本脚本校验。
校验不通过时返回非零退出码，阻断后续流程。

用法:
  python validate_project.py <项目路径>                         # 全部校验
  python validate_project.py <项目路径> --type assets           # 只校验资产 config
  python validate_project.py <项目路径> --type data --group 2   # 校验指定组的故事板数据
  python validate_project.py <项目路径> --type shots video      # 校验逐镜 + 视频

类型:
  assets     资产定妆照/场景图 config (configs/char_*.json, scene_*.json, product_*.json)
  data       故事板结构化数据 (prompts/storyboard_data_N.json)
  storyboard 故事板装配后 config (configs/storyboard_N.json)
  shots      逐镜单张 config (prompts/group{N}_prompt_shot_*.json)
  video      视频提示词 (prompts/group{N}_prompt_video.json)
"""

import json, os, sys, re, glob
from manifest_resolver import find_key_in_manifest as find_manifest_ref, resolve_latest

EXIT_CODE = 0

# ── 输出 ──

def fail(msg):
    global EXIT_CODE
    EXIT_CODE = 1
    print(f"  ❌ {msg}")

def ok(msg=""):
    if msg:
        print(f"  ✅ {msg}")

def warn(msg):
    print(f"  ⚠️  {msg}")

def fatal(msg):
    fail(msg)
    sys.exit(1)

# ── 通用 ──

TOKEN_RE = re.compile(r"--token-[\w-]+[\s:]")
FIELD_TEMPLATES = {
    "assets":   ["name", "prompt", "aspect_ratio", "resolution", "model", "output_dir"],
    "data":     ["group", "shots", "refs"],
    "shot":     ["name", "prompt", "aspect_ratio", "resolution", "model", "output_dir", "reference_image_paths"],
    "video":    ["name", "prompt", "model", "aspect_ratio", "resolution", "duration"],
}
ASSET_PATTERNS = re.compile(r"^(char_|scene_|product_)")
STORYBOARD_CONFIG_PAT = re.compile(r"^storyboard_\d+\.json$")

def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        fail(f"无法读取 JSON: {path} — {e}")
        return None

def is_image_prompt(filepath):
    """判断一个 JSON 是否用于图片生成（非视频）"""
    name = os.path.basename(filepath)
    return "video" not in name

# ── 校验器 ──

def check_required_fields(obj, fields, label):
    """检查必填字段是否存在且非空"""
    for f in fields:
        v = obj.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
            fail(f"{label}: 缺少必填字段 '{f}'")

def check_tokens(prompt, label):
    """检查 prompt 首部是否包含 --token-style/render/shading 风格令牌"""
    first_300 = prompt[:300]
    if not TOKEN_RE.search(first_300):
        fail(f"{label}: prompt 首部缺少 --token-style/render/shading 令牌 (前300字符内)")

def check_no_dollar_not(prompt, label):
    """检查图片 prompt 中是否出现 $not"""
    if "$not" in prompt or "$not " in prompt or "$not)" in prompt:
        fail(f"{label}: 图片 prompt 中不允许出现 $not")

def check_manifest_refs(refs, manifest, project_dir, label):
    """检查 refs[] 中的 key 在 assets_manifest.json 中是否存在"""
    if not refs:
        warn(f"{label}: refs[] 为空")
        return
    for key in refs:
        latest = find_manifest_ref(key, manifest)
        if latest:
            full = os.path.join(project_dir, latest.replace("\\", "/"))
            if os.path.exists(full):
                ok(f"  {key} → {latest}")
            else:
                warn(f"  {key} → {latest} (文件不存在)")
        else:
            fail(f"{label}: refs 中 '{key}' 在 assets_manifest.json 中不存在")

def check_shots(shots, label):
    """检查 shots[] 完整性"""
    if not shots:
        fail(f"{label}: shots 为空，至少需要 1 个镜头")
        return
    for i, s in enumerate(shots):
        tag = f"{label} shot[{i}]"
        if not s.get("title", "").strip():
            fail(f"{tag}: 缺少 'title'")
        en = s.get("en", "").strip()
        if not en:
            fail(f"{tag}: 缺少 'en' (英文画面描述)")


# ── 按类型校验 ──

def validate_assets(project_dir, manifest):
    """Type A: 资产 config (char_/scene_/product_)"""
    config_dir = os.path.join(project_dir, "configs")
    if not os.path.isdir(config_dir):
        warn("configs/ 目录不存在")
        return

    files = sorted(os.listdir(config_dir))
    found = False
    for fname in files:
        if not fname.endswith(".json"):
            continue
        if STORYBOARD_CONFIG_PAT.match(fname):
            continue
        if fname in ("audit-rules.json", "group_map.md"):
            continue
        if not ASSET_PATTERNS.match(fname):
            continue  # 跳过非资产模式的 JSON
        found = True
        path = os.path.join(config_dir, fname)
        label = f"assets/{fname}"
        cfg = load_json(path)
        if cfg is None:
            continue

        check_required_fields(cfg, FIELD_TEMPLATES["assets"], label)
        prompt = cfg.get("prompt", "")
        if prompt:
            check_tokens(prompt, label)
            check_no_dollar_not(prompt, label)

        # 检查 output_dir 指向 assets/
        out = cfg.get("output_dir", "")
        if out and "assets" not in out.replace("\\", "/").split("/"):
            warn(f"{label}: output_dir 不在 assets/ 目录下 ({out})")

        # 检查 reference_image_paths 是否存在（走 manifest 解析，空数组跳过）
        for ref in cfg.get("reference_image_paths", []):
            if not resolve_latest(ref, manifest, project_dir):
                warn(f"{label}: 垫图文件不存在: {ref}")

    if not found:
        ok("  无资产 config 需要校验")

def validate_data(project_dir, group):
    """Type B data: 故事板结构化数据"""
    data_path = os.path.join(project_dir, "prompts", f"storyboard_data_{group}.json")
    if not os.path.exists(data_path):
        fail(f"storyboard_data_{group}.json 不存在")
        return

    label = f"data/group{group}"
    data = load_json(data_path)
    if data is None:
        return

    check_required_fields(data, FIELD_TEMPLATES["data"], label)
    manifest_path = os.path.join(project_dir, "assets_manifest.json")
    manifest = load_json(manifest_path) if os.path.exists(manifest_path) else {}

    refs = data.get("refs", [])
    if refs:
        check_manifest_refs(refs, manifest, project_dir, label)

    shots = data.get("shots", [])
    check_shots(shots, label)

def validate_storyboard_config(project_dir, group, manifest):
    """Type B config: 故事板装配后的 config（脚本自动生成，轻量校验）"""
    config_path = os.path.join(project_dir, "configs", f"storyboard_{group}.json")
    if not os.path.exists(config_path):
        ok(f"  storyboard_{group}.json 尚未生成 (正常 — 还未执行装配)")
        return

    label = f"configs/storyboard_{group}.json"
    cfg = load_json(config_path)
    if cfg is None:
        return

    check_required_fields(cfg, ["name", "prompt", "aspect_ratio", "model", "output_dir"], label)

    # 图片 prompt 绝不用 $not
    prompt = cfg.get("prompt", "")
    if prompt:
        check_no_dollar_not(prompt, label)

    # 垫图文件存在性（走 manifest 解析）
    for ref in cfg.get("reference_image_paths", []):
        if not resolve_latest(ref, manifest, project_dir):
            warn(f"{label}: 垫图文件不存在: {ref}")

def validate_shots(project_dir, group, manifest):
    """Type C: 逐镜 config"""
    pattern = os.path.join(project_dir, "prompts", f"group{group}_prompt_shot_*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        ok(f"  组 {group} 无逐镜 config")

    for path in files:
        fname = os.path.basename(path)
        label = f"shots/{fname}"
        cfg = load_json(path)
        if cfg is None:
            continue

        # 支持单条配置 (name/prompt) 和批量配置 (prompts[])
        items = []
        if "prompts" in cfg:
            items = cfg["prompts"]
        else:
            items = [cfg]

        for item in items:
            check_required_fields(item, FIELD_TEMPLATES["shot"], label)
            prompt = item.get("prompt", "")
            if prompt:
                check_tokens(prompt, label)
                check_no_dollar_not(prompt, label)
            for ref in item.get("reference_image_paths", []):
                if not resolve_latest(ref, manifest, project_dir):
                    warn(f"{label}: 垫图文件不存在: {ref}")

def validate_video(project_dir, group, manifest):
    """Type D: 视频提示词"""
    video_path = os.path.join(project_dir, "prompts", f"group{group}_prompt_video.json")
    if not os.path.exists(video_path):
        # 可能是未生成，不报错（board_to_video.py 会处理）
        return

    label = f"video/group{group}"
    cfg = load_json(video_path)
    if cfg is None:
        return

    check_required_fields(cfg, FIELD_TEMPLATES["video"], label)

    # 视频特有检查
    duration = cfg.get("duration", 0)
    if duration > 15:
        fail(f"{label}: duration={duration} 超过 API 限制 15s")
    model = cfg.get("model", "")
    if "seedance" not in model.lower() and "video" not in model.lower():
        warn(f"{label}: model='{model}' 可能不是视频模型")
    prompt = cfg.get("prompt", "")
    if not prompt.strip():
        fail(f"{label}: prompt 为空")

    # 视频允许 $not，不做检查
    # 检查垫图（走 manifest 解析，CDN 路径跳过）
    for ref in cfg.get("reference_image_paths", []):
        if ref.startswith("http"):
            continue
        if not resolve_latest(ref, manifest, project_dir):
            warn(f"{label}: 垫图文件不存在: {ref}")


# ── 主入口 ──

def parse_args(argv):
    types = ["assets", "data", "storyboard", "shots", "video"]
    selected = []
    group = None
    project_dir = None

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--type":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                if argv[i] in types:
                    selected.append(argv[i])
                i += 1
            continue
        elif a.startswith("--type="):
            for t in a.split("=", 1)[1].split(","):
                t = t.strip()
                if t in types:
                    selected.append(t)
            i += 1
            continue
        elif a == "--group":
            group = argv[i+1] if i+1 < len(argv) else None
            i += 2
            continue
        elif a.startswith("--group="):
            group = a.split("=", 1)[1]
            i += 1
            continue
        elif a == "--help" or a == "-h":
            print(__doc__.strip())
            sys.exit(0)
        elif a.startswith("--"):
            print(f"未知参数: {a}")
            sys.exit(1)
        else:
            project_dir = a
            i += 1

    if not selected:
        selected = types[:]
    if not group:
        group = detect_groups(project_dir)
    return project_dir, selected, group

def detect_groups(project_dir):
    """自动检测项目中有哪些组号"""
    if not project_dir:
        return [1]
    groups = set()
    prompts_dir = os.path.join(project_dir, "prompts")
    if os.path.isdir(prompts_dir):
        for fname in os.listdir(prompts_dir):
            m = re.search(r"storyboard_data_(\d+)\.json$", fname)
            if m:
                groups.add(int(m.group(1)))
            m = re.search(r"group(\d+)_", fname)
            if m:
                groups.add(int(m.group(1)))
    return sorted(groups) if groups else [1]

def run(project_dir, types=None, group=None):
    """程序化调用入口"""
    global EXIT_CODE
    EXIT_CODE = 0

    if not os.path.isdir(project_dir):
        fatal(f"项目目录不存在: {project_dir}")

    print(f"\n ═══ 管线自检: {os.path.basename(project_dir)} ═══\n")

    manifest_path = os.path.join(project_dir, "assets_manifest.json")
    manifest = load_json(manifest_path) if os.path.exists(manifest_path) else {}

    if types is None:
        types = ["assets", "data", "storyboard", "shots", "video"]
    if group is None:
        group = detect_groups(project_dir)
    if isinstance(group, int):
        group = [group]

    # 资产 config 不依赖组号，全局只跑一次
    if "assets" in types:
        print(f" ── Assets ──")
        print(f"  [资产 config]")
        validate_assets(project_dir, manifest)

    for g in group if isinstance(group, (list, tuple)) else [group]:
        if g is None:
            continue
        print(f" ── Group {g} ──")

        if "data" in types:
            print(f"  [故事板数据]")
            validate_data(project_dir, g)

        if "storyboard" in types:
            print(f"  [故事板 config]")
            validate_storyboard_config(project_dir, g, manifest)

        if "shots" in types:
            print(f"  [逐镜 config]")
            validate_shots(project_dir, g, manifest)

        if "video" in types:
            print(f"  [视频提示词]")
            validate_video(project_dir, g, manifest)

    print(f"\n ─── 结果: {'全部通过 ✅' if EXIT_CODE == 0 else '有错误未通过 ❌'} ───\n")
    return EXIT_CODE == 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_dir, types, group = parse_args(sys.argv[1:])
    if not project_dir:
        print(__doc__)
        sys.exit(1)

    success = run(project_dir, types, group)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
