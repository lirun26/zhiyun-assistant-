"""
AutoAgent Loop - 过度拟合检测器
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ChangeProposal:
    """改进提案"""
    description: str
    changed_files: list[str]
    task_specific: bool  # 是否只针对特定 task
    reasoning: str


class OverfitDetector:
    """
    过度拟合检测器
    
    核心问题："如果这个 exact task 消失，这改进还有价值吗？"
    
    如果答案是"否" → 过度拟合，丢弃。
    """
    
    # 过度拟合红旗模式
    OVERFIT_PATTERNS = [
        # task-specific 硬编码
        (r"task.*specific.*hardcode", "任务特定硬编码"),
        (r"only.*work.*for.*\w+", "只对特定任务有效"),
        (r"keyword.*\w+.*exact.*match", "关键词精确匹配"),
        (r"regex.*\w+.*pattern", "正则硬编码特定模式"),
        
        # benchmark-specific hack
        (r"benchmark.*specific", "Benchmark 特异性改动"),
        (r"test.*\d+.*specific", "测试编号特定逻辑"),
        (r"score.*\d+.*improve", "针对特定分数优化"),
        
        # 不可泛化的特殊处理
        (r"if.*task.*==.*[\"']", "任务名称硬编码判断"),
        (r"for.*\w+.*in.*tasks.*:.*if.*==", "遍历任务并逐一判断"),
    ]
    
    # 泛化良好的模式
    GOOD_PATTERNS = [
        "add.*tool.*general.*purpose",
        "improve.*prompt.*instruction",
        "enhance.*error.*handling",
        "add.*verification.*step",
        "refactor.*simplif",
        "remove.*redundant",
    ]
    
    def detect(self, proposal: ChangeProposal, current_harness: str) -> tuple[bool, str]:
        """
        检测提案是否过度拟合
        
        Args:
            proposal: 改进提案
            current_harness: 当前 harness 代码
        
        Returns:
            (is_overfit, reason)
        """
        # 1. 检查红旗模式
        for pattern, description in self.OVERFIT_PATTERNS:
            if re.search(pattern, proposal.description, re.IGNORECASE):
                return True, f"红旗模式: {description}"
        
        # 2. 检查是否是 task-specific hack
        if self._is_task_specific_hack(proposal, current_harness):
            return True, "看起来是针对特定 task 的 hack"
        
        # 3. 检查改动是否可泛化
        if self._is_generic_improvement(proposal):
            return False, "泛化良好的改进"
        
        # 4. 检查是否有过度特化的文件修改
        if self._has_specific_file_changes(proposal):
            return True, "改动了任务特定的文件"
        
        return False, "未检测到过度拟合"
    
    def _is_task_specific_hack(self, proposal: ChangeProposal, harness: str) -> bool:
        """检测是否是 task-specific hack"""
        # 如果改动了 tasks/ 目录下的文件 → 可疑
        for f in proposal.changed_files:
            if "tasks/" in f or "/tasks/" in f:
                return True
        
        # 如果改动了特定 task 相关的代码
        task_patterns = [
            r"if.*task.*==",
            r"task.*name.*in.*\[",
            r"for.*task.*in.*tasks",
        ]
        
        for pattern in task_patterns:
            if re.search(pattern, harness, re.IGNORECASE):
                return True
        
        return False
    
    def _is_generic_improvement(self, proposal: ChangeProposal) -> bool:
        """检查是否是泛化良好的改进"""
        for pattern in self.GOOD_PATTERNS:
            if re.search(pattern, proposal.description, re.IGNORECASE):
                return True
        return False
    
    def _has_specific_file_changes(self, proposal: ChangeProposal) -> bool:
        """检查是否改动了任务特定的文件"""
        suspicious_dirs = ["tasks/", "/tasks/", "benchmark/", "/benchmark/"]
        for f in proposal.changed_files:
            for d in suspicious_dirs:
                if d in f:
                    return True
        return False
    
    def validate_proposal(self, proposal: ChangeProposal) -> tuple[bool, list[str]]:
        """
        验证提案是否应该被接受
        
        Returns:
            (accepted, reasons)
        """
        reasons = []
        accepted = True
        
        # 运行过度拟合检测
        is_overfit, reason = self.detect(proposal, "")
        if is_overfit:
            accepted = False
            reasons.append(f"过度拟合: {reason}")
        
        # 检查改动是否涉及核心 harness
        if "agent.py" not in proposal.changed_files and "harness" not in " ".join(proposal.changed_files).lower():
            # 不涉及核心 harness → 可能是外围改动
            reasons.append("注意: 改动似乎不涉及核心 harness")
        
        # 检查是否有描述
        if not proposal.description:
            accepted = False
            reasons.append("缺少改动描述")
        
        return accepted, reasons
