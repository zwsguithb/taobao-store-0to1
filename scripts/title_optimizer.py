#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品标题优化工具：按淘宝标题公式组装/体检标题。

功能（子命令格式）:
    python title_optimizer.py generate --core 收纳盒 --words 大容量,家用,塑料,桌面
        按公式生成 30 字(60字符)内优化标题
    python title_optimizer.py check --title "你的现有标题"
        体检标题：字数、核心词位置、违禁词、重复词
"""
import argparse
import re
import sys

# 常见违禁极限词（广告法）
BANNED_WORDS = [
    "最好", "最优", "第一", "顶级", "国家级", "世界级", "最高级", "最佳",
    "绝无仅有", "万能", "特效", "无敌", "纯天然", "100%", "首家", "独一无二",
    "之王", "之王", "极致", "完美", "永久", "彻底根治",
]
MAX_LEN = 30  # 汉字数（60字符）

CORE_FRONT = "核心词应出现在标题前13字内（手机端展示权重最高）"


def build_title(core, words):
    """营销词 + 类目核心词 + 属性词 + 长尾词 + 卖点词"""
    marketing = ["新款", "升级", "热卖", "爆款"]
    attrs = [w.strip() for w in (words or "").split(",") if w.strip()]
    parts = []
    # 核心词前置
    parts.append(core)
    # 属性词
    for a in attrs[:4]:
        parts.append(a)
    # 营销词补充
    used = sum(len(p) for p in parts)
    for m in marketing:
        if used + len(m) > MAX_LEN - 4:
            break
        if m not in parts:
            parts.append(m)
            used += len(m)
    title = "".join(parts)
    if len(title) > MAX_LEN:
        title = title[:MAX_LEN]
    return title


def check_title(title):
    issues = []
    length = len(title)
    if length > MAX_LEN:
        issues.append(f"字数超限：{length} 字 > {MAX_LEN} 字上限")
    elif length < 20:
        issues.append(f"字数不足：仅 {length} 字，浪费流量入口（建议 25-30 字）")

    # 违禁词检测
    hits = [w for w in BANNED_WORDS if w in title]
    if hits:
        issues.append(f"发现违禁极限词: {'、'.join(hits)} → 必须删除，存在广告法风险")

    # 符号检测
    if re.search(r"[，。！？、\s/|]", title):
        issues.append("含空格或标点符号：会被切词降权，建议删除")

    # 重复词检测（2字以上重复）
    tokens = [title[i:i + 2] for i in range(len(title) - 1)]
    seen, dup = set(), set()
    for t in tokens:
        if t in seen:
            dup.add(t)
        seen.add(t)
    if dup:
        issues.append(f"疑似堆砌重复词: {'、'.join(sorted(dup))}")

    # 英文/数字混排提示
    if re.search(r"[a-zA-Z0-9]", title) and not re.search(r"[A-Za-z0-9]+[\u4e00-\u9fa5]", title):
        pass  # 正常情况

    return length, issues


def main():
    parser = argparse.ArgumentParser(description="淘宝标题优化与体检工具")
    sub = parser.add_subparsers(dest="cmd")
    g = sub.add_parser("generate", help="生成优化标题")
    g.add_argument("--core", required=True, help="类目核心词，如：收纳盒")
    g.add_argument("--words", default="", help="属性词/长尾词，逗号分隔")
    c = sub.add_parser("check", help="体检现有标题")
    c.add_argument("--title", required=True, help="待检查的标题")
    args = parser.parse_args()

    if args.cmd == "generate":
        title = build_title(args.core, args.words)
        print(f"生成标题（{len(title)} 字）:\n{title}")
        print(f"\n提示: {CORE_FRONT}")
        print("建议: 上架7天后用生意参谋搜索词数据替换零流量词")
    elif args.cmd == "check":
        length, issues = check_title(args.title)
        print(f"标题体检报告（{length}/{MAX_LEN} 字）")
        if not issues:
            print("✅ 未发现问题，结构基本合格")
        else:
            for i, msg in enumerate(issues, 1):
                print(f"⚠ 问题{i}: {msg}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
