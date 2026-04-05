#!/bin/bash
# 每日百度热点推送脚本
# 使用OpenClaw的web_fetch获取热搜

LOG_FILE="/tmp/hot-push.log"
echo "=== 开始获取热搜 $(date) ===" >> $LOG_FILE

# 使用OpenClaw的web_fetch获取热搜
CONTENT=$(curl -s "https://top.baidu.com/board?tab=realtime" 2>/dev/null | grep -oP 'title="[^"]*"' | head -20 | sed 's/title="//;s/"//' | head -10)

if [ -z "$CONTENT" ]; then
    # 如果curl失败，使用备用方法
    echo "curl失败，尝试其他方法" >> $LOG_FILE
    CONTENT=$(curl -s -A "Mozilla/5.0" "https://top.baidu.com/board?tab=realtime" 2>/dev/null | grep -oP '(?<=<a class="[^"]*title[^"]*"[^>]*>)[^<]+' | head -10)
fi

if [ -z "$CONTENT" ]; then
    echo "获取热搜失败" >> $LOG_FILE
    exit 1
fi

# 格式化消息
MESSAGE="🔥 百度热搜榜 $(date '+%Y-%m-%d')

"

i=1
echo "$CONTENT" | while IFS= read -r line; do
    if [ -n "$line" ]; then
        MESSAGE="$MESSAGE$i. $line\n"
        ((i++))
    fi
done

# 保存到文件
echo "=== 热搜内容 ===" >> $LOG_FILE
echo "$MESSAGE" >> $LOG_FILE

echo "推送完成: $(date)" >> $LOG_FILE
