# Memory Pruner - 记忆断舍离

> 基于 AutoAgent Loop 方法论的记忆质量评估与整理

## 核心思路

记忆不是越多越好，要像整理房间一样定期"断舍离"：

- **Keep**：长期有价值、反复用到
- **Discard**：一次性信息、长期未用、噪音
- **Review**：待审核，不确定就放一起

## 7 类记忆评估

| 类别 | 说明 | 策略 |
|:---|:---|:---|
| 误解任务 | 记错、记偏 | Discard + 纠正 |
| 缺少验证 | 未经确认 | Review + 待确认 |
| 信息不足 | 片段记忆 | Review + 补充 |
| 静默失败 | 以为记住实际忘 | Discard |
| 重复堆积 | 多个地方记同一件事 | Merge |
| 长期未用 | >30天没用到 | Archive 或 Discard |
| 噪音 | 一次性临时信息 | Discard |

## 使用场景

### 场景1：每日复盘时
```bash
node memory-pruner/analyze.mjs
```

### 场景2：记忆超限时
```bash
node memory-pruner/prune.mjs --target=HOT_MEMORY
```

### 场景3：检查某条记忆
```bash
node memory-pruner/evaluate.mjs --text="某条记忆内容"
```

## 评估维度

| 维度 | 指标 | 阈值 |
|:---|:---|:---|
| 使用频率 | usage_count | >3 → Keep |
| 最后使用 | days_since_use | >30 → Review |
| 信息密度 | token_count | <50 + 低频 → Discard |
| 时效性 | is_ephemeral | true → Discard |

## 整理策略

1. **HOT_MEMORY**：30分钟未活跃 + 低频 → 移到 Archive 或 Discard
2. **WARM_MEMORY**：60天未变 + 低频 → Archive
3. **COLD_MEMORY**：180天未用 → Archive 到 history/
4. **ERRORS**：同类错误 >3 次 → 提炼教训到 LEARNINGS

## 文件结构

```
memory-pruner/
├── SKILL.md
├── analyze.mjs      # 分析记忆质量
├── prune.mjs        # 整理记忆
├── scorer.mjs       # 评分引擎
└── config.json      # 阈值配置
```

## 配置

```json
{
  "hot": {
    "max_age_minutes": 30,
    "min_usage_to_keep": 1,
    "discard_threshold": 0.3
  },
  "warm": {
    "max_age_days": 60,
    "min_usage_to_keep": 3,
    "discard_threshold": 0.4
  },
  "cold": {
    "max_age_days": 180,
    "min_usage_to_keep": 5,
    "archive_threshold": 0.6
  }
}
```

## 与现有系统集成

- ✅ memory-tiering（三层记忆）
- ✅ autoagent-loop（评估方法论）
- ✅ daily review（每日复盘）

## 使用时机

1. **每日 18:00 复盘**：运行 prune.mjs
2. **心跳检查**：轻量扫描 HOT_MEMORY
3. **记忆搜索后**：评估结果的相关性
