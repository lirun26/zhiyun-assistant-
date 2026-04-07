#!/bin/bash

# 📚 小说章节管理器 v1.0
# 功能：结构化小说章节创作流程管理
# 集成：OpenClaw 2026.4.5+ 结构化任务进度

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 配置
NOVEL_NAME="重生末世废土之生存法则"
NOVEL_DIR="/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则"
CHAPTERS_DIR="$NOVEL_DIR/chapters"
LEARNINGS_DIR="$NOVEL_DIR/.learnings"
TEMPLATE_DIR="/home/admin/.openclaw/workspace/templates"

# 日志函数
log() {
    local level=$1
    local message=$2
    local color=$BLUE
    
    case $level in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARNING") color=$YELLOW ;;
        "ERROR") color=$RED ;;
        "TASK") color=$PURPLE ;;
        "STEP") color=$CYAN ;;
    esac
    
    echo -e "${color}[$level]${NC} $message"
}

# 检查环境
check_environment() {
    log "INFO" "检查环境配置..."
    
    # 检查目录
    for dir in "$NOVEL_DIR" "$CHAPTERS_DIR" "$LEARNINGS_DIR" "$TEMPLATE_DIR"; do
        if [ ! -d "$dir" ]; then
            log "WARNING" "目录不存在: $dir"
            mkdir -p "$dir"
            log "SUCCESS" "已创建目录: $dir"
        fi
    done
    
    # 检查模板文件
    if [ ! -f "$TEMPLATE_DIR/novel-writing-task-template.md" ]; then
        log "WARNING" "任务模板不存在，正在创建..."
        # 这里可以调用创建模板的函数
    fi
}

# 显示章节状态
show_chapter_status() {
    log "INFO" "📊 小说章节状态"
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}小说: $NOVEL_NAME${NC}"
    echo -e "${CYAN}========================================${NC}"
    
    # 查找所有章节文件
    CHAPTER_FILES=($(find "$CHAPTERS_DIR" -name "第*章_*.md" -type f | sort))
    
    if [ ${#CHAPTER_FILES[@]} -eq 0 ]; then
        log "WARNING" "未找到章节文件"
        return
    fi
    
    echo -e "${BLUE}章节列表:${NC}"
    for file in "${CHAPTER_FILES[@]}"; do
        CHAPTER_NAME=$(basename "$file" .md)
        FILE_SIZE=$(stat -c%s "$file")
        WORD_COUNT=$(wc -w < "$file" 2>/dev/null || echo "0")
        LAST_MODIFIED=$(stat -c%y "$file" | cut -d' ' -f1)
        
        echo -e "  📖 $CHAPTER_NAME"
        echo -e "     大小: ${FILE_SIZE}字节 | 字数: ${WORD_COUNT} | 修改: ${LAST_MODIFIED}"
    done
    
    # 显示进度
    TOTAL_CHAPTERS=200
    COMPLETED_CHAPTERS=${#CHAPTER_FILES[@]}
    PERCENTAGE=$((COMPLETED_CHAPTERS * 100 / TOTAL_CHAPTERS))
    
    echo -e "\n${GREEN}📈 总体进度:${NC}"
    echo -e "  已完成: $COMPLETED_CHAPTERS/$TOTAL_CHAPTERS 章"
    echo -e "  进度: $PERCENTAGE%"
    
    # 进度条
    BAR_WIDTH=50
    FILLED=$((PERCENTAGE * BAR_WIDTH / 100))
    EMPTY=$((BAR_WIDTH - FILLED))
    
    echo -n "  ["
    for ((i=0; i<FILLED; i++)); do echo -n "█"; done
    for ((i=0; i<EMPTY; i++)); do echo -n "░"; done
    echo "]"
}

# 开始新章节
start_new_chapter() {
    local chapter_num=$1
    local chapter_title=$2
    
    log "TASK" "开始新章节: 第${chapter_num}章 $chapter_title"
    
    # 创建章节文件
    CHAPTER_FILE="$CHAPTERS_DIR/第${chapter_num}章_${chapter_title}.md"
    
    if [ -f "$CHAPTER_FILE" ]; then
        log "WARNING" "章节文件已存在: $CHAPTER_FILE"
        read -p "是否覆盖? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "INFO" "取消操作"
            return
        fi
    fi
    
    # 创建章节模板
    cat > "$CHAPTER_FILE" << EOF
# 第${chapter_num}章 ${chapter_title}

## 📝 章节信息
- **章节编号**: ${chapter_num}
- **标题**: ${chapter_title}
- **创建时间**: $(date "+%Y-%m-%d %H:%M:%S")
- **目标字数**: 3000字
- **状态**: 创作中

## 🎯 本章目标
<!-- 填写本章的核心目标和冲突 -->

## 📖 正文
<!-- 开始创作 -->

---

## 🔍 创作记录

### $(date +%Y-%m-%d) 创建
- 章节文件创建
- 基础信息填写

### 待完成
- [ ] 正文创作
- [ ] 评审修改
- [ ] 记忆归档
- [ ] 发送发布

## 📊 统计
- 当前字数: 0
- 预计完成时间: 
- 实际完成时间: 

---
*最后更新: $(date "+%Y-%m-%d %H:%M:%S")*
EOF
    
    log "SUCCESS" "章节文件已创建: $CHAPTER_FILE"
    
    # 更新学习记录
    update_learnings "$chapter_num" "$chapter_title" "created"
    
    # 显示下一步
    log "STEP" "下一步: 编辑章节文件"
    echo -e "  命令: vim '$CHAPTER_FILE'"
    echo -e "  或: cat '$CHAPTER_FILE'"
}

# 更新学习记录
update_learnings() {
    local chapter_num=$1
    local chapter_title=$2
    local action=$3
    
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    # 更新角色记忆
    if [ -f "$LEARNINGS_DIR/CHARACTERS.md" ]; then
        echo -e "\n## 第${chapter_num}章更新 ($timestamp)" >> "$LEARNINGS_DIR/CHARACTERS.md"
        echo -e "- 章节: $chapter_title" >> "$LEARNINGS_DIR/CHARACTERS.md"
        echo -e "- 操作: $action" >> "$LEARNINGS_DIR/CHARACTERS.md"
        
        # 更新最后修改时间
        sed -i "s/最后更新:.*/最后更新: $timestamp/" "$LEARNINGS_DIR/CHARACTERS.md"
    fi
    
    # 更新情节记忆
    if [ -f "$LEARNINGS_DIR/PLOT_POINTS.md" ]; then
        echo -e "\n## 第${chapter_num}章 ($timestamp)" >> "$LEARNINGS_DIR/PLOT_POINTS.md"
        echo -e "- 标题: $chapter_title" >> "$LEARNINGS_DIR/PLOT_POINTS.md"
        echo -e "- 状态: $action" >> "$LEARNINGS_DIR/PLOT_POINTS.md"
        
        sed -i "s/最后更新:.*/最后更新: $timestamp/" "$LEARNINGS_DIR/PLOT_POINTS.md"
    fi
    
    log "SUCCESS" "学习记录已更新"
}

# 章节评审
review_chapter() {
    local chapter_num=$1
    
    log "TASK" "评审章节: 第${chapter_num}章"
    
    # 查找章节文件
    CHAPTER_FILE=$(find "$CHAPTERS_DIR" -name "第${chapter_num}章_*.md" -type f | head -1)
    
    if [ -z "$CHAPTER_FILE" ]; then
        log "ERROR" "未找到第${chapter_num}章文件"
        return 1
    fi
    
    local chapter_title=$(basename "$CHAPTER_FILE" .md | sed 's/第[0-9]*章_//')
    
    # 检查文件
    FILE_SIZE=$(stat -c%s "$CHAPTER_FILE")
    WORD_COUNT=$(wc -w < "$CHAPTER_FILE" 2>/dev/null || echo "0")
    
    log "INFO" "章节信息:"
    echo -e "  文件: $(basename "$CHAPTER_FILE")"
    echo -e "  大小: ${FILE_SIZE}字节"
    echo -e "  字数: ${WORD_COUNT}"
    
    # 简单的内容检查
    log "STEP" "执行基础检查..."
    
    # 检查常见问题
    ISSUES=0
    
    # 1. 检查AI词汇
    if grep -q -E "(众所周知|不言而喻|综上所述|总而言之)" "$CHAPTER_FILE"; then
        log "WARNING" "发现AI词汇"
        ISSUES=$((ISSUES + 1))
    fi
    
    # 2. 检查感叹式结尾
    if tail -5 "$CHAPTER_FILE" | grep -q -E "(真是太|实在是|简直是).*[!！]$"; then
        log "WARNING" "发现感叹式结尾"
        ISSUES=$((ISSUES + 1))
    fi
    
    # 3. 检查上帝视角
    if grep -q -E "(所有人|大家都|每个人).*(没想到|不知道)" "$CHAPTER_FILE"; then
        log "WARNING" "发现上帝视角"
        ISSUES=$((ISSUES + 1))
    fi
    
    # 生成评审报告
    REVIEW_FILE="${CHAPTER_FILE%.md}_评审.md"
    
    cat > "$REVIEW_FILE" << EOF
# 第${chapter_num}章评审报告

## 📅 评审信息
- **评审时间**: $(date "+%Y-%m-%d %H:%M:%S")
- **章节文件**: $(basename "$CHAPTER_FILE")
- **章节字数**: ${WORD_COUNT}

## 📊 基础检查
- AI词汇检查: $( [ $ISSUES -gt 0 ] && echo "❌ 发现问题" || echo "✅ 通过" )
- 结尾检查: $(tail -5 "$CHAPTER_FILE" | grep -q -E "(真是太|实在是|简直是)" && echo "❌ 发现问题" || echo "✅ 通过")
- 视角检查: $(grep -q -E "(所有人|大家都|每个人)" "$CHAPTER_FILE" && echo "❌ 发现问题" || echo "✅ 通过")

## 🎯 5角色评分系统

| 角色 | 关注点 | 权重 | 评分 | 备注 |
|:---|:---|:---|:---|:---|
| 阅读者 | 开篇吸引力、节奏、画面感 | 25% | /25 | |
| 编审 | 错别字、病句、一致性 | 25% | /25 | |
| 故事家 | 剧情逻辑、伏笔、钩子 | 25% | /25 | |
| 文学顾问 | 语言艺术、人物刻画 | 15% | /15 | |
| 毒舌读者 | 套路化、水文、毒点 | 10% | /10 | |
| **总分** | | **100%** | **/100** | |

## 🔍 发现的问题
$(if [ $ISSUES -gt 0 ]; then
    grep -n -E "(众所周知|不言而喻|综上所述|总而言之|真是太|实在是|简直是|所有人|大家都|每个人)" "$CHAPTER_FILE" | head -10 | while read line; do
        echo "- 第${line}"
    done
else
    echo "未发现明显问题"
fi)

## 💡 修改建议
1. 建议检查章节开头是否吸引人
2. 建议检查情节逻辑是否连贯
3. 建议检查人物对话是否自然

## 📈 评分标准参考
- 90-100：精品
- 85-89：优秀，可发布
- 75-84：良好，小改可发
- 60-74：合格，需修改
- 60以下：不合格，重写

---
*评审完成时间: $(date)*
EOF
    
    log "SUCCESS" "评审报告已生成: $REVIEW_FILE"
    log "STEP" "请手动填写评分并检查建议"
    
    # 更新学习记录
    update_learnings "$chapter_num" "$chapter_title" "reviewed"
}

# 发送章节
send_chapter() {
    local chapter_num=$1
    
    log "TASK" "准备发送章节: 第${chapter_num}章"
    
    # 查找章节文件
    CHAPTER_FILE=$(find "$CHAPTERS_DIR" -name "第${chapter_num}章_*.md" -type f | head -1)
    
    if [ -z "$CHAPTER_FILE" ]; then
        log "ERROR" "未找到第${chapter_num}章文件"
        return 1
    fi
    
    local chapter_title=$(basename "$CHAPTER_FILE" .md | sed 's/第[0-9]*章_//')
    
    # 检查评审文件
    REVIEW_FILE="${CHAPTER_FILE%.md}_评审.md"
    if [ ! -f "$REVIEW_FILE" ]; then
        log "WARNING" "未找到评审文件，建议先进行评审"
        read -p "是否继续发送? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "INFO" "取消发送"
            return
        fi
    fi
    
    # 发送前检查清单
    log "STEP" "执行发送前检查..."
    
    CHECKLIST=(
        "收件人邮箱正确 (lrun08@163.com)"
        "章节衔接上一章"
        "人物出场有铺垫"
        "时间线无矛盾"
        "无重复情节/描写"
        "章节编号正确"
        "标题格式统一"
    )
    
    echo -e "${YELLOW}发送前检查清单:${NC}"
    for item in "${CHECKLIST[@]}"; do
        echo -e "  [ ] $item"
    done
    
    echo
    read -p "所有检查项是否已完成? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "INFO" "请完成检查后再发送"
        return
    fi
    
    # 模拟发送（实际需要邮件配置）
    log "INFO" "模拟发送配置:"
    echo -e "  发送邮箱: lrun08@163.com"
    echo -e "  收件邮箱: lrun08@163.com"
    echo -e "  SMTP: smtp.163.com:465 (SSL)"
    echo -e "  授权码: TMwqKZ2QdxXj2h3W"
    
    # 创建发送记录
    SEND_RECORD="${CHAPTER_FILE%.md}_发送记录.md"
    
    cat > "$SEND_RECORD" << EOF
# 第${chapter_num}章发送记录

## 📤 发送信息
- **发送时间**: $(date "+%Y-%m-%d %H:%M:%S")
- **章节**: 第${chapter_num}章 $chapter_title
- **文件**: $(basename "$CHAPTER_FILE")
- **字数**: $(wc -w < "$CHAPTER_FILE" 2>/dev/null || echo "0")

## 📧 邮件配置
- 发件人: lrun08@163.com
- 收件人: lrun08@163.com
- SMTP服务器: smtp.163.com:465
- 发送状态: 模拟发送完成

## ✅ 检查项完成情况
$(for item in "${CHECKLIST[@]}"; do
    echo "- [x] $item"
done)

## 📝 备注
- 此为模拟发送记录
- 实际发送需要配置邮件客户端
- 建议使用实际邮件客户端发送

---
*记录生成时间: $(date)*
EOF
    
    log "SUCCESS" "发送记录已生成: $SEND_RECORD"
    log "WARNING" "注意: 此为模拟发送，实际发送需要配置邮件"
    
    # 更新学习记录
    update_learnings "$chapter_num" "$chapter_title" "sent"
}

# 显示帮助
show_help() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}       小说章节管理器 v1.0           ${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo
    echo -e "${BLUE}使用方法:${NC}"
    echo -e "  $0 [命令] [参数]"
    echo
    echo -e "${BLUE}命令列表:${NC}"
    echo -e "  ${GREEN}status${NC}              显示章节状态"
    echo -e "  ${GREEN}start <章号> <标题>${NC} 开始新章节"
    echo -e "  ${GREEN}review <章号>${NC}       评审章节"
    echo -e "  ${GREEN}send <章号>${NC}         发送章节"
    echo -e "  ${GREEN}help${NC}                显示帮助"
    echo
    echo -e "${BLUE}示例:${