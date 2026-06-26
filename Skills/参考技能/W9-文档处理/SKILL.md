---
name: 文档处理
description: PDF/Word/Excel 文档处理。触发词：pdf、word、文档、表格、提取文字、合并文档。
---

# 文档处理

<what-to-do>

## PDF 处理

使用 Python 库 `PyMuPDF`（`fitz`）操作 PDF：

| 你说 | AI 行为 |
|------|---------|
| 提取文字 | `python3 -c "import fitz; doc=fitz.open('文件.pdf'); [print(p.get_text()) for p in doc]"` |
| 提取表格 | `pip install pdfplumber` → `python3 -c "import pdfplumber; ..."` |
| 合并多个 PDF | `python3 -c "import fitz; doc=fitz.open(); [doc.insert_file(f) for f in ['a.pdf','b.pdf']]; doc.save('合并.pdf')"` |
| PDF 转图片 | `python3 -c "import fitz; ..."` 每页导出为 PNG |

**需要先装依赖才操作**：`pip install pymupdf pdfplumber`

## Word 处理（规划中）

见 `references/docx.md`

## Excel 处理

已有 `tools/read-excel.py`，直接调用。

## 文档转换（MarkItDown — PDF/Word/PPT/Excel/图片OCR/音频转写）

| 你说 | 执行 |
|------|------|
| 转 PDF/Word/PPT/Excel 为 Markdown | 加载 `MarkItDown文档转换` 子技能，执行 `markitdown 文件 -o 输出.md` |
| 识别图片文字（OCR） | 同上，MarkItDown 支持图片 OCR |
| 转写音频/YouTube | 同上，MarkItDown 支持音频和 YouTube 转写 |
| 批量转换 | 加载 `MarkItDown文档转换`，使用 `scripts/batch_convert.py` |

首次使用：`pip install 'markitdown[all]'`

## 文案处理

| 你说 | AI 行为 |
|------|---------|
| 优化这段文案 / run autoresearch | 加载 `文案优化器` 子技能，按 Karpathy 风格多轮进化流程执行 |
| 去AI痕迹 / humanize / 去AI味 | 加载 `去除文本AI痕迹` 子技能，检测修复 AI 文本特征 |
| 写公众号 / 写文章 / 公众号文章 | 加载 `公众号文章写作` 子技能，按 Khazix 风格写长文 |

</what-to-do>
