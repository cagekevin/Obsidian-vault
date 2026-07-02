#!/usr/bin/env python3
"""
BM25 搜索 Wiki 知识库

用法:
  python bm25_search.py <关键词1> [关键词2 ...]

示例:
  python bm25_search.py 光影 电影感 打光
  python bm25_search.py 真实感 质感 PBR 材质
"""
import os, re, math, sys
from collections import Counter

def tokenize(text):
    return re.findall(r'[\w\u4e00-\u9fff]+', text.lower())

def bm25(query, docs, k1=1.5, b=0.75):
    q_tokens = tokenize(query)
    doc_tokens = [tokenize(d) for d in docs]
    N = len(docs)
    idf = {}
    for qt in set(q_tokens):
        df = sum(1 for dt in doc_tokens if qt in dt)
        idf[qt] = math.log((N - df + 0.5) / (df + 0.5) + 1)
    doc_lens = [len(dt) for dt in doc_tokens]
    avg_len = sum(doc_lens) / N if N else 1
    scores = []
    for i, dt in enumerate(doc_tokens):
        score = 0
        tf = Counter(dt)
        for qt in q_tokens:
            if qt in tf:
                f = tf[qt]
                score += idf[qt] * (f * (k1 + 1)) / (f + k1 * (1 - b + b * doc_lens[i] / avg_len))
        scores.append((score, i))
    scores.sort(reverse=True)
    return scores


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    query = ' '.join(sys.argv[1:])
    wiki_dir = r'g:\Obsidian-vault\Wiki'

    docs = []
    paths = []
    for root, dirs, files in os.walk(wiki_dir):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read()
                    docs.append(content)
                    paths.append(path)
                except:
                    pass

    results = bm25(query, docs)
    print(f'BM25 搜索 "{query}" 结果:\n')
    for score, idx in results[:20]:
        if score > 0:
            rel_path = os.path.relpath(paths[idx], wiki_dir)
            content = docs[idx]
            first_pos = len(content)
            for kw in query.split():
                pos = content.lower().find(kw)
                if pos != -1 and pos < first_pos:
                    first_pos = pos
            snippet_start = max(0, first_pos - 60)
            snippet = content[snippet_start:snippet_start+250].replace('\n', ' ').strip()
            print(f'[{score:.2f}] {rel_path}')
            print(f'  {snippet}')
            print()


if __name__ == '__main__':
    main()
