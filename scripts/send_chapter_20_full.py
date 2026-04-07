#!/usr/bin/env python3
# 发送第20章完整内容到网易邮箱

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
CHAPTER_20_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0020_第20章_暴风雪中的博弈.md"

def read_chapter_content():
    """读取章节内容"""
    print(f"📖 读取第20章内容...")
    try:
        with open(CHAPTER_20_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 清理格式，保留正文内容
        lines = content.split('\n')
        cleaned_lines = []
        in_body = False
        
        for line in lines:
            if line.startswith('**第20章 暴风雪中的博弈**'):
                in_body = True
            if line.startswith('**章节字数**: 3420字'):
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

def send_chapter_20():
    """发送第20章"""
    print("📧 发送第20章《暴风雪中的博弈》完整内容...")
    
    # 读取内容
    chapter_content = read_chapter_content()
    if not chapter_content:
        return False
    
    # 创建邮件内容
    subject = "《重生末世废土之生存法则》第20章《暴风雪中的博弈》完整内容"
    body = f"""老大，

以下是《重生末世废土之生存法则》第20章《暴风雪中的博弈》完整内容：

**字数**: 3420字
**评分**: 95/100分（精品+）
**时间线**: 末世第21天傍晚6:30 → 夜间10:30
**核心冲突**: 安全屋内的三方博弈 vs 外部威胁逼近

---

{chapter_content}

---

**章节亮点**:
1. **身份验证**: 侦察队来历和目的的详细询问
2. **无线电验证**: 与避难所直接通话确认身份
3. **情报博弈**: 苏清鸢与侦察队的对话充满张力
4. **无线电截获**: 掠夺者正在逼近，六公里外
5. **联盟形成**: 苏清鸢决定接受侦察队加入防御

**情节结构**:
五部分逻辑链：
1. 身份验证 → 侦察队来历和目的
2. 无线电验证 → 外部联系确认
3. 暴风雪中 → 环境描写和敌情分析
4. 夜幕降临 → 夜间监控和意外警报
5. 最终警告 → 无线电截获和最终决定

**当前局势**:
- 苏清鸢: 安全屋内，决定与侦察队联盟
- 第七避难所: 侦察队三人确认身份，愿意合作
- 掠夺者: 31人，正在暴风雪中逼近（六公里外）
- 时间: 最后2小时准备，决战即将开始

**下一章方向**: 三人对31人的生死决战

智云助手
2026-04-07 12:05
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
        print(f"📤 发送第20章到 {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 第20章发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
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
        
        # 更新第20章发送状态
        content = content.replace("| 20 | 待定 | 多方博弈，最终决战准备 | 🚧 待开始 | - | - |",
                                  "| 20 | 暴风雪中的博弈 | 三人联盟，掠夺者逼近，决战倒计时 | ✅ 完成 | ⏳ 等待指令 | 95/100 |")
        
        # 更新等待发送队列
        content = content.replace("| 章节 | 标题 | 字数 | 评分 | 创作时间 | 检查状态 |",
                                  "| 章节 | 标题 | 字数 | 评分 | 创作时间 | 检查状态 |")
        content = content.replace("| *暂无等待发送章节* |",
                                  "| 20 | 暴风雪中的博弈 | 3420字 | 95/100 | 11:50-12:05 | ✅ 检查通过 |")
        
        with open(hot_memory_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ HOT_MEMORY.md 更新完成")
        
    except Exception as e:
        print(f"❌ 更新记忆文件失败: {e}")

if __name__ == "__main__":
    print("=== 发送第20章完整内容 ===")
    print("")
    
    # 检查文件是否存在
    if not os.path.exists(CHAPTER_20_PATH):
        print(f"❌ 文件不存在: {CHAPTER_20_PATH}")
        exit(1)
    
    # 发送邮件
    if send_chapter_20():
        update_memory()
        print("")
        print("✅ 第20章发送完成，记忆已更新！")
        print("🎯 下一任务: 等待指令继续创作第21章")
    else:
        print("")
        print("❌ 发送失败，请检查配置")