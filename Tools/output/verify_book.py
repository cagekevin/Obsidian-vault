"""验证视频创作手册 HTML 结构"""
import re
from pathlib import Path

html_path = Path(r"G:\Obsidian-vault\Tools\output\视频创作手册.html")
html = html_path.read_text(encoding="utf-8")

page_section = 'class="page-section"'
page_link = 'href="#page-'
table_tag = "<table"
pre_tag = "<pre>"
page_title = 'class="page-title"'

print("文件大小:", len(html) // 1024, "KB")
print("H1 标题数:", len(re.findall(r"<h1", html)))
print("H2 标题数:", len(re.findall(r"<h2", html)))
print("页面 section 数:", len(re.findall(re.escape(page_section), html)))
print("wikilink 锚点数:", len(re.findall(re.escape(page_link), html)))
print("表格数:", len(re.findall(re.escape(table_tag), html)))
print("代码块数:", len(re.findall(re.escape(pre_tag), html)))
print("深色模式 CSS:", "prefers-color-scheme: light" in html)
print("目录按钮:", "toc-btn" in html)
print("页面标题数:", len(re.findall(re.escape(page_title), html)))
