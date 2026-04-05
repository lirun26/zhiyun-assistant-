#!/bin/bash
# 记忆层级维护脚本
# 将过期的HOT内容归档到COLD，清理旧的日记录

HOT_FILE="/home/admin/.openclaw/workspace/memory/hot/HOT_MEMORY.md"
WARM_FILE="/home/admin/.openclaw/workspace/memory/warm/WARM_MEMORY.md"
MEMORY_FILE="/home/admin/.openclaw/workspace/MEMORY.md"
LOG_FILE="/home/admin/.openclaw/workspace/memory/$(date +%Y-%m-%d).md"

echo "=== 记忆层级维护 $(date) ==="

# 检查HOT记忆最后更新时间
if [ -f "$HOT_FILE" ]; then
    LAST_UPDATE=$(grep -m1 "最后活跃时间" "$HOT_FILE" | cut -d: -f2 | tr -d ' ')
    echo "HOT最后更新: $LAST_UPDATE"
fi

# 清理3天前的日记录（保留有用信息后合并到MEMORY.md）
DAYS_TO_KEEP=3
find /home/admin/.openclaw/workspace/memory -name "2026-*.md" -mtime +$DAYS_TO_KEEP 2>/dev/null | while read f; do
    echo "旧日记: $f"
done

echo "✅ 记忆层级检查完成"
