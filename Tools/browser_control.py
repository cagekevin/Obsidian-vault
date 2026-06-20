#!/usr/bin/env python3
"""
browser_control — AI 浏览器操作统一入口
========================================
底层使用 browser-harness（CDP 直连本地 Chrome），所有 helpers 函数原生可用。

用法：python3 browser_control.py <命令> [参数]

👤 你（人）用的：
  python3 browser_control.py 录制         鼠标悬停高亮，点击即保存选择器到项目 .selectors/ 目录
  python3 browser_control.py 拾取         同上

🤖 AI 用的：
  导航：
    python3 browser_control.py 打开 <url>                   打开网页
    python3 browser_control.py 新标签页 <url>               打开新标签页
  页面信息：
    python3 browser_control.py 截图 [保存路径]              截取当前页面
    python3 browser_control.py 获取页面信息                 获取 URL/标题/视口
    python3 browser_control.py 获取文本                     获取页面可见文字
    python3 browser_control.py 获取HTML                     获取页面 HTML 源码
    python3 browser_control.py 获取页面内容 [输出路径]      下载页面 → 清理 → 纯文本
    python3 browser_control.py 下载 <url> [保存路径]        下载文件
    python3 browser_control.py 打印PDF [保存路径]           当前页面保存为 PDF
  交互：
    python3 browser_control.py 点击 <选择器/文本/保存名> [--sel]
                                 传 CSS：点击 "#login-btn"
                                 按文本：点击 图像
                                 传保存名：点击 login_btn --sel
    python3 browser_control.py 点击坐标 <x> <y>             坐标点击
    python3 browser_control.py 填写 <选择器/保存名> <内容> [--sel]  填写输入框
    python3 browser_control.py 上传 <选择器/保存名> <路径> [--sel]  上传文件
    python3 browser_control.py 滚动                         向下滚动一屏
    python3 browser_control.py 等待 <秒数>                  等待
  标签页：
    python3 browser_control.py 查看标签页                   列出所有标签页
    python3 browser_control.py 标签页列表                   同上
    python3 browser_control.py 切换到标签页 <targetId>      切换标签页
    python3 browser_control.py 关闭标签页                   关闭当前标签页
  高级：
    python3 browser_control.py 清洗 <HTML文件路径> [输出路径] [--format json]
                                 清洗本地 HTML 文件，提取纯文本
    python3 browser_control.py 执行 <Python代码>            直接执行原生代码
  选择器：
    python3 browser_control.py 保存选择器 <保存名> <选择器>  手动保存选择器
    python3 browser_control.py 查看选择器 [保存名]           查看已保存的选择器

新电脑使用：
  1. Chrome 打开 chrome://inspect/#remote-debugging
  2. 勾选 "Allow remote debugging for this browser instance"（一次性）

遇到复杂场景（弹窗/iframe/下拉框等），查阅：
  skills/工程类技能/S12-浏览器自动化/browser-harness/interaction-skills/
  具体文件：
    dialogs.md       — alert/confirm/prompt/beforeunload 弹窗处理
    iframes.md       — iframe 穿透
    shadow-dom.md    — Shadow DOM 穿透
    dropdowns.md     — 下拉框（原生/自定义/搜索框）
    network-requests.md — Network 请求监控
    scrolling.md     — 滚动（页面/容器/虚拟列表）
    tabs.md          — 标签页控制（CDP + 可见顺序）
    uploads.md       — 文件上传
    downloads.md     — 下载文件
    drag-and-drop.md — 拖拽操作
    cookies.md       — Cookie 获取/保存/设置
    print-as-pdf.md  — PDF 打印
    viewport.md      — 视口调整
    connection.md    — 连接与标签页可见性
"""

#!/usr/bin/env python3
"""
browser_control — AI 浏览器操作统一入口 (优雅架构版)
======================================================
底层使用 browser-harness (CDP 直连本地 Chrome)。
基于职责分离与命令路由模式构建，跨平台全面兼容。
"""

import sys
import json
import subprocess
import tempfile
import re
import time
import base64
from pathlib import Path
from html.parser import HTMLParser
from typing import List, Dict, Callable, Any, Tuple

# ─── 核心引擎系统 ──────────────────────────────────────────

class HarnessRunner:
    """处理与 browser-harness 子进程的底层通信"""
    @staticmethod
    def execute(code: str, timeout: int = 120) -> str:
        try:
            result = subprocess.run(
                ["browser-harness"],
                input=code,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode != 0:
                raise RuntimeError(f"browser-harness 执行失败:\n{result.stderr}")
            return result.stdout.strip()
        except FileNotFoundError:
            raise RuntimeError("未找到 browser-harness 命令，请确保其已安装并在环境变量 PATH 中。")
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"执行超时 ({timeout}s)")

# ─── 命令路由系统 ──────────────────────────────────────────

class CommandRouter:
    """基于装饰器的命令注册表"""
    registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, *names: str):
        def decorator(func: Callable):
            for name in names:
                cls.registry[name] = func
            return func
        return decorator

    @staticmethod
    def parse_args(args: List[str]) -> Tuple[List[str], Dict[str, bool]]:
        """优雅分离位置参数与 Flag 参数 (如 --sel)"""
        positionals = []
        flags = {}
        for arg in args:
            if arg.startswith("--"):
                flags[arg[2:]] = True
            else:
                positionals.append(arg)
        return positionals, flags

command = CommandRouter.register
run_bh = HarnessRunner.execute

# ─── 路径与辅助工具 ────────────────────────────────────────

def get_temp_file(filename: str) -> Path:
    return Path(tempfile.gettempdir()) / filename

def get_selector_dir() -> Path:
    """寻找包含 .git 或 .codebuddy 的项目根目录，存放 .selectors/"""
    current = Path.cwd()
    # 向上追溯寻找根目录
    for parent in [current, *current.parents]:
        if (parent / ".git").exists() or (parent / ".codebuddy").exists():
            return parent / ".selectors"
    return current / ".selectors"

def resolve_selector(selector: str, use_sel_flag: bool = False):
    """解析选择器：--sel 模式返回 [主选择器, 备用选择器列表]；普通模式返回 [selector, []]"""
    if use_sel_flag:
        sel_file = get_selector_dir() / f"{selector}.json"
        if not sel_file.exists():
            raise FileNotFoundError(f"未找到保存的选择器配置: '{selector}'")
        with open(sel_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        primary = data.get("selector", "")
        sels = data.get("selectors", {})
        # 按优先级排列备用选择器
        fallbacks = []
        for key in ["id", "dataTestid", "name", "href", "className", "text", "path"]:
            v = sels.get(key)
            if v and v != primary:
                fallbacks.append(v)
        return primary, fallbacks
    return selector, []

# ─── 页面基础与导航 ────────────────────────────────────────

@command("页面信息", "获取页面信息")
def page_info() -> str:
    return run_bh("print(page_info())")

@command("打开")
def open_url(url: str) -> str:
    return run_bh(f'goto_url({json.dumps(url)})\nwait_for_load()\nprint(page_info())')

@command("新标签页")
def new_tab(url: str = "about:blank") -> str:
    return run_bh(f'new_tab({json.dumps(url)})\nwait_for_load()\nprint(page_info())')

@command("截图")
def screenshot(path: str = None) -> str:
    save_path = Path(path).resolve() if path else get_temp_file("bh_shot.png")
    return run_bh(f'capture_screenshot({json.dumps(str(save_path))})\nprint({json.dumps(str(save_path))})')

@command("执行JS", "执行js")
def execute_js(expression: str) -> str:
    return run_bh(f"print(js({json.dumps(expression)}))")

@command("等待")
def wait(seconds: str = "1") -> str:
    return run_bh(f'wait({seconds})\nprint("waited {seconds}s")')

@command("执行")
def run_raw(code: str) -> str:
    return run_bh(code)

# ─── 标签页控制 ──────────────────────────────────────────

@command("标签页列表", "查看标签页")
def list_tabs() -> str:
    return run_bh("print(list_tabs(include_chrome=False))")

@command("切换到标签页")
def switch_tab(target_id: str) -> str:
    return run_bh(f'switch_tab({json.dumps(target_id)})\nprint(page_info())')

@command("关闭标签页")
def close_tab() -> str:
    return run_bh('close_tab()\nprint("closed")')

# ─── DOM 交互操作 ────────────────────────────────────────

@command("点击")
def click(selector_or_text: str, **flags) -> str:
    try:
        primary, fallbacks = resolve_selector(selector_or_text, flags.get("sel", False))
    except FileNotFoundError as e:
        return str(e)

    # 按优先级尝试所有选择器（主选择器 → 备用列表 → 文本降级）
    candidates = [primary] + fallbacks

    for i, sel in enumerate(candidates):
        try:
            b64_sel = base64.b64encode(sel.encode()).decode()
            result = run_bh(
                f"import base64\n"
                f"sel = base64.b64decode({json.dumps(b64_sel)}).decode()\n"
                f"js('document.querySelector(\"' + sel.replace('\"', '\\\\\"') + '\").click()')\n"
                f"print('clicked')"
            )
            label = "主选择器" if i == 0 else f"备用选择器 #{i}"
            return f"已点击 ({label}): {sel}"
        except RuntimeError:
            continue

    # 全部 CSS 选择器失败，降级文本模糊查找
    js_text_click = f"""
    (() => {{
        const items = document.querySelectorAll("button,a,div,[role=menuitem],[role=option]");
        for (const item of items) {{
            if (item.textContent.trim().includes({json.dumps(primary)})) {{
                item.click(); return "clicked";
            }}
        }}
        throw new Error("not found");
    }})()
    """
    try:
        b64_text = base64.b64encode(js_text_click.encode()).decode()
        run_bh(f"import base64; js(base64.b64decode({json.dumps(b64_text)}).decode())")
        return f"已点击 (文本降级): {primary}"
    except RuntimeError as e:
        return f"点击失败 (所有选择器和文本降级均未命中): {e}"

@command("点击坐标")
def click_xy(x: str, y: str) -> str:
    return run_bh(f'click_at_xy({int(x)}, {int(y)})\nprint("clicked at {x},{y}")')

@command("填写")
def fill(selector: str, text: str, **flags) -> str:
    try:
        target = resolve_selector(selector, flags.get("sel", False))
    except FileNotFoundError as e:
        return str(e)
    return run_bh(f'fill_input({json.dumps(target)}, {json.dumps(text)})\nprint("filled")')

@command("上传")
def upload(selector: str, file_path: str, **flags) -> str:
    try:
        target = resolve_selector(selector, flags.get("sel", False))
    except FileNotFoundError as e:
        return str(e)
    abs_path = str(Path(file_path).expanduser().resolve())
    return run_bh(f'upload_file({json.dumps(target)}, {json.dumps(abs_path)})\nprint("uploaded")')

@command("滚动")
def scroll() -> str:
    return run_bh('info = page_info()\nscroll(info["w"]/2, info["h"]/2)\nprint("scrolled")')

# ─── 内容解析与提取 ────────────────────────────────────────

class Cleaner(HTMLParser):
    """HTML 清洗器：去除标签，提取纯文本（支持实体解码）"""
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = False
        self.block_tags = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "br", "hr", "table", "section", "blockquote"}
        self.skip_tags = {"script", "style", "noscript", "svg", "math"}

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags: self.skip = True
        if tag in self.block_tags: self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.skip_tags: self.skip = False
        if tag in self.block_tags: self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip and (t := data.strip()):
            self.parts.append(t + " ")

    def handle_entityref(self, name):
        if not self.skip:
            self.parts.append(self.unescape(f"&{name};"))

    def handle_charref(self, name):
        if not self.skip:
            self.parts.append(self.unescape(f"&#{name};"))

    def get_text(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return re.sub(r" {2,}", " ", text).strip()

    def get_blocks(self) -> list:
        """按段落/块返回列表"""
        return [b.strip() for b in re.split(r"\n{2,}", self.get_text()) if b.strip()]

@command("获取文本", "获取文字")
def get_text() -> str:
    return run_bh('print(js("document.body.innerText"))')

@command("获取HTML", "获取html")
def get_html() -> str:
    return run_bh('print(js("document.documentElement.outerHTML"))')

@command("获取页面内容")
def fetch_clean_content(out_path: str = None) -> str:
    html = get_html()
    
    # 清理非语义标签
    clean_html = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.DOTALL|re.IGNORECASE)
    clean_html = re.sub(r'<!--.*?-->', '', clean_html, flags=re.DOTALL)
    
    cleaner = Cleaner()
    cleaner.feed(clean_html)
    text = cleaner.get_text()

    # 确定保存路径
    if out_path:
        save_path = Path(out_path).expanduser().resolve()
    else:
        try:
            info = json.loads(page_info())
            title = info.get("title", "page").replace(" ", "_").replace("/", "_")[:30]
            save_path = Path.home() / "Downloads" / f"{title}_clean.md"
        except Exception:
            save_path = get_temp_file("page_clean.md")

    save_path.write_text(text, encoding="utf-8")
    
    orig_kb = len(html) / 1024
    clean_kb = len(text) / 1024
    print(f"提取完成: {orig_kb:.0f}KB → {clean_kb:.0f}KB ({clean_kb/orig_kb*100:.0f}%)")
    print(f"文件输出: {save_path}")
    return f"--- 内容预览 ---\n{text[:800]}"

@command("清洗")
def clean_local_html(input_path: str, out_path: str = None, **flags) -> str:
    """
    清洗本地 HTML 文件，提取纯文本。
    用法: python3 browser_control.py 清洗 <HTML文件路径> [输出路径] [--format json]
    """
    input_file = Path(input_path)
    if not input_file.exists():
        return f"文件不存在: {input_path}"

    html = input_file.read_text(encoding="utf-8", errors="replace")
    clean_html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
    clean_html = re.sub(r'<script[^>]*>.*?</script>', '', clean_html, flags=re.DOTALL|re.IGNORECASE)
    clean_html = re.sub(r'<!--.*?-->', '', clean_html, flags=re.DOTALL)

    cleaner = Cleaner()
    cleaner.feed(clean_html)

    output_format = flags.get("format", "text")
    if output_format == "json":
        result = json.dumps(cleaner.get_blocks(), ensure_ascii=False, indent=2)
    else:
        result = cleaner.get_text()

    if out_path:
        save_path = Path(out_path).expanduser().resolve()
    else:
        save_path = input_file.with_name(input_file.stem + "_clean.md")

    save_path.write_text(result, encoding="utf-8")
    orig_kb = len(html) / 1024
    clean_kb = len(result) / 1024
    print(f"完成: {orig_kb:.0f}KB → {clean_kb:.0f}KB ({clean_kb/orig_kb*100:.0f}%)")
    print(f"输出: {save_path}")
    return f"--- 预览 ---\n{result[:500]}"

# ─── 下载与输出 ──────────────────────────────────────────

@command("下载")
def download(url: str, save_path: str = None) -> str:
    filename = save_path or url.split("/")[-1] or "download"
    target_path = Path(filename).expanduser().resolve() if save_path else get_temp_file(filename)
    
    return run_bh(
        f'data = http_get({json.dumps(url)})\n'
        f'with open({json.dumps(str(target_path))}, "w") as f: f.write(data)\n'
        f'print({json.dumps(str(target_path))})'
    )

@command("打印PDF")
def print_pdf(path: str = None) -> str:
    target_path = Path(path).expanduser().resolve() if path else get_temp_file("bh_page.pdf")
    code = f"""
import base64
r = cdp("Page.printToPDF", printBackground=True)
with open({json.dumps(str(target_path))}, "wb") as f:
    f.write(base64.b64decode(r["data"]))
print({json.dumps(str(target_path))})
"""
    return run_bh(code)

# ─── 选择器录制 ──────────────────────────────────────────

@command("保存选择器")
def save_selector(name: str, selector: str, **flags) -> str:
    sdir = get_selector_dir()
    sdir.mkdir(parents=True, exist_ok=True)
    
    # 优先用最稳的选择器（id > data-testid > name > href > class > text > path）
    info = {
        "name": name,
        "selector": selector,
        "selectors": flags.get("selectors", {}),
        "created": time.strftime("%Y-%m-%d %H:%M"),
        "url": "",
    }
    ctx = flags.get("context", {})
    if ctx:
        info["context"] = ctx
    try:
        info["url"] = json.loads(page_info()).get("url", "")
    except Exception:
        pass

    target_file = sdir / f"{name}.json"
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
        
    return f"已保存 '{name}' → {target_file}\n以后可用: 点击 {name} --sel"

@command("查看选择器")
def show_selector(name: str = None) -> str:
    sdir = get_selector_dir()
    if not sdir.exists():
        return "暂无保存的选择器。"

    if name:
        target = sdir / f"{name}.json"
        if not target.exists():
            available = [f.stem for f in sdir.glob("*.json")]
            return f"未找到 '{name}'。已存: {', '.join(available) or '无'}"
        info = json.loads(target.read_text(encoding="utf-8"))
        return f"名称: {info['name']}\n选择器: {info['selector']}\nURL: {info.get('url', '')}\n创建于: {info.get('created', '')}"

    files = list(sdir.glob("*.json"))
    if not files:
        return "暂无保存的选择器。"
    
    out = "已保存的选择器清单:\n"
    for f in sorted(files):
        info = json.loads(f.read_text(encoding="utf-8"))
        out += f"  {f.stem}: {info['selector']}\n"
    return out

# ─── 主入口 ────────────────────────────────────────────

@command("录制", "拾取")
def record_selector() -> str:
    """
    进入交互式录制模式。
    鼠标悬停在页面元素上会高亮，点击目标元素即可自动生成并保存选择器。
    """
    print("已在浏览器开启可视化录制模式。")
    print("鼠标悬停查看高亮，点击目标元素进行保存。最多等待 60 秒...")

    js_code = """
(() => {
    // 【修复核心1】使用 AbortController 彻底清理上一轮遗留的僵尸监听器
    if (window.__bh_abort) window.__bh_abort.abort();
    window.__bh_abort = new AbortController();
    const signal = window.__bh_abort.signal;

    window.__bh_recorded = null;

    // 清理可能残留的样式和 UI 弹窗
    var oldStyle = document.getElementById("bh-picker-style");
    if (oldStyle) oldStyle.remove();
    var oldDiv = document.getElementById("bh-picker-input");
    if (oldDiv) oldDiv.remove();

    const style = document.createElement("style");
    style.id = "bh-picker-style";
    style.textContent = ".bh-hover-target{outline:2px dashed #ff0055!important;cursor:crosshair!important;background-color:rgba(255,0,85,0.1)!important;transition:all 0.1s}";
    document.head.appendChild(style);

    function getAllSelectors(el) {
        // 返回所有可能的选择器，优先用最稳的
        var all = {};
        var tag = el.tagName.toLowerCase();
        if (el.id) all.id = "#" + el.id;
        var dt = el.getAttribute("data-testid");
        if (dt) all.dataTestid = tag + '[data-testid="' + dt + '"]';
        var nm = el.getAttribute("name");
        if (nm) all.name = tag + '[name="' + nm + '"]';
        var href = el.getAttribute("href");
        if (href && !href.startsWith("javascript") && !href.startsWith("#")) all.href = tag + '[href="' + href.replace(/"/g, '\\"') + '"]';
        var classes = Array.from(el.classList).filter(function(c) { return !c.startsWith("_") && !c.startsWith("css-"); });
        if (classes.length > 0) all.className = tag + "." + classes.slice(0, 3).join(".");
        var text = (el.textContent || "").trim().slice(0, 60);
        if (text) all.text = text;
        // nth-child 路径
        var path = [], cur = el;
        while (cur && cur.nodeType === Node.ELEMENT_NODE) {
            var s = cur.nodeName.toLowerCase();
            if (cur.id) { path.unshift("#" + cur.id); break; }
            var sib = cur, nth = 1;
            while (sib = sib.previousElementSibling) nth++;
            s += ":nth-child(" + nth + ")";
            path.unshift(s);
            cur = cur.parentNode;
            if (path.length >= 4) break;
        }
        all.path = path.join(" > ");
        return all;
    }

    function collectContext(el) {
        const ctx = {tag: el.tagName.toLowerCase(), text: (el.textContent || "").trim().slice(0, 100), id: el.id || "", classes: Array.from(el.classList).slice(0, 5), attributes: {}, parentText: "", siblingTexts: []};
        ["name","role","aria-label","placeholder","title","href","data-testid","type","alt"].forEach(function(a) { var v = el.getAttribute(a); if (v) ctx.attributes[a] = v; });
        var p = el.parentElement;
        if (p) {
            ctx.parentText = (p.textContent || "").trim().slice(0, 120);
            Array.from(p.children).forEach(function(c) { var t = (c.textContent || "").trim(); if (t && c !== el) ctx.siblingTexts.push(t.slice(0, 60)); });
        }
        return ctx;
    }

    var picked = false;
    var overHandler = function(e) { if (!picked) e.target.classList.add("bh-hover-target"); };
    var outHandler = function(e) { if (!picked) e.target.classList.remove("bh-hover-target"); };
    var clickHandler = function(e) {
        if (picked) return; 
        picked = true;
        e.stopPropagation(); e.preventDefault();
        
        // 点击后立即切断所有监听，防止穿透
        window.__bh_abort.abort();
        
        document.querySelectorAll(".bh-hover-target").forEach(function(el) { el.classList.remove("bh-hover-target"); });
        var s = document.getElementById("bh-picker-style"); if (s) s.remove();
        
        var allSelectors = getAllSelectors(e.target);
        var primary = allSelectors.id || allSelectors.dataTestid || allSelectors.name || allSelectors.href || allSelectors.className || allSelectors.text || allSelectors.path;
        var ctx = collectContext(e.target);
        
        var div = document.createElement("div");
        div.id = "bh-picker-input";
        div.style.cssText = "position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:999999;background:#fff;border:2px solid #ff0055;border-radius:8px;padding:20px;box-shadow:0 4px 20px rgba(0,0,0,0.3);font-family:sans-serif;min-width:400px;";
        div.innerHTML = '<div style="margin-bottom:10px;font-size:14px;color:#333;">Primary: <code style="background:#f5f5f5;padding:2px 6px;border-radius:4px;font-size:13px;">' + primary + '</code></div><input id="bh-name-input" type="text" placeholder="输入名称后按回车保存 (Enter)" style="width:100%;padding:8px 12px;border:1px solid #ddd;border-radius:6px;font-size:14px;box-sizing:border-box;"><div style="margin-top:10px;text-align:right;"><button id="bh-save-btn" style="background:#ff0055;color:#fff;border:none;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:14px;">Save</button></div>';
        document.body.appendChild(div);
        
        var nameInput = document.getElementById("bh-name-input");
        var saveBtn = document.getElementById("bh-save-btn");
        
        nameInput.focus();
        
        saveBtn.onclick = function() {
            var name = nameInput.value.trim();
            window.__bh_recorded = name ? {name: name, selector: primary, selectors: allSelectors, context: ctx} : {error: "cancelled"};
            div.remove();
        };
        
        nameInput.onkeydown = function(ev) {
            // 【修复核心2】增加 !ev.isComposing，忽略输入法拼写过程中的回车
            if (ev.key === "Enter" && !ev.isComposing) { 
                saveBtn.click(); 
            }
            if (ev.key === "Escape") { 
                window.__bh_recorded = {error: "cancelled"}; 
                div.remove(); 
            }
        };
    };
    
    // 挂载包含 signal 的事件监听器
    document.addEventListener("mouseover", overHandler, { signal: signal });
    document.addEventListener("mouseout", outHandler, { signal: signal });
    document.addEventListener("click", clickHandler, { capture: true, signal: signal });
})();
"""
    js_b64 = base64.b64encode(js_code.encode()).decode()
    timeout_json = '{"error": "timeout"}'
    
    # 增加超时后对 UI 和 AbortController 的保底清理
    harness_script = (
        f"import base64, time, json\n"
        f"js(base64.b64decode({json.dumps(js_b64)}).decode())\n"
        f"for _ in range(60):\n"
        f"  r = js('window.__bh_recorded')\n"
        f"  if r:\n"
        f"    js('window.__bh_recorded=null;')\n"
        f"    print(json.dumps(r))\n"
        f"    break\n"
        f"  time.sleep(1)\n"
        f"else:\n"
        f"  js('if(window.__bh_abort)window.__bh_abort.abort(); var s=document.getElementById(\"bh-picker-style\"); if(s)s.remove(); var d=document.getElementById(\"bh-picker-input\"); if(d)d.remove();')\n"
        f"  print({json.dumps(timeout_json)})\n"
    )
    
    try:
        output = run_bh(harness_script).strip()
        if not output:
            return "录制异常退出。"
        data = json.loads(output)
        if "error" in data:
            return f"录制结果: {data['error']}"
        ctx = data.get("context", {})
        sels = data.get("selectors", {})
        return save_selector(data["name"], data["selector"], context=ctx, selectors=sels)
    except json.JSONDecodeError:
        return f"解析结果失败: {output}"
    except Exception as e:
        return f"录制过程错误: {e}"
        
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    raw_args = sys.argv[2:]

    if cmd not in CommandRouter.registry:
        print(f"未知命令: {cmd}")
        print(f"可用命令: {', '.join(sorted(CommandRouter.registry.keys()))}")
        return

    positionals, flags = CommandRouter.parse_args(raw_args)

    try:
        result = CommandRouter.registry[cmd](*positionals, **flags)
        if result:
            print(result)
    except TypeError as e:
        print(f"参数错误，请检查输入格式。\n系统提示: {e}")
    except RuntimeError as e:
        print(f"运行时错误:\n{e}")
    except Exception as e:
        print(f"未知异常: {e}")

if __name__ == "__main__":
    main()