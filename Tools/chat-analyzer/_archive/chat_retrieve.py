#!/usr/bin/env python3
"""chat_retrieve.py — 混合搜索管道。

流程:
  query → BM25 检索 → 语义重排序 → 输出结果

直接导入 chat_bm25 和 chat_rerank 的模块函数。

用法:
  python chat_retrieve.py "漫步丨港股打新群" "Momenta 新股"
  python chat_retrieve.py "漫步丨港股打新群" "港股打新" --top 10
  python chat_retrieve.py "漫步丨港股打新群" "新股分析" --bm25-only
"""

import argparse
import json
import sys
from pathlib import Path

# 直接导入同级模块
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import chat_bm25
import chat_rerank

EXIT_OK = 0
EXIT_USAGE = 2


def log(msg):
    print(msg, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="聊天记录混合搜索")
    parser.add_argument("chat", help="群名称或 JSON 文件")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--top", type=int, default=5, help="最终结果数")
    parser.add_argument("--bm25-top", type=int, default=30, help="BM25 候选数")
    parser.add_argument("--bm25-only", action="store_true", help="仅 BM25，跳过重排序")
    parser.add_argument("--explain", action="store_true", help="输出诊断信息")
    parser.add_argument("--allow-remote-ollama", action="store_true")

    args = parser.parse_args()

    filepath = chat_bm25.resolve_chat(args.chat)

    # 检查索引是否存在
    idx_path = chat_bm25.get_index_path(filepath)
    if not idx_path.is_file():
        log(f"索引不存在: {idx_path}")
        log("请先运行: python chat_bm25.py build \"{args.chat}\"")
        return EXIT_USAGE

    # Stage 1: BM25 检索
    bm25_hits = chat_bm25.query(filepath, args.query, top_k=args.bm25_top)
    log(f"BM25: {len(bm25_hits)} 条候选")

    if not bm25_hits:
        print("未找到匹配结果。")
        return EXIT_OK

    candidates = []
    for h in bm25_hits:
        candidates.append({
            "msg_id": h["msg_id"],
            "datetime": h["datetime"],
            "sender": h["sender"],
            "content": h["content"],
            "bm25_score": h["score"],
        })

    # Stage 2: 语义重排序
    if args.bm25_only:
        final = candidates[:args.top]
        strategy = "bm25-only"
        for c in final:
            c["rerank_score"] = c["bm25_score"]
            c["rerank_source"] = "skipped"
    else:
        final = chat_rerank.rerank(
            filepath, args.query, candidates,
            top_k=args.top, allow_remote=args.allow_remote_ollama,
        )
        first_src = final[0].get("rerank_source") if final else "unknown"
        strategy = f"bm25+rerank:{first_src}"

    log(f"策略: {strategy}")
    log(f"结果: {len(final)} 条")

    # 输出
    out = {
        "query": args.query,
        "strategy": strategy,
        "top_k": args.top,
        "results": final,
    }
    if args.explain:
        out["explain"] = {
            "bm25_candidate_count": len(bm25_hits),
            "final_count": len(final),
            "bm25_top_param": args.bm25_top,
        }

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
