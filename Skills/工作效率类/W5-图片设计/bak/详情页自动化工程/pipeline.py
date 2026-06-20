"""
完整管线：加载 draft JSON → 渲染 HTML
  python3 pipeline.py --json draft_xxx.json
  python3 pipeline.py              （默认走 draft_hkh.json）
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.renderer import DetailPageRenderer

d = os.path.dirname(os.path.abspath(__file__))

import argparse
parser = argparse.ArgumentParser(description="详情页自动化管线")
parser.add_argument("--json", type=str, default=None, help="draft JSON 文件路径")
parser.add_argument("--out", type=str, default=None, help="输出 HTML 路径")
args = parser.parse_args()

# ── 加载初稿 ──
if args.json:
    with open(args.json, encoding="utf-8") as f:
        draft = json.load(f)
    print(f"📂 从 {args.json} 加载初稿")
else:
    default_json = os.path.join(d, "draft_hkh.json")
    if os.path.exists(default_json):
        with open(default_json, encoding="utf-8") as f:
            draft = json.load(f)
        print(f"📂 从 {default_json} 加载初稿")
    else:
        print("❌ 未找到 draft JSON，请指定 --json")
        sys.exit(1)

engine_key = draft.get("engine_key", "premium_luxury")

# ── 渲染（render_instruction 由 AI 在 draft JSON 中直接提供） ──
modules = []
prompts = []
for mod in draft["modules"]:
    modules.append({
        "layout_key": mod["layout_key"],
        "texts": mod["texts"],
        "render_instruction": mod.get("render_instruction", {}),
        "engine_key": engine_key,
    })
    fp = mod.get("flow_prompt", "")
    if fp:
        prompts.append(f"═══ {mod['name']} ({mod['layout_key']}) ═══\n{fp}\n")

r = DetailPageRenderer()
out_path = args.out or os.path.join(d, "output", f"detail_{draft.get('project_id', 'output')}.html")
os.makedirs(os.path.dirname(out_path) or d, exist_ok=True)
r.render_full_page(modules, ek=engine_key, out=out_path)

# ── 输出图片提示词 TXT ──
if prompts:
    txt_path = out_path.rsplit(".", 1)[0] + "_prompts.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"引擎: {engine_key}\n产品色: {draft.get('product_color','')}\n项目: {draft.get('project_id','')}\n\n" + "\n".join(prompts))
    print(f"📝 图片提示词: {os.path.relpath(txt_path, d)}")

size = os.path.getsize(out_path)
print(f"✅ 管线完成：{len(modules)} 模块 → {out_path} ({size}B)")
print(f"   引擎: {engine_key} | 输出: {os.path.relpath(out_path, d)}")
print(f"   浏览器打开文件即可查看")
