#!/usr/bin/env python3
"""量化交易实时监控脚本"""
import ccxt
import json
import os
from datetime import datetime

# Bitget API
bitget = ccxt.bitget({
    'apiKey': 'bg_faa615ea273253ec1c62459bc8123396',
    'secret': 'bd47f550865e71eb52eddc2d493402b8a63f490b5e1d570722393de107b9db65',
    'password': 'yjllyzlyx521',
})

# 波动阈值 (百分比)
VOLATILE_THRESHOLD = 2.0  # 2%以上波动通知
CHECK_FILE = '/tmp/crypto_monitor.json'

def load_last_price():
    if os.path.exists(CHECK_FILE):
        with open(CHECK_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_current_price(prices):
    with open(CHECK_FILE, 'w') as f:
        json.dump(prices, f)

def check_volatility():
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
    prices = {}
    alerts = []
    
    last_prices = load_last_price()
    
    for symbol in symbols:
        try:
            ticker = bitget.fetch_ticker(symbol)
            current_price = ticker['last']
            prices[symbol] = current_price
            
            if symbol in last_prices:
                change_pct = abs((current_price - last_prices[symbol]) / last_prices[symbol] * 100)
                if change_pct >= VOLATILE_THRESHOLD:
                    direction = "📈 上涨" if current_price > last_prices[symbol] else "📉 下跌"
                    alerts.append(f"{symbol}: {direction} {change_pct:.2f}% (${last_prices[symbol]:,.2f} → ${current_price:,.2f})")
        except Exception as e:
            print(f"获取{symbol}失败: {e}")
    
    save_current_price(prices)
    return alerts

if __name__ == '__main__':
    alerts = check_volatility()
    if alerts:
        print("🚨 大波动提醒!")
        for alert in alerts:
            print(alert)
    else:
        print("✅ 价格平稳")
