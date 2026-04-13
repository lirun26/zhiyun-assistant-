#!/usr/bin/env python3
# 测试网易邮箱发送

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 网易邮箱配置
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "lrun08@163.com"
SENDER_PASSWORD = "TMwqKZ2QdxXj2h3W"
RECEIVER_EMAIL = "lrun08@163.com"

def send_test_email():
    """发送测试邮件"""
    print("📧 发送测试邮件到网易邮箱...")
    
    # 创建邮件内容
    subject = "测试邮件 - 第17章内容"
    body = """老大，

这是测试邮件，检查网易邮箱是否能正常接收。

如果收到此邮件，说明邮件发送功能正常。

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
        print(f"📤 发送邮件到 {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 测试邮件发送成功！")
        print("请检查网易邮箱是否收到测试邮件。")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 网易邮箱发送测试 ===")
    print("")
    send_test_email()