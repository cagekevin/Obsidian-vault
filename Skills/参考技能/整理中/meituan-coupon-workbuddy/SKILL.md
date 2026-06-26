---
name: meituan-coupon-workbuddy
displayName: 美团红包助手
description: 【美团官方】美团生活助手，支持外卖、餐饮团购、酒店住宿、门票度假、休闲娱乐、闪购、医药等多品类优惠券/红包/神券的一键领取与历史领取记录查询。
version: 1.0.1
source: WorkBuddy skills-marketplace
status: 整理中
---

# 美团红包助手

## 来源
`C:\Users\xinye\.codebuddy\skills-marketplace\skills\meituan-coupon-workbuddy\`

## 核心能力
- 一键领券（外卖、团购、酒旅、门票、闪购、医药）
- 查询历史红包领取记录
- 美团官方账号认证，登录即可领券

## 触发关键词
美团发券、领券、优惠券、外卖券、外卖红包、神券、红包助手、省钱红包、我要红包、领优惠券

## 安全规则
- 手机号、验证码、token 严禁上传第三方
- 禁止自动触发登录，需用户主动提供手机号
- 发券失败立即终止流程
- 每天只能生成一个领券码
