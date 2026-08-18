# taobao-store-0to1

淘宝店铺从 0 到 1 全流程运营 Skill（WorkBuddy 技能包）。

## 简介

覆盖新店铺从零起步到稳定盈利的十个阶段方法论，附 4 个零依赖自动化脚本：

| 阶段 | 文档 |
|------|------|
| 1. 市场调研与选品定位 | `references/phase-01-positioning.md` |
| 2. 店铺注册与搭建 | `references/phase-02-registration.md` |
| 3. 货源与供应链 | `references/phase-03-sourcing.md` |
| 4. 商品上架与优化 | `references/phase-04-listing.md` |
| 5. 店铺装修 | `references/phase-05-design.md` |
| 6. 营销推广 | `references/phase-06-marketing.md` |
| 7. 客服体系 | `references/phase-07-service.md` |
| 8. 运营与数据分析 | `references/phase-08-data.md` |
| 9. 物流与发货 | `references/phase-09-logistics.md` |
| 10. 规模化增长 | `references/phase-10-scaling.md` |

## 自动化脚本

```bash
# 选品四维度评估报告
python scripts/product_research.py --demo

# 标题生成 / 体检（违禁词、堆砌检查）
python scripts/title_optimizer.py generate --core 收纳盒 --words 大容量,家用
python scripts/title_optimizer.py check --title "现有标题"

# 竞品分析（价格带空白 + 差评机会点）
python scripts/competitor_analysis.py --demo

# 月度经营 HTML 看板
python scripts/dashboard_generator.py --demo --output dashboard.html
```

## 安装到 WorkBuddy

将本仓库放入 `~/.workbuddy/skills/` 目录（或压缩为 zip 后在技能管理中导入）即可生效。

## 使用声明

内容为电商运营方法论参考，不构成任何投资或经营建议。请遵守平台规则，禁止刷单等违规操作。
