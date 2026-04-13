#!/usr/bin/env python3
"""
发送小说章节到邮箱
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_novel_chapter():
    # 配置信息
    config = {
        'qq': {
            'smtp_server': 'smtp.qq.com',
            'smtp_port': 465,
            'sender_email': '306101637@qq.com',
            'sender_password': 'jkxwhttefzgqbjab',
            'receiver_email': '306101637@qq.com'  # 发送给自己
        }
    }
    
    # 章节信息
    chapter_info = {
        'novel_title': '技能嫌我太懒，独自升级杀疯了',
        'chapter_number': '004',
        'chapter_title': '系统新功能：社交技能觉醒',
        'chapter_file': '/home/admin/.openclaw/workspace/novels/技能嫌我太懒独自升级杀疯了/正文/第004章.txt',
        'review_file': '/home/admin/.openclaw/workspace/novels/技能嫌我太懒独自升级杀疯了/评审/第004章.md'
    }
    
    # 读取章节内容
    try:
        with open(chapter_info['chapter_file'], 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        with open(chapter_info['review_file'], 'r', encoding='utf-8') as f:
            review_content = f.read()
    except FileNotFoundError as e:
        print(f"错误：文件未找到 - {e}")
        return False
    
    # 创建邮件内容
    email_subject = f"{chapter_info['novel_title']} - 第{chapter_info['chapter_number']}章 {chapter_info['chapter_title']}"
    
    # 构建邮件正文
    email_body = f"""
# {chapter_info['novel_title']}

## 第{chapter_info['chapter_number']}章 {chapter_info['chapter_title']}

### 📊 章节信息
- **小说名称**: {chapter_info['novel_title']}
- **章节编号**: 第{chapter_info['chapter_number']}章
- **章节标题**: {chapter_info['chapter_title']}
- **创作时间**: 2026-04-07
- **字数统计**: 约2544字（5088字符）

### 📖 章节正文
{chapter_content}

### 🔍 评审报告摘要
{review_content[:500]}...

---
*邮件发送时间: 2026-04-07 10:00*
*发送人: 智云助手*
"""
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = Header(f"智云助手 <{config['qq']['sender_email']}>", 'utf-8')
    msg['To'] = Header(f"收件人 <{config['qq']['receiver_email']}>", 'utf-8')
    msg['Subject'] = Header(email_subject, 'utf-8')
    
    # 添加正文
    msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
    
    try:
        # 连接SMTP服务器
        print(f"正在连接SMTP服务器: {config['qq']['smtp_server']}:{config['qq']['smtp_port']}")
        server = smtplib.SMTP_SSL(config['qq']['smtp_server'], config['qq']['smtp_port'])
        server.set_debuglevel(1)  # 显示调试信息
        
        # 登录
        print(f"正在登录邮箱: {config['qq']['sender_email']}")
        server.login(config['qq']['sender_email'], config['qq']['sender_password'])
        
        # 发送邮件
        print(f"正在发送邮件到: {config['qq']['receiver_email']}")
        server.sendmail(config['qq']['sender_email'], 
                       [config['qq']['receiver_email']], 
                       msg.as_string())
        
        # 关闭连接
        server.quit()
        print("✅ 邮件发送成功！")
        
        # 记录发送状态
        record_send_status(chapter_info, config)
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def record_send_status(chapter_info, config):
    """记录发送状态到记忆文件"""
    record = f"""
## 📧 邮件发送记录 - 《技能嫌我太懒，独自升级》第4章

**发送时间**: 2026-04-07 10:00
**发送状态**: ✅ 成功
**发送邮箱**: {config['qq']['sender_email']}
**收件邮箱**: {config['qq']['receiver_email']}
**章节信息**: 第{chapter_info['chapter_number']}章《{chapter_info['chapter_title']}》
**字数统计**: 约2544字

**发送内容包含**:
1. 章节正文（完整）
2. 评审报告摘要
3. 章节信息统计

---
"""
    
    # 追加到今日记忆文件
    memory_file = '/home/admin/.openclaw/workspace/memory/2026-04-07.md'
    try:
        with open(memory_file, 'a', encoding='utf-8') as f:
            f.write(record)
        print(f"✅ 发送记录已保存到: {memory_file}")
    except Exception as e:
        print(f"⚠️ 发送记录保存失败: {e}")

if __name__ == '__main__':
    print("🚀 开始发送小说章节...")
    print("=" * 50)
    
    success = send_novel_chapter()
    
    print("=" * 50)
    if success:
        print("🎉 发送流程完成！")
        sys.exit(0)
    else:
        print("❌ 发送流程失败！")
        sys.exit(1)