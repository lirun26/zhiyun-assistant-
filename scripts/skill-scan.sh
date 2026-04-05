#!/bin/bash
# 每周扫描ClawHub热门技能，发送到钉钉

LOG_FILE="/tmp/skill-scan.log"
echo "=== 技能扫描 $(date) ===" >> $LOG_FILE

# 扫描热门技能
HOT_SKILLS=$(clawhub search "agent" 2>/dev/null | head -10)
TECH_SKILLS=$(clawhub search "video" 2>/dev/null | head -5)
NEW_SKILLS=$(clawhub search "sora" 2>/dev/null | head -5)

# 对比上次记录
LAST_SCAN=$(cat /tmp/last-skill-scan 2>/dev/null)
CURRENT_SCAN=$(date +%Y%m%d)

if [ "$LAST_SCAN" != "$CURRENT_SCAN" ]; then
    echo "发现新技能，推送通知" >> $LOG_FILE
    
    MESSAGE="🆕 今日热门Skills发现

🤖 Agent类：
$HOT_SKILLS

🎬 视频类：
$TECH_SKILLS

🔮 新技术：
$NEW_SKILLS"

    # 保存到文件供查看
    echo "$MESSAGE" > /tmp/new-skills.txt
    
    echo "$CURRENT_SCAN" > /tmp/last-skill-scan
fi

echo "扫描完成 $(date)" >> $LOG_FILE
