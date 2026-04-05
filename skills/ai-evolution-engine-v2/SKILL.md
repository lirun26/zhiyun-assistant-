# AI Evolution Engine v2

AI自我进化引擎 - 融入 AutoAgent Loop 方法论。

## 核心升级（v2）

基于 [kevinrgu/autoagent](https://github.com/kevinrgu/autoagent) 方法论，集成以下核心机制：

1. **Keep/Discard 规则** - passed 提升才保留，否则丢弃
2. **根因分析** - 7类失败分类，按类修复
3. **过度拟合检测** - 问自己"如果这个 task 消失，这改进还有价值吗？"
4. **NEVER STOP** - 持续迭代直到被打断
5. **实验记录** - results.tsv 追踪所有实验

## 核心架构

基于 SEA 循环 + AutoAgent Loop：

```
感知层 (Sense) → 评估层 (Evaluate) → 进化层 (Evolve) → 验证层 (Validate)
                      ↓
              Keep/Discard 判定 ← 实验循环
```

## 功能模块

### 1. 自我评估 v2

```bash
node scripts/assess-v2.mjs
```

评估内容：
- 能力清单（工具、技能、知识）
- 性能指标（从 results.tsv 读取 passed/score）
- 根因分析（7类失败分类统计）
- 知识缺口识别
- 改进建议（基于分析）

### 2. 进化机制 v2

```bash
node scripts/evolve-v2.mjs
```

进化流程：
1. 检查当前 baseline
2. 根因分析（从 .learnings/ERRORS.md）
3. 生成改进提案
4. 过度拟合检测
5. 应用改进
6. Keep/Discard 判定

### 3. 实验循环

基于 AutoAgent Loop 的持续改进：

```python
# 伪代码
while True:
    result = run_benchmark()
    analysis = analyze_failures(result)
    proposals = generate_proposals(analysis)
    applied = apply_best(proposals)
    new_result = run_benchmark()
    
    if keep(new_result, prev):
        commit()
    else:
        discard()
    
    if interrupted:
        break
```

## 实验记录（results.tsv）

| 字段 | 说明 |
|:---|:---|
| commit | git commit hash |
| avg_score | 平均分 (0-1) |
| passed | 通过数 (如 15/50) |
| task_scores | 各 task 分数 JSON |
| cost_usd | 消耗成本 |
| status | keep / discard / crash |
| description | 实验描述 |

## 根因分类

| 类别 | 说明 | 改进方向 |
|:---|:---|:---|
| 误解任务 | 没看懂 task | 改进 prompt |
| 缺少能力或工具 | 没有合适工具 | 添加专用工具 |
| 信息收集不足 | 没获取足够信息 | 增加信息确认 |
| 执行策略不当 | 方法不对 | 改进策略 |
| 缺少验证 | 没检查结果 | 增加验证步骤 |
| 环境/依赖问题 | 依赖有问题 | 修复环境 |
| 静默失败 | 以为成功实际失败 | 增加结果检查 |

## Keep/Discard 规则

- ✅ **KEEP**: passed 提升了
- ✅ **KEEP**: passed 相同 + harness 更简单
- ❌ **DISCARD**: 无提升且更复杂
- ❌ **DISCARD**: 过度拟合（只对特定 task 有效）

## 过度拟合检测

问自己：
> "如果这个 exact task 消失，这改进还有价值吗？"

如果答案是"否" → 过度拟合，丢弃。

**红旗模式**：
- task-specific hardcode
- benchmark-specific hack
- 关键词精确匹配
- 任务名称硬编码判断

## 集成 AutoAgent Loop

本引擎已集成 `skills/autoagent-loop/` 的核心模块：

| 模块 | 用途 |
|:---|:---|
| evaluator | Keep/Discard 判定 |
| analyzer | 根因分析 |
| detector | 过度拟合检测 |
| registry | 实验记录管理 |
| executor | 实验循环执行 |

## 使用场景

### 场景1：每日自我复盘
```bash
# 评估今日表现
node scripts/assess-v2.mjs

# 生成明日改进计划
node scripts/evolve-v2.mjs
```

### 场景2：持续实验
```bash
# 在 skills/autoagent-loop/ 目录
cd skills/autoagent-loop
python3 demo.py  # 演示核心功能

# 或运行完整实验循环
bash scripts/continuous.sh
```

### 场景3：团队协作学习
```bash
node scripts/collaborate.mjs
```

## 与旧版 v1 的区别

| 特性 | v1 | v2 |
|:---|:---|:---|
| 评估方式 | 简单清单 | 根因分析 |
| 改进判定 | 无明确规则 | Keep/Discard 规则 |
| 过度拟合 | 无检测 | 红旗模式检测 |
| 实验记录 | 无 | results.tsv |
| 迭代方式 | 手动 | NEVER STOP |

## 下一步

1. 运行 `assess-v2.mjs` 建立 baseline
2. 运行 `evolve-v2.mjs` 生成改进提案
3. 应用提案并记录到 results.tsv
4. 持续迭代直到目标达成

## 参考

- AutoAgent: https://github.com/kevinrgu/autoagent
- Harbor: https://github.com/laude-institute/harbor
