from upbit import Upbit
from coinone import Coinone
import time
from termcolor import colored, cprint
from trade_algo import *

def simple_sell_after_buy(broker, symbol, trade_qty):
    net_profit = 0
    share_count = 10
    last_xaction = 'buy'
    while True:
        time.sleep(0.3)
        avg = broker.orderbook_avg(symbol)
        current_price = broker.price(symbol)
        trade_fee = (trade_qty * current_price) * 0.002
        expected_price = avg
        waiting_xaction = 'sell' if last_xaction == 'buy' else 'buy'
        color = 'green' if waiting_xaction == 'buy' else 'red'
        buy_sell = colored(waiting_xaction.upper(), color=color, attrs=['bold'] )
        print(f'Waiting to {buy_sell} current price:{current_price} trade_fee:{trade_fee} expected_price:{expected_price}')
        if current_price < expected_price and last_xaction == 'sell':
            # buy
            net_profit -= (current_price - trade_fee) * trade_qty
            share_count += trade_qty
            last_xaction = 'buy'
        elif current_price > expected_price and last_xaction == 'buy':
            # sell
            net_profit += (current_price - trade_fee) * trade_qty
            share_count -= trade_qty
            last_xaction = 'sell'

        print(f'net profit:{net_profit}')
