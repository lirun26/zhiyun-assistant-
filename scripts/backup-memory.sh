#!/bin/bash
# PATH 必须包含 openclaw
export PATH="/home/admin/.npm-global/bin:/usr/bin:/bin:/home/admin/.local/bin"

# 记忆文件备份脚本 - 自动推送到GitHub私有仓库
# 创建日期：2026-03-27

BACKUP_DIR="/tmp/memory-backup-git"
# 使用 GITHUB_TOKEN 环境变量
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️ GITHUB_TOKEN 环境变量未设置，备份跳过"
    exit 0
fi
TARGET_REPO="https://${GITHUB_TOKEN}@github.com/lirun26/zhiyun-memory-backup.git"

echo "🧠 开始记忆备份 $(date)"

# 清理旧备份
rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cd "$BACKUP_DIR"

# 初始化
git init -b main
git config user.email "backup@zhiyun.ai"
git config user.name "Zhiyun Backup"

# 复制记忆文件
cp -r /home/admin/.openclaw/workspace/memory ./memory
cp /home/admin/.openclaw/workspace/AGENTS.md ./AGENTS.md
cp /home/admin/.openclaw/workspace/HEARTBEAT.md ./HEARTBEAT.md

# 添加并提交
git add memory AGENTS.md HEARTBEAT.md
git commit -m "🧠 记忆备份 $(date +%Y-%m-%d\ %H:%M)"

# 推送
git remote add origin "$TARGET_REPO"
git push -u origin main --force 2>&1 | tail -5

echo "✅ 备份完成"
