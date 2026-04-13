#!/usr/bin/env python3
"""
模拟交易机器人 - 网格策略
支持模拟盘测试
"""

import ccxt
import time
import json
from datetime import datetime

# 配置
SYMBOL = 'BTC/USDT'  # 交易对
GRID_COUNT = 10      # 网格数量
GRID_SPREAD = 0.02   # 价格区间 (2%)
INITIAL_BALANCE = {'USDT': 10000, 'BTC': 0}  # 初始资金
MODE = 'simulate'    # simulate = 模拟盘, live = 实盘

class GridTradingBot:
    def __init__(self, exchange_id='binance', symbol=SYMBOL, simulate=True):
        self.symbol = symbol
        self.grids = []
        self.orders = []
        self.balance = INITIAL_BALANCE.copy()
        self.simulate = simulate
        
        if simulate:
            # 模拟盘
            if exchange_id == 'binance':
                self.exchange = ccxt.binance({
                    'enableRateLimit': True,
                    'options': {'defaultType': 'spot'}
                })
                # 尝试用测试网
                try:
                    self.exchange.set_sandbox_mode(True)
                    print("✅ 启用 Binance 测试网模式")
                except:
                    print("⚠️ 测试网不可用，使用模拟数据")
        else:
            # 实盘
            self.exchange = ccxt.okx({})  # 需要配置 API
            
    def get_current_price(self):
        """获取当前价格"""
        if self.simulate:
            try:
                ticker = self.exchange.fetch_ticker(self.symbol)
                return ticker['last']
            except:
                # 模拟价格
                return 71000
        else:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return ticker['last']
    
    def setup_grid(self, price, spread=GRID_SPREAD, count=GRID_COUNT):
        """设置网格"""
        lowest = price * (1 - spread / 2)
        highest = price * (1 + spread / 2)
        step = (highest - lowest) / count
        
        self.grids = []
        for i in range(count):
            grid_price = lowest + step * i
            self.grids.append({
                'price': grid_price,
                'buy_order': None,
                'sell_order': None,
                'filled': False
            })
        print(f"✅ 网格设置完成: {lowest:.2f} - {highest:.2f} USDT")
        
    def place_order(self, side, price, amount):
        """下单（模拟）"""
        order = {
            'id': f"sim_{int(time.time())}_{side}",
            'side': side,
            'price': price,
            'amount': amount,
            'status': 'closed',
            'timestamp': time.time() * 1000
        }
        
        # 更新余额
        if side == 'buy':
            cost = price * amount
            self.balance['USDT'] -= cost
            self.balance['BTC'] += amount
            print(f"🟢 买入: {amount} BTC @ {price:.2f} USDT")
        else:
            revenue = price * amount
            self.balance['USDT'] += revenue
            self.balance['BTC'] -= amount
            print(f"🔴 卖出: {amount} BTC @ {price:.2f} USDT")
            
        return order
    
    def check_grid_orders(self, current_price):
        """检查网格触发"""
        for grid in self.grids:
            if grid['filled']:
                continue
                
            # 买入触发
            if grid['price'] >= current_price * 0.998 and not grid['buy_order']:
                amount = 0.001  # 每次买 0.001 BTC
                if self.balance['USDT'] >= grid['price'] * amount:
                    grid['buy_order'] = self.place_order('buy', grid['price'], amount)
                    
            # 卖出触发  
            elif grid['price'] <= current_price * 1.002 and grid['buy_order'] and not grid['sell_order']:
                amount = 0.001
                if self.balance['BTC'] >= amount:
                    grid['sell_order'] = self.place_order('sell', grid['price'], amount)
                    grid['filled'] = True
    
    def get_balance_value(self, current_price):
        """计算总资产价值"""
        total_usdt = self.balance['USDT'] + self.balance['BTC'] * current_price
        return total_usdt
    
    def print_balance(self, current_price):
        """打印当前余额"""
        total = self.get_balance_value(current_price)
        print(f"💰 余额: {self.balance['USDT']:.2f} USDT + {self.balance['BTC']:.6f} BTC")
        print(f"📊 总价值: {total:.2f} USDT")
        
    def run(self, iterations=10, interval=5):
        """运行机器人"""
        print("=" * 50)
        print("🤖 网格交易机器人启动")
        print(f"📌 交易对: {self.symbol}")
        print(f"💵 初始资金: {INITIAL_BALANCE['USDT']} USDT")
        print("=" * 50)
        
        # 初始化网格
        current_price = self.get_current_price()
        self.setup_grid(current_price)
        
        # 主循环
        for i in range(iterations):
            current_price = self.get_current_price()
            print(f"\n--- 第 {i+1}/{iterations} 轮 | 价格: ${current_price:,.2f} ---")
            
            self.check_grid_orders(current_price)
            self.print_balance(current_price)
            
            if i < iterations - 1:
                time.sleep(interval)
                
        print("\n" + "=" * 50)
        print("🏁 模拟交易结束")
        final_price = self.get_current_price()
        self.print_balance(final_price)
        
        # 计算收益
        initial_value = INITIAL_BALANCE['USDT']
        final_value = self.get_balance_value(final_price)
        profit = final_value - initial_value
        profit_pct = (profit / initial_value) * 100
        
        print(f"\n📈 总收益: {profit:.2f} USDT ({profit_pct:+.2f}%)")
        print("=" * 50)

if __name__ == '__main__':
    # 运行模拟交易
    bot = GridTradingBot(symbol='BTC/USDT', simulate=True)
    bot.run(iterations=20, interval=3)
