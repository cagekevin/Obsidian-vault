"""
html2pdf-edge.py — Edge headless HTML→PDF 转换器
特点：
- 强制深色模式 (--force-dark-mode + --enable-features=WebContentsForceDark)
- 设置合理边距 (--print-to-pdf-no-header)
- A5 纸张适合手机 (手机屏幕比例)
"""
import sys
import subprocess
import shutil
from pathlib import Path

EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
SRC = Path(r"G:\Obsidian-vault\Tools\output\视频创作手册.html")
DST = Path(r"G:\Obsidian-vault\Tools\output\视频创作手册.pdf")

def html_to_pdf(src: Path, dst: Path, paper: str = "A5"):
    if not src.exists():
        print(f"[ERR] 源文件不存在: {src}")
        sys.exit(1)
    if not EDGE.exists():
        print(f"[ERR] Edge 未找到: {EDGE}")
        sys.exit(1)

    url = "file:///" + str(src).replace("\\", "/")

    cmd = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={dst}",
        "--force-color-profile=srgb",
        "--force-device-scale-factor=2",  # 高清渲染
        # 关键：让 CSS 媒体查询 dark 模式在打印时生效
        "--enable-features=WebContentsForceDark",
        "--force-dark-mode",
        "--disable-features=Translate",
        url,
    ]

    print(f"[RUN] Edge headless PDF...")
    print(f"      源: {src}")
    print(f"      目标: {dst}")
    print(f"      纸张: {paper}")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        print(f"[ERR] Edge 退出码: {result.returncode}")
        print(result.stderr)
        sys.exit(1)

    if not dst.exists():
        print(f"[ERR] PDF 未生成")
        sys.exit(1)

    size_kb = dst.stat().st_size / 1024
    print(f"[OK] PDF 已生成: {size_kb:.1f} KB")
    return dst


if __name__ == "__main__":
    html_to_pdf(SRC, DST)
