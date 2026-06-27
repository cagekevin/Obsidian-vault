#!/usr/bin/env python3
"""
Convert old-format .doc files to Markdown.
Uses olefile to extract text from legacy Word documents (not .docx).

Usage:
    python convert-doc.py input.doc -o output.md
"""
import argparse
import re
import struct
import sys
from pathlib import Path


def extract_text_from_doc(filepath: str) -> str:
    """Extract readable text from a legacy .doc file using olefile."""
    import olefile

    ole = olefile.OleFileIO(filepath)

    # Try WordDocument stream first
    if ole.exists('WordDocument'):
        data = ole.openstream('WordDocument').read()
        # Extract UTF-16LE text chunks
        text = ''
        # Try to find text between BOM markers or just decode as UTF-16LE
        try:
            text = data.decode('utf-16-le', errors='ignore')
        except Exception:
            text = data.decode('utf-8', errors='ignore')

        # Clean up control characters but keep newlines
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        text = re.sub(r'\r\n?', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        # If we got meaningful text, return it
        if len(text) > 100:
            ole.close()
            return text

    # Fallback: try other common streams
    for stream_name in ole.listdir():
        name = '/'.join(stream_name)
        try:
            data = ole.openstream(stream_name).read()
            chunk = data.decode('utf-16-le', errors='ignore')
            chunk = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', chunk)
            chunk = re.sub(r'\r\n?', '\n', chunk)
            chunk = chunk.strip()
            if len(chunk) > len(text):
                text = chunk
        except Exception:
            try:
                chunk = data.decode('utf-8', errors='ignore')
                chunk = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', chunk)
                chunk = chunk.strip()
                if len(chunk) > len(text):
                    text = chunk
            except Exception:
                pass

    ole.close()
    return text.strip()


def main():
    parser = argparse.ArgumentParser(description='Convert legacy .doc files to Markdown')
    parser.add_argument('input', help='Input .doc file')
    parser.add_argument('-o', '--output', help='Output .md file (default: stdout)')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'✗ File not found: {args.input}', file=sys.stderr)
        sys.exit(1)

    text = extract_text_from_doc(str(input_path))
    if not text:
        print(f'✗ Could not extract text from {args.input}', file=sys.stderr)
        sys.exit(1)

    # Basic Markdown wrapping
    lines = text.split('\n')
    md_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                in_list = False
            md_lines.append('')
            continue
        # Detect likely headings (short lines ending without punctuation)
        if len(stripped) < 60 and not stripped.endswith(('.', '，', '。', '；', '：')) and len(stripped) > 0:
            if not stripped.startswith('#'):
                md_lines.append(f'## {stripped}')
            else:
                md_lines.append(stripped)
        # Detect list items
        elif stripped.startswith(('- ', '* ', '+ ', '• ', '· ')):
            md_lines.append(stripped)
            in_list = True
        else:
            md_lines.append(stripped)

    markdown = '\n'.join(md_lines) + '\n'

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, 'utf-8')
        print(f'✓ Written to {output_path} ({len(markdown)} chars)', file=sys.stderr)
    else:
        sys.stdout.write(markdown)


if __name__ == '__main__':
    main()
