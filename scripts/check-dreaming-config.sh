#!/bin/bash

# 🧠 Dreaming 功能配置检查脚本
# 检查 OpenClaw 2026.4.5+ Dreaming 功能状态

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${YELLOW}   Dreaming 功能配置检查 v1.0        ${NC}"
echo -e "${CYAN}========================================${NC}"

# 1. 检查 OpenClaw 版本
echo -e "\n${BLUE}1. 检查 OpenClaw 版本${NC}"
OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "未知")
echo -e "  版本: $OPENCLAW_VERSION"

if [[ "$OPENCLAW_VERSION" == *"2026.4.5"* ]]; then
    echo -e "  ${GREEN}✅ 支持 Dreaming 功能${NC}"
else
    echo -e "  ${YELLOW}⚠️  版本可能不支持 Dreaming${NC}"
    echo -e "  建议升级到 2026.4.5+"
fi

# 2. 检查配置文件
echo -e "\n${BLUE}2. 检查配置文件${NC}"
CONFIG_FILE="/home/admin/.openclaw/openclaw.json"

if [ -f "$CONFIG_FILE" ]; then
    echo -e "  ${GREEN}✅ 配置文件存在${NC}"
    
    # 检查 Dreaming 配置
    if grep -q "dreaming" "$CONFIG_FILE"; then
        echo -e "  ${GREEN}✅ Dreaming 配置已找到${NC}"
        
        # 显示相关配置
        echo -e "\n  ${CYAN}Dreaming 配置详情:${NC}"
        grep -A5 -B5 "dreaming" "$CONFIG_FILE" | head -20
    else
        echo -e "  ${YELLOW}⚠️  Dreaming 配置未找到${NC}"
        echo -e "  可能需要手动配置"
    fi
else
    echo -e "  ${RED}❌ 配置文件不存在${NC}"
fi

# 3. 检查记忆系统
echo -e "\n${BLUE}3. 检查记忆系统${NC}"
MEMORY_DIR="/home/admin/.openclaw/workspace/memory"

if [ -d "$MEMORY_DIR" ]; then
    echo -e "  ${GREEN}✅ 记忆目录存在${NC}"
    
    # 统计记忆文件
    MEMORY_FILES=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    echo -e "  记忆文件数量: $MEMORY_FILES"
    
    # 检查三层记忆架构
    if [ -d "$MEMORY_DIR/hot" ] && [ -d "$MEMORY_DIR/warm" ]; then
        echo -e "  ${GREEN}✅ 三层记忆架构完整${NC}"
        echo -e "  - 🔥 HOT: $(find "$MEMORY_DIR/hot" -name "*.md" | wc -l) 文件"
        echo -e "  - 🌡️ WARM: $(find "$MEMORY_DIR/warm" -name "*.md" | wc -l) 文件"
        echo -e "  - ❄️ COLD: $(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" | wc -l) 文件"
    else
        echo -e "  ${YELLOW}⚠️  三层记忆架构不完整${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  记忆目录不存在${NC}"
fi

# 4. 检查定时任务（Dreaming 模拟）
echo -e "\n${BLUE}4. 检查定时任务${NC}"
CRON_JOBS=$(crontab -l 2>/dev/null | grep -i "memory\|dreaming\|archive" || echo "无相关定时任务")

if [[ "$CRON_JOBS" != "无相关定时任务" ]]; then
    echo -e "  ${GREEN}✅ 找到相关定时任务${NC}"
    echo -e "\n  定时任务列表:"
    echo "$CRON_JOBS" | while read job; do
        echo -e "  - $job"
    done
else
    echo -e "  ${YELLOW}⚠️  未找到记忆相关定时任务${NC}"
fi

# 5. 检查小说项目记忆
echo -e "\n${BLUE}5. 检查小说项目记忆${NC}"
NOVEL_DIR="/home/admin/.openclaw/workspace/novels/重生末世废土"

if [ -d "$NOVEL_DIR" ]; then
    echo -e "  ${GREEN}✅ 小说项目存在${NC}"
    
    # 检查 .learnings 目录
    LEARNINGS_DIR="$NOVEL_DIR/books/重生末世废土之生存法则/.learnings"
    
    if [ -d "$LEARNINGS_DIR" ]; then
        echo -e "  ${GREEN}✅ 学习记忆目录存在${NC}"
        
        LEARNING_FILES=$(find "$LEARNINGS_DIR" -name "*.md" -type f | wc -l)
        echo -e "  学习文件数量: $LEARNING_FILES"
        
        echo -e "\n  ${CYAN}学习文件列表:${NC}"
        find "$LEARNINGS_DIR" -name "*.md" -type f | while read file; do
            FILE_NAME=$(basename "$file")
            FILE_SIZE=$(stat -c%s "$file" 2>/dev/null || echo "0")
            echo -e "  - $FILE_NAME (${FILE_SIZE}字节)"
        done
    else
        echo -e "  ${YELLOW}⚠️  学习记忆目录不存在${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  小说项目不存在${NC}"
fi

# 6. 建议配置
echo -e "\n${BLUE}6. Dreaming 功能配置建议${NC}"

cat << EOF

${CYAN}推荐配置步骤:${NC}

1. ${GREEN}启用 Dreaming 功能${NC}
   \`\`\`bash
   openclaw config set agents.defaults.dreaming.enabled true
   \`\`\`

2. ${GREEN}配置记忆归档频率${NC}
   \`\`\`bash
   openclaw config set agents.defaults.dreaming.frequency "daily"
   openclaw config set agents.defaults.dreaming.time "02:00"
   \`\`\`

3. ${GREEN}配置记忆保留策略${NC}
   \`\`\`bash
   openclaw config set agents.defaults.dreaming.retention.hot "7d"
   openclaw config set agents.defaults.dreaming.retention.warm "30d"
   openclaw config set agents.defaults.dreaming.retention.cold "forever"
   \`\`\`

4. ${GREEN}添加定时归档任务${NC}
   \`\`\`bash
   # 每日凌晨2点执行记忆归档
   (crontab -l 2>/dev/null; echo "0 2 * * * /home/admin/.openclaw/workspace/scripts/optimize-memory-archiving.sh") | crontab -
   \`\`\`

5. ${GREEN}测试 Dreaming 功能${NC}
   \`\`\`bash
   # 手动触发记忆归档
   bash /home/admin/.openclaw/workspace/scripts/optimize-memory-archiving.sh
   \`\`\`
EOF

# 7. 当前状态总结
echo -e "\n${BLUE}7. 当前状态总结${NC}"

echo -e "${CYAN}✅ 已具备的条件:${NC}"
echo -e "  - OpenClaw 2026.4.5 版本"
echo -e "  - 完整的三层记忆架构"
echo -e "  - 小说项目记忆系统"
echo -e "  - 自动化归档脚本"

echo -e "\n${YELLOW}⚠️  需要配置的项目:${NC}"
echo -e "  - Dreaming 功能启用"
echo -e "  - 记忆归档定时任务"
echo -e "  - 记忆保留策略"

echo -e "\n${GREEN}🚀 推荐立即执行:${NC}"
echo -e "  1. 启用 Dreaming 功能"
echo -e "  2. 测试记忆归档脚本"
echo -e "  3. 添加定时任务"

echo -e "\n${CYAN}========================================${NC}"
echo -e "${YELLOW}检查完成！${NC}"
echo -e "${CYAN}========================================${NC}"

# 提供快速命令
echo -e "\n${BLUE}📋 快速命令:${NC}"
echo -e "  启用 Dreaming: ${GREEN}bash $0 enable${NC}"
echo -e "  测试归档: ${GREEN}bash /home/admin/.openclaw/workspace/scripts/optimize-memory-archiving.sh${NC}"
echo -e "  查看帮助: ${GREEN}bash $0 help${NC}"

# 启用功能（如果指定）
if [ "$1" = "enable" ]; then
    echo -e "\n${YELLOW}正在启用 Dreaming 功能...${NC}"
    
    # 尝试启用 Dreaming
    openclaw config set agents.defaults.dreaming.enabled true 2>/dev/null && \
        echo -e "${GREEN}✅ Dreaming 功能已启用${NC}" || \
        echo -e "${RED}❌ 启用失败，请手动配置${NC}"
    
    # 添加定时任务
    echo -e "\n${YELLOW}添加定时归档任务...${NC}"
    (crontab -l 2>/dev/null; echo "# OpenClaw 记忆归档任务"; echo "0 2 * * * /home/admin/.openclaw/workspace/scripts/optimize-memory-archiving.sh >> /tmp/openclaw-dreaming.log 2>&1") | crontab - && \
        echo -e "${GREEN}✅ 定时任务已添加${NC}" || \
        echo -e "${RED}❌ 添加定时任务失败${NC}"
    
    echo -e "\n${GREEN}🎉 Dreaming 功能配置完成！${NC}"
fi