#!/bin/bash
# 快速进化命令 - 随时手动触发
# 用法: bash skills/self-review/scripts/quick_evolve.sh [action]
# action: assess | evolve | status | log-error | log-learning

ACTION=${1:-"status"}
WORKSPACE="$HOME/.openclaw/workspace"
LEARNINGS="$WORKSPACE/.learnings"

case $ACTION in
  assess)
    echo "🧬 运行 AI Evolution Engine 评估..."
    cd "$WORKSPACE/skills/ai-evolution-engine-v2" && node scripts/assess.mjs
    ;;
  evolve)
    echo "🚀 运行 AI Evolution Engine 进化..."
    cd "$WORKSPACE/skills/ai-evolution-engine-v2" && node scripts/evolve.mjs
    ;;
  status)
    echo "📊 进化状态检查..."
    echo ""
    echo "=== AI Evolution Engine ==="
    cd "$WORKSPACE/skills/ai-evolution-engine-v2" && node scripts/assess.mjs 2>/dev/null | head -15
    echo ""
    echo "=== Learnings 记录 ==="
    python3 "$WORKSPACE/skills/actual-self-improvement/scripts/learnings.py" status --root "$WORKSPACE" --format text 2>/dev/null
    echo ""
    echo "=== 进化日志 ==="
    ls -t "$WORKSPACE/memory/evolution/" 2>/dev/null | head -3
    ;;
  log-error)
    ERROR=${2:-"新错误"}
    CONTEXT=${3:-""}
    echo "❌ 记录错误: $ERROR"
    python3 "$WORKSPACE/skills/actual-self-improvement/scripts/learnings.py" log-error --root "$WORKSPACE" --error "$ERROR" --context "$CONTEXT" 2>/dev/null
    ;;
  log-learning)
    LESSON=${2:-"新学到的东西"}
    echo "📝 记录学习: $LESSON"
    python3 "$WORKSPACE/skills/actual-self-improvement/scripts/learnings.py" log-learning --root "$WORKSPACE" --lesson "$LESSON" 2>/dev/null
    ;;
  full)
    echo "🔄 执行完整进化流程..."
    echo ""
    echo "1️⃣ 评估阶段"
    cd "$WORKSPACE/skills/ai-evolution-engine-v2" && node scripts/assess.mjs
    echo ""
    echo "2️⃣ 进化阶段"
    cd "$WORKSPACE/skills/ai-evolution-engine-v2" && node scripts/evolve.mjs
    echo ""
    echo "3️⃣ 记录阶段"
    python3 "$WORKSPACE/skills/self-review/scripts/daily_review.py" 2>/dev/null | tail -10
    echo ""
    echo "✅ 完整进化流程完成"
    ;;
  *)
    echo "用法: $0 [action]"
    echo "action: assess | evolve | status | log-error | log-learning | full"
    ;;
esac
