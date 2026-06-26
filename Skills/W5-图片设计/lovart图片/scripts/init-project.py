#!/usr/bin/env python3
"""
一键创建 Lovart 图片项目目录结构。
用法：
    python init-project.py "26-07-图片-HKH618活动"
"""
import sys, os

BASE = r"G:\AgentSpace\1_Active"

STRUCTURE = [
    "设计规范",
    "参考图",
    "原始素材",
    "需求",
    "输出",
]


def main():
    if len(sys.argv) < 2:
        print("用法: python init-project.py \"26-07-图片-项目名\"")
        return

    name = sys.argv[1]
    path = os.path.join(BASE, name)

    if os.path.exists(path):
        print(f"⚠️  项目已存在: {path}")
        return

    os.makedirs(path)
    for folder in STRUCTURE:
        os.makedirs(os.path.join(path, folder))

    # 创建 README
    readme = os.path.join(path, "README.md")
    with open(readme, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write("## 项目结构\n\n")
        f.write("| 目录 | 用途 |\n")
        f.write("|------|------|\n")
        f.write("| 设计规范/ | Step 1 输出的设计规范文档 |\n")
        f.write("| 参考图/ | 原始参考图片 |\n")
        f.write("| 原始素材/ | Excel / TXT / PDF 等原始输入 |\n")
        f.write("| 需求/ | 预处理后的最终文案 |\n")
        f.write("| 输出/ | Lovart 生成的最终图片 |\n")

    print(f"✅ 已创建: {path}")
    for folder in STRUCTURE:
        print(f"   ├── {folder}/")
    print(f"   └── README.md")


if __name__ == "__main__":
    main()
