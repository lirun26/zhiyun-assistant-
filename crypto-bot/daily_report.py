#!/usr/bin/env python3
"""每日加密货币行情汇报 - 带推送"""
import ccxt
import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from configenv import load_config

# 加载配置
config = load_config()

bitget = ccxt.bitget({
    'apiKey': config.get('apiKey'),
    'secret': config.get('secret'),
    'password': config.get('password'),
})

symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']

def get_price_change(symbol, days):
    """获取特定天数的涨跌幅"""
    try:
        ticker = bitget.fetch_ticker(symbol)
        current = ticker['last']
        
        ohlcv = bitget.fetch_ohlcv(symbol, '1d', limit=days)
        if ohlcv and len(ohlcv) >= days:
            old_price = ohlcv[0][1]
            change = (current - old_price) / old_price * 100
            return current, change
        return current, None
    except Exception as e:
        return None, None

def generate_message():
    """生成消息文本"""
    lines = ["📊 加密货币每日行情汇报", ""]
    
    for symbol in symbols:
        current, change_7d = get_price_change(symbol, 7)
        _, change_15d = get_price_change(symbol, 15)
        _, change_30d = get_price_change(symbol, 30)
        _, change_60d = get_price_change(symbol, 60)
        
        if current:
            emoji = "🟢" if change_30d and change_30d > 0 else "🔴"
            coin = symbol.replace('/USDT', '')
            lines.append(f"#### {emoji} {coin}")
            lines.append(f"- 当前: **${current:,.0f}**")
            lines.append(f"- 7天: {change_7d:+.2f}%" if change_7d else "- 7天: --")
            lines.append(f"- 15天: {change_15d:+.2f}%" if change_15d else "- 15天: --")
            lines.append(f"- 30天: {change_30d:+.2f}%" if change_30d else "- 30天: --")
            lines.append(f"- 60天: {change_60d:+.2f}%" if change_60d else "- 60天: --")
            lines.append("")
    
    lines.append("---")
    lines.append("*数据来源: Bitget*")
    
    return "\n".join(lines)

def send_to_dingtalk(message, target="6259271732847896"):
    """通过 OpenClaw 发送到钉钉"""
    try:
        # 使用 subprocess 调用 openclaw message send
        cmd = [
            "openclaw", "message", "send",
            "--channel", "dingtalk",
            "--message", message,
            "--target", target
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 钉钉消息发送成功")
            return True
        else:
            print(f"❌ 发送失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False

def main():
    print("📊 生成加密货币行情报告...")
    message = generate_message()
    
    # 打印到控制台
    print(message)
    print()
    
    # 发送到钉钉
    send_to_dingtalk(message)

if __name__ == '__main__':
    main()
