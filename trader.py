from upbit import Upbit
from coinone import Coinone
import time
from termcolor import colored, cprint
from trade_algo import *

# configuration
Broker = Upbit
broker = Broker()
trading_algorithm = simple_sell_after_buy
symbol = "btc"
current_price = broker.price(symbol)
trade_won = 10000.00
trade_qty = 10000.00 / current_price

trade_volume = broker.volume_24h(symbol)

cprint(f"Using Broker : {type(broker).__name__}", color="yellow", attrs=["bold"])
cprint(f"Trading coin : {symbol.upper()}", color="yellow", attrs=["bold"])
cprint(f"Current {symbol.upper()} price : {current_price}", color="yellow", attrs=["bold"])
cprint(f"Current {symbol.upper()} trade volume : {trade_volume}", color="yellow", attrs=["bold"])
cprint(f"Trading amount : {trade_won} KRW  {trade_qty} {symbol.upper()}", color="yellow", attrs=["bold"])


while True:
    start_trading_magic = "trade"
    start_simulate_magic = "simulate"
    simulation = True
    cprint(
        f'Type "{start_trading_magic}" to do a real trading and type "{start_simulate_magic}" to do a simulation...',
        color="blue",
        attrs=["bold"],
    )
    confirm = input()
    if confirm == start_trading_magic:
        simulation = False
        cprint("Confirmed! Starting trade...", color="green", attrs=["bold"])
        break
    elif confirm == start_simulate_magic:
        simulation = True
        cprint("Confirmed! Starting simulation...", color="green", attrs=["bold"])
        break
trading_algorithm(broker, symbol, trade_qty, simulation=simulation)
