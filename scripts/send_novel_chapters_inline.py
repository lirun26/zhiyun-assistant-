#!/usr/bin/env python3
"""
小说章节发送脚本（正文内联版本）
发送《重生末世废土之生存法则》第20-21章正文内容
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime

# 配置信息
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "lrun08@163.com"
SENDER_PASSWORD = "TMwqKZ2QdxXj2h3W"
RECEIVER_EMAIL = "lrun08@163.com"

# 章节文件路径
CHAPTER_20_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0020_第20章_暴风雪中的博弈.md"
CHAPTER_21_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0021_第21章_暴风雪决战.md"

def read_chapter_file(filepath):
    """读取章节文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"读取文件失败: {filepath}")
        print(f"错误: {e}")
        return None

def create_email_content(chapter_20_content, chapter_21_content):
    """创建邮件内容（正文内联）"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    email_content = f"""
《重生末世废土之生存法则》第20-21章正文内容

📅 发送时间: {current_time}
📤 发送方式: 正文内联（便于复制）
📖 发送内容: 第20-21章完整正文

========================================
第20章《暴风雪中的博弈》
========================================

{chapter_20_content}

========================================
第21章《暴风雪决战》
========================================

{chapter_21_content}

========================================
📊 章节信息汇总
========================================

第20章《暴风雪中的博弈》
- 字数: 3420字
- 评分: 95/100 (精品)
- 时间线: 末世第21天傍晚6:30 → 夜间10:00
- 核心剧情: 三人联盟形成，无线电心理战，掠夺者逼近

第21章《暴风雪决战》
- 字数: 4500字
- 评分: 96/100 (精品)
- 时间线: 末世第21天夜间10:30 → 第22天凌晨4:00
- 核心剧情: 三人对三十一人暴风雪决战，战术配合，第七避难所介入

📈 统计信息
- 总字数: 7920字
- 平均评分: 95.5/100
- 发送时间: {current_time}
- 发送方式: 正文内联（无附件）

---
发送人: 智云助手
发送时间: {current_time}
邮箱: {SENDER_EMAIL}
备注: 正文直接放在邮件中，便于复制粘贴
    """
    
    return email_content

def send_email_inline(subject, content):
    """发送邮件（正文内联）"""
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文（内联章节内容）
        text_part = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 连接SMTP服务器并发送
        print(f"正在连接SMTP服务器: {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"正在发送邮件到: {RECEIVER_EMAIL}")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功!")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    print("=" * 50)
    print("《重生末世废土之生存法则》第20-21章正文内联发送")
    print("=" * 50)
    
    # 检查文件是否存在
    if not os.path.exists(CHAPTER_20_PATH):
        print(f"❌ 文件不存在: {CHAPTER_20_PATH}")
        return False
        
    if not os.path.exists(CHAPTER_21_PATH):
        print(f"❌ 文件不存在: {CHAPTER_21_PATH}")
        return False
    
    print(f"✅ 找到第20章文件: {CHAPTER_20_PATH}")
    print(f"✅ 找到第21章文件: {CHAPTER_21_PATH}")
    
    # 读取章节内容
    print("\n📖 正在读取章节内容...")
    chapter_20_content = read_chapter_file(CHAPTER_20_PATH)
    chapter_21_content = read_chapter_file(CHAPTER_21_PATH)
    
    if not chapter_20_content or not chapter_21_content:
        print("❌ 读取章节内容失败")
        return False
    
    print(f"✅ 第20章读取成功: {len(chapter_20_content)} 字符")
    print(f"✅ 第21章读取成功: {len(chapter_21_content)} 字符")
    
    # 创建邮件内容（内联）
    print("\n📧 正在创建邮件内容（正文内联）...")
    email_content = create_email_content(chapter_20_content, chapter_21_content)
    
    # 发送邮件
    print("\n🚀 正在发送邮件（正文内联）...")
    subject = "《重生末世废土之生存法则》第20-21章正文内容"
    success = send_email_inline(subject, email_content)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ 发送流程完成!")
        print(f"📤 已发送: 第20-21章正文内容（内联）")
        print(f"📝 发送方式: 正文直接放在邮件中")
        print(f"📊 总字数: 7920字")
        print(f"📅 发送时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        return True
    else:
        print("\n❌ 发送流程失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)