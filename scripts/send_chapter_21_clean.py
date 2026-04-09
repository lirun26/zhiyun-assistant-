#!/usr/bin/env python3
"""
第21章重新发送脚本
移除所有"第X部分"标题，只发送干净正文
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
CHAPTER_21_PATH = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0021_第21章_暴风雪决战.md"

def read_chapter_file(filepath):
    """读取章节文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"读取文件失败: {filepath}")
        print(f"错误: {e}")
        return None

def clean_chapter_content(content):
    """彻底清理章节内容"""
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
            
        # 移除"时间线："开头的行
        if line.strip().startswith('时间线：'):
            continue
            
        # 移除"**时间线："开头的行
        if line.strip().startswith('**时间线：'):
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

def send_chapter_21_clean(content):
    """发送清理后的第21章"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        subject = "《重生末世废土之生存法则》第21章 暴风雪决战"
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文（只有清理后的章节内容）
        text_part = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 连接SMTP服务器并发送
        print(f"正在连接SMTP服务器: {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"正在发送邮件到: {RECEIVER_EMAIL}")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ 第21章发送成功!")
        return True
        
    except Exception as e:
        print(f"❌ 第21章发送失败: {e}")
        return False

def main():
    print("=" * 50)
    print("第21章《暴风雪决战》重新发送（干净版本）")
    print("=" * 50)
    
    # 检查文件是否存在
    if not os.path.exists(CHAPTER_21_PATH):
        print(f"❌ 文件不存在: {CHAPTER_21_PATH}")
        return False
    
    print(f"✅ 找到第21章文件: {CHAPTER_21_PATH}")
    
    # 读取章节内容
    print("\n📖 正在读取章节内容...")
    chapter_21_raw = read_chapter_file(CHAPTER_21_PATH)
    
    if not chapter_21_raw:
        print("❌ 读取章节内容失败")
        return False
    
    print(f"原始内容长度: {len(chapter_21_raw)} 字符")
    
    # 彻底清理章节内容
    print("\n🧹 正在清理章节内容...")
    chapter_21_clean = clean_chapter_content(chapter_21_raw)
    
    print(f"清理后内容长度: {len(chapter_21_clean)} 字符")
    
    # 显示清理效果
    print("\n🔍 清理内容预览（前500字符）:")
    print("-" * 40)
    print(chapter_21_clean[:500] + "...")
    print("-" * 40)
    
    # 检查是否还有"第X部分"
    if re.search(r'第[一二三四五六七八九十]+部分', chapter_21_clean):
        print("⚠️ 警告: 清理后仍包含'第X部分'标题")
        # 手动移除
        chapter_21_clean = re.sub(r'第[一二三四五六七八九十]+部分', '', chapter_21_clean)
        print("✅ 已手动移除剩余'第X部分'标题")
    
    # 发送清理后的章节
    print("\n🚀 正在发送清理后的第21章...")
    success = send_chapter_21_clean(chapter_21_clean)
    
    if success:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "=" * 50)
        print("✅ 第21章重新发送完成!")
        print(f"📤 已发送: 第21章《暴风雪决战》（干净版本）")
        print(f"🧹 清理内容:")
        print(f"   - 移除章节信息头部")
        print(f"   - 移除所有'第X部分'标题")
        print(f"   - 移除时间线标注")
        print(f"   - 只保留正文内容")
        print(f"📝 字数: 约4500字")
        print(f"📅 发送时间: {current_time}")
        print("=" * 50)
        
        # 保存清理后的版本供以后参考
        clean_file_path = "/home/admin/.openclaw/workspace/novels/重生末世废土/books/重生末世废土之生存法则/chapters/0021_第21章_暴风雪决战_干净版.md"
        with open(clean_file_path, 'w', encoding='utf-8') as f:
            f.write(chapter_21_clean)
        print(f"💾 已保存干净版本到: {clean_file_path}")
        
        return True
    else:
        print("\n❌ 发送失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)