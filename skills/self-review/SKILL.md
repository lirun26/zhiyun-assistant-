---
name: self-review
description: |
  智云助手自我复盘技能 v2。整合 AI Evolution Engine + actual-self-improvement，
  实现完整的感知-评估-进化-验证闭环。
version: 2.0.0
author: 智云助手
tags: [meta, self-improvement, daily-review, evolution]
---

# 自我复盘技能 v2

整合多个进化系统的完整自我进化解决方案。

## 🧬 整合的进化引擎

| 引擎 | 功能 | 状态 |
|:---|:---|:---|
| AI Evolution Engine v2 | 每日评估 + 进化 | ✅ 已整合 |
| actual-self-improvement | 错误记录 + 学习记录 | ✅ 已整合 |
| auto-skill-evolver | 技能优化提案 | ✅ 可用 |

## 🚀 核心功能

### 1. 每日自动复盘（18:00）
```bash
python3 skills/self-review/scripts/daily_review.py
```

**流程：**
1. 运行 AI Evolution Engine 评估
2. 分析对话数量、错误记录、学习记录
3. 计算质量评分
4. 生成改进建议
5. 记录学到的东西
6. 运行 AI Evolution Engine 进化
7. 保存进化日志

### 2. 快速进化命令
```bash
bash skills/self-review/scripts/quick_evolve.sh [action]
```

**可用 action：**
- `assess` - 运行评估
- `evolve` - 运行进化
- `status` - 查看状态
- `log-error` - 记录错误
- `log-learning` - 记录学习
- `full` - 执行完整流程

### 3. 进化早报（08:00）
每天早上推送，包含：
- 昨日质量评分
- 发现的问题
- 改进建议
- 待处理的学习记录
- 今日重点关注

## 📁 数据存储

| 类型 | 位置 |
|:---|:---|
| 进化日志 | `memory/evolution/YYYY-MM-DD.md` |
| 学习记录 | `.learnings/LEARNINGS.md` |
| 错误记录 | `.learnings/ERRORS.md` |
| 功能请求 | `.learnings/FEATURE_REQUESTS.md` |
| 评估日志 | `skills/self-review/logs/assess.log` |
| 进化日志 | `skills/self-review/logs/evolve.log` |

## 🔧 依赖的技能

- `skills/ai-evolution-engine-v2/` - AI 评估和进化引擎
- `skills/actual-self-improvement/` - 错误和学习记录系统
- `skills/auto-skill-evolver/` - 技能优化提案生成

## 📊 质量评分规则

```
基础分: 75
+ 对话数 > 20: +5
+ 对话数 > 10: +3
+ 每条学习记录: +2
- 错误数 > 5: -10
- 每条错误: -2
范围限制: 50-100
```

## 💡 使用示例

### 手动触发完整复盘
```bash
bash skills/self-review/scripts/quick_evolve.sh full
```

### 查看进化状态
```bash
bash skills/self-review/scripts/quick_evolve.sh status
```

### 记录一个错误
```bash
bash skills/self-review/scripts/quick_evolve.sh log-error "API调用超时" "payment-service.ts"
```

### 记录学到的东西
```bash
bash skills/self-review/scripts/quick_evolve.sh log-learning "发现新的高效批量处理模式"
```

## ⚙️ Cron 配置

| 任务 | 时间 | Cron Expression |
|:---|:---|:---|
| 每日自我复盘 | 18:00 | `0 0 18 * * *` |
| 每日进化早报 | 08:00 | `0 0 8 * * *` |

## 🔄 进化闭环

```
┌─────────────────────────────────────────────────┐
│  每天 18:00                                     │
│  ┌─────────────────┐    ┌────────────────────┐ │
│  │  daily_review   │ -> │  AI Evolution      │ │
│  │  .py           │    │  assess + evolve   │ │
│  └─────────────────┘    └────────────────────┘ │
│         │                       │               │
│         v                       v               │
│  ┌─────────────────┐    ┌────────────────────┐ │
│  │  记录到          │    │  更新知识库        │ │
│  │  .learnings/    │    │  MEMORY.md        │ │
│  └─────────────────┘    └────────────────────┘ │
│                                                 │
│  每天 08:00                                     │
│  ┌─────────────────┐                           │
│  │  推送进化早报    │ -> 老大收到报告           │
│  └─────────────────┘                           │
└─────────────────────────────────────────────────┘
```
