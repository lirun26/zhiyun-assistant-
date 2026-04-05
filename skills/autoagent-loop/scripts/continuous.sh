#!/bin/bash
# AutoAgent Loop - 持续迭代脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "========================================"
echo "AutoAgent Loop - Continuous Mode"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# 可选：设置最大迭代次数
MAX_ITERATIONS="${1:-0}"  # 默认 0 = 无限

# 运行持续实验
python3 -c "
import asyncio
from executor import ExperimentLoop, LoopConfig

async def main():
    config = LoopConfig(
        max_iterations=$MAX_ITERATIONS,
        on_iteration=lambda i: print(f'\n[Iteration {i} completed]\n')
    )
    loop = ExperimentLoop(config)
    await loop.run_continuous()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\n\nStopped.')
"

echo ""
echo "[*] Experiment session ended."
