"""
AutoAgent Loop - 实验循环执行器
"""

import asyncio
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

from evaluator import Evaluator, ExperimentResult, ExperimentRecord
from analyzer import FailureAnalyzer, TaskFailure
from overfit_detector import OverfitDetector, ChangeProposal


@dataclass
class LoopConfig:
    """实验循环配置"""
    harness_path: str = "agent.py"  # harness 文件路径
    tasks_path: str = "tasks/"  # benchmark tasks 目录
    results_file: str = "results.tsv"  # 实验记录文件
    max_iterations: int = 100  # 最大迭代次数（0=无限）
    docker_image: str = "autoagent-base"  # Docker 镜像
    concurrency: int = 4  # 并发数
    always_keep_baseline: bool = True  # 是否始终保留 baseline
    
    # 可选回调
    on_iteration: Optional[Callable] = None  # 每次迭代后的回调
    on_discard: Optional[Callable] = None  # 被 discard 时的回调
    on_keep: Optional[Callable] = None  # 被 keep 时的回调


class ExperimentLoop:
    """
    自动实验循环执行器
    
    流程：
    1. 读取 harness 状态
    2. 运行 benchmark
    3. 分析结果
    4. 生成改进提案
    5. 应用改动
    6. 重新评估
    7. Keep/Discard 判定
    8. 记录并重复
    """
    
    def __init__(self, config: Optional[LoopConfig] = None):
        self.config = config or LoopConfig()
        self.evaluator = Evaluator()
        self.analyzer = FailureAnalyzer()
        self.detector = OverfitDetector()
        self.registry = ExperimentRegistry(self.config.results_file)
        
        self.current_iteration = 0
        self.prev_result: Optional[ExperimentResult] = None
        self.baseline_result: Optional[ExperimentResult] = None
        
        # 统计
        self.stats = {
            "keep": 0,
            "discard": 0,
            "total_cost": 0.0
        }
    
    async def run_once(self) -> ExperimentResult:
        """运行一次实验"""
        self.current_iteration += 1
        print(f"\n{'='*60}")
        print(f"Iteration #{self.current_iteration}")
        print(f"{'='*60}")
        
        # 1. 记录当前 git 状态
        commit = self.registry.get_current_commit()
        branch = self.registry.get_current_branch()
        print(f"Branch: {branch}")
        print(f"Commit: {commit}")
        
        # 2. 运行 benchmark
        print("\n[1/6] Running benchmark...")
        result = await self._run_benchmark()
        
        # 3. 分析失败
        print("\n[2/6] Analyzing failures...")
        analysis = self._analyze_failures(result)
        
        # 4. 生成改进提案
        print("\n[3/6] Generating improvement proposals...")
        proposals = self._generate_proposals(analysis)
        
        # 5. 应用最好的提案
        print("\n[4/6] Applying best proposal...")
        applied = await self._apply_best_proposal(proposals)
        
        # 6. 重新运行 benchmark
        print("\n[5/6] Re-running benchmark...")
        new_result = await self._run_benchmark()
        
        # 7. Keep/Discard 判定
        print("\n[6/6] Judge Keep/Discard...")
        status = self.evaluator.judge(new_result, self.prev_result)
        
        # 记录结果
        record = ExperimentRecord(
            commit=self.registry.get_current_commit(),
            avg_score=new_result.avg_score,
            passed=f"{new_result.passed}/{new_result.total}",
            task_scores=json.dumps(new_result.task_scores),
            cost_usd=new_result.cost_usd,
            status=status,
            description=f"iter_{self.current_iteration}: {new_result.passed - (self.prev_result.passed if self.prev_result else 0):+d} passed",
            branch=self.registry.get_current_branch()
        )
        self.registry.add(record)
        
        # 更新统计
        self.stats[status] += 1
        if new_result.cost_usd:
            self.stats["total_cost"] += new_result.cost_usd
        
        # 回调
        if status == "keep" and self.config.on_keep:
            await self.config.on_keep(new_result)
        elif status == "discard" and self.config.on_discard:
            await self.config.on_discard(new_result)
        
        print(f"\nResult: {status.upper()}")
        print(f"Stats: keep={self.stats['keep']}, discard={self.stats['discard']}, cost=${self.stats['total_cost']:.4f}")
        
        self.prev_result = new_result
        
        # 保存 baseline
        if self.baseline_result is None:
            self.baseline_result = new_result
        
        return new_result
    
    async def run_continuous(self):
        """持续运行直到被停止"""
        print("Starting continuous experiment loop...")
        print("Press Ctrl+C to stop\n")
        
        while True:
            try:
                await self.run_once()
                
                # 检查最大迭代
                if self.config.max_iterations > 0:
                    if self.current_iteration >= self.config.max_iterations:
                        print(f"\nMax iterations ({self.config.max_iterations}) reached. Stopping.")
                        break
                
                # 回调
                if self.config.on_iteration:
                    await self.config.on_iteration(self.current_iteration)
                
                # 短暂休息
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\nStopped by user.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                # 继续运行，不中断
                await asyncio.sleep(5)
        
        self._print_summary()
    
    async def _run_benchmark(self) -> ExperimentResult:
        """运行 benchmark 并解析结果"""
        # TODO: 实现实际的 benchmark 运行逻辑
        # 目前是模拟实现
        
        # 实际实现应该调用：
        # subprocess.run([
        #     "docker", "run", "--rm", "-v", ".:/app", "autoagent-base",
        #     "bash", "-c", "cd /app && uv run harbor run ..."
        # ])
        
        # 模拟返回
        return ExperimentResult(
            commit=self.registry.get_current_commit(),
            passed=10,
            total=50,
            avg_score=0.65,
            task_scores={"task1": 1.0, "task2": 0.5},
            cost_usd=0.50,
            status="pending",
            description="mock",
            complexity=3
        )
    
    def _analyze_failures(self, result: ExperimentResult) -> dict:
        """分析失败"""
        failures = []
        for task, score in result.task_scores.items():
            if score < 0.5:  # 失败阈值
                failure = TaskFailure(
                    task_name=task,
                    score=score,
                    trajectory={}  # TODO: 从 trajectory.json 读取
                )
                failures.append(failure)
        
        return self.analyzer.analyze(failures)
    
    def _generate_proposals(self, analysis: dict) -> list[ChangeProposal]:
        """生成改进提案"""
        proposals = []
        
        # 根据根因分析生成提案
        suggestions = self.analyzer.generate_suggestions(analysis["categorized"])
        
        for suggestion in suggestions:
            proposals.append(ChangeProposal(
                description=suggestion,
                changed_files=["agent.py"],
                task_specific=False,
                reasoning="auto_generated"
            ))
        
        return proposals
    
    async def _apply_best_proposal(self, proposals: list[ChangeProposal]) -> bool:
        """应用最好的提案"""
        if not proposals:
            print("No proposals to apply.")
            return False
        
        # 过滤过度拟合
        valid_proposals = []
        for p in proposals:
            is_overfit, _ = self.detector.detect(p, "")
            if not is_overfit:
                valid_proposals.append(p)
        
        if not valid_proposals:
            print("All proposals are overfit. Skipping.")
            return False
        
        # TODO: 实现实际的代码修改逻辑
        print(f"Would apply: {valid_proposals[0].description}")
        return True
    
    def _print_summary(self):
        """打印总结"""
        print(f"\n{'='*60}")
        print("EXPERIMENT SUMMARY")
        print(f"{'='*60}")
        print(f"Total iterations: {self.current_iteration}")
        print(f"Keep: {self.stats['keep']}")
        print(f"Discard: {self.stats['discard']}")
        print(f"Total cost: ${self.stats['total_cost']:.4f}")
        
        if self.baseline_result and self.prev_result:
            improvement = self.prev_result.passed - self.baseline_result.passed
            print(f"Improvement: {improvement:+d} passed (baseline → latest)")
