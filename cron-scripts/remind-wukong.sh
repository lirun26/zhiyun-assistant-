#!/bin/bash
# 提醒老大领取悟空邀请码
STATE_FILE="/tmp/wukong-reminder-acknowledged"

if [ -f "$STATE_FILE" ]; then
  exit 0
fi

echo "📢 老大，8:50到了！记得领取悟空邀请码！"
echo ""
echo "领取地址：https://www.dingtalk.com/wukong"
echo ""
echo "多次提醒：如果你已领取，请告诉我"已领取"，我就不再提醒了。"
