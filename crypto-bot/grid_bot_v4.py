#!/usr/bin/env python3
"""
火币智能网格交易机器人 V4 - 修复版
"""
import ccxt
import time
from datetime import datetime

# ===== 可调参数 =====
SYMBOL = 'BTC/USDT'
INITIAL_USDT = 10000

# 网格参数
GRID_SPREAD = 0.06    # 6%波动范围
GRID_COUNT = 12       # 12个网格
BUY_AMOUNT = 0.0005   # 每次买0.0005 BTC
TAKE_PROFIT = 0.003   # 盈利0.3%就卖出
STOP_LOSS = -0.02     # 亏损2%止损

CHECK_INTERVAL = 60    

API_KEY = 'dbuqg6hkte-2ecd8a42-f451fc26-c0bac'
SECRET_KEY = '1338cef7-7798fc08-b996290f-71653'

LOG_FILE = '/tmp/grid_bot_v4.log'

class SmartGridBotV4:
    def __init__(self):
        self.exchange = ccxt.huobi({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,
        })
        self.balance_usdt = float(INITIAL_USDT)
        self.balance_btc = 0.0
        self.positions = []
        self.total_trades = 0
        self.total_profit = 0
        self.start_price = 0
        self.initial_grids = []
        
    def init_grids(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        self.start_price = price
        
        # 创建网格 - 价格从低到高
        lowest = price * (1 - GRID_SPREAD/2)
        highest = price * (1 + GRID_SPREAD/2)
        step = (highest - lowest) / GRID_COUNT
        
        self.grids = []
        self.initial_grids = []
        for i in range(GRID_COUNT):
            grid_price = lowest + step * i
            self.grids.append({
                'price': grid_price,
                'filled': False
            })
            self.initial_grids.append(grid_price)
        
        self.log(f"✅ 网格设置: ${lowest:,.0f} - ${highest:,.0f}")
        self.log(f"   当前价格: ${price:,.0f}")
        self.log(f"   网格: {[f'${g:,.0f}' for g in self.initial_grids]}")
        
    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def get_status(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        total = self.balance_usdt + self.balance_btc * price
        profit = total - INITIAL_USDT
        return price, total, profit
    
    def check_trades(self):
        price, total, profit = self.get_status()
        profit_pct = (profit / INITIAL_USDT) * 100
        
        # 止损
        if profit_pct <= STOP_LOSS * 100 and self.balance_btc > 0:
            self.balance_usdt += self.balance_btc * price * 0.999
            self.log(f"🛑 止损! {profit_pct:.2f}%")
            self.balance_btc = 0
            self.positions = []
            # 重置网格
            for g in self.grids:
                g['filled'] = False
        
        # 买入 - 价格跌到网格时买入
        # 从低到高检查，当价格 <= 网格价格且未买入时买入
        for i, grid in enumerate(self.grids):
            if not grid['filled']:
                # 当价格跌破这个网格时买入
                if price <= grid['price']:
                    cost = price * BUY_AMOUNT
                    if self.balance_usdt >= cost:
                        self.balance_usdt -= cost
                        self.balance_btc += BUY_AMOUNT
                        self.positions.append({
                            'buy_price': price,
                            'amount': BUY_AMOUNT,
                            'grid_price': grid['price']
                        })
                        grid['filled'] = True
                        self.total_trades += 1
                        self.log(f"  🟢 买入 {BUY_AMOUNT} BTC @ ${price:,.0f} (网格${grid['price']:,.0f})")
        
        # 卖出 - 盈利0.3%就卖
        for pos in self.positions[:]:
            if price >= pos['buy_price'] * (1 + TAKE_PROFIT):
                revenue = pos['amount'] * price * 0.999
                p = revenue - pos['buy_price'] * pos['amount']
                self.balance_usdt += revenue
                self.balance_btc -= pos['amount']
                self.total_profit += p
                self.total_trades += 1
                self.positions.remove(pos)
                self.log(f"  🔴 卖出 {pos['amount']} BTC @ ${price:,.0f} | 利润: ${p:.2f}")
        
        # 状态
        self.log(f"📊 ${price:,.0f} | USDT:{self.balance_usdt:.2f} | BTC:{self.balance_btc:.6f} | "
                f"持仓:{len(self.positions)}笔 | 总值:${total:,.2f} ({profit_pct:+.2f}%)")
    
    def run(self):
        print("="*60)
        self.log("🤖 火币网格机器人 V4 启动")
        self.init_grids()
        print("="*60)
        
        try:
            while True:
                self.check_trades()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            price, total, profit = self.get_status()
            self.log(f"\n⏹️ 停止 | 总值:${total:,.2f} | 交易:{self.total_trades}次")

if __name__ == '__main__':
    bot = SmartGridBotV4()
    bot.run()
