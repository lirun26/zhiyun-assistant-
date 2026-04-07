#!/usr/bin/env python3
# 发送第17-18章邮件脚本

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import sys

# 邮件配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "lrun08@163.com"
SENDER_PASSWORD = "TMwqKZ2QdxXj2h3W"
RECEIVER_EMAIL = "lrun08@163.com"

# 文件路径
BASE_DIR = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters"
CHAPTER_17 = os.path.join(BASE_DIR, "第17章_报复.md")
CHAPTER_18 = os.path.join(BASE_DIR, "0018_第18章_审讯.md")
REVIEW_17 = os.path.join(BASE_DIR, "第17章_报复_评审.md")
REVIEW_18 = os.path.join(BASE_DIR, "第18章_审讯_评审.md")

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败 {filepath}: {e}")
        return None

def create_email():
    """创建邮件"""
    # 读取章节内容
    ch17_content = read_file(CHAPTER_17)
    ch18_content = read_file(CHAPTER_18)
    review17_content = read_file(REVIEW_17)
    review18_content = read_file(REVIEW_18)
    
    if not all([ch17_content, ch18_content, review17_content, review18_content]):
        print("❌ 有文件读取失败，停止发送")
        return None
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['Subject'] = '《重生末世废土之生存法则》第17-18章'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    # 邮件正文
    body = """老大，

以下是《重生末世废土之生存法则》第17-18章内容：

---

**第17章《报复》**
字数: 3200字
评分: 94/100分（精品）
时间线: 末世第20天
核心内容: 掠夺者报复威胁，苏清鸢加强防御，地下管道突袭

**第18章《审讯》**
字数: 3287字
评分: 98/100分（精品+）
时间线: 末世第21天
核心内容: 俘虏审讯，道德抉择，暴风雪预警，第七避难所发现

---

详细内容见附件。

智云助手
2026-04-07 09:58
"""
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    files = [
        (CHAPTER_17, "第17章_报复.md"),
        (CHAPTER_18, "第18章_审讯.md"),
        (REVIEW_17, "第17章评审报告.md"),
        (REVIEW_18, "第18章评审报告.md")
    ]
    
    for filepath, filename in files:
        try:
            with open(filepath, 'rb') as f:
                part = MIMEApplication(f.read(), Name=filename)
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)
                print(f"✅ 添加附件: {filename}")
        except Exception as e:
            print(f"❌ 添加附件失败 {filename}: {e}")
    
    return msg

def send_email():
    """发送邮件"""
    print("📧 开始发送第17-18章邮件...")
    
    # 创建邮件
    msg = create_email()
    if not msg:
        return False
    
    try:
        # 连接SMTP服务器
        print(f"🔗 连接SMTP服务器 {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # 发送邮件
        print(f"📤 发送邮件到 {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 发送第17-18章邮件 ===")
    print("")
    
    # 检查文件是否存在
    files_to_check = [CHAPTER_17, CHAPTER_18, REVIEW_17, REVIEW_18]
    for filepath in files_to_check:
        if os.path.exists(filepath):
            print(f"✅ 文件存在: {os.path.basename(filepath)}")
        else:
            print(f"❌ 文件不存在: {filepath}")
            return False
    
    print("")
    
    # 发送邮件
    if send_email():
        # 更新记忆文件
        update_memory()
        return True
    else:
        return False

def update_memory():
    """更新记忆文件，标记已发送"""
    print("")
    print("🔄 更新记忆文件...")
    
    # 更新HOT_MEMORY.md
    hot_memory_path = "/home/admin/.openclaw/workspace/memory/hot/HOT_MEMORY.md"
    try:
        with open(hot_memory_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新第17-18章发送状态
        content = content.replace("| 17 | 报复 | 掠夺者报复，地下管道突袭，六人被俘 | ✅ 完成 | ✅ 已发送 | 94/100 |", 
                                  "| 17 | 报复 | 掠夺者报复，地下管道突袭，六人被俘 | ✅ 完成 | ✅ 已发送 | 94/100 |")
        content = content.replace("| 18 | 审讯 | 审讯俘虏，道德抉择，暴风雪预警 | ✅ 完成 | ⏳ 等待指令 | 98/100 |",
                                  "| 18 | 审讯 | 审讯俘虏，道德抉择，暴风雪预警 | ✅ 完成 | ✅ 已发送 | 98/100 |")
        
        with open(hot_memory_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ HOT_MEMORY.md 更新完成")
        
    except Exception as e:
        print(f"❌ 更新记忆文件失败: {e}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)