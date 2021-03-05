from upbit import Upbit
from coinone import Coinone
from broker import *
import time
from termcolor import colored, cprint
from trade_algo import *


def simple_sell_after_buy(broker: BrokerBase, symbol, trade_qty, simulation=True):
    net_profit = 0
    share_count = 0
    last_xaction = "sell"
    trade_fee_rate = broker.trade_fee(symbol)
    while True:
        time.sleep(0.3)
        avg = broker.orderbook_avg(symbol)
        current_price = broker.price(symbol)
        trade_fee_per_curr_price = current_price * trade_fee_rate
        trade_fee = (trade_qty * current_price) * trade_fee_rate
        expected_price = avg
        waiting_xaction = "sell" if last_xaction == "buy" else "buy"
        color = "green" if waiting_xaction == "buy" else "red"
        buy_sell = colored(waiting_xaction.upper(), color=color, attrs=["bold"])
        print(f"\rWaiting to {buy_sell} current price:{current_price:.4f} trade_fee:{trade_fee_per_curr_price:.2f} expected_price:{expected_price:.4f}", end='', flush=True)
        if last_xaction == "sell" and current_price < expected_price :
            # buy
            print()
            if not simulation:
                xact_result = broker.buy(symbol, current_price, trade_qty, sync=True)
                if xact_result.status == Status.FAIL:
                    continue
                buy_price = current_price
                msg = colored('BOUGHT', color='green', attrs=['bold'])
                cprint(f'{msg} at {buy_price}')
            net_profit -= (current_price - trade_fee) * trade_qty
            share_count += trade_qty
            last_xaction = "buy"
        elif last_xaction == "buy" and current_price > expected_price and current_price > (buy_price + trade_fee_per_curr_price):
            # sell
            print()
            if not simulation:
                xact_result = broker.sell(symbol, current_price, trade_qty, sync=True)
                if xact_result.status == Status.FAIL:
                    continue
                sell_price = current_price
                msg = colored('SOLD', color='red', attrs=['bold'])
                cprint(f'{msg} at {sell_price}')
                cprint(f"Net profit:{net_profit}")
            net_profit += (current_price - trade_fee) * trade_qty
            share_count -= trade_qty
            last_xaction = "sell"

        
