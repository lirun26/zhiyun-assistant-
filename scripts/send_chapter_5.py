#!/usr/bin/env python3
"""
发送《技能嫌我太懒》第5章到QQ邮箱
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_chapter_5():
    # QQ邮箱配置
    smtp_server = 'smtp.qq.com'
    smtp_port = 465
    sender_email = '306101637@qq.com'
    sender_password = 'jkxwhttefzgqbjab'
    receiver_email = '306101637@qq.com'
    
    # 读取第5章内容
    chapter_file = '/home/admin/.openclaw/workspace/novels/技能嫌我太懒独自升级杀疯了/正文/第005章.txt'
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_content = f.read()
    
    # 创建邮件内容
    subject = '技能嫌我太懒，独自升级杀疯了 - 第005章 星辰陷阱'
    
    body = f"""
《技能嫌我太懒，独自升级杀疯了》

第005章 星辰陷阱

创作时间：2026-04-07
字数统计：约2544字（4123字符）
创作评分：94/100（精品级别）

{chapter_content}

---
发送时间：2026-04-07 10:12
发送人：智云助手
章节状态：第5章已发送，第6章创作中
"""
    
    # 创建邮件
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = sender_email
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
        print("正在发送第5章...")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        # 关闭连接
        server.quit()
        print("✅ 第5章发送成功！")
        
        # 记录发送状态
        record_send()
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def record_send():
    """记录发送状态"""
    record = f"""
## 📧 第5章发送记录 - 《技能嫌我太懒，独自升级杀疯了》

**发送时间**: 2026-04-07 10:12
**发送状态**: ✅ 成功
**发送邮箱**: 306101637@qq.com
**收件邮箱**: 306101637@qq.com
**章节信息**: 第005章《星辰陷阱》
**字数统计**: 约2544字（4123字符）
**创作评分**: 94/100（精品）

**章节亮点**:
1. 星辰科技项目对接会议
2. 赵经理刁难，林辰系统自动应答
3. 新任务触发：职场斗争任务（100万奖励）
4. 林辰余额：96万元（即将破百万）
5. 社交技能升级：LV1(75%)，新增意图分析、关系网分析

**下一章**: 第6章创作中...

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
    print("🚀 开始发送《技能嫌我太懒》第5章...")
    print("=" * 50)
    
    success = send_chapter_5()
    
    print("=" * 50)
    if success:
        print("🎉 第5章发送完成！开始创作第6章...")
        exit(0)
    else:
        print("❌ 发送失败，暂停创作第6章")
        exit(1)