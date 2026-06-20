#!/usr/bin/env python3
"""
网盘下载 — 网盘资源搜索与转存工具
====================================
搜索夸克/百度网盘资源，检测链接有效性，并可转存到自己的网盘。

用法:
  # 搜索资源
  python3 tools/网盘下载/网盘下载.py search <关键词> [选项]

  # 保存到夸克网盘（需配置 QUARK_COOKIE）
  python3 tools/网盘下载/网盘下载.py quark-save <分享链接> <目标目录> [选项]

  # 保存到百度网盘（需配置 BAIDU_COOKIE）
  python3 tools/网盘下载/网盘下载.py baidu-save <分享链接> <目标路径> [选项]

  # 检查环境
  python3 tools/网盘下载/网盘下载.py check
  python3 tools/网盘下载/网盘下载.py check-env
  python3 tools/网盘下载/网盘下载.py check-cookies

搜索选项:
  --format json|markdown    输出格式（默认 markdown）
  --max-candidates N        最大返回条数（默认 50）
  --cloud-types baidu,quark 限定网盘类型
  --include 关键词           包含过滤
  --exclude 关键词           排除过滤
  --check-links             检测链接是否有效
  --refresh                 强制刷新缓存

保存选项:
  --dry-run                 只预览，不真正保存（推荐先预览）
  --yes                     跳过确认直接保存
  --resource-type auto|series|movie|collection  资源类型
  --context-name "名称"     指定资源名（用于修正文件名）
  --passcode 提取码          百度网盘提取码
  --select all|1,3|2-5      选择要保存的条目

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
保存流程（AI 按此步骤操作）：

1. 先预览：用 --dry-run 查看分享内容，不实际保存
   → 判断资源类型（剧集/电影/合集）
   → 判断资源名是否需要修正

2. 确认后再保存：加 --yes 真正执行
   → 传 --resource-type 告诉脚本资源类型
   → 传 --context-name 修正文件名（如有必要）

3. 保存后检查：确认转存成功

错误处理：
  1. Cookie 无效 → 重新登录网页版，复制新的 Cookie
  2. 目录不存在 → 先在网盘里创建目标目录
  3. 分享链接失效 → 重新搜索
  4. 提取码错误 → 检查链接里的 pwd 参数
  5. 网络超时 → 重试

安全规则：
  - Cookie = 完整登录凭证，绝对不能打印、不能提交到 Git
  - 不确定时先用 --dry-run 预览，不要直接保存
  - 不要批量保存不确认的资源
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

配置:
  复制本目录下的 .env.example 为 .env
  填写 QUARK_COOKIE 或 BAIDU_COOKIE
  纯搜索不需要 Cookie
"""

import sys
import json
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR


def run_npm(script_name: str, *args) -> str:
    cmd = ["npm", "run", script_name, "--"] + list(args)
    result = subprocess.run(cmd, cwd=PROJECT_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        err = result.stderr.strip()
        if err:
            print(err, file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def cmd_search(args: list):
    if not args:
        print("用法: python3 tools/网盘下载/网盘下载.py search <关键词> [选项]")
        return
    print(run_npm("search", *args))


def cmd_quark_save(args: list):
    if len(args) < 2:
        print("用法: python3 tools/网盘下载/网盘下载.py quark-save <分享链接> <目标目录> [选项]")
        return
    print(run_npm("quark-save", args[0], args[1], *args[2:]))


def cmd_baidu_save(args: list):
    if len(args) < 2:
        print("用法: python3 tools/网盘下载/网盘下载.py baidu-save <分享链接> <目标路径> [选项]")
        return
    print(run_npm("baidu-save", args[0], args[1], *args[2:]))


def cmd_check(args: list):
    print(run_npm("check-ready"))


def cmd_check_env(args: list):
    result = run_npm("check-env")
    if not result:
        return
    try:
        data = json.loads(result)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(result)


def cmd_check_cookies(args: list):
    print(run_npm("check-cookies"))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    cmd_args = sys.argv[2:]

    commands = {
        "search": cmd_search,
        "quark-save": cmd_quark_save,
        "baidu-save": cmd_baidu_save,
        "check": cmd_check,
        "check-env": cmd_check_env,
        "check-cookies": cmd_check_cookies,
    }

    if cmd not in commands:
        print(f"未知命令: {cmd}")
        print(f"可用命令: {', '.join(commands.keys())}")
        return

    commands[cmd](cmd_args)


if __name__ == "__main__":
    main()
