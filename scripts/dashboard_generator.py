#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
店铺经营看板生成器：读取月度经营数据 CSV，生成 HTML 可视化看板 + 核心指标解读。

用法:
    python dashboard_generator.py --input monthly_data.csv --output dashboard.html
    python dashboard_generator.py --demo

CSV 列 (monthly_data.csv):
month,orders,visitors,uv_value,revenue,cost,ads_fee,refund_amount
2026-03,320,8500,9.8,31000,14000,4200,900
"""
import argparse
import base64
import csv
import html
import sys
from datetime import datetime

DEMO = [
    {"month": "2026-03", "orders": 320, "visitors": 8500, "uv_value": 3.6, "revenue": 31000, "cost": 14000, "ads_fee": 4200, "refund_amount": 900},
    {"month": "2026-04", "orders": 540, "visitors": 14200, "uv_value": 3.8, "revenue": 51000, "cost": 23500, "ads_fee": 7800, "refund_amount": 1600},
    {"month": "2026-05", "orders": 710, "visitors": 19800, "uv_value": 4.0, "revenue": 68000, "cost": 31000, "ads_fee": 10200, "refund_amount": 2100},
    {"month": "2026-06", "orders": 950, "visitors": 26400, "uv_value": 4.2, "revenue": 92000, "cost": 42500, "ads_fee": 14100, "refund_amount": 2900},
]

PLATFORM_FEE = 0.05


def load(path):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r["orders"] = int(r["orders"]); r["visitors"] = int(r["visitors"])
            r["uv_value"] = float(r["uv_value"])
            r["revenue"] = float(r["revenue"]); r["cost"] = float(r["cost"])
            r["ads_fee"] = float(r["ads_fee"]); r["refund_amount"] = float(r["refund_amount"])
            rows.append(r)
    return rows


def metrics(rows):
    out = []
    for r in rows:
        net = r["revenue"] - r["cost"] - r["ads_fee"] - r["revenue"] * PLATFORM_FEE - r["refund_amount"]
        out.append({
            "month": r["month"],
            "revenue": r["revenue"],
            "net_profit": net,
            "net_margin": net / r["revenue"] * 100,
            "ads_ratio": r["ads_fee"] / r["revenue"] * 100,
            "conversion": r["orders"] / r["visitors"] * 100,
            "aov": r["revenue"] / r["orders"],
        })
    return out


def svg_chart(ms, key, title, unit="¥", color="#e4393c"):
    """极简 SVG 柱状图"""
    vals = [m[key] for m in ms]
    vmax = max(vals) * 1.15 or 1
    W, H, PAD, BW = 560, 220, 40, 50
    bars = []
    for i, v in enumerate(vals):
        h = v / vmax * (H - 60)
        x = PAD + i * (BW + 30)
        y = H - 40 - h
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="{BW}" height="{h:.1f}" rx="4" fill="{color}"/>')
        bars.append(f'<text x="{x + BW / 2}" y="{y - 6:.1f}" text-anchor="middle" font-size="11" fill="#333">{v:,.0f}{unit if unit != "¥" else ""}</text>')
        bars.append(f'<text x="{x + BW / 2}" y="{H - 20}" text-anchor="middle" font-size="11" fill="#666">{ms[i]["month"]}</text>')
    return f'''<svg viewBox="0 0 {W} {H}" style="width:100%;max-width:600px">
<text x="{PAD}" y="20" font-size="14" font-weight="bold" fill="#333">{title}</text>
{"".join(bars)}</svg>'''


def render(ms, out_path):
    last = ms[-1]
    advice = []
    if last["net_margin"] < 10:
        advice.append(f"净利率 {last['net_margin']:.1f}% 偏低（健康值≥10%）：检查货款成本与退款损耗")
    if last["ads_ratio"] > 30:
        advice.append(f"推广费占比 {last['ads_ratio']:.1f}% 过高（健康值≤30%）：优化标题主图提升免费流量")
    if last["conversion"] < 2:
        advice.append(f"转化率 {last['conversion']:.2f}% 偏低：优化详情页、评价与价格竞争力")
    if not advice:
        advice.append("各项指标健康，聚焦扩大爆款与产品矩阵")

    cards = ""
    for label, val, sub in [
        ("月销售额", f"¥{last['revenue']:,.0f}", last["month"]),
        ("净利润", f"¥{last['net_profit']:,.0f}", f"净利率 {last['net_margin']:.1f}%"),
        ("转化率", f"{last['conversion']:.2f}%", f"客单价 ¥{last['aov']:.0f}"),
        ("推广占比", f"{last['ads_ratio']:.1f}%", "健康值 ≤30%"),
    ]:
        cards += f'''<div style="flex:1;min-width:150px;background:#fff;border:1px solid #eee;border-radius:10px;padding:16px">
<div style="color:#888;font-size:13px">{label}</div>
<div style="font-size:24px;font-weight:700;color:#e4393c;margin:6px 0">{val}</div>
<div style="color:#aaa;font-size:12px">{sub}</div></div>'''

    advice_html = "".join(f"<li style='margin:6px 0'>{html.escape(a)}</li>" for a in advice)
    page = f'''<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>店铺经营看板</title></head>
<body style="font-family:system-ui,'Microsoft YaHei';background:#f6f6f6;margin:0;padding:24px">
<h2 style="margin:0 0 4px">📊 淘宝店铺经营看板</h2>
<div style="color:#999;font-size:13px;margin-bottom:20px">生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:24px">{cards}</div>
<div style="display:flex;gap:20px;flex-wrap:wrap">
<div style="background:#fff;border:1px solid #eee;border-radius:10px;padding:16px">{svg_chart(ms, 'revenue', '月度销售额（¥）')}</div>
<div style="background:#fff;border:1px solid #eee;border-radius:10px;padding:16px">{svg_chart(ms, 'net_profit', '月度净利润（¥）', '', '#2f8f5b')}</div>
</div>
<div style="background:#fff8f0;border:1px solid #f0e0c8;border-radius:10px;padding:16px;margin-top:20px">
<div style="font-weight:700;margin-bottom:8px">🔍 运营诊断建议</div><ul style="margin:0;padding-left:20px">{advice_html}</ul></div>
</body></html>'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"看板已生成: {out_path}")
    for a in advice:
        print(f"  💡 {a}")


def main():
    p = argparse.ArgumentParser(description="店铺经营看板生成器")
    p.add_argument("--input", help="月度经营数据 CSV")
    p.add_argument("--output", default="dashboard.html")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    rows = DEMO if (args.demo or not args.input) else load(args.input)
    render(metrics(rows), args.output)


if __name__ == "__main__":
    main()
