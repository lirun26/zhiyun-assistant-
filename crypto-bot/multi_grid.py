#!/usr/bin/env python3
"""
火币多币种网格机器人 - 同时监控多个币种
"""
import ccxt
import time
from datetime import datetime

# ===== 配置 =====
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'LINK/USDT', 'NEAR/USDT', 'SUI/USDT']
INITIAL_USDT = 20000  # 总资金

# 每个币种分配资金
PER_COIN_USDT = INITIAL_USDT / len(SYMBOLS)

# 网格参数
GRID_SPREAD = 0.06   # 6%波动
GRID_COUNT = 12      # 12格
BUY_AMOUNT = 0.001   # 每次买数量
TAKE_PROFIT = 0.003  # 0.3%止盈

CHECK_INTERVAL = 60

API_KEY = 'dbuqg6hkte-2ecd8a42-f451fc26-c0bac'
SECRET_KEY = '1338cef7-7798fc08-b996290f-71653'

LOG_FILE = '/tmp/multi_grid.log'

class MultiGridBot:
    def __init__(self):
        self.ex = ccxt.huobi({'apiKey': API_KEY, 'secret': SECRET_KEY, 'enableRateLimit': True})
        self.coins = {}
        
        for symbol in SYMBOLS:
            self.coins[symbol] = {
                'usdt': PER_COIN_USDT,
                'btc': 0,
                'grids': [],
                'positions': [],
                'trades': 0,
                'start_price': 0
            }
    
    def init_grids(self, symbol):
        ticker = self.ex.fetch_ticker(symbol)
        price = ticker['last']
        self.coins[symbol]['start_price'] = price
        
        lowest = price * (1 - GRID_SPREAD/2)
        highest = price * (1 + GRID_SPREAD/2)
        step = (highest - lowest) / GRID_COUNT
        
        grids = [{'price': lowest + step*i, 'filled': False} for i in range(GRID_COUNT)]
        self.coins[symbol]['grids'] = grids
        
        return symbol, price, lowest, highest
    
    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def check_one(self, symbol):
        coin = self.coins[symbol]
        ticker = self.ex.fetch_ticker(symbol)
        price = ticker['last']
        
        # 买入
        for grid in coin['grids']:
            if not grid['filled'] and price <= grid['price']:
                cost = price * BUY_AMOUNT
                if coin['usdt'] >= cost:
                    coin['usdt'] -= cost
                    coin['btc'] += BUY_AMOUNT
                    coin['positions'].append({'price': price, 'amount': BUY_AMOUNT})
                    coin['trades'] += 1
                    grid['filled'] = True
                    self.log(f"  🟢 {symbol}: 买入 {BUY_AMOUNT} @ ${price:.2f}")
        
        # 卖出
        for pos in coin['positions'][:]:
            if price >= pos['price'] * (1 + TAKE_PROFIT):
                revenue = pos['amount'] * price * 0.999
                coin['usdt'] += revenue
                coin['btc'] -= pos['amount']
                coin['trades'] += 1
                profit = revenue - pos['price'] * pos['amount']
                self.log(f"  🔴 {symbol}: 卖出 {pos['amount']} @ ${price:.2f} | +${profit:.2f}")
                coin['positions'].remove(pos)
        
        # 重置
        for grid in coin['grids']:
            if grid['filled'] and price > grid['price'] * 1.01:
                grid['filled'] = False
        
        total = coin['usdt'] + coin['btc'] * price
        profit = total - PER_COIN_USDT
        profit_pct = profit / PER_COIN_USDT * 100
        
        return symbol, price, total, profit, profit_pct
    
    def run(self):
        print("="*70)
        self.log("🤖 多币种网格机器人启动")
        
        for symbol in SYMBOLS:
            sym, price, low, high = self.init_grids(symbol)
            self.log(f"✅ {symbol}: ${price:.2f} | 网格: ${low:.0f}-${high:.0f}")
        
        print("="*70)
        
        try:
            while True:
                self.log("-"*50)
                total_profit = 0
                
                for symbol in SYMBOLS:
                    sym, price, total, profit, pct = self.check_one(symbol)
                    total_profit += profit
                    self.log(f"📊 {sym}: ${price:>10,.2f} | 总值:${total:>10,.2f} ({pct:+.2f}%)")
                
                self.log(f"💰 组合总收益: ${total_profit:,.2f}")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            self.log("\n⏹️ 停止")

if __name__ == '__main__':
    bot = MultiGridBot()
    bot.run()
