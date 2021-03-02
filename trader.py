from upbit import Upbit
from coinone import Coinone
import time
from termcolor import colored, cprint
from trade_algo import *

# configuration
Broker = Coinone
broker = Broker()
trading_algorithm = simple_sell_after_buy
symbol = 'ada'
current_price = broker.price(symbol)
trade_won = 10000.00
trade_qty = 10000.00 / current_price

trade_volume = broker.volume_24h(symbol)

cprint(f'Using Broker : {type(broker).__name__}', color='yellow', attrs=['bold'])
cprint(f'Trading coin : {symbol.upper()}', color='yellow', attrs=['bold'])
cprint(f'Current {symbol.upper()} price : {current_price}', color='yellow', attrs=['bold'])
cprint(f'Current {symbol.upper()} trade volume : {trade_volume}', color='yellow', attrs=['bold'])
cprint(f'Trading amount : {trade_won} KRW  {trade_qty} {symbol.upper()}', color='yellow', attrs=['bold'])



trading_algorithm(broker, symbol, trade_qty)


