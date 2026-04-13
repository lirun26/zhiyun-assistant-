#!/usr/bin/env python3
"""
火币网格交易机器人 - 后台运行版
"""
import ccxt
import time
import json
from datetime import datetime

# 配置
SYMBOL = 'BTC/USDT'
INITIAL_USDT = 10000
GRID_SPREAD = 0.05  # 5%波动范围
GRID_COUNT = 10      # 10个网格
BUY_AMOUNT = 0.001   # 每次买0.001 BTC
CHECK_INTERVAL = 30  # 每30秒检查一次
LOG_FILE = '/home/admin/.openclaw/workspace/crypto-bot/grid_trades.log'

# API配置
API_KEY = 'dbuqg6hkte-2ecd8a42-f451fc26-c0bac'
SECRET_KEY = '1338cef7-7798fc08-b996290f-71653'

class GridBot:
    def __init__(self):
        self.exchange = ccxt.huobi({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,
        })
        self.balance_usdt = INITIAL_USDT
        self.balance_btc = 0
        self.grids = []
        self.trades = []
        
    def setup_grids(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        
        lowest = price * (1 - GRID_SPREAD/2)
        highest = price * (1 + GRID_SPREAD/2)
        step = (highest - lowest) / GRID_COUNT
        
        self.grids = []
        for i in range(GRID_COUNT):
            self.grids.append({
                'price': lowest + step * i,
                'buy_price': None,
                'sold': False
            })
        
        msg = f"[{datetime.now()}] 网格设置: {lowest:.2f} - {highest:.2f} USDT"
        print(msg)
        self.log(msg)
        
    def check_and_trade(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        
        total_value = self.balance_usdt + self.balance_btc * price
        profit = total_value - INITIAL_USDT
        profit_pct = (profit / INITIAL_USDT) * 100
        
        msg = f"[{datetime.now()}] 价格: ${price:,.0f} | USDT: {self.balance_usdt:.2f} | BTC: {self.balance_btc:.6f} | 收益: {profit:+.2f} ({profit_pct:+.2f}%)"
        print(msg)
        self.log(msg)
        
        # 买入逻辑
        for i, grid in enumerate(self.grids):
            if price <= grid['price'] and not grid['buy_price']:
                cost = price * BUY_AMOUNT
                if self.balance_usdt >= cost:
                    self.balance_usdt -= cost
                    self.balance_btc += BUY_AMOUNT
                    grid['buy_price'] = price
                    buy_msg = f"  🟢 买入 {BUY_AMOUNT} BTC @ ${price:.2f}"
                    print(buy_msg)
                    self.log(buy_msg)
        
        # 卖出逻辑  
        for i, grid in enumerate(self.grids):
            if grid['buy_price'] and not grid['sold']:
                # 上涨1%卖出
                if price >= grid['buy_price'] * 1.01:
                    revenue = price * self.balance_btc
                    self.balance_usdt += revenue
                    profit = revenue - (grid['buy_price'] * self.balance_btc)
                    self.balance_btc = 0
                    grid['sold'] = True
                    sell_msg = f"  🔴 卖出 {self.balance_btc:.6f} BTC @ ${price:.2f} | 利润: ${profit:.2f}"
                    print(sell_msg)
                    self.log(sell_msg)
                    # 重置网格
                    grid['buy_price'] = None
                    grid['sold'] = False
        
    def log(self, msg):
        with open(LOG_FILE, 'a') as f:
            f.write(msg + '\n')
    
    def run(self):
        print("="*60)
        print("🤖 火币网格交易机器人 - 后台运行")
        print("="*60)
        self.setup_grids()
        print("开始监控... 按 Ctrl+C 停止")
        print("="*60)
        
        try:
            while True:
                self.check_and_trade()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n机器人已停止")
            total = self.balance_usdt + self.balance_btc * self.exchange.fetch_ticker(SYMBOL)['last']
            print(f"最终资产: ${total:,.2f}")

if __name__ == '__main__':
    bot = GridBot()
    bot.run()
