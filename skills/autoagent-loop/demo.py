#!/usr/bin/env python3
"""
AutoAgent Loop - 演示脚本
展示核心功能：Keep/Discard 判定、根因分析、过度拟合检测
"""

import json
from evaluator import Evaluator, ExperimentResult
from analyzer import FailureAnalyzer, TaskFailure, FailureCategory
from overfit_detector import OverfitDetector, ChangeProposal


def demo_keep_discard():
    """演示 Keep/Discard 判定"""
    print("\n" + "="*60)
    print("Demo 1: Keep/Discard 判定")
    print("="*60)
    
    evaluator = Evaluator()
    
    # 模拟两次实验
    prev = ExperimentResult(
        commit="abc123",
        passed=10,
        total=50,
        avg_score=0.65,
        task_scores={"task1": 1.0, "task2": 0.5},
        cost_usd=0.50,
        status="pending",
        description="baseline",
        complexity=3
    )
    
    # 情况1: passed 提升了
    current = ExperimentResult(
        commit="def456",
        passed=12,  # +2
        total=50,
        avg_score=0.68,
        task_scores={"task1": 1.0, "task2": 0.5, "task3": 1.0, "task4": 0.5},
        cost_usd=0.55,
        status="pending",
        description="improved",
        complexity=3
    )
    
    result = evaluator.judge(current, prev)
    print(f"情况1 - passed 10→12: {result.upper()}")
    
    # 情况2: passed 相同但更简单
    prev2 = ExperimentResult(
        commit="ghi789",
        passed=12,
        total=50,
        avg_score=0.68,
        task_scores={},
        cost_usd=0.55,
        status="pending",
        description="prev",
        complexity=5
    )
    
    current2 = ExperimentResult(
        commit="jkl012",
        passed=12,  # 相同
        total=50,
        avg_score=0.68,
        task_scores={},
        cost_usd=0.55,
        status="pending",
        description="simpler",
        complexity=3  # 更简单
    )
    
    result2 = evaluator.judge(current2, prev2)
    print(f"情况2 - passed 相同12→12, 复杂度5→3: {result2.upper()}")
    
    # 情况3: 无提升且更复杂
    current3 = ExperimentResult(
        commit="mno345",
        passed=12,  # 相同
        total=50,
        avg_score=0.68,
        task_scores={},
        cost_usd=0.55,
        status="pending",
        description="more_complex",
        complexity=7  # 更复杂
    )
    
    result3 = evaluator.judge(current3, prev2)
    print(f"情况3 - passed 相同12→12, 复杂度3→7: {result3.upper()}")


def demo_root_cause_analysis():
    """演示根因分析"""
    print("\n" + "="*60)
    print("Demo 2: 根因分析")
    print("="*60)
    
    analyzer = FailureAnalyzer()
    
    failures = [
        TaskFailure(
            task_name="excel_calc",
            score=0.0,
            trajectory={"steps": [
                {"message": "No tool found for spreadsheet", "source": "agent"}
            ]}
        ),
        TaskFailure(
            task_name="file_parse",
            score=0.2,
            trajectory={"steps": [
                {"message": "didn't understand the task", "source": "agent"}
            ]}
        ),
        TaskFailure(
            task_name="db_query",
            score=0.0,
            trajectory={"steps": [
                {"message": "ERROR: no such table", "source": "agent", 
                 "observation": {"results": [{"content": "sqlite3.OperationalError"}]}}
            ]}
        ),
    ]
    
    analysis = analyzer.analyze(failures)
    
    print("\n根因分组:")
    for category, items in analysis["categorized"].items():
        if items:
            print(f"  - {category}: {[f.task_name for f in items]}")
    
    print("\n改进建议:")
    suggestions = analyzer.generate_suggestions(analysis["categorized"])
    for s in suggestions:
        print(f"  {s}")


def demo_overfit_detection():
    """演示过度拟合检测"""
    print("\n" + "="*60)
    print("Demo 3: 过度拟合检测")
    print("="*60)
    
    detector = OverfitDetector()
    
    # 提案1: 泛化良好的改进
    good_proposal = ChangeProposal(
        description="Add general-purpose file inspection tool",
        changed_files=["agent.py"],
        task_specific=False,
        reasoning="generic tool"
    )
    
    is_overfit1, reason1 = detector.detect(good_proposal, "")
    print(f"提案1 - 通用工具: {'过度拟合 ⚠️' if is_overfit1 else '✅ 正常'}")
    
    # 提案2: 过度拟合
    bad_proposal = ChangeProposal(
        description="Add hardcoded solution for task_abc specifically",
        changed_files=["agent.py", "tasks/task_abc/test.py"],
        task_specific=True,
        reasoning="task-specific hack"
    )
    
    is_overfit2, reason2 = detector.detect(bad_proposal, "")
    print(f"提案2 - Task特异hack: {'过度拟合 ⚠️' if is_overfit2 else '✅ 正常'} ({reason2})")


def main():
    print("="*60)
    print("AutoAgent Loop - 功能演示")
    print("="*60)
    
    demo_keep_discard()
    demo_root_cause_analysis()
    demo_overfit_detection()
    
    print("\n" + "="*60)
    print("演示完成！")
    print("="*60)
    print("\n查看详情:")
    print("  SKILL.md - 整体说明")
    print("  INTEGRATION.md - 与现有系统集成指南")
    print("  program.md - meta-agent 指令")


if __name__ == "__main__":
    main()
