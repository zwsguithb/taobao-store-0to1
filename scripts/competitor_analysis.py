#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品分析工具：导入竞品数据 CSV/JSON，输出定价与卖点建议 + 空白价格带分析。

用法:
    python competitor_analysis.py --input competitors.csv
    python competitor_analysis.py --demo

CSV 列 (competitors.csv):
name,price,monthly_sales,main_selling_point,review_count,negative_keywords
"""
import argparse
import csv
import json
import sys
from statistics import median

DEMO = [
    {"name": "竞品A-旗舰店", "price": 89, "monthly_sales": 3000, "main_selling_point": "静音电机", "review_count": 12000, "negative_keywords": "噪音大,续航短"},
    {"name": "竞品B-C店", "price": 59, "monthly_sales": 5000, "main_selling_point": "低价走量", "review_count": 8000, "negative_keywords": "质量差,塑料感"},
    {"name": "竞品C-企业店", "price": 129, "monthly_sales": 1200, "main_selling_point": "app智控", "review_count": 4500, "negative_keywords": "贵,app难用"},
    {"name": "竞品D-C店", "price": 69, "monthly_sales": 2200, "main_selling_point": "赠品多", "review_count": 3000, "negative_keywords": "发货慢"},
]


def load_data(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["price"] = float(row["price"])
            row["monthly_sales"] = int(row["monthly_sales"])
            row["review_count"] = int(row.get("review_count", 0))
            rows.append(row)
    return rows


def analyze(rows):
    prices = sorted(r["price"] for r in rows)
    total_sales = sum(r["monthly_sales"] for r in rows)
    prices_med = median(prices)

    # 头部集中度: TOP10(此处取前3)销量占比
    top3 = sorted(rows, key=lambda x: -x["monthly_sales"])[:3]
    concentration = sum(r["monthly_sales"] for r in top3) / total_sales if total_sales else 0

    # 价格带分析: 以 20 元为档找空白带
    bands = {}
    for r in rows:
        band = int(r["price"] // 20) * 20
        bands.setdefault(band, {"count": 0, "sales": 0})
        bands[band]["count"] += 1
        bands[band]["sales"] += r["monthly_sales"]
    all_bands = range(0, int(max(prices)) + 20, 20)
    gaps = [b for b in all_bands if b not in bands]

    # 差评关键词汇总
    neg = {}
    for r in rows:
        for kw in str(r.get("negative_keywords", "")).split(","):
            kw = kw.strip()
            if kw:
                neg[kw] = neg.get(kw, 0) + 1
    top_neg = sorted(neg.items(), key=lambda x: -x[1])[:5]

    # 卖点分布
    selling_points = [r.get("main_selling_point", "") for r in rows if r.get("main_selling_point")]

    return {
        "price_min": prices[0], "price_max": prices[-1], "price_median": prices_med,
        "top3_concentration": concentration,
        "gap_bands": gaps,
        "top_negative": top_neg,
        "selling_points": selling_points,
    }


def render(rows, a):
    L = []
    L.append("=" * 60)
    L.append("竞品分析报告")
    L.append("=" * 60)
    L.append(f"\n【价格区间】¥{a['price_min']:.0f} ~ ¥{a['price_max']:.0f}，中位数 ¥{a['price_median']:.0f}")
    L.append(f"【头部集中度】TOP3 销量占比 {a['top3_concentration'] * 100:.0f}%"
             + ("（<50%，竞争尚可）" if a["top3_concentration"] < 0.5 else "（>50%，红海警示）"))
    L.append(f"【空白价格带】{', '.join(f'¥{b}-{b+20}' for b in a['gap_bands']) or '无（各价格带均有竞品）'}")
    L.append("\n【竞品卖点】")
    for r in sorted(rows, key=lambda x: -x["monthly_sales"]):
        L.append(f"  {r['name']}  ¥{r['price']:.0f}  月销{r['monthly_sales']}  卖点: {r.get('main_selling_point','-')}")
    L.append("\n【差评高频词（机会点！）】")
    for kw, cnt in a["top_negative"]:
        L.append(f"  {kw} ×{cnt}")
    L.append("\n【定价建议】")
    if a["gap_bands"]:
        b = a["gap_bands"][0]
        L.append(f"  优先卡位空白带 ¥{b}-{b+20}；或对标中位数 ¥{a['price_median']:.0f} 下浮 5-10%")
    else:
        L.append(f"  无空白带，对标中位数 ¥{a['price_median']:.0f}，用赠品/服务做差异化")
    L.append("\n【差异化方向】针对差评高频词反向优化详情页与选品，逐条解决用户痛点。")
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description="淘宝竞品分析工具")
    p.add_argument("--input", help="竞品 CSV 文件")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    rows = DEMO if (args.demo or not args.input) else load_data(args.input)
    if not rows:
        print("无数据", file=sys.stderr); sys.exit(1)
    print(render(rows, analyze(rows)))


if __name__ == "__main__":
    main()
