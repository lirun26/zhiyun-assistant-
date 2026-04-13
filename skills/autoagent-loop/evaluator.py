"""
AutoAgent Loop - 实验评分与 Keep/Discard 判定器
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExperimentResult:
    """单次实验结果"""
    commit: str
    passed: int
    total: int
    avg_score: float
    task_scores: dict[str, float]
    cost_usd: Optional[float]
    status: str  # "keep", "discard", "crash"
    description: str
    complexity: int  # 工具数 + 组件数


class Evaluator:
    """
    评分器：执行 Keep/Discard 判定
    
    规则：
    - passed 提升了 → Keep
    - passed 相同 + harness 更简单 → Keep
    - 否则 → Discard
    """
    
    def __init__(self, baseline: Optional[ExperimentResult] = None):
        self.baseline = baseline  # 初始基准线
    
    def judge(self, result: ExperimentResult, prev_result: Optional[ExperimentResult] = None) -> str:
        """
        判定 Keep 或 Discard
        
        Args:
            result: 当前实验结果
            prev_result: 上一次实验结果（用于对比）
        
        Returns:
            "keep" 或 "discard"
        """
        # 如果是第一次实验，保留
        if prev_result is None:
            return "keep"
        
        # 计算 passed 变化
        current_passed = result.passed
        prev_passed = prev_result.passed
        
        # 1. passed 提升了 → Keep
        if current_passed > prev_passed:
            return "keep"
        
        # 2. passed 相同，检查复杂度
        if current_passed == prev_passed:
            # 更简单 → Keep
            if result.complexity < prev_result.complexity:
                return "keep"
        
        # 3. 否则 → Discard
        return "discard"
    
    def analyze_regression(self, result: ExperimentResult, prev_result: ExperimentResult) -> dict:
        """分析回归：新失败 / 新成功"""
        current_tasks = set(result.task_scores.keys())
        prev_tasks = set(prev_result.task_scores.keys())
        
        # 新解决的 task
        newly_passed = [
            task for task in current_tasks
            if result.task_scores[task] > 0 and prev_result.task_scores.get(task, 0) == 0
        ]
        
        # 回归的 task
        regressed = [
            task for task in current_tasks
            if result.task_scores[task] == 0 and prev_result.task_scores.get(task, 0) > 0
        ]
        
        return {
            "newly_passed": newly_passed,
            "regressed": regressed,
            "improvement": result.passed - prev_result.passed
        }
    
    def format_result(self, result: ExperimentResult) -> str:
        """格式化实验结果"""
        return (
            f"commit={result.commit} "
            f"passed={result.passed}/{result.total} "
            f"avg_score={result.avg_score:.3f} "
            f"cost=${result.cost_usd or 0:.4f} "
            f"status={result.status} "
            f"complexity={result.complexity} "
            f"desc={result.description}"
        )
