#!/bin/bash

# OpenClaw 健康检查脚本
# 如果检查失败，发送钉钉通知并尝试重启

LOG_FILE="/home/admin/.openclaw/workspace/logs/health-check.log"
DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=88fcb0e04bdca4f0bc6603d7bdd8351163151fe4638d783641748a2a245e19bc"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 记录时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 执行健康检查..." >> "$LOG_FILE"

# 执行健康检查
RESULT=$(openclaw health --json 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 健康检查命令失败，尝试重启..." >> "$LOG_FILE"
    
    # 尝试重启 Gateway
    openclaw gateway restart >> "$LOG_FILE" 2>&1
    
    # 发送钉钉通知
    if [ -n "$DINGTALK_WEBHOOK" ] && [ "$DINGTALK_WEBHOOK" != "https://oapi.dingtalk.com/robot/send?access_token=填写你的token" ]; then
        curl -s -X POST "$DINGTALK_WEBHOOK" \
            -H 'Content-Type: application/json' \
            -d '{"msgtype": "text", "text": {"content": "⚠️ OpenClaw 健康检查失败，已尝试重启！"}}' >> "$LOG_FILE" 2>&1
    fi
    exit 1
fi

# 检查 JSON 中的 ok 字段
OK=$(echo "$RESULT" | grep -o '"ok": true' | head -1)
if [ -z "$OK" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 健康检查返回异常，尝试重启..." >> "$LOG_FILE"
    
    # 尝试重启 Gateway
    openclaw gateway restart >> "$LOG_FILE" 2>&1
    
    # 发送钉钉通知
    if [ -n "$DINGTALK_WEBHOOK" ] && [ "$DINGTALK_WEBHOOK" != "https://oapi.dingtalk.com/robot/send?access_token=填写你的token" ]; then
        curl -s -X POST "$DINGTALK_WEBHOOK" \
            -H 'Content-Type: application/json' \
            -d '{"msgtype": "text", "text": {"content": "⚠️ OpenClaw 健康检查返回异常，已尝试重启！"}}' >> "$LOG_FILE" 2>&1
    fi
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 健康检查通过" >> "$LOG_FILE"
exit 0