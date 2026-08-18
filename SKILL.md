---
name: taobao-store-0to1
description: 淘宝店铺从0到1全流程运营指导技能。当用户想要开淘宝店、做淘宝店铺运营、选品定位、商品上架优化、店铺装修、淘宝推广（直通车/万相台）、客服话术、经营数据分析、物流发货设置或店铺规模化增长时使用本技能。覆盖开店前调研到月销破千的完整十阶段方法论，并附带选品评估、标题优化、竞品分析、经营看板四个自动化脚本。触发词：开淘宝店、淘宝开店、淘宝运营、店铺从0到1、选品、上架、直通车、生意参谋。
---

# 淘宝店铺从 0 到 1

## 概述

本技能提供淘宝新店铺从零起步到稳定盈利的完整运营方法论，分为十个阶段：市场调研与选品定位 → 店铺注册 → 货源供应链 → 商品上架优化 → 店铺装修 → 营销推广 → 客服体系 → 数据化运营 → 物流发货 → 规模化增长。附四个可直接执行的自动化脚本和开店启动清单。

## 工作流决策树

接到用户请求后，先判断其所处阶段，再加载对应参考文档：

```
用户请求
├── 还没开店 / 想开店 / 卖什么好？
│   → 阶段一《选品定位》+ 阶段二《店铺注册》
│   → 运行 scripts/product_research.py 生成选品评估报告
├── 店已开，没流量 / 没销量
│   → 阶段四《商品上架》+ 阶段六《营销推广》
│   → 运行 scripts/title_optimizer.py 体检标题
├── 想分析竞争对手 / 怎么定价
│   → 阶段一 §2 + scripts/competitor_analysis.py
├── 客服/售后/差评问题
│   → 阶段七《客服体系》
├── 数据分析 / 利润核算 / 经营复盘
│   → 阶段八《运营与数据分析》+ scripts/dashboard_generator.py
├── 发货 / 快递 / 退货
│   → 阶段九《物流与发货》
└── 想扩大规模 / 做品牌 / 多渠道
    → 阶段十《规模化增长》
```

## 十阶段速查

| 阶段 | 参考文档 | 核心动作 | 关键产出 |
|------|---------|---------|---------|
| 1 选品定位 | references/phase-01-positioning.md | 四维度评估 + 利润测算 | 选品评估表、竞品拆解表 |
| 2 店铺注册 | references/phase-02-registration.md | C店注册 + 保证金 + 基础设置 | 可营业店铺 |
| 3 货源供应链 | references/phase-03-sourcing.md | 一件代发起步 + 供应商评估 | 稳定货源 |
| 4 商品上架 | references/phase-04-listing.md | 标题公式 + 主图规划 + 详情页 FABE | 优化后的商品列表 |
| 5 店铺装修 | references/phase-05-design.md | 手机端首页 + 视觉统一 | 装修完成的店铺 |
| 6 营销推广 | references/phase-06-marketing.md | 搜索优化 + 直通车 + 活动 + 内容 | 推广排期表 |
| 7 客服体系 | references/phase-07-service.md | 话术 SOP + 售后流程 | 客服话术手册 |
| 8 数据运营 | references/phase-08-data.md | 指标体系 + 诊断三步法 | 月度经营看板 |
| 9 物流发货 | references/phase-09-logistics.md | 发货 SOP + 快递谈判 | 48h 时效达标 |
| 10 规模增长 | references/phase-10-scaling.md | 产品矩阵 + 品牌 + 多渠道 | 增长路线图 |

## 自动化脚本使用

所有脚本零依赖（仅 Python 标准库），均支持 `--demo` 演示模式：

```bash
# 1. 选品评估：四维度打分 + 净利测算（输入 JSON 见脚本头部说明）
python scripts/product_research.py --input candidates.json

# 2. 标题优化：生成 / 体检（违禁词、堆砌、字数）
python scripts/title_optimizer.py generate --core 收纳盒 --words 大容量,家用,塑料
python scripts/title_optimizer.py check --title "现有标题"

# 3. 竞品分析：价格带空白 + 头部集中度 + 差评机会点（输入 CSV 见脚本头部）
python scripts/competitor_analysis.py --input competitors.csv

# 4. 经营看板：月度数据 → HTML 可视化 + 运营诊断建议
python scripts/dashboard_generator.py --input monthly_data.csv --output dashboard.html
```

## 核心原则（贯穿全流程）

1. **先选品后开店**：完成调研再注册，珍惜新店 3 个月扶持期
2. **严禁刷单**：2026 年稽查必抓，合规运营是底线
3. **数据驱动**：所有优化决策基于生意参谋数据，不凭感觉
4. **利润优先**：盯净利润率（≥10%）而非销售额，每月核算
5. **聚焦单品**：新手先打透 1 个爆款，再谈产品矩阵

## 资源清单

- `references/phase-01~10-*.md`：十阶段详细方法论（按需加载，勿一次性全读）
- `scripts/`：product_research.py、title_optimizer.py、competitor_analysis.py、dashboard_generator.py
- `assets/store_launch_checklist.md`：开店启动全流程勾选清单（可直接交付给用户跟踪进度）
- `assets/title_formula.json`：标题公式、关键词来源、主图规划（结构化数据，供程序读取）
