# AutoAgent Loop Skill

> Autonomous agent engineering loop. 借鉴 autoagent 方法论，让 AI 代理自主迭代优化。

## 核心概念

受 [kevinrgu/autoagent](https://github.com/kevinrgu/autoagent) 启发，封装"实验循环 + 量化评分 + Keep/Discard"方法论。

## 文件结构

```
autoagent-loop/
├── SKILL.md                      # 本文件
├── program.md                    # meta-agent 指令模板
├── executor.py                  # 实验循环执行器
├── evaluator.py                 # 评分 + Keep/Discard 判定
├── analyzer.py                   # 根因分析
├── overfit_detector.py           # 过度拟合检测
├── registry.py                   # 实验记录（results.tsv）
└── scripts/
    ├── run_loop.sh               # 单次循环脚本
    └── continuous.sh            # 持续迭代脚本
```

## 实验循环（Experiment Loop）

```
1. 读取当前 harness 状态
2. 运行 benchmark / 评估任务
3. 诊断失败（根因分析）
4. 生成改进提案
5. 应用改动
6. 重新评估
7. Keep / Discard 判定
8. 记录到 results.tsv
9. 重复
```

## Keep / Discard 规则

- ✅ **Keep**: `passed` 提升了
- ✅ **Keep**: `passed` 相同 + harness 更简单
- ❌ **Discard**: 无提升且更复杂

## 评分指标

- `passed` / total：通过的 task 数量
- `avg_score`：平均分（0-1）
- `cost_usd`：消耗成本
- `complexity`：复杂度（工具数、token 数等）

## 根因分析类别

1. 误解任务
2. 缺少能力或工具
3. 信息收集不足
4. 执行策略不当
5. 缺少验证
6. 环境/依赖问题
7. 静默失败（以为成功但结果错误）

## 过度拟合检测

改进必须反问：
> "如果这个 task 消失，这改进还有价值吗？"

如果答案是"否"→ 过度拟合，丢弃。

## 使用方法

### 启动单次实验
```bash
cd ~/.openclaw/workspace/skills/autoagent-loop
bash scripts/run_loop.sh
```

### 启动持续迭代
```bash
bash scripts/continuous.sh
# 会一直运行，直到被停止
```

### 手动触发进化评估
```python
from executor import ExperimentLoop

loop = ExperimentLoop()
result = await loop.run_once()
keep = evaluator.judge(result)
```

## 对接现有系统

本 skill 可独立运行，也可集成到 `ai-evolution-engine-v2`：

1. 每日复盘时调用 `analyzer.analyze_failures()`
2. 借鉴 Keep/Discard 规则到评分系统
3. 借鉴过度拟合检测到改进提案筛选

## 参考

- https://github.com/kevinrgu/autoagent
- Harbor benchmark format: https://github.com/laude-institute/harbor
