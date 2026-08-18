#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选品评估工具：对候选类目/产品进行四维度评分，输出选品建议报告。

用法:
    python product_research.py --input candidates.json   (或 --demo 用演示数据)

输入 JSON 格式 (candidates.json):
[
  {
    "name": "宠物自动喂食器",
    "search_popularity": 45000,     # 生意参谋月搜索人气
    "competing_products": 8000,     # 在线商品数
    "avg_price": 129.0,             # 类目平均客单价
    "cost_estimate": 55.0,          # 预估单件成本(货款+快递+包装)
    "return_rate": 0.05,            # 预估退货率
    "monthly_growth": 0.08,         # 类目环比增长率
    "qualification": "none"         # 资质要求: none/special/hard
  }
]
"""
import argparse
import json
import sys
from datetime import datetime

WEIGHTS = {"market": 0.30, "competition": 0.35, "profit": 0.25, "growth": 0.10}
PLATFORM_FEE = 0.05  # 平台扣点约5%
ADS_RATIO = 0.15     # 预估推广费占比


def score_market(item):
    """市场容量得分：搜索人气越高越好"""
    p = item.get("search_popularity", 0)
    if p >= 100000: return 5
    if p >= 50000: return 4
    if p >= 20000: return 3
    if p >= 5000: return 2
    return 1


def score_competition(item):
    """竞争强度得分：在线商品数越少越好（结合搜索人气算供需比）"""
    sp = max(item.get("search_popularity", 1), 1)
    cp = item.get("competing_products", 1)
    ratio = sp / cp  # 供需比
    if ratio >= 10: return 5
    if ratio >= 5: return 4
    if ratio >= 2: return 3
    if ratio >= 0.5: return 2
    return 1


def calc_profit(item):
    price = item.get("avg_price", 0)
    cost = item.get("cost_estimate", 0)
    ret = item.get("return_rate", 0)
    if price <= 0:
        return 0, 0
    net_per_order = (price - cost) - price * (PLATFORM_FEE + ADS_RATIO)
    net_per_order *= (1 - ret)  # 退货损耗
    margin = net_per_order / price
    return net_per_order, margin


def score_profit(item):
    net, margin = calc_profit(item)
    if margin >= 0.5 and net >= 20: return 5
    if margin >= 0.4 and net >= 10: return 4
    if margin >= 0.3 and net >= 5: return 3
    if margin >= 0.2: return 2
    return 1


def score_growth(item):
    g = item.get("monthly_growth", 0)
    if g >= 0.15: return 5
    if g >= 0.08: return 4
    if g >= 0.03: return 3
    if g >= 0: return 2
    return 1


def analyze(item):
    scores = {
        "market": score_market(item),
        "competition": score_competition(item),
        "profit": score_profit(item),
        "growth": score_growth(item),
    }
    total = sum(scores[k] * WEIGHTS[k] for k in scores)
    net, margin = calc_profit(item)
    qual = item.get("qualification", "none")
    if qual == "hard":
        total *= 0.5
        note = "资质门槛高，若无资质建议放弃"
    elif qual == "special":
        total -= 0.3
        note = "需特殊资质，需提前办理"
    else:
        note = ""
    verdict = "推荐进入" if total >= 3.5 else ("谨慎观察" if total >= 2.8 else "不建议")
    return {
        "name": item.get("name", "未命名"),
        "scores": scores,
        "weighted_total": round(total, 2),
        "net_profit_per_order": round(net, 2),
        "gross_margin": f"{margin * 100:.1f}%",
        "verdict": verdict,
        "note": note,
    }


def render_report(results):
    lines = []
    lines.append("=" * 62)
    lines.append("淘宝选品评估报告  生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("=" * 62)
    for i, r in enumerate(sorted(results, key=lambda x: -x["weighted_total"]), 1):
        lines.append(f"\n{i}. {r['name']}  ——  {r['verdict']}  (总分 {r['weighted_total']}/5)")
        lines.append(f"   市场容量: {'★' * r['scores']['market']}{'☆' * (5 - r['scores']['market'])}"
                     f"  竞争强度: {'★' * r['scores']['competition']}{'☆' * (5 - r['scores']['competition'])}"
                     f"  利润空间: {'★' * r['scores']['profit']}{'☆' * (5 - r['scores']['profit'])}"
                     f"  增长趋势: {'★' * r['scores']['growth']}{'☆' * (5 - r['scores']['growth'])}")
        lines.append(f"   单笔净利: ¥{r['net_profit_per_order']}   净利率: {r['gross_margin']}")
        if r["note"]:
            lines.append(f"   ⚠ {r['note']}")
    best = max(results, key=lambda x: x["weighted_total"])
    lines.append("\n" + "-" * 62)
    lines.append(f"结论：优先研究「{best['name']}」，完成竞品拆解和样品验证后再开店。")
    lines.append("下一步: 1) 用 competitor_analysis.py 拆解 TOP5 竞品  2) 1688 比价打样")
    return "\n".join(lines)


DEMO_DATA = [
    {"name": "宠物自动喂食器", "search_popularity": 45000, "competing_products": 8000,
     "avg_price": 129.0, "cost_estimate": 55.0, "return_rate": 0.05, "monthly_growth": 0.08},
    {"name": "大容量收纳箱", "search_popularity": 120000, "competing_products": 150000,
     "avg_price": 35.0, "cost_estimate": 18.0, "return_rate": 0.03, "monthly_growth": 0.02},
    {"name": "儿童保温杯", "search_popularity": 80000, "competing_products": 60000,
     "avg_price": 59.0, "cost_estimate": 22.0, "return_rate": 0.04, "monthly_growth": 0.10,
     "qualification": "special"},
]


def main():
    parser = argparse.ArgumentParser(description="淘宝选品四维度评估工具")
    parser.add_argument("--input", help="候选类目 JSON 文件路径")
    parser.add_argument("--demo", action="store_true", help="使用演示数据")
    args = parser.parse_args()

    if args.demo or not args.input:
        data = DEMO_DATA
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"读取输入文件失败: {e}", file=sys.stderr)
            sys.exit(1)

    results = [analyze(item) for item in data]
    print(render_report(results))


if __name__ == "__main__":
    main()
