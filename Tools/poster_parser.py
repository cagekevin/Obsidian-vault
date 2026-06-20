#!/usr/bin/env python3
"""
OCR 电商海报排版解析 — 提取文字、坐标、字号，输出 JSON。

依赖：
    pip install rapidocr_onnxruntime Pillow

用法：
    # 独立模式：JSON 输出到图片同目录
    python3 poster_parser.py <图片路径>

    # PS 调用模式：指定输出路径
    python3 poster_parser.py <图片路径> <输出JSON路径>

示例：
    python3 poster_parser.py ~/Desktop/poster.jpg
    python3 poster_parser.py ~/Desktop/poster.jpg ~/Desktop/result.json
"""

import json
import os
import math
from rapidocr_onnxruntime import RapidOCR
from PIL import Image

def merge_text_blocks(blocks, y_tolerance_ratio=1.5, x_tolerance=20):
    """
    智能段落合并算法：将视觉上相邻的单行文本合并为多行段落
    """
    if not blocks: return []
    
    # 先按 Y 坐标从上到下排序
    blocks.sort(key=lambda b: b['rect']['top'])
    
    merged = []
    current_group = blocks[0]

    for next_block in blocks[1:]:
        # 计算两行文字之间的垂直间距
        vertical_gap = next_block['rect']['top'] - (current_group['rect']['top'] + current_group['rect']['height'])
        
        # 检查 X 轴左侧是否大致对齐
        x_aligned = abs(current_group['rect']['left'] - next_block['rect']['left']) < x_tolerance
        
        # 如果垂直间距合理，且左侧对齐，则认为是同一段落
        if vertical_gap < (current_group['inferred_font_size'] * y_tolerance_ratio) and x_aligned:
            # 执行合并
            current_group['content'] += "\r" + next_block['content']  # PS 识别 \r 为强制换行
            
            # 重新计算包围盒
            new_left = min(current_group['rect']['left'], next_block['rect']['left'])
            new_top = current_group['rect']['top']
            new_right = max(current_group['rect']['left'] + current_group['rect']['width'], 
                            next_block['rect']['left'] + next_block['rect']['width'])
            new_bottom = next_block['rect']['top'] + next_block['rect']['height']
            
            current_group['rect']['left'] = new_left
            current_group['rect']['top'] = new_top
            current_group['rect']['width'] = new_right - new_left
            current_group['rect']['height'] = new_bottom - new_top
        else:
            merged.append(current_group)
            current_group = next_block
            
    merged.append(current_group)
    return merged


def parse_image_to_json(image_path: str, output_json_path: str = "layout_data.json"):
    """
    解析电商海报，提取文本和排版坐标，输出标准 JSON 结构
    """
    if not os.path.exists(image_path):
        print(f"❌ 找不到图片: {image_path}")
        return None

    print("⏳ 初始化 OCR 引擎中...")
    engine = RapidOCR()

    print(f"🔍 正在解析图片: {image_path}")
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    result, elapse = engine(image_path)
    
    raw_blocks = []
    if result:
        for item in result:
            dt_boxes, text_content = item[0], item[1]
            x_coords = [p[0] for p in dt_boxes]
            y_coords = [p[1] for p in dt_boxes]

            left, top = int(min(x_coords)), int(min(y_coords))
            width, height = int(max(x_coords) - left), int(max(y_coords) - top)

            # 核心优化：利用中文字体特性，用宽度反推字号
            char_count = max(len(text_content.replace(" ", "")), 1)
            # 中文为主时，单字宽度约等于字号
            estimated_size_by_width = width / char_count
            estimated_size_by_height = height
            
            # 取两者的加权平均，并吸附到偶数像素，使排版更规整
            inferred_font_size = int((estimated_size_by_width * 0.7 + estimated_size_by_height * 0.3))
            inferred_font_size = max(math.ceil(inferred_font_size / 2) * 2, 12)  # 最小 12px

            raw_blocks.append({
                "type": "text",
                "content": text_content,
                "rect": {"left": left, "top": top, "width": width, "height": height},
                "inferred_font_size": inferred_font_size
            })
            print(f"✅ 提取文本: [{text_content}] (字号约 {inferred_font_size}px)")

    # 调用合并算法
    merged_blocks = merge_text_blocks(raw_blocks)

    output_data = {
        "image_size": {"width": img_width, "height": img_height},
        "blocks": merged_blocks
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 解析完成！原始 {len(raw_blocks)} 个块 → 合并后 {len(merged_blocks)} 个段落。")
    print(f"💾 数据已保存至: {output_json_path}\n耗时: {elapse[0] if elapse else 0:.2f} 秒")
    
    return output_json_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        # PS 调用模式：PS 指定输出路径（通常是临时目录）
        parse_image_to_json(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        # 独立模式：JSON 输出到图片所在目录
        img_path = sys.argv[1]
        img_dir = os.path.dirname(img_path) or "."
        out_path = os.path.join(img_dir, "layout_data.json")
        parse_image_to_json(img_path, out_path)
    else:
        print("⚠️ 参数不足！用法: python3 poster_parser.py <图片路径> [输出JSON路径]")
