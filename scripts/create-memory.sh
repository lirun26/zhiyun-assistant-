#!/bin/bash

# 每天23点自动创建记忆文件
# 智云助手自动任务

DATE=$(date +%Y-%m-%d)
MEMORY_DIR="/home/admin/.openclaw/workspace/memory"
FILE="$MEMORY_DIR/$DATE.md"

# 检查文件是否已存在
if [ ! -f "$FILE" ]; then
    cat > "$FILE" << EOF
# $(date +%Y-%m-%d) 工作日志

## 📅 日期
$DATE ($(date +%A))

---

## ✅ 今日完成

- [ ] 

---

## 📌 待办

- [ ] 

---

## 🧠 重要记忆

- 

---

_持续更新中_
EOF
    echo "[$(date)] 创建记忆文件: $FILE"
else
    echo "[$(date)] 记忆文件已存在: $FILE"
fi
