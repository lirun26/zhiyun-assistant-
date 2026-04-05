#!/usr/bin/env python3
"""
火币智能网格交易机器人 V3 - 优化版
"""
import ccxt
import time
from datetime import datetime

# ===== 可调参数 =====
SYMBOL = 'BTC/USDT'
INITIAL_USDT = 10000

# 网格参数 - 改进版
GRID_SPREAD = 0.08    # 8%波动范围
GRID_COUNT = 16       # 16个网格
BUY_AMOUNT = 0.0005   # 每次买0.0005 BTC
TAKE_PROFIT = 0.003   # 盈利0.3%就卖出
STOP_LOSS = -0.02     # 亏损2%止损

# 监控间隔
CHECK_INTERVAL = 60    

# API
API_KEY = 'dbuqg6hkte-2ecd8a42-f451fc26-c0bac'
SECRET_KEY = '1338cef7-7798fc08-b996290f-71653'

LOG_FILE = '/tmp/grid_bot_v3.log'

class SmartGridBotV3:
    def __init__(self):
        self.exchange = ccxt.huobi({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,
        })
        self.balance_usdt = float(INITIAL_USDT)
        self.balance_btc = 0.0
        self.positions = []  # 持仓记录
        self.total_trades = 0
        self.total_profit = 0
        self.start_price = 0
        
    def init_grids(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        self.start_price = price
        
        # 创建不同价位的网格
        lowest = price * (1 - GRID_SPREAD/2)
        highest = price * (1 + GRID_SPREAD/2)
        step = (highest - lowest) / GRID_COUNT
        
        self.grids = []
        for i in range(GRID_COUNT):
            self.grids.append({
                'price': lowest + step * i,
                'filled': False
            })
        
        self.log(f"✅ 网格初始化: ${lowest:,.0f} - ${highest:,.0f}")
        self.log(f"   网格数: {GRID_COUNT}, 步长: ${step:.2f}")
        
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {msg}\n")
    
    def get_status(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        
        total_value = self.balance_usdt + self.balance_btc * price
        profit = total_value - INITIAL_USDT
        profit_pct = (profit / INITIAL_USDT) * 100
        
        return {
            'price': price,
            'value': total_value,
            'profit': profit,
            'profit_pct': profit_pct,
            'positions': len(self.positions)
        }
    
    def check_trades(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        status = self.get_status()
        
        # 检查止损
        if status['profit_pct'] <= STOP_LOSS * 100:
            if self.balance_btc > 0:
                self.balance_usdt += self.balance_btc * price * 0.999
                self.log(f"🛑 止损! 亏损 {status['profit_pct']:.2f}%")
                self.balance_btc = 0
                self.positions = []
        
        # 买入：每个网格只买一次
        for grid in self.grids:
            if not grid['filled']:
                if price <= grid['price']:
                    cost = price * BUY_AMOUNT
                    if self.balance_usdt >= cost:
                        self.balance_usdt -= cost
                        self.balance_btc += BUY_AMOUNT
                        self.positions.append({
                            'buy_price': price,
                            'amount': BUY_AMOUNT,
                            'buy_time': datetime.now().strftime("%H:%M:%S")
                        })
                        grid['filled'] = True
                        self.total_trades += 1
                        self.log(f"  🟢 买入 {BUY_AMOUNT} BTC @ ${price:,.0f}")
        
        # 卖出：盈利0.3%就卖
        for pos in self.positions[:]:
            if price >= pos['buy_price'] * (1 + TAKE_PROFIT):
                revenue = pos['amount'] * price * 0.999
                profit = revenue - (pos['buy_price'] * pos['amount'])
                self.balance_usdt += revenue
                self.balance_btc -= pos['amount']
                self.total_profit += profit
                self.total_trades += 1
                self.positions.remove(pos)
                self.log(f"  🔴 卖出 {pos['amount']} BTC @ ${price:,.0f} | 利润: ${profit:.2f}")
        
        # 状态输出
        self.log(f"📊 ${price:,.0f} | USDT: {self.balance_usdt:.2f} | "
                f"BTC: {self.balance_btc:.6f} | 持仓: {len(self.positions)}笔 | "
                f"总价值: ${status['value']:,.2f} ({status['profit_pct']:+.2f}%)")
    
    def run(self):
        print("="*60)
        self.log("🤖 火币网格机器人 V3 启动")
        self.init_grids()
        print("="*60)
        
        try:
            while True:
                self.check_trades()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            status = self.get_status()
            self.log(f"\n⏹️ 停止 | 最终: ${status['value']:,.2f} | 交易: {self.total_trades}次")

if __name__ == '__main__':
    bot = SmartGridBotV3()
    bot.run()
