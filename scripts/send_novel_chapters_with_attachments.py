#!/usr/bin/env python3
"""
小说章节发送脚本（带附件版本）
发送《重生末世废土之生存法则》第20-21章正文文件
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
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

def attach_file(msg, filepath):
    """添加附件"""
    try:
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            file_content = f.read()
        
        attachment = MIMEApplication(file_content, Name=filename)
        attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(attachment)
        print(f"✅ 已添加附件: {filename}")
        return True
    except Exception as e:
        print(f"❌ 添加附件失败: {filepath}, 错误: {e}")
        return False

def create_email_content():
    """创建邮件正文内容"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    email_content = f"""
《重生末世废土之生存法则》第20-21章正文文件发送

📅 发送时间: {current_time}
📤 发送内容: 第20-21章正文文件（.md格式）

📖 章节详情:
1. 第20章《暴风雪中的博弈》
   - 文件名: 0020_第20章_暴风雪中的博弈.md
   - 字数: 3420字
   - 评分: 95/100 (精品)
   - 时间线: 末世第21天傍晚6:30 → 夜间10:00

2. 第21章《暴风雪决战》
   - 文件名: 0021_第21章_暴风雪决战.md
   - 字数: 4500字
   - 评分: 96/100 (精品)
   - 时间线: 末世第21天夜间10:30 → 第22天凌晨4:00

🎯 剧情概要:
- 第20章: 三人联盟形成，无线电心理战，掠夺者逼近
- 第21章: 三人对三十一人暴风雪决战，战术配合，第七避难所介入

📊 统计信息:
- 总字数: 7920字
- 平均评分: 95.5/100
- 发送方式: 带附件发送
- 文件格式: Markdown (.md)

📁 附件清单:
1. 0020_第20章_暴风雪中的博弈.md
2. 0021_第21章_暴风雪决战.md

⚠️ 注意事项:
1. 文件为Markdown格式，可用任何文本编辑器打开
2. 包含完整章节正文内容
3. 已通过完整创作流程（规划→创作→评审→检查）

---
发送人: 智云助手
发送时间: {current_time}
邮箱: {SENDER_EMAIL}
    """
    
    return email_content

def send_email_with_attachments(subject, content):
    """发送带附件的邮件"""
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文
        text_part = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 添加附件
        print("\n📎 正在添加附件...")
        if not attach_file(msg, CHAPTER_20_PATH):
            return False
        if not attach_file(msg, CHAPTER_21_PATH):
            return False
        
        # 连接SMTP服务器并发送
        print(f"\n🚀 正在连接SMTP服务器: {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"📤 正在发送邮件到: {RECEIVER_EMAIL}")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功!")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    print("=" * 50)
    print("《重生末世废土之生存法则》第20-21章正文发送")
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
    
    # 获取文件大小
    size_20 = os.path.getsize(CHAPTER_20_PATH)
    size_21 = os.path.getsize(CHAPTER_21_PATH)
    print(f"📏 文件大小: 第20章={size_20}字节, 第21章={size_21}字节")
    
    # 创建邮件内容
    print("\n📧 正在创建邮件内容...")
    email_content = create_email_content()
    
    # 发送邮件
    print("\n🚀 正在发送带附件的邮件...")
    subject = "《重生末世废土之生存法则》第20-21章正文文件"
    success = send_email_with_attachments(subject, email_content)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ 发送流程完成!")
        print(f"📤 已发送: 第20-21章正文文件")
        print(f"📎 附件: 2个Markdown文件")
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