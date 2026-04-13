# AutoAgent Loop 与现有系统集成指南

## 与 ai-evolution-engine-v2 集成

### 1. 借鉴 Keep/Discard 规则

在每日复盘时，使用 `Evaluator` 进行判定：

```python
from autoagent_loop import Evaluator, ExperimentResult

evaluator = Evaluator()

# 复盘时对比昨日和今日的表现
decision = evaluator.judge(today_result, yesterday_result)
```

### 2. 使用根因分析

在分析失败时，使用 `FailureAnalyzer`：

```python
from autoagent_loop import FailureAnalyzer, TaskFailure

analyzer = FailureAnalyzer()

# 分析失败
failures = [
    TaskFailure(task_name="某任务", score=0.3, trajectory={}),
    # ...
]
analysis = analyzer.analyze(failures)

# 生成改进建议
suggestions = analyzer.generate_suggestions(analysis["categorized"])
for s in suggestions:
    print(s)
```

### 3. 使用过度拟合检测

在评估改进提案时，使用 `OverfitDetector`：

```python
from autoagent_loop import OverfitDetector, ChangeProposal

detector = OverfitDetector()

proposal = ChangeProposal(
    description="为 task_abc 添加专用工具",
    changed_files=["agent.py", "tasks/task_abc/test.py"],
    task_specific=False,
    reasoning="只针对特定任务"
)

is_overfit, reason = detector.detect(proposal, harness_code)
if is_overfit:
    print(f"Discard: {reason}")
```

### 4. 集成到每日 cron 任务

可以在现有的每日 18:00 复盘任务中增加：

```python
# 在每日复盘流程中
from autoagent_loop import evaluator, analyzer, detector

# 1. 分析今天的失败
analysis = analyzer.analyze(today_failures)

# 2. 生成改进提案
proposals = analyzer.generate_proposals(analysis)

# 3. 过滤过度拟合
valid_proposals = [p for p in proposals if not detector.detect(p, "")[0]]

# 4. Keep/Discard 判定
# ... 应用最佳提案 ...
```

## 与 Beads 任务追踪集成

```bash
# 创建进化任务
bd create "集成 AutoAgent Loop 方法论" -p 1

# 任务清单：
# 1. 将 Keep/Discard 规则集成到 ai-evolution-engine-v2
# 2. 将根因分析集成到每日复盘流程
# 3. 添加过度拟合检测到提案筛选
# 4. 创建每日实验记录到 results.tsv
```

## 记忆系统集成

在完成集成后，更新记忆：

```
## 2026-04-05 更新

### AutoAgent Loop 已集成
- 核心模块：evaluator, analyzer, detector, registry, executor
- 方法论：Keep/Discard 规则、根因分析、过度拟合检测
- 位置：skills/autoagent-loop/
```

## 下一步

1. 将 evaluator 集成到每日复盘
2. 将 analyzer 集成到失败诊断
3. 将 detector 集成到提案筛选
4. 创建 results.tsv 记录实验历史
