"""
AutoAgent Loop - 根因分析器
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class FailureCategory(Enum):
    """失败根因分类"""
    TASK_MISUNDERSTANDING = "误解任务"
    MISSING_CAPABILITY = "缺少能力或工具"
    WEAK_INFO_GATHERING = "信息收集不足"
    BAD_EXECUTION_STRATEGY = "执行策略不当"
    MISSING_VERIFICATION = "缺少验证"
    ENVIRONMENT_ISSUE = "环境/依赖问题"
    SILENT_FAILURE = "静默失败"  # 以为成功但结果错误


@dataclass
class TaskFailure:
    """单个 task 失败信息"""
    task_name: str
    score: float
    trajectory: dict  # ATIF trajectory
    root_cause: Optional[FailureCategory] = None
    suggestion: Optional[str] = None


class FailureAnalyzer:
    """
    根因分析器：分析 benchmark 失败，按根因分组
    """
    
    # 根因关键词映射
    ROOT_CAUSE_KEYWORDS = {
        FailureCategory.TASK_MISUNDERSTANDING: [
            "misunderstand", "unclear", "confused", "wrong interpretation",
            "didn't understand", "not what was asked"
        ],
        FailureCategory.MISSING_CAPABILITY: [
            "no tool", "missing", "cannot", "unable to", "not implemented",
            "function not found", "missing capability"
        ],
        FailureCategory.WEAK_INFO_GATHERING: [
            "not enough info", "missing information", "didn't check",
            "didn't read", "incomplete data"
        ],
        FailureCategory.BAD_EXECUTION_STRATEGY: [
            "wrong approach", "bad strategy", "inefficient", "should try",
            "incorrect method", "failed attempt"
        ],
        FailureCategory.MISSING_VERIFICATION: [
            "didn't verify", "no check", "assumed correct", "silent fail",
            "output wrong", "result incorrect"
        ],
        FailureCategory.ENVIRONMENT_ISSUE: [
            "error", "exception", "crash", "timeout", "dependency",
            "import error", "not found"
        ],
        FailureCategory.SILENT_FAILURE: [
            "thought it succeeded", "but was wrong", "incorrect output",
            "seemed right", "but failed"
        ]
    }
    
    def analyze(self, failures: list[TaskFailure]) -> dict:
        """
        分析失败列表，按根因分组
        
        Returns:
            {
                "category_name": [task1, task2, ...],
                ...
            }
        """
        categorized = {cat.value: [] for cat in FailureCategory}
        uncategorized = []
        
        for failure in failures:
            category = self._detect_root_cause(failure)
            if category:
                categorized[category.value].append(failure)
            else:
                uncategorized.append(failure)
        
        return {
            "categorized": categorized,
            "uncategorized": uncategorized,
            "summary": self._summarize(categorized)
        }
    
    def _detect_root_cause(self, failure: TaskFailure) -> Optional[FailureCategory]:
        """根据 trajectory 中的关键词检测根因"""
        # 构建要搜索的文本
        search_text = self._extract_search_text(failure.trajectory)
        
        for category, keywords in self.ROOT_CAUSE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in search_text.lower():
                    return category
        
        return None
    
    def _extract_search_text(self, trajectory: dict) -> str:
        """从 trajectory 中提取可搜索的文本"""
        texts = []
        
        for step in trajectory.get("steps", []):
            if "message" in step:
                texts.append(step["message"])
            if "observation" in step:
                obs = step["observation"]
                if isinstance(obs, dict) and "results" in obs:
                    for r in obs["results"]:
                        if isinstance(r, dict) and "content" in r:
                            texts.append(str(r["content"]))
        
        return " ".join(texts)
    
    def _summarize(self, categorized: dict) -> str:
        """生成汇总报告"""
        lines = ["## 根因分析汇总\n"]
        
        for category, failures in categorized.items():
            if failures:
                lines.append(f"- **{category}**: {len(failures)} 个 task")
        
        return "\n".join(lines)
    
    def generate_suggestions(self, categorized: dict) -> list[str]:
        """
        根据根因分组生成改进建议
        
        Returns:
            ["建议1", "建议2", ...]
        """
        suggestions = []
        
        # 误解任务 → 改进 SYSTEM_PROMPT
        if categorized.get(FailureCategory.TASK_MISUNDERSTANDING.value):
            suggestions.append(
                "【高优先级】多个 task 被误解，建议改进 SYSTEM_PROMPT，增加任务澄清步骤"
            )
        
        # 缺少能力 → 添加/改进工具
        missing = categorized.get(FailureCategory.MISSING_CAPABILITY.value, [])
        if missing:
            suggestions.append(
                f"【高优先级】{len(missing)} 个 task 缺少能力，建议添加专用工具"
            )
        
        # 信息收集不足 → 增加信息获取步骤
        if categorized.get(FailureCategory.WEAK_INFO_GATHERING.value):
            suggestions.append(
                "【中优先级】信息收集不足，建议在 prompt 中增加信息确认环节"
            )
        
        # 执行策略不当 → 增加示例/few-shot
        if categorized.get(FailureCategory.BAD_EXECUTION_STRATEGY.value):
            suggestions.append(
                "【中优先级】执行策略问题，建议增加 few-shot examples 或策略提示"
            )
        
        # 缺少验证 → 增加自检步骤
        if categorized.get(FailureCategory.MISSING_VERIFICATION.value):
            suggestions.append(
                "【高优先级】缺少验证环节，建议增加 output 检查步骤"
            )
        
        # 环境问题 → 修复依赖
        if categorized.get(FailureCategory.ENVIRONMENT_ISSUE.value):
            suggestions.append(
                "【高优先级】环境问题，建议检查依赖安装"
            )
        
        # 静默失败 → 增加验证 + 输出检查
        if categorized.get(FailureCategory.SILENT_FAILURE.value):
            suggestions.append(
                "【高优先级】静默失败，建议增加结果验证机制"
            )
        
        return suggestions
