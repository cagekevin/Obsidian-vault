#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-video-book.py — 以"视频创作快速导航" MOC 为主轴，
复用 generate-wiki-html.py 的解析能力，生成手机可看的单文件 HTML。

用法：python build-video-book.py
输出：G:\\Obsidian-vault\\Tools\\output\\视频创作手册.html
"""

import re
import sys
from datetime import datetime
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
MOC_PATH = VAULT_ROOT / "Wiki" / "concepts" / "视频创作快速导航.md"
WIKI_DIR = VAULT_ROOT / "Wiki"
OUTPUT_DIR = VAULT_ROOT / "Tools" / "output"
OUTPUT_FILE = OUTPUT_DIR / "视频创作手册.html"

# ── 复用 generate-wiki-html.py 的解析函数（文件名带连字符，用 importlib） ──
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "generate_wiki_html",
    VAULT_ROOT / "scripts" / "generate-wiki-html.py"
)
_gwh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gwh)
parse_concept_page = _gwh.parse_concept_page
md_to_html = _gwh.md_to_html
print("[OK] 复用 generate-wiki-html.py 解析函数（importlib 加载）")


# ── 从 MOC 收集引用的所有页面 ──────────────────────────────────
def collect_pages(moc_path):
    text = moc_path.read_text(encoding="utf-8")
    links = re.findall(r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]', text)
    seen, pages = set(), []
    for link in links:
        link = link.strip()
        if not link or link in seen or link.startswith("http"):
            continue
        seen.add(link)
        for sub in ("concepts", "sources", ""):
            cand = (WIKI_DIR / sub / f"{link}.md") if sub else (WIKI_DIR / f"{link}.md")
            if cand.exists():
                pages.append((link, cand))
                break
    return pages


# ── 抽取 MOC 的章节（用于生成目录） ─────────────────────────────
def extract_chapters(moc_text):
    return [m.strip() for m in re.findall(r'^##\s+(.+)$', moc_text, re.MULTILINE)]


# ── 移动优先 HTML 模板 ─────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes">
<meta name="theme-color" content="#1a1a1a">
<title>视频创作手册 · Wiki 视频创作导航</title>
<style>
:root {{
  --bg: #1a1a1a; --fg: #e6e6e6; --muted: #999;
  --accent: #ffb84d; --link: #66b3ff;
  --code-bg: #2a2a2a; --border: #3a3a3a;
  --card-bg: #232323; --bq: #4a3a1a;
}}
@media (prefers-color-scheme: light) {{
  :root {{
    --bg: #fafafa; --fg: #222; --muted: #666;
    --accent: #d4690a; --link: #0066cc;
    --code-bg: #f0f0f0; --border: #ddd;
    --card-bg: #fff; --bq: #fff5e6;
  }}
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
body {{
  background: var(--bg); color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 17px; line-height: 1.75;
  margin: 0; padding: 0;
}}
.wrap {{ max-width: 720px; margin: 0 auto; padding: 24px 20px 100px; }}
.topbar {{
  position: sticky; top: 0; z-index: 100;
  background: var(--bg); border-bottom: 1px solid var(--border);
  padding: 12px 20px; display: flex; align-items: center; gap: 12px;
  margin: -24px -20px 24px;
}}
.topbar .title {{ font-size: 14px; font-weight: 700; color: var(--accent); flex: 1; }}
.topbar .toc-btn {{
  background: var(--card-bg); border: 1px solid var(--border);
  color: var(--fg); padding: 6px 12px; border-radius: 6px;
  font-size: 13px; font-weight: 600; cursor: pointer;
}}
.toc-drawer {{
  position: fixed; top: 0; right: 0; bottom: 0; width: 300px;
  background: var(--card-bg); border-left: 1px solid var(--border);
  transform: translateX(100%); transition: transform 0.25s;
  overflow-y: auto; padding: 20px; z-index: 200;
  box-shadow: -4px 0 16px rgba(0,0,0,0.2);
}}
.toc-drawer.open {{ transform: translateX(0); }}
.toc-overlay {{
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  opacity: 0; pointer-events: none; transition: opacity 0.25s; z-index: 150;
}}
.toc-overlay.open {{ opacity: 1; pointer-events: auto; }}
.toc-drawer h3 {{ font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 12px; }}
.toc-drawer ol {{ padding-left: 20px; margin: 0; }}
.toc-drawer li {{ margin: 6px 0; }}
.toc-drawer a {{ color: var(--link); text-decoration: none; font-size: 14px; }}
.cover {{ text-align: center; padding: 60px 0 40px; border-bottom: 2px solid var(--accent); margin-bottom: 40px; }}
.cover h1 {{ font-size: 2.2em; margin: 0 0 12px; color: var(--accent); letter-spacing: 2px; }}
.cover .sub {{ color: var(--muted); font-size: 0.95em; margin: 0 0 8px; }}
.cover .meta {{ color: var(--muted); font-size: 0.8em; margin-top: 20px; }}
h1 {{ font-size: 1.8em; margin: 1.5em 0 0.6em; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
h2 {{ font-size: 1.4em; margin: 1.4em 0 0.5em; }}
h3 {{ font-size: 1.15em; margin: 1.2em 0 0.4em; }}
h4 {{ font-size: 1.05em; margin: 1em 0 0.3em; }}
p {{ margin: 0 0 1em; }}
ul, ol {{ padding-left: 1.5em; margin: 0 0 1em; }}
li {{ margin: 4px 0; }}
strong {{ font-weight: 700; }}
em {{ font-style: italic; }}
a {{ color: var(--link); text-decoration: none; border-bottom: 1px dashed var(--link); }}
a:hover {{ border-bottom-style: solid; }}
code {{ background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-size: 14px; font-family: ui-monospace, "SF Mono", Consolas, monospace; }}
pre {{ background: var(--code-bg); padding: 16px; border-radius: 8px; overflow-x: auto; margin: 0 0 1em; border: 1px solid var(--border); }}
pre code {{ background: none; padding: 0; font-size: 13px; line-height: 1.6; }}
blockquote {{ border-left: 3px solid var(--accent); background: var(--bq); padding: 12px 16px; margin: 1em 0; border-radius: 0 6px 6px 0; font-style: italic; }}
table {{ width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 14px; display: block; overflow-x: auto; }}
th, td {{ border-bottom: 1px solid var(--border); padding: 10px 8px; text-align: left; }}
th {{ font-weight: 700; color: var(--muted); text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; }}
hr {{ border: none; border-top: 1px solid var(--border); margin: 2.5em 0; }}
.page-section {{
  background: var(--card-bg); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; margin: 1.5em 0;
}}
.page-section .page-title {{
  font-size: 1.5em; margin: 0 0 4px; color: var(--accent);
  border-bottom: 2px solid var(--accent); padding-bottom: 8px;
}}
.page-section .page-source {{ color: var(--muted); font-size: 12px; margin: 0 0 16px; font-family: ui-monospace, "SF Mono", Consolas, monospace; }}

/* 打印优化（A5 纸张友好的小屏幕） */
@media print {{
  body {{ font-size: 11pt; line-height: 1.55; }}
  .topbar, .toc-drawer, .toc-overlay {{ display: none !important; }}
  .wrap {{ max-width: 100%; padding: 0; }}
  .cover {{ padding: 20px 0; margin-bottom: 20px; page-break-after: always; }}
  .cover h1 {{ font-size: 1.8em; }}
  .page-section {{
    page-break-inside: avoid; break-inside: avoid;
    margin: 1em 0; padding: 14px; border-radius: 8px;
  }}
  .page-section .page-title {{ font-size: 1.2em; }}
  h1 {{ font-size: 1.5em; page-break-after: avoid; }}
  h2 {{ font-size: 1.2em; page-break-after: avoid; }}
  h3, h4 {{ page-break-after: avoid; }}
  pre {{ page-break-inside: avoid; }}
  table {{ page-break-inside: avoid; font-size: 10pt; }}
  a {{ color: var(--link); border-bottom: none; }}
}}
</style>
</head>
<body>
<div class="wrap">
<div class="topbar">
  <span class="title">视频创作手册</span>
  <button class="toc-btn" onclick="toggleToc()">☰ 目录</button>
</div>
<div class="toc-overlay" id="tocOverlay" onclick="toggleToc()"></div>
<div class="toc-drawer" id="tocDrawer">
  <h3>目录</h3>
  <ol>
{toc_items}
  </ol>
</div>
<div class="cover">
  <h1>视频创作手册</h1>
  <p class="sub">从剧本到成片的完整 Wiki 知识库</p>
  <p class="sub">{n_pages} 个核心页面 · 全本内嵌 · 离线可读</p>
  <p class="meta">生成于 {timestamp} · 由 Wiki 视频创作快速导航 编译</p>
</div>
{moc_html}
<hr>
{pages_html}
</div>
<script>
function toggleToc() {{
  document.getElementById('tocDrawer').classList.toggle('open');
  document.getElementById('tocOverlay').classList.toggle('open');
}}
</script>
</body>
</html>
"""


# ── 主流程 ─────────────────────────────────────────────────────
def main():
    if not MOC_PATH.exists():
        print(f"[ERR] 找不到 MOC: {MOC_PATH}")
        sys.exit(1)

    print(f"[1/4] 读取 MOC: {MOC_PATH.name}")
    moc_page = parse_concept_page(MOC_PATH)
    moc_raw = MOC_PATH.read_text(encoding="utf-8")
    chapters = extract_chapters(moc_raw)
    print(f"       发现 {len(chapters)} 个章节")
    for i, ch in enumerate(chapters, 1):
        print(f"         {i}. {ch}")

    print(f"[2/4] 收集引用页面...")
    pages = collect_pages(MOC_PATH)
    print(f"       找到 {len(pages)} 个页面")

    print(f"[3/4] 渲染 HTML...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 渲染 MOC 自身（目录主页）
    moc_html = md_to_html(moc_page["body"])

    # 渲染每个引用页面
    pages_html_parts = []
    for name, path in pages:
        page = parse_concept_page(path)
        body_html = md_to_html(page["body"])
        # 把正文里的 [[PageName]] 替换为锚点链接
        body_html = re.sub(
            r'<a href="#" class="wiki-link" data-name="([^"]+)">[^<]+</a>',
            lambda m: f'<a href="#page-{m.group(1)}">{m.group(1)}</a>',
            body_html
        )
        pages_html_parts.append(
            f'<section class="page-section" id="page-{name}">'
            f'<h2 class="page-title">{page["title"] or name}</h2>'
            f'<p class="page-source">来源：Wiki/{path.relative_to(WIKI_DIR).as_posix()}</p>'
            f'{body_html}'
            f'</section>'
        )
    pages_html = "\n".join(pages_html_parts)

    # 目录项（MOC 的 9 个章节 + 所有页面锚点）
    toc_items = []
    for i, ch in enumerate(chapters, 1):
        anchor = re.sub(r'[^\w\u4e00-\u9fff\-]', '', ch).strip()
        toc_items.append(f'<li><a href="#h-{anchor}">{i}. {ch}</a></li>')
    for name, _ in pages:
        toc_items.append(f'<li style="margin-left:-16px;font-size:12px;color:var(--muted)"><a href="#page-{name}">→ {name}</a></li>')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_html = HTML_TEMPLATE.format(
        toc_items="\n".join(toc_items),
        n_pages=len(pages),
        timestamp=timestamp,
        moc_html=moc_html,
        pages_html=pages_html,
    )

    print(f"[4/4] 写入: {OUTPUT_FILE}")
    OUTPUT_FILE.write_text(final_html, encoding="utf-8")

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"[DONE] {size_kb:.1f} KB · {len(pages)} 个页面已内嵌")
    print(f"       路径: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
