#!/usr/bin/env python3
"""
简单发送小说章节 - 修复QQ邮箱格式问题
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

def send_simple():
    # QQ邮箱配置
    smtp_server = 'smtp.qq.com'
    smtp_port = 465
    sender_email = '306101637@qq.com'
    sender_password = 'jkxwhttefzgqbjab'
    receiver_email = '306101637@qq.com'
    
    # 读取章节内容
    chapter_file = '/home/admin/.openclaw/workspace/novels/技能嫌我太懒独自升级杀疯了/正文/第004章.txt'
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_content = f.read()
    
    # 创建邮件内容
    subject = '技能嫌我太懒，独自升级 - 第004章 系统新功能：社交技能觉醒'
    
    # 简化邮件正文
    body = f"""
《技能嫌我太懒，独自升级》

第004章 系统新功能：社交技能觉醒

创作时间：2026-04-07
字数统计：约2544字（5088字符）

{chapter_content}

---
发送时间：2026-04-07 10:00
发送人：智云助手
"""
    
    # 创建邮件（简化格式）
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = sender_email  # 简化发件人格式
    msg['To'] = receiver_email
    msg['Subject'] = Header(subject, 'utf-8')
    
    try:
        # 连接SMTP服务器
        print("正在连接QQ邮箱SMTP服务器...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        # 登录
        print("正在登录邮箱...")
        server.login(sender_email, sender_password)
        
        # 发送邮件
        print("正在发送邮件...")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        # 关闭连接
        server.quit()
        print("✅ 邮件发送成功！")
        
        # 记录发送状态
        record_send()
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def record_send():
    """记录发送状态"""
    record = f"""
## 📧 QQ邮箱发送记录 - 《技能嫌我太懒，独自升级》第4章

**发送时间**: 2026-04-07 10:00
**发送状态**: ✅ 成功
**发送邮箱**: 306101637@qq.com
**收件邮箱**: 306101637@qq.com
**章节信息**: 第004章《系统新功能：社交技能觉醒》
**字数统计**: 约2544字

**发送内容**: 完整章节正文

**备注**: 使用简化格式发送，避免QQ邮箱格式限制

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
    print("🚀 开始发送小说章节（简化版）...")
    print("=" * 50)
    
    success = send_simple()
    
    print("=" * 50)
    if success:
        print("🎉 发送流程完成！")
        exit(0)
    else:
        print("❌ 发送流程失败！")
        exit(1)