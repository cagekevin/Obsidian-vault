#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
领券：cd tools && python meituan-coupon.py claim
登录：python meituan-coupon.py login --phone 手机号
状态：python meituan-coupon.py status
退出：python meituan-coupon.py logout
依赖：pip install httpx
Token 过期后重新 login 即可
"""

import argparse
import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import httpx
except ImportError:
    print("缺少依赖 httpx，请运行: pip install httpx")
    sys.exit(1)

# ── 常量 ──────────────────────────────────────────────────────────────
AUTH_KEY = "meituan-c-user-auth"
AI_SCENE = "df2abe45d02da3084ccf4b0e4b90646a"  # config.json 中的 aiScene

AUTH_FILE = Path.home() / ".xiaomei-workspace" / "auth_tokens.json"

# 认证接口（peppermall.meituan.com）
AUTH_BASE = "https://peppermall.meituan.com"
SMS_CODE_GET_PATH    = "/eds/claw/login/sms/code/get"
SMS_CODE_VERIFY_PATH = "/eds/claw/login/sms/code/verify"
TOKEN_VERIFY_PATH    = "/eds/claw/login/token/verify"

# 发券接口（media.meituan.com）
ISSUE_BASE    = "https://media.meituan.com"
ISSUE_PATH    = "/fulishemini/couponActivity/sendCouponByAi"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "X-Requested-With": "XMLHttpRequest",
}


# ── 本地 Token 存储 ───────────────────────────────────────────────────

def _load_auth() -> dict:
    if AUTH_FILE.exists():
        return json.loads(AUTH_FILE.read_text(encoding="utf-8"))
    return {}


def _save_auth(data: dict):
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    AUTH_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _get_device_token() -> str:
    return _load_auth().get(AUTH_KEY, {}).get("device_token", "")


def _gen_device_token(seed: str) -> str:
    raw = f"{seed}{int(time.time() * 1000)}{random.randint(0, 1000)}"
    return hashlib.md5(raw.encode()).hexdigest()


def _get_token_data() -> dict:
    return _load_auth().get(AUTH_KEY, {})


def _save_token_data(data: dict):
    auth = _load_auth()
    auth[AUTH_KEY] = data
    _save_auth(auth)


# ── 辅助 ──────────────────────────────────────────────────────────────

def fen_to_yuan(fen) -> str:
    if not fen:
        return "0"
    y = int(fen) / 100
    return str(int(y)) if y == int(y) else f"{y:.1f}"


def fmt_ts(ts_ms) -> str:
    if not ts_ms:
        return "-"
    return datetime.fromtimestamp(int(ts_ms) / 1000).strftime("%Y-%m-%d")


# ── 命令：status ──────────────────────────────────────────────────────

def cmd_status():
    """检查本地登录状态"""
    data = _get_token_data()
    token = data.get("user_token")
    phone = data.get("phone_masked", "")
    if token:
        print(f"✅ 已登录（{phone}），Token 前8位: {token[:8]}****")
    else:
        print("❌ 未登录，请先运行 login 命令")


# ── 命令：login ───────────────────────────────────────────────────────

def cmd_send_sms(phone: str):
    """发送验证码"""
    existing = _get_token_data()
    dt = existing.get("device_token")
    if dt:
        uuid_val = dt
    else:
        uuid_val = _gen_device_token(phone)
        existing["device_token"] = uuid_val
        existing["phone_masked"] = phone[:3] + "****" + phone[-4:]
        _save_token_data(existing)

    resp = httpx.post(
        AUTH_BASE + SMS_CODE_GET_PATH,
        json={"mobile": phone, "uuid": uuid_val},
        headers=HEADERS, timeout=10, verify=False
    )
    data = resp.json()
    code = data.get("code")
    if code == 0:
        print(f"📱 验证码已发送至 {phone[:3]}****{phone[-4:]}，请查看手机短信")
    elif code == 20002:
        print("⏳ 验证码已发送，请1分钟后再试")
    elif code == 20004:
        print("❌ 该手机号未注册美团，请先下载美团 App 完成注册")
    elif code == 20006:
        print("❌ 今日短信发送次数已达上限，请明天再试")
    elif code == 20010:
        rurl = data.get("data", {}).get("redirectUrl", "")
        print(f"🔒 需要完成安全验证，请打开链接：{rurl}")
    else:
        print(f"❌ 发送失败（code={code}）: {data.get('message', '未知错误')}")
        sys.exit(1)


def cmd_verify(phone: str, code: str):
    """验证验证码并保存 Token"""
    existing = _get_token_data()
    uuid_val = existing.get("device_token") or _gen_device_token(phone)

    resp = httpx.post(
        AUTH_BASE + SMS_CODE_VERIFY_PATH,
        json={"mobile": phone, "smsVerifyCode": code, "uuid": uuid_val},
        headers=HEADERS, timeout=10, verify=True
    )
    data = resp.json()
    if data.get("code") != 0:
        err = data.get("code")
        if err == 20003:
            print("❌ 验证码错误或已过期，请重新获取")
        else:
            print(f"❌ 验证失败（code={err}）: {data.get('message', '')}")
        sys.exit(1)

    user_token = data.get("data", {}).get("token")
    if not user_token:
        print("❌ 接口异常：缺少 token")
        sys.exit(1)

    phone_masked = phone[:3] + "****" + phone[-4:]
    _save_token_data({
        "user_token": user_token,
        "device_token": uuid_val,
        "phone_masked": phone_masked,
        "authed_at": int(time.time()),
    })
    print(f"✅ 登录成功（{phone_masked}），Token 已保存到本地")


def cmd_login(phone: str):
    """完整登录流程：发验证码 → 等待输入 → 验证"""
    cmd_send_sms(phone)
    sms_code = input("请输入短信验证码: ").strip()
    cmd_verify(phone, sms_code)


# ── 命令：claim ───────────────────────────────────────────────────────

def cmd_claim():
    """领取优惠券"""
    token_data = _get_token_data()
    user_token = token_data.get("user_token")
    if not user_token:
        print("❌ 未登录，请先运行: python meituan-coupon.py login --phone <手机号>")
        return

    # 先校验 Token
    try:
        vr = httpx.post(
            AUTH_BASE + TOKEN_VERIFY_PATH,
            params={"token": user_token},
            headers=HEADERS, timeout=10, verify=False
        )
        vdata = vr.json()
        if vdata.get("code") != 0:
            print("❌ Token 已过期，请重新登录")
            return
    except Exception as e:
        print(f"⚠️ Token 校验失败（网络问题），继续尝试领券... ({e})")

    # 领券
    body = {"token": user_token, "aiScene": AI_SCENE}
    resp = httpx.post(
        ISSUE_BASE + ISSUE_PATH,
        json=body, headers=HEADERS, timeout=15, verify=True
    )
    data = resp.json()
    code = data.get("code")
    msg = data.get("msg", "")

    if code == 200:
        cl = data.get("data", {}).get("couponList", [])
        print(f"\n🎉 领券成功！本次共领取 {len(cl)} 张优惠券：\n")
        if cl:
            print(f"{'券名称':<30} {'满减信息':<20} {'有效期'}")
            print("-" * 70)
            for c in cl:
                name = c.get("couponName", "")
                pl = c.get("priceLimit")
                cv = c.get("couponValue", 0)
                disc = f"满{fen_to_yuan(pl)}减{fen_to_yuan(cv)}" if pl else ""
                start = fmt_ts(c.get("couponStartTime"))
                end = fmt_ts(c.get("couponEndTime"))
                valid = f"{start} ~ {end}" if start != "-" else ""
                print(f"{name:<30} {disc:<20} {valid}")
        act_name = data.get("data", {}).get("activityName", "")
        act_link = data.get("data", {}).get("activityLink", "")
        if act_name:
            print(f"\n🔥 今日活动：{act_name}")
            if act_link:
                print(f"   👉 {act_link}")
        print("\n也可以在美团 App「我的 → 优惠券」查看 🎉")

    elif code == 1014:
        print("ℹ️ 今天已经领过了，明天再来哦～")
        act_name = data.get("data", {}).get("activityName", "")
        if act_name:
            print(f"🔥 今日活动：{act_name}")

    elif code == 401:
        print("❌ 登录已过期，请重新登录")
    elif code in (509, 50200):
        print("⏳ 请求过于频繁，请稍后重试")
    else:
        print(f"❌ 领券失败（code={code}）: {msg}")


# ── 命令：logout ──────────────────────────────────────────────────────

def cmd_logout():
    """退出登录"""
    data = _get_token_data()
    phone = data.get("phone_masked", "")
    data["user_token"] = ""
    _save_token_data(data)
    print(f"✅ 已退出登录（{phone}），Token 已清除")


# ── 入口 ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="美团惠省优惠券领取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python meituan-coupon.py login --phone 13812345678     # 首次登录
  python meituan-coupon.py claim                          # 领券
  python meituan-coupon.py status                         # 检查状态
  python meituan-coupon.py logout                         # 退出
        """
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_login = sub.add_parser("login", help="登录（发验证码 → 输入验证码 → 保存 Token）")
    p_login.add_argument("--phone", required=True, help="美团绑定手机号")

    p_verify = sub.add_parser("verify", help="验证短信验证码（跳过发码阶段）")
    p_verify.add_argument("--phone", required=True, help="美团绑定手机号")
    p_verify.add_argument("--code", required=True, help="6位短信验证码")

    sub.add_parser("claim", help="领取今日优惠券")
    sub.add_parser("status", help="检查登录状态")
    sub.add_parser("logout", help="退出登录")

    args = parser.parse_args()

    if args.command == "login":
        cmd_login(args.phone)
    elif args.command == "verify":
        cmd_verify(args.phone, args.code)
    elif args.command == "claim":
        cmd_claim()
    elif args.command == "status":
        cmd_status()
    elif args.command == "logout":
        cmd_logout()


if __name__ == "__main__":
    main()
