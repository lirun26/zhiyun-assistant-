#!/bin/bash
# AutoAgent Loop - 单次实验脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "========================================"
echo "AutoAgent Loop - Single Run"
echo "========================================"
echo ""

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# 检查 Docker（如果需要）
if ! command -v docker &> /dev/null; then
    echo "Warning: docker not found. Benchmark may not work."
fi

# 运行单次实验
echo "[*] Running single experiment iteration..."
python3 -c "
import asyncio
from executor import ExperimentLoop, LoopConfig

async def main():
    config = LoopConfig(max_iterations=1)
    loop = ExperimentLoop(config)
    result = await loop.run_once()
    print(f'\nFinal result: passed={result.passed}/{result.total}, score={result.avg_score:.3f}')

asyncio.run(main())
"

echo ""
echo "[*] Done!"
