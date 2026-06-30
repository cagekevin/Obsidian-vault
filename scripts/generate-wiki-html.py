# generate-wiki-html.py — 将 Wiki/ 知识图谱渲染为单页 HTML (Scandi Minimalist Edition)
# Visual Architecture: 斯堪的纳维亚极简风

import re, json
from pathlib import Path

WIKI_DIR = Path(__file__).parent.parent / "Wiki"
OUTPUT   = WIKI_DIR / "index.html"

# ── 1. 解析 index.md 获取分类结构 ──────────────────────────
def parse_index(text):
    sections = []
    current_cat = None
    current_sub = None
    for line in text.splitlines():
        if line.startswith("## "):
            current_cat = line[3:].strip()
            current_sub = None
            sections.append({"category": current_cat, "subcategories": {}, "items": []})
        elif line.startswith("### "):
            current_sub = line[4:].strip()
            if current_sub:
                sections[-1]["subcategories"][current_sub] = []
        elif line.strip().startswith("- [["):
            m = re.match(r'- \[\[([^\]]+)\]\]\s*—\s*(.+?)(?:\s*\(status:\s*(\w+)\))?\s*$', line.strip())
            if m:
                name = m.group(1).split("/")[-1]
                desc = m.group(2).strip()
                status = m.group(3) or ""
                item = {"name": name, "desc": desc, "status": status}
                sections[-1]["items"].append(item)
                if current_sub and current_sub in sections[-1]["subcategories"]:
                    sections[-1]["subcategories"][current_sub].append(item)
    return sections

# ── 2. 解析概念页正文 ──────────────────────────────────────
def parse_concept_page(path):
    text = path.read_text(encoding="utf-8")
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            kv = re.match(r'(\w+):\s*(.*)', line)
            if kv:
                fm[kv.group(1)] = kv.group(2).strip().strip('"')
    body = text
    if m:
        body = text[m.end():].strip()
    title = fm.get("title", "")
    if not title:
        tm = re.match(r'^#\s+(.+)', body)
        if tm:
            title = tm.group(1).strip()
    status = fm.get("status", "")
    return {"title": title, "status": status, "body": body}

# ── 3. 收集所有概念页内容 ──────────────────────────────────
def collect_pages(sections):
    pages = {}
    for sec in sections:
        for item in sec["items"]:
            page_path = WIKI_DIR / "concepts" / f"{item['name']}.md"
            if page_path.exists():
                pages[item["name"]] = parse_concept_page(page_path)
            else:
                pages[item["name"]] = {"title": item["name"], "status": item["status"], "body": ""}
    return pages

# ── 4. Markdown → HTML ────────────────────────────
def md_to_html(text):
    lines = text.split('\n')
    html = []
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            if in_code:
                html.append(f'<pre><code>{chr(10).join(code_buf)}</code></pre>')
                code_buf = []
                in_code = False
                i += 1
                continue
            else:
                in_code = True
                i += 1
                continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            in_table = True
            table_buf.append(line)
            if i + 1 < len(lines) and ('|' not in lines[i+1] or not lines[i+1].strip().startswith('|')):
                html.append(render_table(table_buf))
                table_buf = []
                in_table = False
            i += 1
            continue
        else:
            if in_table:
                html.append(render_table(table_buf))
                table_buf = []
                in_table = False

        line = re.sub(r'\[\[([^\]]+)\]\]', r'<a href="#" class="wiki-link" data-name="\1">\1</a>', line)

        hm = re.match(r'^(#{1,4})\s+(.+)$', line)
        if hm:
            level = len(hm.group(1))
            html.append(f'<h{level}>{hm.group(2)}</h{level}>')
            i += 1
            continue

        if re.match(r'^---+$', line.strip()):
            html.append('<hr>')
            i += 1
            continue

        if line.startswith('> '):
            qlines = []
            while i < len(lines) and lines[i].startswith('> '):
                qlines.append(lines[i][2:])
                i += 1
            html.append(f'<blockquote>{"<br>".join(qlines)}</blockquote>')
            continue

        if re.match(r'^[-*+]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^[-*+]\s+', lines[i]):
                item = re.sub(r'^[-*+]\s+', '', lines[i])
                item = re.sub(r'\[\[([^\]]+)\]\]', r'<a href="#" class="wiki-link" data-name="\1">\1</a>', item)
                item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                item = re.sub(r'\*(.+?)\*', r'<em>\1</em>', item)
                item = re.sub(r'`(.+?)`', r'<code>\1</code>', item)
                items.append(item)
                i += 1
            lis = ''.join(f'<li>{item}</li>' for item in items)
            html.append(f'<ul>{lis}</ul>')
            continue

        if re.match(r'^\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                item = re.sub(r'^\d+\.\s+', '', lines[i])
                item = re.sub(r'\[\[([^\]]+)\]\]', r'<a href="#" class="wiki-link" data-name="\1">\1</a>', item)
                item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                item = re.sub(r'\*(.+?)\*', r'<em>\1</em>', item)
                item = re.sub(r'`(.+?)`', r'<code>\1</code>', item)
                items.append(item)
                i += 1
            lis = ''.join(f'<li>{item}</li>' for item in items)
            html.append(f'<ol>{lis}</ol>')
            continue

        if not line.strip():
            i += 1
            continue

        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
        html.append(f'<p>{line}</p>')
        i += 1

    if in_code:
        html.append(f'<pre><code>{chr(10).join(code_buf)}</code></pre>')
    if in_table:
        html.append(render_table(table_buf))

    return '\n'.join(html)

def render_table(rows):
    if len(rows) < 2: return ''
    headers = [h.strip() for h in rows[0].strip('|').split('|')]
    data_rows = rows[2:]
    html = '<table><thead><tr>'
    for h in headers: html += f'<th>{h}</th>'
    html += '</tr></thead><tbody>'
    for row in data_rows:
        cells = [c.strip() for c in row.strip('|').split('|')]
        html += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
    html += '</tbody></table>'
    return html

# ── 5. 渲染高阶 HTML ────────────────────────────────────────────
def render_html(sections, pages):
    tree = []
    for sec in sections:
        cat = sec["category"]
        subs = []
        for sub_name, sub_items in sec["subcategories"].items():
            subs.append({
                "name": sub_name,
                "items": [{"name": it["name"], "desc": it["desc"], "status": it["status"]} for it in sub_items]
            })
        standalone = [it for it in sec["items"] if not any(it["name"] in [si["name"] for s in subs for si in s["items"]] for s in subs)]
        tree.append({
            "category": cat,
            "subcategories": subs,
            "standalone": [{"name": it["name"], "desc": it["desc"], "status": it["status"]} for it in standalone]
        })

    body_html_map = {}
    for name, page in pages.items():
        body_html_map[name] = md_to_html(page["body"])

    tree_json = json.dumps(tree, ensure_ascii=False)
    pages_json = json.dumps({name: {"title": p["title"], "status": p["status"]} for name, p in pages.items()}, ensure_ascii=False)

    # 这里的 HTML 注入了极致的斯堪的纳维亚系统
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>某人的数字花园 | Knowledge Graph</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js"></script>
<style>
    :root {{
        --color-bg-base: oklch(0.99 0.00 0);      
        --color-bg-hover: oklch(0.97 0.00 0);     
        --color-text-main: oklch(0.20 0.02 250);  
        --color-text-muted: oklch(0.60 0.02 250); 
        --color-border: oklch(0.94 0.01 250);     
        --color-accent: oklch(0.50 0.15 200);     

        --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'SF Mono', SFMono-Regular, Consolas, monospace;

        --space-8: 8px; --space-16: 16px; --space-24: 24px;
        --space-32: 32px; --space-48: 48px; --space-64: 64px; --space-96: 96px;
        
        --radius-sm: 6px;
        --ease-snap: cubic-bezier(0.2, 0, 0, 1);
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
        font-family: var(--font-sans); background-color: var(--color-bg-base);
        color: var(--color-text-main); display: flex; height: 100vh;
        overflow: hidden; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;
    }}

    /* --- Sidebar --- */
    .sidebar {{
        width: 280px; min-width: 280px; border-right: 1px solid var(--color-border);
        display: flex; flex-direction: column; background-color: var(--color-bg-base);
    }}
    .sidebar-header {{ padding: var(--space-32) var(--space-24) var(--space-24); }}
    .brand {{ font-size: 16px; font-weight: 800; letter-spacing: -0.02em; color: var(--color-text-main); margin-bottom: var(--space-24); cursor: pointer; }}
    .brand span {{ display: block; font-size: 10px; font-weight: 600; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.15em; margin-top: var(--space-8); }}
    
    .search-box {{
        width: 100%; padding: 10px 12px; background: var(--color-bg-base);
        border: 1px solid var(--color-border); border-radius: var(--radius-sm);
        color: var(--color-text-main); font-size: 13px; font-family: inherit;
        transition: border-color 0.2s var(--ease-snap);
    }}
    .search-box:focus {{ border-color: var(--color-text-muted); outline: none; }}
    
    .tree {{ flex: 1; overflow-y: auto; padding: 0 var(--space-16) var(--space-24); }}
    .tree::-webkit-scrollbar {{ width: 4px; }}
    .tree::-webkit-scrollbar-thumb {{ background: var(--color-border); border-radius: 4px; }}

    .nav-group-title {{
        font-size: 11px; font-weight: 700; color: var(--color-text-muted);
        text-transform: uppercase; letter-spacing: 0.1em; margin: var(--space-24) 0 var(--space-8);
        padding-left: var(--space-8); cursor: pointer; user-select: none;
    }}
    .nav-group-title:hover {{ color: var(--color-text-main); }}
    .nav-group-title::before {{ content: "▾ "; }}
    .nav-group-title.collapsed::before {{ content: "▸ "; }}

    .nav-sub-title {{
        font-size: 12px; font-weight: 600; color: var(--color-text-muted);
        margin: var(--space-8) 0 4px; padding-left: var(--space-16); cursor: pointer; user-select: none;
    }}
    .nav-sub-title:hover {{ color: var(--color-text-main); }}
    .nav-sub-title::before {{ content: "▾ "; font-size: 10px; }}
    .nav-sub-title.collapsed::before {{ content: "▸ "; }}

    .nav-item {{
        padding: 6px var(--space-8); font-size: 13px; font-weight: 500;
        color: var(--color-text-muted); cursor: pointer; border-radius: var(--radius-sm);
        transition: all 0.2s var(--ease-snap); margin-bottom: 2px; padding-left: var(--space-16);
    }}
    .nav-item:hover {{ background-color: var(--color-bg-hover); color: var(--color-text-main); }}
    .nav-item.active {{ background-color: var(--color-bg-hover); color: var(--color-text-main); font-weight: 700; }}
    .sub-items .nav-item {{ padding-left: var(--space-32); }}
    
    .cat-items, .sub-items {{ overflow: hidden; }}
    .cat-items.collapsed, .sub-items.collapsed {{ display: none; }}

    .stats {{ font-size: 11px; font-weight: 600; color: var(--color-text-muted); padding: var(--space-16) var(--space-24); border-top: 1px solid var(--color-border); letter-spacing: 0.05em; text-transform: uppercase; }}

    /* --- Main Content --- */
    .main-content {{ flex: 1; overflow-y: auto; display: flex; justify-content: center; align-items: flex-start; padding: var(--space-48) var(--space-24); box-sizing: border-box; }}
    .main-content .article-container {{ width: 100%; max-width: 800px; min-height: calc(100vh - var(--space-96)); box-sizing: border-box; }}
    .main-content::-webkit-scrollbar {{ width: 6px; }}
    .main-content::-webkit-scrollbar-thumb {{ background: var(--color-border); border-radius: 4px; }}
    
    .article-title {{ font-size: 48px; line-height: 1.1; font-weight: 800; margin-bottom: var(--space-16); letter-spacing: -0.03em; }}
    
    .article-meta {{
        font-size: 12px; font-weight: 600; color: var(--color-text-muted);
        text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: var(--space-64);
        display: flex; gap: var(--space-16); align-items: center; border-bottom: 1px solid var(--color-border); padding-bottom: var(--space-24);
    }}
    .status-badge {{ color: var(--color-accent); border: 1px solid var(--color-border); padding: 2px var(--space-8); border-radius: var(--radius-sm); }}

    /* Markdown Body Styling (Strict Scandi) */
    .article-body p {{ font-size: 16px; line-height: 1.8; font-weight: 400; margin-bottom: var(--space-24); color: var(--color-text-main); }}
    .article-body h2 {{ font-size: 24px; font-weight: 700; margin: var(--space-32) 0 var(--space-16); letter-spacing: -0.02em; }}
    .article-body h3 {{ font-size: 18px; font-weight: 600; margin: var(--space-24) 0 var(--space-8); }}
    .article-body ul, .article-body ol {{ padding-left: var(--space-24); margin-bottom: var(--space-24); font-size: 16px; line-height: 1.8; color: var(--color-text-main); }}
    .article-body li {{ margin-bottom: var(--space-8); }}
    .article-body a {{ color: var(--color-accent); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.2s; }}
    .article-body a:hover {{ border-color: var(--color-accent); }}
    .article-body strong {{ font-weight: 700; }}
    
    .article-body code {{ font-family: var(--font-mono); font-size: 14px; background: var(--color-bg-hover); padding: 2px 6px; border-radius: 4px; border: 1px solid var(--color-border); }}
    .article-body pre {{ background: var(--color-bg-hover); padding: var(--space-24); border-radius: var(--radius-sm); font-size: 14px; overflow-x: auto; margin-bottom: var(--space-24); border: 1px solid var(--color-border); line-height: 1.6; }}
    .article-body pre code {{ background: none; padding: 0; border: none; }}
    
    .article-body blockquote {{ border-left: 2px solid var(--color-text-main); padding-left: var(--space-24); margin: var(--space-32) 0; color: var(--color-text-muted); font-style: italic; font-size: 18px; }}
    
    .article-body table {{ width: 100%; border-collapse: collapse; margin-bottom: var(--space-32); font-size: 14px; }}
    .article-body th, .article-body td {{ border-bottom: 1px solid var(--color-border); padding: var(--space-16) var(--space-8); text-align: left; }}
    .article-body th {{ font-weight: 600; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-size: 12px; }}
    
    .article-body hr {{ border: none; border-top: 1px solid var(--color-border); margin: var(--space-32) 0; }}

    /* Overview Cards */
    .overview-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--space-24); margin-top: var(--space-32); }}
    .overview-card {{ border: 1px solid var(--color-border); padding: var(--space-24); border-radius: var(--radius-sm); cursor: pointer; transition: border-color 0.2s var(--ease-snap); background: var(--color-bg-base); }}
    .overview-card:hover {{ border-color: var(--color-text-muted); }}
    .overview-card h2 {{ font-size: 16px; font-weight: 700; margin-bottom: var(--space-8); }}
    .overview-card .count {{ font-size: 32px; font-weight: 800; color: var(--color-text-muted); margin-bottom: var(--space-16); font-family: var(--font-mono); }}
    .overview-card .sub-desc {{ font-size: 13px; color: var(--color-text-muted); line-height: 1.5; }}

    /* Search Results */
    .search-result-item {{ padding: var(--space-16) 0; border-bottom: 1px solid var(--color-border); cursor: pointer; transition: padding-left 0.2s var(--ease-snap); }}
    .search-result-item:hover {{ padding-left: var(--space-8); }}
    .search-result-title {{ font-size: 16px; font-weight: 700; margin-bottom: 4px; color: var(--color-text-main); }}
    .search-result-desc {{ font-size: 14px; color: var(--color-text-muted); }}
    .search-match {{ background: rgba(0,0,0,0.1); padding: 0 4px; border-radius: 2px; color: var(--color-text-main); font-weight: 600; }}

</style>
</head>
<body>

<aside class="sidebar">
    <div class="sidebar-header">
        <div class="brand" onclick="showOverview()">
            某人的数字花园
            <span>Knowledge Graph</span>
        </div>
        <input class="search-box" id="search" type="text" placeholder="Search knowledge..." oninput="onSearch()">
    </div>
    <div class="tree" id="tree"></div>
    <div class="stats" id="stats"></div>
</aside>

<main class="main-content" id="main">
    <article class="article-container" id="content-area"></article>
</main>

<script>
const treeData = {tree_json};
const pagesMeta = {pages_json};
const bodyHtml = {json.dumps(body_html_map, ensure_ascii=False)};

function renderTree() {{
    const el = document.getElementById('tree');
    let html = '';
    let totalItems = 0;
    treeData.forEach(cat => {{
        html += `<div class="nav-group-title collapsed" onclick="toggleCat(this)">${{cat.category}}</div>`;
        html += `<div class="cat-items collapsed" id="cat-${{cat.category}}">`;
        
        cat.subcategories.forEach(sub => {{
            html += `<div class="nav-sub-title collapsed" onclick="toggleSub(this)">${{sub.name}}</div>`;
            html += `<div class="sub-items collapsed" id="sub-${{sub.name}}">`;
            sub.items.forEach(item => {{
                html += `<div class="nav-item" onclick="showDetail('${{item.name}}', this)" data-name="${{item.name}}">${{item.name}}</div>`;
                totalItems++;
            }});
            html += `</div>`;
        }});
        
        cat.standalone.forEach(item => {{
            html += `<div class="nav-item" onclick="showDetail('${{item.name}}', this)" data-name="${{item.name}}">${{item.name}}</div>`;
            totalItems++;
        }});
        html += `</div>`;
    }});
    el.innerHTML = html;
    document.getElementById('stats').textContent = `INDEXED: ${{totalItems}} NODES`;
}}

function toggleCat(el) {{ el.classList.toggle('collapsed'); el.nextElementSibling.classList.toggle('collapsed'); }}
function toggleSub(el) {{ el.classList.toggle('collapsed'); el.nextElementSibling.classList.toggle('collapsed'); }}

function showOverview() {{
    document.querySelectorAll('.nav-item.active').forEach(e => e.classList.remove('active'));
    
    let html = `<h1 class="article-title">System Overview</h1>
                <div class="article-meta"><span>ROOT DIRECTORY</span></div>
                <div class="overview-grid">`;
                
    treeData.forEach(cat => {{
        const count = cat.subcategories.reduce((s, sub) => s + sub.items.length, 0) + cat.standalone.length;
        const subNames = cat.subcategories.map(s => s.name).join(' / ') || 'General Nodes';
        html += `<div class="overview-card" onclick="showCategory('${{cat.category}}')">
            <div class="count">${{count}}</div>
            <h2>${{cat.category}}</h2>
            <div class="sub-desc">${{subNames}}</div>
        </div>`;
    }});
    html += '</div>';
    document.getElementById('content-area').innerHTML = html;
}}

function showCategory(catName) {{
    const cat = treeData.find(c => c.category === catName);
    if (!cat) return;
    
    let html = `<h1 class="article-title">${{catName}}</h1>
                <div class="article-meta"><span>CATEGORY VIEW</span></div>
                <div class="article-body">`;
                
    cat.subcategories.forEach(sub => {{
        html += `<h3>${{sub.name}}</h3><ul>`;
        sub.items.forEach(item => {{
            html += `<li><a href="#" onclick="showDetail('${{item.name}}'); return false;">${{item.name}}</a> <span style="color:var(--color-text-muted);font-size:14px;">— ${{item.desc}}</span></li>`;
        }});
        html += `</ul>`;
    }});
    
    if (cat.standalone.length > 0) {{
        html += `<h3>General Items</h3><ul>`;
        cat.standalone.forEach(item => {{
            html += `<li><a href="#" onclick="showDetail('${{item.name}}'); return false;">${{item.name}}</a> <span style="color:var(--color-text-muted);font-size:14px;">— ${{item.desc}}</span></li>`;
        }});
        html += `</ul>`;
    }}
    
    html += '</div>';
    document.getElementById('content-area').innerHTML = html;
}}

function showDetail(name, el) {{
    document.querySelectorAll('.nav-item.active').forEach(e => e.classList.remove('active'));
    if (el) el.classList.add('active');
    
    const sidebarItem = document.querySelector(`.nav-item[data-name="${{name}}"]`);
    if (sidebarItem) {{
        sidebarItem.classList.add('active');
        // 展开所在分类和子分类
        let parent = sidebarItem.parentElement;
        while (parent) {{
            if (parent.classList.contains('cat-items') || parent.classList.contains('sub-items')) {{
                parent.classList.remove('collapsed');
            }}
            if (parent.previousElementSibling && (parent.previousElementSibling.classList.contains('nav-group-title') || parent.previousElementSibling.classList.contains('nav-sub-title'))) {{
                parent.previousElementSibling.classList.remove('collapsed');
            }}
            parent = parent.parentElement;
        }}
        // 滚动到侧边栏可见
        sidebarItem.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}
    
    const meta = pagesMeta[name] || {{}};
    const htmlContent = bodyHtml[name] || '<p>Content not found.</p>';
    const statusHtml = meta.status ? `<span class="status-badge">STATUS: ${{meta.status}}</span>` : '';
    
    document.getElementById('content-area').innerHTML = `
        <h1 class="article-title">${{name}}</h1>
        <div class="article-meta">
            ${{statusHtml}}
            <span>KNOWLEDGE NODE</span>
        </div>
        <div class="article-body">
            ${{htmlContent}}
        </div>
    `;
    
    document.querySelectorAll('.wiki-link').forEach(a => {{
        a.addEventListener('click', function(e) {{
            e.preventDefault();
            showDetail(this.dataset.name);
        }});
    }});
}}

renderTree();

// ── Fuse.js 搜索索引 ──
const fuseItems = [];
treeData.forEach(cat => {{
    const allItems = [];
    cat.subcategories.forEach(sub => sub.items.forEach(it => allItems.push(it)));
    cat.standalone.forEach(it => allItems.push(it));
    allItems.forEach(item => {{
        const bodyText = (bodyHtml[item.name] || '').replace(/<[^>]+>/g, '');
        fuseItems.push({{ name: item.name, desc: item.desc, body: bodyText }});
    }});
}});
const fuse = new Fuse(fuseItems, {{
    keys: [
        {{ name: 'name', weight: 10 }},
        {{ name: 'desc', weight: 3 }},
        {{ name: 'body', weight: 1 }}
    ],
    threshold: 0.4,
    includeScore: true
}});

let searchTimer = null;
function onSearch() {{
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {{
        const q = document.getElementById('search').value.trim();
        if (!q) {{ showOverview(); return; }}
        const results = fuse.search(q);
        let html = `<h1 class="article-title">Search Results</h1>
                    <div class="article-meta"><span>${{results.length}} RESULTS FOR "${{q.toUpperCase()}}"</span></div>
                    <div class="article-body">`;
        results.forEach(r => {{
            const item = r.item;
            html += `<div class="search-result-item" onclick="showDetail('${{item.name}}')">
                <div class="search-result-title">${{item.name}}</div>
                <div class="search-result-desc">${{item.desc}}</div>
            </div>`;
        }});
        html += '</div>';
        document.getElementById('content-area').innerHTML = html;
        document.querySelectorAll('.nav-item.active').forEach(e => e.classList.remove('active'));
    }}, 200);
}}

showOverview();
</script>
</body>
</html>"""

# ── 主流程 ──
text = (WIKI_DIR / "index.md").read_text(encoding="utf-8")
sections = parse_index(text)
pages = collect_pages(sections)
html = render_html(sections, pages)
OUTPUT.write_text(html, encoding="utf-8")
print(f"✅ 已生成顶级视觉架构: {OUTPUT}  (处理了 {len(pages)} 个节点)")