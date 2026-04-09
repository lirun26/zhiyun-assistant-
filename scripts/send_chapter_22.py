#!/usr/bin/env python3
"""
第22章单独发送脚本
章节单独发送，不要第几部分，只要正文内容
"""

import smtplib
import os
import re
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
CHAPTER_22_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0022_第22章_黎明协议.md"

def read_chapter_file(filepath):
    """读取章节文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"读取文件失败: {filepath}")
        return None

def clean_chapter_content(content):
    """清理章节内容"""
    lines = content.split('\n')
    cleaned_lines = []
    in_body = False
    
    for line in lines:
        # 跳过章节信息头部（"---"之前的所有内容）
        if line.strip() == '---':
            in_body = True
            continue
        if not in_body:
            continue
            
        # 移除所有"第X部分"标题
        if re.match(r'^第[一二三四五六七八九十]+部分', line.strip()):
            continue
            
        # 移除空行（但保留段落间的空行）
        if line.strip() == '' and (not cleaned_lines or cleaned_lines[-1].strip() == ''):
            continue
            
        cleaned_lines.append(line)
    
    # 合并清理后的内容
    cleaned_content = '\n'.join(cleaned_lines).strip()
    
    # 移除多余的空行（连续3个以上空行保留2个）
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    return cleaned_content

def send_chapter(chapter_num, title, content, word_count):
    """单独发送一个章节"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        subject = f"《重生末世废土之生存法则》第{chapter_num}章 {title}"
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文（只有清理后的章节内容）
        text_part = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 连接SMTP服务器并发送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print(f"✅ 第{chapter_num}章《{title}》发送成功")
        return True
        
    except Exception as e:
        print(f"❌ 第{chapter_num}章发送失败: {e}")
        return False

def main():
    print("=" * 50)
    print("第22章《黎明协议》发送")
    print("=" * 50)
    
    # 检查文件是否存在
    if not os.path.exists(CHAPTER_22_PATH):
        print(f"❌ 文件不存在: {CHAPTER_22_PATH}")
        return False
    
    print(f"✅ 找到第22章文件: {CHAPTER_22_PATH}")
    
    # 读取章节内容
    print("\n📖 正在读取章节内容...")
    chapter_22_raw = read_chapter_file(CHAPTER_22_PATH)
    
    if not chapter_22_raw:
        print("❌ 读取章节内容失败")
        return False
    
    print(f"原始内容长度: {len(chapter_22_raw)} 字符")
    
    # 清理章节内容
    print("\n🧹 正在清理章节内容...")
    chapter_22_clean = clean_chapter_content(chapter_22_raw)
    
    print(f"清理后内容长度: {len(chapter_22_clean)} 字符")
    
    # 发送清理后的章节
    print("\n🚀 正在发送第22章...")
    success = send_chapter(
        chapter_num=22,
        title="黎明协议",
        content=chapter_22_clean,
        word_count=3980
    )
    
    if success:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "=" * 50)
        print("✅ 第22章发送完成!")
        print(f"📤 已发送: 第22章《黎明协议》（干净版本）")
        print(f"📝 字数: 3980字")
        print(f"⭐ 评分: 95.25/100 (精品)")
        print(f"📅 发送时间: {current_time}")
        print("=" * 50)
        return True
    else:
        print("\n❌ 发送失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)