#!/usr/bin/env python3
"""
火币稳健版网格机器人 - 只做 BTC + ETH
"""
import ccxt
import time
from datetime import datetime

SYMBOLS = ['BTC/USDT', 'ETH/USDT']
INITIAL_USDT = 10000
PER_COIN_USDT = INITIAL_USDT / len(SYMBOLS)

GRID_SPREAD = 0.04   # 4% 更小波动
GRID_COUNT = 8        # 8格
TAKE_PROFIT = 0.002  # 0.2% 就卖
CHECK_INTERVAL = 60

API_KEY = 'dbuqg6hkte-2ecd8a42-f451fc26-c0bac'
SECRET_KEY = '1338cef7-7798fc08-b996290f-71653'

LOG_FILE = '/tmp/stable_grid.log'

BUY_AMOUNTS = {
    'BTC/USDT': 0.0001,
    'ETH/USDT': 0.005,
}

class StableGridBot:
    def __init__(self):
        self.ex = ccxt.huobi({'apiKey': API_KEY, 'secret': SECRET_KEY, 'enableRateLimit': True})
        self.coins = {}
        
        for symbol in SYMBOLS:
            self.coins[symbol] = {
                'usdt': PER_COIN_USDT,
                'holdings': 0,
                'grids': [],
                'positions': [],
                'trades': 0,
                'start_price': 0,
                'buy_amt': BUY_AMOUNTS.get(symbol, 0.001)
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
        
        # 买入
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
        
        # 卖出
        for pos in coin['positions'][:]:
            if price >= pos['price'] * (1 + TAKE_PROFIT):
                revenue = pos['amount'] * price * 0.999
                profit = revenue - pos['price'] * pos['amount']
                coin['usdt'] += revenue
                coin['holdings'] -= pos['amount']
                coin['trades'] += 1
                self.log(f"🔴 卖出 {symbol}: {pos['amount']} @ ${price:.2f} +${profit:.2f}")
                coin['positions'].remove(pos)
        
        # 重置
        if coin['positions']:
            lowest_buy = min(p['price'] for p in coin['positions'])
            for grid in coin['grids']:
                if grid['filled'] and price > lowest_buy * 1.003:
                    grid['filled'] = False
        
        total = coin['usdt'] + coin['holdings'] * price
        profit = total - PER_COIN_USDT
        pct = profit / PER_COIN_USDT * 100
        
        return price, total, profit, pct
    
    def run(self):
        print("="*50)
        self.log("🛡️ 稳健版网格机器人 - BTC+ETH")
        
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
                        self.log(f"📊 {coin_name:3} ${price:>10,.0f} | 总${total:>8,.0f} ({pct:+.2f}%)")
                
                self.log(f"💰 组合收益: ${total_profit:,.2f}")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            self.log("\n⏹️ 停止")

if __name__ == '__main__':
    bot = StableGridBot()
    bot.run()
