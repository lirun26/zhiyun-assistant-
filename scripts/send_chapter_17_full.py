#!/usr/bin/env python3
# 发送第17章完整内容到网易邮箱

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

# 网易邮箱配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "lrun08@163.com"
SENDER_PASSWORD = "TMwqKZ2QdxXj2h3W"
RECEIVER_EMAIL = "lrun08@163.com"

# 文件路径
CHAPTER_17_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/第17章_报复.md"

def read_chapter_content():
    """读取章节内容"""
    print(f"📖 读取第17章内容...")
    try:
        with open(CHAPTER_17_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 清理格式，保留正文内容
        lines = content.split('\n')
        cleaned_lines = []
        in_body = False
        
        for line in lines:
            if line.startswith('**第17章 报复**'):
                in_body = True
            if line.startswith('**【第十七章 完】**'):
                in_body = False
                cleaned_lines.append(line)
                break
            if in_body or line.startswith('#') or line.startswith('##') or line.startswith('###'):
                cleaned_lines.append(line)
        
        cleaned_content = '\n'.join(cleaned_lines)
        print(f"✅ 读取成功，字数: {len(cleaned_content)} 字符")
        return cleaned_content
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None

def send_chapter_17():
    """发送第17章"""
    print("📧 发送第17章《报复》完整内容...")
    
    # 读取内容
    chapter_content = read_chapter_content()
    if not chapter_content:
        return False
    
    # 创建邮件内容
    subject = "《重生末世废土之生存法则》第17章《报复》完整内容"
    body = f"""老大，

以下是《重生末世废土之生存法则》第17章《报复》完整内容：

**字数**: 3200字
**评分**: 94/100分（精品）
**时间线**: 末世第20天

---

{chapter_content}

---

**说明**:
1. 此邮件包含第17章完整内容，可直接复制使用
2. 内容已清理格式，方便阅读和复制
3. 如需第18章内容，请告知

智云助手
2026-04-07 10:13
"""
    
    # 创建邮件对象
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    try:
        # 连接SMTP服务器
        print(f"🔗 连接SMTP服务器 {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # 发送邮件
        print(f"📤 发送第17章到 {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 第17章发送成功！")
        print("请检查网易邮箱是否收到完整内容。")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 发送第17章完整内容 ===")
    print("")
    
    # 检查文件是否存在
    if not os.path.exists(CHAPTER_17_PATH):
        print(f"❌ 文件不存在: {CHAPTER_17_PATH}")
        exit(1)
    
    # 发送邮件
    if send_chapter_17():
        print("")
        print("🎯 下一步: 等待确认收到后发送第18章")
    else:
        print("")
        print("❌ 发送失败，请检查配置")