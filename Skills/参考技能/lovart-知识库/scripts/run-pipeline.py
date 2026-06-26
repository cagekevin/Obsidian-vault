#!/usr/bin/env python3
"""
【全自动管线】钓鱼 → 晋升 → 清理 → 重建索引，一步完成。

用法：
    python scripts/run-pipeline.py              # 全流程
    python scripts/run-pipeline.py --no-delete  # 晋升但不删原始文件
"""
import subprocess, sys, os, json

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_KB_DIR = os.path.dirname(_SCRIPTS_DIR)

# W7 的 lovart.py — 统一对话入口
_W7_DIR = os.path.normpath(os.path.join(_SCRIPTS_DIR, "..", "..", "W7-API链接", "lovart-skill"))
LOVART = os.path.join(_W7_DIR, "lovart.py")
PROMOTE = os.path.join(_SCRIPTS_DIR, "promote.py")
FISH_TASKS = os.path.join(_KB_DIR, "_meta", "fish_tasks.json")
FISH_OUTPUT = os.path.join(_KB_DIR, "00-钓鱼话术")


def run_step(label, cmd):
    print(f"\n{'='*50}")
    print(f"  ▶  {label}")
    print(f"{'='*50}")
    sys.stdout.flush()
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode


def main():
    no_delete = "--no-delete" in sys.argv

    # Step 1: 批量对话（通过 W7 lovart.py batch 模式）
    # fish_tasks.json 格式: {"tasks": [{"label":"...", "prompt":"..."}]}
    # 需要包装成 lovart.py 的 batch 格式 JSON
    batch_config = os.path.join(_KB_DIR, "_meta", "_batch_config.json")
    try:
        with open(FISH_TASKS, encoding="utf-8") as f:
            fish_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ fish_tasks.json 不存在或格式错误")
        return

    cfg = {
        "mode": "batch",
        "name": "知识库钓鱼",
        "tasks": fish_data.get("tasks", []),
        "follow_ups": 5,
        "output_dir": FISH_OUTPUT,
        "mark_done": True,
    }
    with open(batch_config, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    run_step("Layer 1: 批量对话",
             [sys.executable, LOVART, batch_config])

    # Step 2: 晋升 + 自动 rebuild
    promote_cmd = [sys.executable, PROMOTE, "--batch"]
    if not no_delete:
        promote_cmd.append("--delete")
    run_step("Layer 2: 晋升 + 重建索引", promote_cmd)

    # 清理临时文件
    try:
        os.remove(batch_config)
    except OSError:
        pass

    print(f"\n{'='*50}")
    print("  ✅ 全流程完成！")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
