#!/bin/bash
# 钉钉插件修复脚本
# 用于OpenClaw版本升级后自动修复钉钉插件
# 使用方法: bash scripts/fix-dingtalk.sh

set -e

DINGTALK_DIR="/home/admin/.openclaw/extensions/dingtalk"
CHANNEL_FILE="$DINGTALK_DIR/src/channel.ts"

echo "🔧 开始修复钉钉插件..."

# 检查channel.ts是否存在
if [ ! -f "$CHANNEL_FILE" ]; then
    echo "❌ 错误: $CHANNEL_FILE 不存在"
    exit 1
fi

# 检查是否已经修复过（通过检查是否包含shim注释）
if grep -q "jsonResult shim - removed in OpenClaw" "$CHANNEL_FILE"; then
    echo "✅ 钉钉插件已经修复，跳过"
    exit 0
fi

# 检查是否包含旧的import语句
if grep -q 'import { jsonResult } from "openclaw/plugin-sdk/telegram-core";' "$CHANNEL_FILE"; then
    echo "📝 替换jsonResult import为兼容shim..."
    
    # 使用sed替换
    sed -i 's|import { jsonResult } from "openclaw/plugin-sdk/telegram-core";|// jsonResult shim - removed in OpenClaw 2026.4.5\nfunction jsonResult(payload) { return { success: true, data: payload }; }|g' "$CHANNEL_FILE"
    
    echo "✅ 修复完成!"
    echo "📌 请重启Gateway使更改生效: openclaw gateway restart"
else
    echo "⚠️ 未找到需要修复的import语句"
fi
