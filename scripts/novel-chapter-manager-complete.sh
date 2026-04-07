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

# 主函数
main() {
    local command=$1
    local arg1=$2
    local arg2=$3
    
    case $command in
        "status")
            show_chapter_status
            ;;
        "start")
            if [ -z "$arg1" ] || [ -z "$arg2" ]; then
                echo "用法: $0 start <章号> <标题>"
                exit 1
            fi
            start_new_chapter "$arg1" "$arg2"
            ;;
        "review")
            if [ -z "$arg1" ]; then
                echo "用法: $0 review <章号>"
                exit 1
            fi
            review_chapter "$arg1"
            ;;
        "send")
            if [ -z "$arg1" ]; then
                echo "用法: $0 send <章号>"
                exit 1
            fi
            send_chapter "$arg1"
            ;;
        "help"|"")
            show_help
            ;;
        *)
            echo "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
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
    echo -e "${BLUE}示例:${NC}"
    echo -e "  $0 status                     # 显示章节状态"
    echo -e "  $0 start 15 \"新的开始\"        # 开始第15章"
    echo -e "  $0 review 15                  # 评审第15章"
    echo -e "  $0 send 15                    # 发送第15章"
    echo
    echo -e "${CYAN}========================================${NC}"
}

# 显示章节状态
show_chapter_status() {
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}小说: $NOVEL_NAME${NC}"
    echo -e "${CYAN}========================================${NC}"
    
    # 检查目录
    if [ ! -d "$CHAPTERS_DIR" ]; then
        echo -e "${RED}错误: 章节目录不存在${NC}"
        echo "请先创建目录: mkdir -p $CHAPTERS_DIR"
        exit 1
    fi
    
    # 查找所有章节文件
    CHAPTER_FILES=($(find "$CHAPTERS_DIR" -name "第*章_*.md" -type f | sort))
    
    if [ ${#CHAPTER_FILES[@]} -eq 0 ]; then
        echo -e "${YELLOW}未找到章节文件${NC}"
        echo "使用: $0 start <章号> <标题> 开始新章节"
        return
    fi
    
    echo -e "${BLUE}📚 章节列表:${NC}"
    for file in "${CHAPTER_FILES[@]}"; do
        CHAPTER_NAME=$(basename "$file" .md)
        FILE_SIZE=$(stat -c%s "$file" 2>/dev/null || echo "0")
        WORD_COUNT=$(wc -w < "$file" 2>/dev/null || echo "0")
        LAST_MODIFIED=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1)
        
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
    
    echo -e "${CYAN}========================================${NC}"
}

# 开始新章节
start_new_chapter() {
    local chapter_num=$1
    local chapter_title=$2
    
    echo -e "${CYAN}========================================${NC}"
    echo -e "${YELLOW}开始新章节: 第${chapter_num}章 $chapter_title${NC}"
    echo -e "${CYAN}========================================${NC}"
    
    # 创建目录
    mkdir -p "$CHAPTERS_DIR"
    mkdir -p "$LEARNINGS_DIR"
    
    # 创建章节文件
    CHAPTER_FILE="$CHAPTERS_DIR/第${chapter_num}章_${chapter_title}.md"
    
    if [ -f "$CHAPTER_FILE" ]; then
        echo -e "${YELLOW}警告: 章节文件已存在${NC}"
        read -p "是否覆盖? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}取消操作${NC}"
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
    
    echo -e "${GREEN}✅ 章节文件已创建:${NC}"
    echo -e "  $CHAPTER_FILE"
    
    # 更新学习记录
    update_learnings "$chapter_num" "$chapter_title" "created"
    
    echo -e "\n${BLUE}📋 下一步:${NC}"
    echo -e "  1. 编辑章节文件: vim '$CHAPTER_FILE'"
    echo -e "  2. 或查看内容: cat '$CHAPTER_FILE'"
    echo -e "  3. 完成后运行: $0 review $chapter_num"
    
    echo -e "${CYAN}========================================${NC}"
}

# 更新学习记录
update_learnings() {
    local chapter_num=$1
    local chapter_title=$2
    local action=$3
    
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    # 创建学习目录
    mkdir -p "$LEARNINGS_DIR"
    
    # 更新角色记忆
    CHARACTERS_FILE="$LEARNINGS_DIR/CHARACTERS.md"
    if [ ! -f "$CHARACTERS_FILE" ]; then
        cat > "$CHARACTERS_FILE" << EOF
# 角色状态追踪

## 主要角色
- 苏清鸢: 26岁白领，重生者，有随身空间
- 其他角色: 待补充

---
*最后更新: $timestamp*
EOF
    fi
    
    echo -e "\n## 第${chapter_num}章更新 ($timestamp)" >> "$CHARACTERS_FILE"
    echo -e "- 章节: $chapter_title" >> "$CHARACTERS_FILE"
    echo -e "- 操作: $action" >> "$CHARACTERS_FILE"
    sed -i "s/最后更新:.*/最后更新: $timestamp/" "$CHARACTERS_FILE"
    
    echo -e "${GREEN}✅ 学习记录已更新${NC}"
}

# 执行主函数
main "$@"