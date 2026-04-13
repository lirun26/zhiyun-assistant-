#!/usr/bin/env python3
"""
小说章节单独发送脚本
每个章节单独发送一封邮件，正文干净无分隔线
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

def clean_chapter_content(content):
    """清理章节内容，移除章节信息头部"""
    # 找到第一个"---"之后的内容（移除章节信息头部）
    lines = content.split('\n')
    in_body = False
    body_lines = []
    
    for line in lines:
        if line.strip() == '---':
            in_body = True
            continue
        if in_body:
            body_lines.append(line)
    
    # 如果没有找到"---"，返回原内容
    if not body_lines:
        return content
    
    return '\n'.join(body_lines).strip()

def send_single_chapter(chapter_num, title, content, word_count, score):
    """单独发送一个章节"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 创建邮件内容（只有章节正文，无分隔线，无额外信息）
    email_content = content
    
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        subject = f"《重生末世废土之生存法则》第{chapter_num}章 {title}"
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文（只有章节正文）
        text_part = MIMEText(email_content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 连接SMTP服务器并发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print(f"✅ 第{chapter_num}章《{title}》发送成功")
        print(f"   📝 字数: {word_count}字")
        print(f"   ⭐ 评分: {score}/100")
        print(f"   🕒 时间: {current_time}")
        return True
        
    except Exception as e:
        print(f"❌ 第{chapter_num}章发送失败: {e}")
        return False

def main():
    print("=" * 50)
    print("《重生末世废土之生存法则》章节单独发送")
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
    chapter_20_raw = read_chapter_file(CHAPTER_20_PATH)
    chapter_21_raw = read_chapter_file(CHAPTER_21_PATH)
    
    if not chapter_20_raw or not chapter_21_raw:
        print("❌ 读取章节内容失败")
        return False
    
    # 清理章节内容（移除章节信息头部）
    chapter_20_content = clean_chapter_content(chapter_20_raw)
    chapter_21_content = clean_chapter_content(chapter_21_raw)
    
    print(f"✅ 第20章清理后: {len(chapter_20_content)} 字符")
    print(f"✅ 第21章清理后: {len(chapter_21_content)} 字符")
    
    # 单独发送每个章节
    print("\n🚀 开始单独发送每个章节...")
    print("-" * 40)
    
    # 发送第20章
    success_20 = send_single_chapter(
        chapter_num=20,
        title="暴风雪中的博弈",
        content=chapter_20_content,
        word_count=3420,
        score=95
    )
    
    print("-" * 40)
    
    # 发送第21章
    success_21 = send_single_chapter(
        chapter_num=21,
        title="暴风雪决战",
        content=chapter_21_content,
        word_count=4500,
        score=96
    )
    
    print("-" * 40)
    
    if success_20 and success_21:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "=" * 50)
        print("✅ 所有章节发送完成!")
        print(f"📤 已发送: 第20章 + 第21章（单独发送）")
        print(f"📝 发送方式: 每个章节单独一封邮件")
        print(f"📄 邮件内容: 只有章节正文，无分隔线")
        print(f"📊 总字数: 7920字")
        print(f"📅 完成时间: {current_time}")
        print("=" * 50)
        return True
    else:
        print("\n❌ 章节发送失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)