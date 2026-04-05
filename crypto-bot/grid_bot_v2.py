#!/usr/bin/env python3
"""
火币智能网格交易机器人 v2 - 后台运行
优化参数：
- 更宽的网格范围 (10%)
- 更小的买入金额
- 止盈止损
- 更智能的价格监控
"""
import ccxt
import time
from datetime import datetime

# ===== 可调参数 =====
SYMBOL = 'BTC/USDT'
INITIAL_USDT = 10000

# 网格参数
GRID_SPREAD = 0.10    # 10%波动范围（更宽）
GRID_COUNT = 20       # 20个网格（更密）
BUY_AMOUNT = 0.0005  # 每次买0.0005 BTC（更保守）
TAKE_PROFIT = 0.005  # 盈利0.5%就卖出
STOP_LOSS = -0.03     # 亏损3%止损

# 监控间隔
CHECK_INTERVAL = 60    # 每60秒检查一次

# API
API_KEY = 'dbuqg6hkte-2ecd8a42-f451fc26-c0bac'
SECRET_KEY = '1338cef7-7798fc08-b996290f-71653'

LOG_FILE = '/tmp/grid_bot_v2.log'

class SmartGridBot:
    def __init__(self):
        self.exchange = ccxt.huobi({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,
        })
        self.balance_usdt = float(INITIAL_USDT)
        self.balance_btc = 0.0
        self.grids = []
        self.total_trades = 0
        self.total_profit = 0
        self.start_price = 0
        
    def init_grids(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        self.start_price = price
        
        lowest = price * (1 - GRID_SPREAD/2)
        highest = price * (1 + GRID_SPREAD/2)
        step = (highest - lowest) / GRID_COUNT
        
        self.grids = []
        for i in range(GRID_COUNT):
            self.grids.append({
                'price': lowest + step * i,
                'buy_price': None,
                'amount': 0,
                'sold': False
            })
        
        self.log(f"✅ 网格初始化: {lowest:.0f} - {highest:.0f} USDT")
        self.log(f"   网格数: {GRID_COUNT}, 步长: {step:.2f} USDT")
        
    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {msg}"
        print(log_msg)
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + '\n')
    
    def get_status(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        
        total_value = self.balance_usdt + self.balance_btc * price
        profit = total_value - INITIAL_USDT
        profit_pct = (profit / INITIAL_USDT) * 100
        
        price_change = (price / self.start_price - 1) * 100
        
        return {
            'price': price,
            'usdt': self.balance_usdt,
            'btc': self.balance_btc,
            'value': total_value,
            'profit': profit,
            'profit_pct': profit_pct,
            'price_change': price_change,
            'trades': self.total_trades
        }
    
    def check_trades(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        price = ticker['last']
        status = self.get_status()
        
        # 检查止盈止损
        if status['profit_pct'] <= STOP_LOSS * 100:
            self.log(f"🛑 触发止损! 亏损 {status['profit_pct']:.2f}%")
            # 全部清仓
            if self.balance_btc > 0:
                self.balance_usdt += self.balance_btc * price * 0.999  # 扣手续费
                self.log(f"   清仓止损: 卖出 {self.balance_btc:.6f} BTC")
                self.balance_btc = 0
                # 重置网格
                for g in self.grids:
                    g['buy_price'] = None
                    g['amount'] = 0
                    g['sold'] = False
        
        # 检查止盈
        if status['profit_pct'] >= TAKE_PROFIT * 100 * 10:  # 盈利5%
            self.log(f"🎯 触发止盈! 盈利 {status['profit_pct']:.2f}%")
            if self.balance_btc > 0:
                self.balance_usdt += self.balance_btc * price * 0.999
                self.log(f"   止盈卖出: {self.balance_btc:.6f} BTC")
                self.balance_btc = 0
                for g in self.grids:
                    g['buy_price'] = None
                    g['amount'] = 0
                    g['sold'] = False
        
        # 买入逻辑：价格触及网格且未买入
        for i, grid in enumerate(self.grids):
            if price <= grid['price'] and not grid['buy_price']:
                cost = price * BUY_AMOUNT
                if self.balance_usdt >= cost:
                    self.balance_usdt -= cost
                    self.balance_btc += BUY_AMOUNT
                    grid['buy_price'] = price
                    grid['amount'] = BUY_AMOUNT
                    self.total_trades += 1
                    self.log(f"  🟢 买入 {BUY_AMOUNT} BTC @ ${price:.0f}")
        
        # 卖出逻辑：价格回升超过买入点+盈利
        for grid in self.grids:
            if grid['buy_price'] and not grid['sold']:
                # 盈利 TAKE_PROFIT % 就卖出
                if price >= grid['buy_price'] * (1 + TAKE_PROFIT):
                    revenue = grid['amount'] * price * 0.999
                    profit = revenue - (grid['buy_price'] * grid['amount'])
                    self.balance_usdt += revenue
                    self.balance_btc -= grid['amount']
                    self.total_profit += profit
                    self.log(f"  🔴 卖出 {grid['amount']} BTC @ ${price:.0f} | 利润: ${profit:.2f}")
                    grid['sold'] = True
                    grid['buy_price'] = None
        
        # 重置已卖出的网格
        for grid in self.grids:
            if grid['sold']:
                grid['sold'] = False
                grid['buy_price'] = None
                grid['amount'] = 0
        
        # 输出状态
        self.log(f"📊 价格: ${price:,.0f} ({status['price_change']:+.2f}%) | "
                f"USDT: {self.balance_usdt:.2f} | BTC: {self.balance_btc:.6f} | "
                f"总价值: ${status['value']:,.2f} ({status['profit_pct']:+.2f}%)")
    
    def run(self):
        print("="*60)
        self.log("🤖 火币智能网格机器人 V2 启动")
        self.init_grids()
        print("="*60)
        
        try:
            while True:
                self.check_trades()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            status = self.get_status()
            self.log(f"\n⏹️ 机器人停止")
            self.log(f"   最终资产: ${status['value']:,.2f}")
            self.log(f"   总交易: {self.total_trades} 次")
            self.log(f"   总利润: ${self.total_profit:.2f}")

if __name__ == '__main__':
    bot = SmartGridBot()
    bot.run()
