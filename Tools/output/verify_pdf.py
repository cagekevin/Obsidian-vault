"""验证 PDF 信息"""
import re
from pathlib import Path

pdf_path = Path(r"G:\Obsidian-vault\Tools\output\视频创作手册.pdf")
data = pdf_path.read_bytes()

# PDF 通常以 /Type /Page 计数
size_kb = len(data) / 1024
n_pages = len(re.findall(rb"/Type\s*/Page[^s]", data))

print(f"文件: {pdf_path.name}")
print(f"大小: {size_kb:.1f} KB ({size_kb/1024:.2f} MB)")
print(f"估算页数: {n_pages}")
print(f"首部: {data[:8]}")
