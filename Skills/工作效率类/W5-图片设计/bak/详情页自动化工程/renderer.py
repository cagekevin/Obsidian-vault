"""
HTML 渲染器 — 按布局规则生成图文分区结构
===========================================
PRD 4.1 [P0]: 每个 layout 按 gestalt_rules 生成：
  - 图区（渐变占位，预留产品/场景图位置）
  - 文字卡片（白底圆角、内留白、微阴影）

所有 11 种 layout 独立实现。
设计语言从 dicts/ 读取（typography.json, style_presets.json），不硬编码。
"""
import json, os, re, math
from typing import List, Optional
try:
    from PIL import Image; _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
DICTS_DIR  = os.path.join(ENGINE_DIR, "..", "dicts")
TYPO_PATH  = os.path.join(DICTS_DIR, "typo-scales.json")
STYLE_PATH = os.path.join(DICTS_DIR, "typo-modes.json")

def _load(p):
    with open(p, encoding="utf-8") as f: return json.load(f)

def _hex_to_rgb(h):
    if h.startswith("#") and len(h) == 7:
        return f"{int(h[1:3],16)}, {int(h[3:5],16)}, {int(h[5:7],16)}"
    # 颜色名非 hex 时用已知映射
    MAP = {"soft glowing pastel green": "123, 200, 130", "deep amber gold": "201, 169, 110",
           "warm amber": "212, 148, 74", "pale pink": "255, 192, 203"}
    if h.lower() in MAP:
        return MAP[h.lower()]
    return "128, 128, 128"  # fallback gray

def _is_dark(hex_color):
    if not hex_color or not hex_color.startswith("#"):
        return False
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return False
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r * 0.299 + g * 0.587 + b * 0.114) < 160


# ── 全局 CSS（设计系统） ──
GLOBAL_CSS = """
/* =============================================================
   Detail Page Design System
   11 种布局 + 图区占位 + 文字卡片
   ============================================================= */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ── 1. Reset ── */
*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

/* ── 2. Design Tokens ── */
:root {
  --serif-zh: "Noto Serif SC","Songti SC","STSong",serif;
  --serif-en: "Playfair Display","Noto Serif SC",serif;
  --sans: "Noto Sans SC",-apple-system,"PingFang SC","Microsoft YaHei UI",sans-serif;
  --mono: "IBM Plex Mono",ui-monospace,"SF Mono",Consolas,monospace;
  --sp-2: 4px;  --sp-3: 8px;   --sp-4: 12px;  --sp-5: 16px;
  --sp-6: 24px; --sp-7: 32px;  --sp-8: 40px;  --sp-9: 48px;
  --sp-10: 64px; --sp-11: 80px; --sp-12: 96px; --sp-13: 128px;
  --canvas-w: 790px;
  --canvas-h: 1200px;
  --body-bg: #0f0d0b;
}

/* ── 3. Typography Roles（字号/字族来自 typography.json，通过 CSS 变量注入） ── */
.mod .kicker {
  font-family: var(--ff-kicker); font-size: var(--fs-kicker); font-weight: var(--fw-kicker);
  letter-spacing: var(--ls-kicker); text-transform: uppercase;
  color: rgba(var(--ink-rgb), .45); margin-bottom: var(--sp-6);
}
.mod .h-display {
  font-family: var(--ff-display); font-weight: var(--fw-display);
  font-size: var(--fs-display); line-height: var(--lh-display);
  letter-spacing: var(--ls-display); color: var(--ink); margin-bottom: var(--sp-5);
}
.mod .h-xl {
  font-family: var(--ff-display); font-weight: var(--fw-xl);
  font-size: var(--fs-xl); line-height: var(--lh-xl);
  letter-spacing: var(--ls-xl); color: var(--ink); margin-bottom: var(--sp-5);
}
.mod .h-md {
  font-family: var(--ff-display); font-weight: var(--fw-md);
  font-size: var(--fs-md); line-height: var(--lh-md);
  letter-spacing: var(--ls-md); color: var(--ink); margin-bottom: var(--sp-4);
}
.mod .h-sub {
  font-family: var(--ff-sub); font-style: italic; font-weight: var(--fw-sub);
  font-size: var(--fs-sub); color: var(--mut); margin-bottom: var(--sp-5);
}
.mod .body {
  font-family: var(--ff-body); font-weight: var(--fw-body);
  font-size: var(--fs-body); line-height: var(--lh-body);
  color: rgba(var(--ink-rgb), .72); white-space: pre-line;
}
.mod .body-sm {
  font-family: var(--ff-body); font-weight: var(--fw-body-sm);
  font-size: var(--fs-body-sm); line-height: var(--lh-body-sm);
  color: rgba(var(--ink-rgb), .62);
}
.mod .stat-num {
  font-family: var(--ff-stat); font-weight: var(--fw-stat);
  font-size: var(--fs-stat); line-height: var(--lh-stat);
  letter-spacing: var(--ls-stat); color: var(--acc); margin-bottom: var(--sp-3);
}
.mod .stat-num-lg {
  font-family: var(--ff-stat); font-weight: var(--fw-stat-lg);
  font-size: var(--fs-stat-lg); line-height: var(--lh-stat-lg);
  letter-spacing: var(--ls-stat-lg); color: var(--acc); margin-bottom: var(--sp-3);
}
.mod .badge {
  display: inline-block; padding: 5px 18px;
  border: 1px solid rgba(var(--acc-rgb), .35); border-radius: 100px;
  font-family: var(--ff-kicker); font-size: var(--fs-badge); font-weight: var(--fw-kicker);
  letter-spacing: var(--ls-kicker); color: var(--acc);
}
.mod .badge-icon {
  display: inline-block; vertical-align: middle;
  width: 14px; height: 14px; margin-right: 6px;
}
.mod .badge-icon svg { width: 100%; height: 100%; }
.mod .badge-icon svg path, .mod .badge-icon svg rect, .mod .badge-icon svg circle,
.mod .badge-icon svg polygon, .mod .badge-icon svg line {
  fill: none; stroke: currentColor;
  stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
}
.mod .badge-set { display: flex; flex-wrap: wrap; gap: var(--sp-4); margin-top: var(--sp-6); }

/* ── 4. Layout Primitives ── */
.mod .stack     { display: flex; flex-direction: column; }
.mod .row       { display: flex; flex-direction: row; }
.mod .grow      { flex: 1; }
.mod .center    { text-align: center; }
.mod .right     { text-align: right; }
.mod .gap-3 { gap: var(--sp-3); } .mod .gap-4 { gap: var(--sp-4); }
.mod .gap-5 { gap: var(--sp-5); } .mod .gap-6 { gap: var(--sp-6); }
.mod .gap-7 { gap: var(--sp-7); } .mod .gap-8 { gap: var(--sp-8); }

/* ── 5. 文字卡片 ── */
.mod .text-card {
  background: var(--card-bg, #FFFFFF);
  --ink: #1A1A1A;
  --mut: #666666;
  --ink-rgb: 26, 26, 26;
  --acc-rgb: var(--card-acc-rgb, 128, 128, 128);
  border-radius: 4px;
  padding: var(--sp-8);
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  position: relative;
  z-index: 2;
}
.mod .card {
  background: var(--card-bg, #FFFFFF);
  --ink: #1A1A1A;
  --mut: #666666;
  --ink-rgb: 26, 26, 26;
  --acc-rgb: var(--card-acc-rgb, 128, 128, 128);
  border-radius: 4px;
  padding: var(--sp-8);
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  position: relative;
  z-index: 2;
}
.mod .text-card-center {
  display: flex; flex-direction: column;
  justify-content: center;
}
.mod .card-center {
  display: flex; flex-direction: column;
  justify-content: center;
}
.mod .sep {
  height: 1px; background: rgba(var(--ink-rgb), .10); border: 0;
  margin: var(--sp-6) 0; width: 64px;
}
.mod .num-step {
  font-family: var(--mono); font-size: 13px; font-weight: 600;
  letter-spacing: .10em; color: rgba(var(--acc-rgb), .55);
  margin-bottom: var(--sp-2);
}

/* ── 6.1 图区比例类 ── */
.mod .img-full { position: absolute; z-index: 0; inset: 0; background: var(--img-grad); }
.mod .img-r-1x1 { aspect-ratio: 1/1; }
.mod .img-r-3x4 { aspect-ratio: 3/4; }
.mod .img-r-4x3 { aspect-ratio: 4/3; }
.mod .img-r-16x9 { aspect-ratio: 16/9; }

/* ── 6. 图区占位（渐变） ── */
.mod .img-zone {
  position: absolute; z-index: 0;
  background: var(--img-grad);
}
/* 外框线 */
.mod .img-zone::after {
  content: ''; position: absolute; inset: 0;
  pointer-events: none; z-index: 1;
  border: 1px solid rgba(var(--acc-rgb), .06);
}
/* 光晕效果 */
.mod .img-zone::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 40%, rgba(255,255,255,0.06) 0%, transparent 70%);
}
.mod.dark .img-zone::before {
  background: radial-gradient(ellipse at 50% 40%, rgba(255,255,255,0.08) 0%, transparent 70%);
}

/* ── 7. 拱门遮罩布局 ── */
.mod .arch-frame {
  position: absolute; z-index: 0; inset: 0;
  background: var(--img-grad);
  clip-path: ellipse(70% 88% at 50% 12%);
}
.mod .arch-frame::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 30%, rgba(255,255,255,0.07) 0%, transparent 65%);
}

/* ── 9. 模块容器 ── */
.mod {
  position: relative; overflow: hidden; isolation: isolate;
  width: var(--canvas-w); height: var(--canvas-h);
  background: var(--bg);
}
.mod + .mod { border-top: 1px solid rgba(var(--acc-rgb), .06); }

/* ── 10. 分页编号 ── */
.mod .pg {
  position: absolute; bottom: 28px; right: 32px; z-index: 3;
  font-family: var(--mono); font-size: 13px; font-weight: 500;
  letter-spacing: .15em; color: rgba(var(--acc-rgb), .25);
}
""".strip()


class DetailPageRenderer:
    def __init__(self, canvas_size=(790, 1200)):
        self.w, self.h = canvas_size
        self._page = 0
        self._typo_data = _load(TYPO_PATH)
        self._style_data = _load(STYLE_PATH)

    @staticmethod
    def _img_gradient(bg, acc):
        return f"linear-gradient(145deg, {bg} 0%, {acc}22 40%, {bg} 100%)"

    def _get_mode(self, ek):
        """根据引擎 key 从 style_presets.json 获取排版模式"""
        return self._style_data.get("engines", {}).get(ek, {}).get("mode", "ecommerce")

    def _typo_css_vars(self, ek):
        """从 typography.json 生成排版 CSS 变量"""
        mode = self._get_mode(ek)
        typo = self._typo_data.get(mode, self._typo_data.get("ecommerce", {}))
        bands = typo.get("title_bands") if isinstance(typo.get("title_bands"), list) else None

        def band(i, key, default):
            if bands and i < len(bands):
                return bands[i].get(key, default)
            return default
        def tval(key, sub, default):
            v = typo.get(key)
            if isinstance(v, dict): return v.get(sub, default)
            return default

        vars_ = {
            "ff-display": typo.get("display_family", "serif"),
            "ff-body": typo.get("body_family", typo.get("sans_family", "sans-serif")),
            "ff-sub": typo.get("display_family", "serif") + ", serif",
            "ff-kicker": typo.get("mono_family", "monospace"),
            "ff-stat": typo.get("display_family", "serif"),
            "fs-display": f"{band(0, 'size', tval('title', 'size', 52))}px",
            "fs-xl": f"{band(1, 'size', tval('section_title', 'size', 40))}px",
            "fs-md": f"{band(2, 'size', tval('title', 'size', 30))}px",
            "fs-sub": f"{tval('quote', 'size', 24)}px",
            "fs-body": f"{tval('body', 'size', 18)}px",
            "fs-body-sm": f"{max(tval('body', 'size', 18) - 2, 14)}px",
            "fs-stat": f"{tval('caption', 'size', 14)}px",
            "fs-stat-lg": f"{tval('caption', 'size', 14) + 4}px",
            "fs-kicker": f"{tval('caption', 'size', 13)}px",
            "fs-badge": f"{tval('caption', 'size', 12)}px",
            "fs-step": f"{tval('caption', 'size', 13)}px",
            "fw-display": f"{band(0, 'weight', tval('title', 'weight', 500))}",
            "fw-xl": f"{band(1, 'weight', tval('section_title', 'weight', 500))}",
            "fw-md": f"{band(2, 'weight', 500)}",
            "fw-sub": f"{tval('quote', 'weight', 400)}",
            "fw-body": f"{tval('body', 'weight', 400)}",
            "fw-body-sm": f"{tval('body', 'weight', 400)}",
            "fw-stat": "600", "fw-stat-lg": "600", "fw-kicker": "500", "fw-step": "600",
            "ls-display": f"{band(0, 'tracking', 0.03)}em",
            "ls-xl": f"{band(1, 'tracking', 0.02)}em",
            "ls-md": f"{band(2, 'tracking', 0.02)}em",
            "ls-kicker": f"{tval('caption', 'tracking', 0.18)}em",
            "ls-step": f"{tval('caption', 'tracking', 0.10)}em",
            "ls-stat": "-.01em", "ls-stat-lg": "-.02em",
            "lh-display": "1.2", "lh-xl": "1.25", "lh-md": "1.3",
            "lh-body": f"{tval('body', 'line_height', 1.7)}",
            "lh-body-sm": "1.65", "lh-stat": "1.1", "lh-stat-lg": "1.05",
        }
        return "".join(f"--{k}:{v};" for k, v in vars_.items())

    def _render(self, lk, txt, ek, ri={}):
        self._page += 1
        bg = ri.get("background_hex", "#FFF")
        ink = ri.get("text_primary", "#111")
        mut = ri.get("text_secondary", "#888")
        acc = ri.get("accent", "#07A")
        card_bg = "#FFFFFF"
        card_acc = acc

        def cssv(k, v): return f"--{k}:{v};"
        typo_vars = self._typo_css_vars(ek)
        vars_ = (
            cssv("bg", bg) + cssv("ink", ink) + cssv("mut", mut) + cssv("acc", acc) +
            cssv("card-bg", card_bg) +
            f"--ink-rgb:{_hex_to_rgb(ink)};" +
            f"--acc-rgb:{_hex_to_rgb(acc)};" +
            f"--card-acc-rgb:{_hex_to_rgb(card_acc)};" +
            f"--img-grad:{self._img_gradient(bg, acc)};" +
            typo_vars
        )

        is_dark = _is_dark(bg)
        dark_cls = " dark" if is_dark else ""

        # ── 分派 ──
        d = {
            "hero_banner":                self._t_hero,
            "ingredient_zigzag_left":     self._t_ingredient,
            "ingredient_zigzag_right":    self._t_ingredient,
            "split_before_after":         self._t_split,
            "texture_smear_bottom_text":  self._t_bottom,
            "model_lifestyle_side_anchor":self._t_side,
            "three_column_features":      self._t_grid,
            "authority_endorsement_split":self._t_authority,
            "full_bleed_lifestyle":       self._t_overlay,
            "texture_center_floating":    self._t_texture_center,
            "module_arch_window":         self._t_arch_window,
        }
        fn = d.get(lk, self._t_default)
        return fn(txt, vars_, dark_cls, lk)

    # ═══════════════════════════════════════════
    #  各布局模板
    # ═══════════════════════════════════════════

    def _kicker(self, lk):
        """根据布局返回默认 kicker（仅供文档参考，AI 生成的 draft 必须提供 kicker 字段）"""
        return ""  # 不应走到这里

    def _badges(self, t):
        """渲染 badge 列表，支持 badge_N 文字 + badge_N_icon SVG（由 draft JSON 提供）"""
        keys = [k for k in sorted(t) if k.startswith("badge_") and not k.endswith("_icon") and t[k]]
        items = []
        for k in keys:
            text = t[k]
            icon = t.get(f"{k}_icon", "")
            if icon:
                items.append(f'<span class="badge"><span class="badge-icon">{icon}</span>{text}</span>')
            else:
                items.append(f'<span class="badge">{text}</span>')
        return "".join(items)

    def _t_hero(self, t, v, dc, lk=""):
        """01 首屏：全幅渐变图区 + 下中部文字卡片"""
        badges = self._badges(t)
        kicker = t["kicker"]
        return f'''<div class="mod{dc}" style="{v}">
  <div class="img-zone" style="inset:0;"></div>
  <div class="card" style="position:absolute;left:var(--sp-12);right:var(--sp-12);top:var(--sp-11);padding:var(--sp-9) var(--sp-8);">
    <p class="kicker">{kicker}</p>
    <h1 class="h-display">{t.get("hero_title","")}</h1>
    <p class="h-sub">{t.get("subtitle","")}</p>
    <div class="body" style="margin-top:var(--sp-4)">{t.get("body_text","")}</div>
    {('<div class="badge-set">'+badges+'</div>') if badges else ''}
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_ingredient(self, t, v, dc, lk):
        """03/04 成分 Z 字：左文右图 / 左图右文"""
        is_left = "left" in lk
        feats = "".join(f'<div class="body" style="padding:10px 0;border-bottom:1px solid rgba(var(--ink-rgb),.08)">{t[k]}</div>'
                       for k in sorted(t) if k.startswith("feature_") and t[k])
        highlight = t.get("highlight", "")
        body_text = t.get("body_text", "")
        kicker = t["kicker"]
        card_html = f'''<div class="card card-center" style="flex:4;margin:var(--sp-11) var(--sp-8);border-radius:6px;">
    <p class="kicker">{kicker}</p>
    <h1 class="h-xl">{t.get("section_title","")}</h1>
    <div class="body-sm" style="margin-bottom:var(--sp-5)">{t.get("subtitle","")}</div>
    <hr class="sep">
    {('<p class="body" style="color:var(--acc);font-weight:500">'+highlight+'</p>') if highlight else ''}
    {('<p class="body">'+body_text+'</p>') if body_text else ''}
    {feats}
  </div>'''
        img_html = '<div class="img-zone" style="position:relative;flex:6;"></div>'
        # left = 左文右图（card 先，img 后）；right = 左图右文（img 先，card 后）
        left_first, right_second = (card_html, img_html) if is_left else (img_html, card_html)
        return f'''<div class="mod{dc}" style="{v};display:flex;flex-direction:row;">
  {left_first}
  {right_second}
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_split(self, t, v, dc, lk):
        """02 前后对比 / 痛点唤醒：上半 kicker+标题+副标题，下半双列 痛点 | 数据"""
        feats = "".join(f'<div class="body" style="padding:10px 0;border-bottom:1px solid rgba(var(--ink-rgb),.08)">{t[k]}</div>'
                       for k in sorted(t) if k.startswith("feature_") and t[k])
        datas = "".join(f'<p class="stat-num-lg">{t[k]}</p>'
                       for k in sorted(t) if k.startswith("data_") and t[k])
        kicker = t["kicker"]
        return f'''<div class="mod{dc}" style="{v}">
  <div class="text-card" style="position:absolute;inset:var(--sp-11) var(--sp-12);display:flex;flex-direction:column;justify-content:center;">
    <p class="kicker">{kicker}</p>
    <h1 class="h-xl" style="max-width:75%">{t.get("section_title","")}</h1>
    <div class="body" style="max-width:70%;margin-bottom:var(--sp-7)">{t.get("subtitle","")}</div>
    <div class="row" style="gap:var(--sp-10);align-items:stretch;">
      <div class="stack gap-3" style="flex:1;">{feats}</div>
      <div class="stack gap-3" style="flex:1;text-align:right;justify-content:center;">{datas}</div>
    </div>
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_bottom(self, t, v, dc, lk):
        """05 肤感底部：上图 65% + 下文字卡片 35%"""
        badges = self._badges(t)
        kicker = t["kicker"]
        return f'''<div class="mod{dc}" style="{v}">
  <div class="card" style="position:absolute;left:var(--sp-12);right:var(--sp-12);top:var(--sp-11);padding:var(--sp-7) var(--sp-8);text-align:center;">
    <p class="kicker" style="text-align:center">{kicker}</p>
    <h1 class="h-md">{t.get("section_title","")}</h1>
    <div class="body-sm" style="margin-bottom:var(--sp-3)">{t.get("subtitle","")}</div>
    <div class="body">{t.get("body_text","")}</div>
    {('<div class="badge-set" style="justify-content:center">'+badges+'</div>') if badges else ''}
  </div>
  <div class="img-zone" style="position:absolute;top:45%;bottom:0;left:0;right:0;"></div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_side(self, t, v, dc, lk):
        """07 模特侧边：左 50% 文字卡片 + 右 50% 图区"""
        steps = "".join(
            f'<div class="stack" style="gap:var(--sp-2)"><span class="num-step">STEP {i+1:02d}</span><div class="body" style="color:var(--ink)">{t[k]}</div></div>'
            for i, k in enumerate(k for k in sorted(t) if k.startswith("step_") and t[k]))
        kicker = t["kicker"]
        return f'''<div class="mod{dc}" style="{v};display:flex;flex-direction:row;">
  <div class="card card-center" style="flex:5;margin:var(--sp-11) var(--sp-8);border-radius:6px;">
    <p class="kicker">{kicker}</p>
    <h2 class="h-xl" style="font-style:italic;font-family:var(--serif-en)">{t.get("quote_text","")}</h2>
    <hr class="sep">
    <div class="stack gap-6">{steps}</div>
  </div>
  <div class="img-zone" style="position:relative;flex:5;"></div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_grid(self, t, v, dc, lk):
        """08 三列网格：全幅渐变背景 + 三列文字卡片"""
        feats = [t[k] for k in sorted(t) if k.startswith("feature_") and t[k]]
        cols = "".join(
            f'<div class="card card-center" style="padding:var(--sp-7) var(--sp-5);text-align:center;gap:var(--sp-4);border-radius:6px;">'
            f'<div class="body" style="font-weight:600;color:var(--acc);font-size:18px">{f.split("：")[0] if "：" in f else ""}</div>'
            f'<div class="body-sm">{f.split("：",1)[1] if "：" in f else f}</div></div>'
            for f in feats)
        kicker = t["kicker"]
        return f'''<div class="mod{dc}" style="{v}">
  <div class="img-zone" style="inset:0;"></div>
  <div class="card" style="position:absolute;inset:var(--sp-11) var(--sp-12);display:flex;flex-direction:column;justify-content:center;padding:var(--sp-9) var(--sp-8);">
    <p class="kicker" style="text-align:center">{kicker}</p>
    <h1 class="h-xl" style="text-align:center">{t.get("hero_title","")}</h1>
    <div class="row" style="gap:var(--sp-5);margin-top:var(--sp-7);justify-content:center;">{cols}</div>
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_authority(self, t, v, dc, lk):
        """06 专家背书：左 40% 图区（专家像） + 右 60% 文字卡片"""
        datas = "".join(f'<p class="stat-num">{t[k]}</p>'
                       for k in sorted(t) if k.startswith("data_") and t[k])
        kicker = t["kicker"]
        return f'''<div class="mod{dc}" style="{v};display:flex;flex-direction:row;">
  <div class="img-zone" style="position:relative;flex:4;"></div>
  <div class="card card-center" style="flex:6;margin:var(--sp-11) var(--sp-8) var(--sp-11) 0;border-radius:6px;">
    <p class="kicker" style="text-align:right;margin-left:auto;">{kicker}</p>
    <h1 class="h-xl" style="text-align:right">{t.get("section_title","")}</h1>
    <hr class="sep" style="margin-left:auto;">
    <div class="stack gap-4" style="align-items:flex-end;">{datas}</div>
    <div class="body" style="margin-top:var(--sp-6);text-align:right;">{t.get("body_text","")}</div>
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_overlay(self, t, v, dc, lk):
        """09 全幅场景：满屏渐变图区 + 底部暗色渐变叠加文字"""
        return f'''<div class="mod{dc}" style="{v}">
  <div class="img-zone" style="inset:0;"></div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:35%;z-index:2;
    background:linear-gradient(transparent, rgba(0,0,0,0.65));display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 var(--sp-12);">
    <h1 class="h-xl" style="color:#fff;margin-bottom:var(--sp-5)">{t.get("tagline","")}</h1>
    <div class="body" style="color:rgba(255,255,255,0.6)">{t.get("body_text","")}</div>
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_texture_center(self, t, v, dc, lk):
        """10 悬浮微距：左右 25% 各一文字卡片 + 中间 50% 图区"""
        feats = [t[k] for k in sorted(t) if k.startswith("feature_") and t[k]]
        left_badges = feats[:len(feats)//2] if feats else []
        right_badges = feats[len(feats)//2:] if feats else []
        left_html = "".join(f'<span class="badge">{b}</span>' for b in left_badges)
        right_html = "".join(f'<span class="badge">{b}</span>' for b in right_badges)
        return f'''<div class="mod{dc}" style="{v};display:flex;flex-direction:row;">
  <div class="card card-center" style="flex:3;margin:var(--sp-11) 0 var(--sp-11) var(--sp-8);padding:var(--sp-7);border-radius:6px;gap:var(--sp-3);">
    <p class="kicker">质地特写</p>
    <h1 class="h-md">{t.get("section_title","")}</h1>
    <div class="body-sm">{t.get("subtitle","")}</div>
    {('<div class="badge-set" style="flex-direction:column;gap:var(--sp-3)">'+left_html+'</div>') if left_html else ''}
  </div>
  <div class="img-zone" style="position:relative;flex:4;margin:0;"></div>
  <div class="card card-center" style="flex:3;margin:var(--sp-11) var(--sp-8) var(--sp-11) 0;padding:var(--sp-7);border-radius:6px;gap:var(--sp-3);text-align:right;">
    <div class="body">{t.get("body_text","")}</div>
    {('<div class="badge-set" style="flex-direction:column;gap:var(--sp-3);align-items:flex-end;">'+right_html+'</div>') if right_html else ''}
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_arch_window(self, t, v, dc, lk):
        """11 拱门遮罩：满幅拱门图区 + 上下文字卡片"""
        return f'''<div class="mod{dc}" style="{v}">
  <div class="arch-frame"></div>
  <div class="card card-center" style="position:absolute;top:var(--sp-8);left:var(--sp-12);right:var(--sp-12);height:8%;padding:var(--sp-5) var(--sp-8);border-radius:6px;text-align:center;">
    <h1 class="h-md" style="margin-bottom:0;font-size:24px;">{t.get("section_title","")}</h1>
  </div>
  <div class="card card-center" style="position:absolute;bottom:var(--sp-8);left:var(--sp-12);right:var(--sp-12);height:auto;padding:var(--sp-6) var(--sp-8);border-radius:6px;text-align:center;">
    <div class="body-sm">{t.get("subtitle","")}</div>
    {('<div class="body" style="margin-top:var(--sp-3)">'+t.get("body_text","")+'</div>') if t.get("body_text") else ''}
  </div>
  <div class="pg">{self._page:02d}</div>
</div>'''

    def _t_default(self, t, v, dc, lk=""):
        return self._t_hero(t, v, dc, lk)

    # ── 长页 ──
    def render_full_page(self, mods, ek="", out=""):
        self._page = 0
        blocks = ""
        for m in mods:
            html = self._render(m["layout_key"], m["texts"], m.get("engine_key", ek),
                                m.get("render_instruction", {}))
            blocks += html + "\n"

        full = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<style>{GLOBAL_CSS}
body{{background:var(--body-bg);width:var(--canvas-w);margin:0 auto;}}
</style>
</head>
<body>
{blocks}
</body></html>"""
        if out:
            os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(full)
        return full

    # ── 遮罩 ──
    @staticmethod
    def generate_edge_mask(w, h, style="linear", amp=20, freq=3.0):
        if not _HAS_PIL:
            raise RuntimeError("需安装 Pillow")
        from PIL import Image as P
        import PIL.ImageDraw as D
        m = P.new("L", (w, h), 0)
        d = D.Draw(m)
        if style == "linear":
            for y in range(h):
                d.line([(0, y), (w, y)], fill=int(255 * y / h))
        elif style == "sine":
            for x in range(w):
                wy = h * .5 + amp * math.sin(x * 2 * math.pi * freq / w)
                d.line([(x, max(0, min(h, int(wy)))), (x, h)], fill=255)
        elif style == "soft_brush":
            import random
            r = random.Random(42)
            for x in range(0, w, 4):
                by = h * (.3 + .4 * r.random())
                for dx in range(min(4, w - x)):
                    ly = max(0, min(h, int(by + r.randint(-amp, amp))))
                    d.line([(x + dx, ly), (x + dx, h)], fill=255)
        elif style == "arch":
            for x in range(w):
                ye = int(h - math.sqrt(max(0, (1 - (x - w // 2) * (x - w // 2) / ((w // 2) * (w // 2))) * h * h * 4)))
                d.line([(x, max(0, min(h, ye))), (x, h)], fill=255)
        elif style == "jagged":
            for x in range(0, w, 6):
                y = h * .5 + (x % 12 - 6) * (amp // 3)
                y = max(0, min(h, int(y)))
                for dx in range(min(6, w - x)):
                    d.line([(x + dx, y), (x + dx, h)], fill=255)
        return m

    @staticmethod
    def apply_arch_mask(img):
        if not _HAS_PIL:
            raise RuntimeError("需安装 Pillow")
        from PIL import Image as P
        import PIL.ImageDraw as D
        w, h = img.size
        img = img.convert("RGBA")
        m = P.new("L", (w, h), 0)
        d = D.Draw(m)
        for x in range(w):
            ye = int(h - math.sqrt(max(0, (1 - (x - w // 2) * (x - w // 2) / ((w // 2) * (w // 2))) * h * h * 4)))
            d.line([(x, max(0, min(h, ye))), (x, h)], fill=255)
        r = P.new("RGBA", (w, h), (0, 0, 0, 0))
        r.paste(img, (0, 0), m)
        return r

    @staticmethod
    def stitch_blocks(blocks, op=5.0, es=None, bg=(255, 255, 255)):
        if not _HAS_PIL:
            raise RuntimeError("需安装 Pillow")
        if not blocks:
            raise ValueError
        from PIL import Image as P
        bw, bh = blocks[0].width, blocks[0].height
        oh = int(bh * op / 100)
        if es is None:
            es = ["linear"] * (len(blocks) - 1)
        th = len(blocks) * bh - (len(blocks) - 1) * oh
        c = P.new("RGBA", (bw, th), bg + (255,))
        cy = 0
        for i, b in enumerate(blocks):
            if b.mode != "RGBA":
                b = b.convert("RGBA")
            if i == 0:
                c.paste(b, (0, 0), b)
                cy = bh - oh
            else:
                ts = b.crop((0, 0, bw, oh))
                bs = b.crop((0, oh, bw, bh))
                mk = DetailPageRenderer.generate_edge_mask(bw, oh, style=es[i - 1] if i - 1 < len(es) else "linear",
                                                           amp=oh // 4, freq=2.5)
                c.paste(ts, (0, cy), mk)
                cy += oh
                c.paste(bs, (0, cy), bs)
                cy += bh - oh
        return c
