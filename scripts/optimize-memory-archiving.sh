#!/bin/bash

# 🧠 记忆归档优化脚本 v1.0
# 功能：自动化记忆整理、归档和优化
# 适用：OpenClaw 2026.4.5+ with Dreaming 功能

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查目录
check_directories() {
    log_info "检查目录结构..."
    
    # 必需目录
    DIRS=(
        "/home/admin/.openclaw/workspace/memory"
        "/home/admin/.openclaw/workspace/memory/hot"
        "/home/admin/.openclaw/workspace/memory/warm"
        "/home/admin/.openclaw/workspace/novels"
    )
    
    for dir in "${DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            log_warning "目录不存在: $dir"
            mkdir -p "$dir"
            log_success "已创建目录: $dir"
        fi
    done
}

# 1. 记忆整理 (Dreaming 功能模拟)
consolidate_memory() {
    log_info "开始记忆整理 (Dreaming 模拟)..."
    
    TODAY=$(date +%Y-%m-%d)
    YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
    
    # 检查今天的记忆文件
    if [ ! -f "/home/admin/.openclaw/workspace/memory/$TODAY.md" ]; then
        log_info "创建今日记忆文件: $TODAY.md"
        echo -e "# $TODAY 记忆记录\n\n---\n" > "/home/admin/.openclaw/workspace/memory/$TODAY.md"
    fi
    
    # 整理 HOT_MEMORY
    if [ -f "/home/admin/.openclaw/workspace/memory/hot/HOT_MEMORY.md" ]; then
        log_info "整理 HOT_MEMORY..."
        
        # 提取重要信息到今日记忆
        IMPORTANT_INFO=$(grep -E "(⚠️|✅|🚨|🎯|🔧)" "/home/admin/.openclaw/workspace/memory/hot/HOT_MEMORY.md" | head -10)
        
        if [ ! -z "$IMPORTANT_INFO" ]; then
            echo -e "## 🔥 今日重要事项\n$IMPORTANT_INFO\n" >> "/home/admin/.openclaw/workspace/memory/$TODAY.md"
            log_success "HOT_MEMORY 重要信息已归档"
        fi
        
        # 更新 HOT_MEMORY 最后活跃时间
        sed -i "s/最后活跃时间:.*/最后活跃时间: $TODAY $(date +%H:%M)/" "/home/admin/.openclaw/workspace/memory/hot/HOT_MEMORY.md"
    fi
    
    # 检查昨天的记忆文件，提取重要信息到 MEMORY.md
    if [ -f "/home/admin/.openclaw/workspace/memory/$YESTERDAY.md" ]; then
        log_info "整理昨日记忆 ($YESTERDAY.md)..."
        
        # 提取重要学习点
        LEARNINGS=$(grep -E "(教训|经验|学习到|发现)" "/home/admin/.openclaw/workspace/memory/$YESTERDAY.md" | head -5)
        
        if [ ! -z "$LEARNINGS" ]; then
            echo -e "## 📝 $YESTERDAY 学习总结\n$LEARNINGS\n" >> "/home/admin/.openclaw/workspace/memory/$TODAY.md"
            log_success "昨日学习点已提取"
        fi
    fi
}

# 2. 小说项目记忆归档
archive_novel_memory() {
    log_info "归档小说项目记忆..."
    
    NOVEL_DIR="/home/admin/.openclaw/workspace/novels/重生末世废土"
    
    if [ -d "$NOVEL_DIR" ]; then
        # 检查 .learnings 目录
        LEARNINGS_DIR="$NOVEL_DIR/books/重生末世废土之生存法则/.learnings"
        
        if [ ! -d "$LEARNINGS_DIR" ]; then
            log_warning ".learnings 目录不存在，正在创建..."
            mkdir -p "$LEARNINGS_DIR"
        fi
        
        # 记忆文件模板
        MEMORY_FILES=(
            "CHARACTERS.md:# 角色状态追踪"
            "LOCATIONS.md:# 地点追踪" 
            "PLOT_POINTS.md:# 关键情节追踪"
            "STORY_BIBLE.md:# 世界观设定"
            "ERRORS.md:# 错误记录"
        )
        
        for file_info in "${MEMORY_FILES[@]}"; do
            FILE_NAME="${file_info%%:*}"
            FILE_HEADER="${file_info#*:}"
            
            if [ ! -f "$LEARNINGS_DIR/$FILE_NAME" ]; then
                echo -e "$FILE_HEADER\n\n---\n\n*最后更新: $(date +%Y-%m-%d %H:%M)*\n" > "$LEARNINGS_DIR/$FILE_NAME"
                log_success "创建记忆文件: $FILE_NAME"
            fi
        done
        
        # 更新角色状态（示例）
        if [ -f "$LEARNINGS_DIR/CHARACTERS.md" ]; then
            # 检查是否需要更新
            LAST_UPDATE=$(grep "最后更新" "$LEARNINGS_DIR/CHARACTERS.md" | head -1)
            if [[ ! "$LAST_UPDATE" == *"$(date +%Y-%m-%d)"* ]]; then
                echo -e "\n## $(date +%Y-%m-%d) 更新\n- 系统运行正常\n- 记忆归档优化完成" >> "$LEARNINGS_DIR/CHARACTERS.md"
                sed -i "s/最后更新:.*/最后更新: $(date +%Y-%m-%d %H:%M)/" "$LEARNINGS_DIR/CHARACTERS.md"
                log_success "角色记忆文件已更新"
            fi
        fi
    else
        log_warning "小说目录不存在: $NOVEL_DIR"
    fi
}

# 3. 清理旧文件
cleanup_old_files() {
    log_info "清理旧文件..."
    
    # 清理7天前的日志文件
    find /home/admin/.openclaw/workspace -name "*.log" -type f -mtime +7 -delete 2>/dev/null && \
        log_success "已清理7天前的日志文件"
    
    # 清理临时文件
    find /tmp -name "openclaw-*" -type f -mtime +1 -delete 2>/dev/null && \
        log_success "已清理临时文件"
    
    # 检查磁盘空间
    DISK_USAGE=$(df -h /home | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 80 ]; then
        log_warning "磁盘使用率超过80%: ${DISK_USAGE}%"
    else
        log_success "磁盘使用率正常: ${DISK_USAGE}%"
    fi
}

# 4. 生成归档报告
generate_report() {
    log_info "生成归档报告..."
    
    REPORT_FILE="/home/admin/.openclaw/workspace/memory/归档报告_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$REPORT_FILE" << EOF
# 🧠 记忆归档报告

## 📅 归档时间
$(date "+%Y-%m-%d %H:%M:%S")

## 📊 归档统计

### 文件统计
$(find /home/admin/.openclaw/workspace/memory -name "*.md" -type f | wc -l) 个记忆文件
$(find /home/admin/.openclaw/workspace/novels -name "*.md" -type f | wc -l) 个小说文件

### 目录大小
\`\`\`
$(du -sh /home/admin/.openclaw/workspace/memory 2>/dev/null || echo "无法获取大小")
$(du -sh /home/admin/.openclaw/workspace/novels 2>/dev/null || echo "无法获取大小")
\`\`\`

### 磁盘状态
\`\`\`
$(df -h /home | grep -v Filesystem)
\`\`\`

## ✅ 完成的任务
1. 记忆整理 (Dreaming 模拟)
2. 小说项目记忆归档
3. 旧文件清理
4. 报告生成

## 🎯 后续建议
1. 定期运行此脚本（建议每日一次）
2. 检查记忆文件的一致性
3. 备份重要记忆到云端

---

*报告生成时间: $(date)*
*脚本版本: v1.0*
EOF
    
    log_success "归档报告已生成: $REPORT_FILE"
}

# 5. 配置 Dreaming 功能（如果可用）
configure_dreaming() {
    log_info "检查 Dreaming 功能配置..."
    
    # 尝试配置 Dreaming
    if command -v openclaw &> /dev/null; then
        log_info "尝试配置 Dreaming 功能..."
        
        # 检查当前配置
        DREAMING_CONFIG=$(openclaw config get agents.defaults.dreaming 2>/dev/null || echo "未配置")
        
        if [[ "$DREAMING_CONFIG" == *"未配置"* ]]; then
            log_warning "Dreaming 功能未配置，尝试启用..."
            
            # 尝试启用（可能需要手动确认）
            openclaw config set agents.defaults.dreaming.enabled true 2>/dev/null && \
                log_success "Dreaming 功能已启用" || \
                log_warning "无法自动启用 Dreaming，请手动配置"
        else
            log_success "Dreaming 功能已配置: $DREAMING_CONFIG"
        fi
    else
        log_warning "openclaw 命令不可用，跳过 Dreaming 配置"
    fi
}

# 主函数
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}       记忆归档优化脚本 v1.0           ${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # 执行所有步骤
    check_directories
    consolidate_memory
    archive_novel_memory
    cleanup_old_files
    configure_dreaming
    generate_report
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}✅ 记忆归档优化完成！${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    # 显示总结
    echo -e "${YELLOW}📋 执行总结:${NC}"
    echo -e "  1. 记忆整理完成"
    echo -e "  2. 小说记忆归档完成"
    echo -e "  3. 旧文件清理完成"
    echo -e "  4. Dreaming 功能检查完成"
    echo -e "  5. 归档报告已生成"
    
    # 建议
    echo -e "\n${YELLOW}💡 建议:${NC}"
    echo -e "  将此脚本添加到 crontab 每日执行:"
    echo -e "  \`0 2 * * * /home/admin/.openclaw/workspace/scripts/optimize-memory-archiving.sh\`"
}

# 执行主函数
main "$@"
