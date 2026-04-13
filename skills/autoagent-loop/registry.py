"""
AutoAgent Loop - 实验记录注册表（results.tsv）
"""

import csv
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class ExperimentRecord:
    """实验记录"""
    commit: str
    avg_score: float
    passed: str  # "20/58" 格式
    task_scores: str  # JSON 字符串
    cost_usd: Optional[float]
    status: str  # "keep", "discard", "crash"
    description: str
    
    # 元数据
    timestamp: str = ""
    branch: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_tsv_row(self) -> list:
        return [
            self.commit,
            f"{self.avg_score:.4f}",
            self.passed,
            self.task_scores,
            f"{self.cost_usd:.4f}" if self.cost_usd else "",
            self.status,
            self.description,
            self.timestamp,
            self.branch
        ]
    
    @staticmethod
    def tsv_headers() -> list:
        return ["commit", "avg_score", "passed", "task_scores", "cost_usd", 
                "status", "description", "timestamp", "branch"]


class ExperimentRegistry:
    """
    实验记录注册表
    
    管理 results.tsv 文件，记录每次实验
    """
    
    def __init__(self, results_file: str = "results.tsv"):
        self.results_file = Path(results_file)
        self._ensure_file()
    
    def _ensure_file(self):
        """确保 results.tsv 存在"""
        if not self.results_file.exists():
            self.results_file.write_text("\t".join(ExperimentRecord.tsv_headers()) + "\n")
    
    def add(self, record: ExperimentRecord):
        """添加实验记录"""
        with open(self.results_file, "a", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(record.to_tsv_row())
    
    def get_latest(self) -> Optional[ExperimentRecord]:
        """获取最新实验记录"""
        if not self.results_file.exists():
            return None
        
        with open(self.results_file, "r") as f:
            lines = f.readlines()
        
        if len(lines) <= 1:
            return None
        
        # 最后一行是最新记录
        latest = lines[-1].strip().split("\t")
        if len(latest) >= 7:
            return ExperimentRecord(
                commit=latest[0],
                avg_score=float(latest[1]),
                passed=latest[2],
                task_scores=latest[3],
                cost_usd=float(latest[4]) if latest[4] else None,
                status=latest[5],
                description=latest[6],
                timestamp=latest[7] if len(latest) > 7 else "",
                branch=latest[8] if len(latest) > 8 else ""
            )
        return None
    
    def get_history(self, limit: int = 10) -> list[ExperimentRecord]:
        """获取历史实验记录"""
        if not self.results_file.exists():
            return []
        
        with open(self.results_file, "r") as f:
            lines = f.readlines()
        
        records = []
        for line in lines[1:]:  # 跳过 header
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                try:
                    records.append(ExperimentRecord(
                        commit=parts[0],
                        avg_score=float(parts[1]),
                        passed=parts[2],
                        task_scores=parts[3],
                        cost_usd=float(parts[4]) if parts[4] else None,
                        status=parts[5],
                        description=parts[6],
                        timestamp=parts[7] if len(parts) > 7 else "",
                        branch=parts[8] if len(parts) > 8 else ""
                    ))
                except (ValueError, IndexError):
                    continue
        
        return records[-limit:]
    
    def get_current_commit(self) -> str:
        """获取当前 git commit hash"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, cwd=self.results_file.parent
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"
    
    def get_current_branch(self) -> str:
        """获取当前分支"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, cwd=self.results_file.parent
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"
