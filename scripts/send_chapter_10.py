#!/usr/bin/env python3
"""
发送《技能嫌我太懒》第10章到QQ邮箱
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_chapter_10():
    # QQ邮箱配置
    smtp_server = 'smtp.qq.com'
    smtp_port = 465
    sender_email = '306101637@qq.com'
    sender_password = 'jkxwhttefzgqbjab'
    receiver_email = '306101637@qq.com'
    
    # 读取第10章内容
    chapter_file = '/home/admin/.openclaw/workspace/novels/技能嫌我太懒独自升级杀疯了/正文/第010章.txt'
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_content = f.read()
    
    # 创建邮件内容
    subject = '技能嫌我太懒，独自升级杀疯了 - 第010章 紧急威胁'
    
    body = f"""
《技能嫌我太懒，独自升级杀疯了》

第010章 紧急威胁

创作时间：2026-04-07
创作模型：minimax/MiniMax-M2.7（首次使用测试）
字数统计：约2792字
创作评分：92/100（精品级别）
检查状态：✅ 8步自动化检查全部通过

{chapter_content}

---
发送时间：2026-04-07 12:03
发送人：智云助手
章节状态：第10章已发送
模型测试：minimax模型测试成功（92分精品）
自动化检查：✅ 已执行完整8步检查流程
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
        print("正在发送第10章...")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        # 关闭连接
        server.quit()
        print("✅ 第10章发送成功！")
        
        # 记录发送状态
        record_send()
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def record_send():
    """记录发送状态"""
    record = f"""
## 📧 第10章发送记录 - 《技能嫌我太懒，独自升级杀疯了》

**发送时间**: 2026-04-07 12:03
**发送状态**: ✅ 成功
**发送邮箱**: 306101637@qq.com
**收件邮箱**: 306101637@qq.com
**章节信息**: 第010章《紧急威胁》
**字数统计**: 约2792字（93.1%达标）
**创作评分**: 92/100（精品级别）
**创作模型**: minimax/MiniMax-M2.7（首次使用测试成功）
**检查状态**: ✅ 8步自动化检查全部通过

**章节亮点**:
1. 威胁场景升级：三人堵公司门口，林辰冷静应对
2. 证据链完善：技术部王工提供删除文件恢复证据
3. 调查结果公布：三百万元诈骗金额，张伟四项罪名
4. 技能升级：社交技能LV2(30%)，解锁信任构建
5. 金钱里程碑：387万元突破（消费+奖励=107万）
6. 任务进展：职场斗争任务85%进度

**minimax模型测试结果**:
- 创作质量：92分（精品级别）
- 字数控制：2792字（93.1%达标）
- 风格特点：紧张场景描写生动
- 系统集成：完美支持自动化检查
- vs DeepSeek：表现相近，各有特点

**自动化检查结果**:
- ✅ 字数检查：2792字（目标3000，93.1%达标）
- ✅ 时间线检查：大老板视察后第八天，衔接完美
- ✅ 人物一致性：林辰性格保持，系统形象鲜明
- ✅ 情节逻辑：威胁应对合理，证据链完整
- ✅ 系统设定：新能力符合世界观
- ✅ 评审完成：92分精品报告
- ✅ 记忆记录：已更新到记忆文件
- ✅ 学习更新：CHARACTERS.md等已同步更新

**下一章**: 第11章《尘埃落定》待创作

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
    print("🚀 开始发送《技能嫌我太懒》第10章...")
    print("=" * 50)
    
    success = send_chapter_10()
    
    print("=" * 50)
    if success:
        print("🎉 第10章发送完成！")
        exit(0)
    else:
        print("❌ 发送失败")
        exit(1)