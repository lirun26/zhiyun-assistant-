#!/usr/bin/env python3
"""
激进版网格机器人 - 多币种 + 高频交易
"""
import ccxt
import time
from datetime import datetime

# 激进配置
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT']
INITIAL_USDT = 10000
PER_COIN_USDT = INITIAL_USDT / len(SYMBOLS)

# 激进参数
GRID_SPREAD = 0.02   # 2% 更小波动（更密集）
GRID_COUNT = 10       # 10格
TAKE_PROFIT = 0.001  # 0.1% 就卖（更快获利）
CHECK_INTERVAL = 30   # 30秒检查一次（更快反应）

# Bitget API
API_KEY = 'bg_faa615ea273253ec1c62459bc8123396'
SECRET_KEY = 'bd47f550865e71eb52eddc2d493402b8a63f490b5e1d570722393de107b9db65'
PASSWORD = 'yjllyzlyx521'

LOG_FILE = '/tmp/grid_aggressive.log'

# 每次买入数量（激进加大）
BUY_AMOUNTS = {
    'BTC/USDT': 0.001,   # 约$73
    'ETH/USDT': 0.01,    # 约$22
    'SOL/USDT': 0.1,     # 约$15
    'BNB/USDT': 0.01,    # 约$5
    'XRP/USDT': 10,       # 约$5
}

class AggressiveGridBot:
    def __init__(self):
        self.ex = ccxt.bitget({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'password': PASSWORD,
            'enableRateLimit': True
        })
        self.coins = {}
        
        for symbol in SYMBOLS:
            self.coins[symbol] = {
                'usdt': PER_COIN_USDT,
                'holdings': 0,
                'grids': [],
                'positions': [],
                'trades': 0,
                'start_price': 0,
                'buy_amt': BUY_AMOUNTS.get(symbol, 0.01)
            }
    
    def init_grids(self, symbol):
        ticker = self.ex.fetch_ticker(symbol)
        price = ticker['last']
        self.coins[symbol]['start_price'] = price
        
        # 激进版：只在当前价格下方设置买入网格
        # 从当前价格往下每隔0.5%设置一个买入点
        grids = []
        for i in range(1, GRID_COUNT + 1):
            grid_price = price * (1 - 0.005 * i)  # 每格0.5%
            grids.append({'price': grid_price, 'filled': False})
        
        self.coins[symbol]['grids'] = grids
        
        return symbol, price
    
    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def check_one(self, symbol):
        coin = self.coins[symbol]
        amt = coin['buy_amt']
        
        try:
            ticker = self.ex.fetch_ticker(symbol)
            price = ticker['last']
        except:
            return None
        
        # 买入 - 触发网格
        for grid in coin['grids']:
            if not grid['filled'] and price <= grid['price']:
                cost = price * amt
                if coin['usdt'] >= cost:
                    coin['usdt'] -= cost
                    coin['holdings'] += amt
                    coin['positions'].append({'price': price, 'amount': amt})
                    coin['trades'] += 1
                    grid['filled'] = True
                    self.log(f"🟢 买入 {symbol}: {amt} @ ${price:.2f}")
        
        # 卖出 - 止盈
        for pos in coin['positions'][:]:
            if price >= pos['price'] * (1 + TAKE_PROFIT):
                revenue = pos['amount'] * price * 0.999  # 扣除手续费
                profit = revenue - pos['price'] * pos['amount']
                coin['usdt'] += revenue
                coin['holdings'] -= pos['amount']
                coin['trades'] += 1
                self.log(f"🔴 卖出 {symbol}: {pos['amount']} @ ${price:.2f} +${profit:.2f}")
                coin['positions'].remove(pos)
        
        # 重置已卖出的网格
        if coin['positions']:
            lowest_buy = min(p['price'] for p in coin['positions'])
            for grid in coin['grids']:
                if grid['filled'] and price > lowest_buy * 1.002:
                    grid['filled'] = False
        
        total = coin['usdt'] + coin['holdings'] * price
        profit = total - PER_COIN_USDT
        pct = profit / PER_COIN_USDT * 100
        
        return price, total, profit, pct
    
    def run(self):
        print("="*50)
        self.log("⚡ 激进版网格机器人 - 多币种")
        
        for symbol in SYMBOLS:
            sym, price = self.init_grids(symbol)
            self.log(f"✅ {sym}: ${price:.2f}")
        
        print("="*50)
        
        try:
            while True:
                self.log("-"*30)
                total_profit = 0
                
                for symbol in SYMBOLS:
                    result = self.check_one(symbol)
                    if result:
                        price, total, profit, pct = result
                        total_profit += profit
                        coin_name = symbol.replace('/USDT', '')
                        self.log(f"📊 {coin_name:3} ${price:>10,.2f} | 总${total:>8,.2f} ({pct:+.2f}%)")
                
                self.log(f"💰 组合收益: ${total_profit:,.2f}")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            self.log("\n⏹️ 停止")

if __name__ == '__main__':
    bot = AggressiveGridBot()
    bot.run()
