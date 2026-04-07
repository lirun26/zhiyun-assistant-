#!/usr/bin/env python3
# 发送第19章完整内容到网易邮箱

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
CHAPTER_19_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0019_第19章_暴风雪对峙.md"

def read_chapter_content():
    """读取章节内容"""
    print(f"📖 读取第19章内容...")
    try:
        with open(CHAPTER_19_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 清理格式，保留正文内容
        lines = content.split('\n')
        cleaned_lines = []
        in_body = False
        
        for line in lines:
            if line.startswith('**第19章 暴风雪对峙**'):
                in_body = True
            if line.startswith('**章节字数**: 3280字'):
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

def send_chapter_19():
    """发送第19章"""
    print("📧 发送第19章《暴风雪对峙》完整内容...")
    
    # 读取内容
    chapter_content = read_chapter_content()
    if not chapter_content:
        return False
    
    # 创建邮件内容
    subject = "《重生末世废土之生存法则》第19章《暴风雪对峙》完整内容"
    body = f"""老大，

以下是《重生末世废土之生存法则》第19章《暴风雪对峙》完整内容：

**字数**: 3280字
**评分**: 96/100分（精品+）
**时间线**: 末世第21天上午9:00 → 傍晚6:00
**核心冲突**: 暴风雪生存 vs 掠夺者报复倒计时

---

{chapter_content}

---

**章节亮点**:
1. **环境即敌人**: "暴风雪不是背景，是敌人" - 自然环境提升为主动威胁
2. **新势力引入**: 第七避难所侦察队三人出现（林雨、陈刚、赵峰）
3. **心理煎熬**: 通过时钟、计算、回忆表现等待决战的压力
4. **理性决策**: 作战计划A/B/C分析，体现主角末世生存逻辑
5. **细节真实**: 防寒维护、武器检查、物资盘点增强可信度

**情节结构**:
1. 暴风雪降临 → 生存威胁
2. 无线电尝试 → 外部联系
3. 防御升级 → 应对措施
4. 心理煎熬 → 内在冲突
5. 意外发现 → 新变量引入
6. 最终准备 → 冲突升级

**当前局势**:
- 苏清鸢: 安全屋内，武器就位，收留侦察队但严密监控
- 掠夺者: 31人，8公里外，24小时报复倒计时（剩余约20小时）
- 第七避难所: 侦察队三人出现，身份待验证
- 环境: 暴风雪持续，-35°C，能见度0，剩余约18小时

**下一章方向**: 暴风雪中的多方博弈，侦察队身份验证，掠夺者最终进攻准备

智云助手
2026-04-07 10:38
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
        print(f"📤 发送第19章到 {RECEIVER_EMAIL}...")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 第19章发送成功！")
        print("请检查网易邮箱是否收到完整内容。")
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
        
        # 更新第19章发送状态
        content = content.replace("| 19 | 暴风雪对峙 | 极端天气应对，第七避难所侦察队出现 | ✅ 完成 | ⏳ 等待指令 | 96/100 |",
                                  "| 19 | 暴风雪对峙 | 极端天气应对，第七避难所侦察队出现 | ✅ 完成 | ✅ 已发送 | 96/100 |")
        
        # 清空等待发送队列
        content = content.replace("### 📋 **等待发送队列**\n| 章节 | 标题 | 字数 | 评分 | 创作时间 | 检查状态 |\n|:---|:---|:---|:---|:---|:---|\n| 19 | 暴风雪对峙 | 3280字 | 96/100 | 10:30-10:45 | ✅ 检查通过 |",
                                  "### 📋 **等待发送队列**\n| 章节 | 标题 | 字数 | 评分 | 创作时间 | 检查状态 |\n|:---|:---|:---|:---|:---|:---|\n| *暂无等待发送章节* |")
        
        with open(hot_memory_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ HOT_MEMORY.md 更新完成")
        
    except Exception as e:
        print(f"❌ 更新记忆文件失败: {e}")

if __name__ == "__main__":
    print("=== 发送第19章完整内容 ===")
    print("")
    
    # 检查文件是否存在
    if not os.path.exists(CHAPTER_19_PATH):
        print(f"❌ 文件不存在: {CHAPTER_19_PATH}")
        exit(1)
    
    # 发送邮件
    if send_chapter_19():
        # 更新记忆文件
        update_memory()
        print("")
        print("✅ 第19章发送完成，记忆已更新！")
        print("🎯 下一任务: 等待指令继续创作第20章")
    else:
        print("")
        print("❌ 发送失败，请检查配置")