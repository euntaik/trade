def method1():
    net_profit = 0
    share_count = 10
    while True:
        time.sleep(0.3)
        outstading_orders = upbit.orderbook(symbol)
        sum_sell_price = [0] * 15
        sum_sell_count = [0] * 15
        sum_buy_price = [0] * 15
        sum_buy_count = [0] * 15
        for i, orders in zip(range(15), outstading_orders["orderbook_units"]):
            for j in range(15 - i):
                sum_sell_price[i + j] += orders["ask_price"] * orders["ask_size"]
                sum_sell_count[i + j] += orders["ask_size"]
                sum_buy_price[i + j] += orders["bid_price"] * orders["bid_size"]
                sum_buy_count[i + j] += orders["bid_size"]

        orderers_price = [0] * 15
        for i in range(15):
            orderers_price[i] = (sum_sell_price[i] + sum_buy_price[i]) / (sum_sell_count[i] + sum_buy_count[i])

        direction = [0] * 15
        for i in range(15):
            direction[i] = (sum_buy_count[i] - sum_sell_count[i]) / sum_buy_count[i]
            # print(f'[{i}] {orderers_price[i]} pressure={direction[i]}')
        current_price = upbit.price(symbol)
        trade_fee = current_price * 0.002
        expected_price = orderers_price[14]
        print(f"current price:{current_price} trade_fee:{trade_fee} expected_price:{expected_price}")
        if orderers_price[0] <= current_price and direction[0] < 0 and share_count > 1:
            print(f"Price going down. expected price={expected_price}")
            # sell
            net_profit += current_price - trade_fee
            share_count -= 1
        elif (
            orderers_price[0] > (current_price + trade_fee)
            and direction[0] > 0
            and expected_price > (current_price + current_price * 0.01 + trade_fee)
        ):
            print(f"Price going up. expected price={expected_price}")
            net_profit -= current_price + trade_fee
            share_count += 1
        print(f"net profit:{net_profit}")


def method2():
    net_profit = 0
    last_net_profit = net_profit
    share_count = 1
    buy_price = upbit.price(symbol)
    xaction_price = buy_price
    last_xaction = "buy"
    while True:
        time.sleep(0.3)
        current_price = upbit.price(symbol)
        trade_fee = current_price * 0.002
        print(f"{current_price} > ({xaction_price} + {trade_fee}) and {last_xaction} == buy and {share_count}")
        if current_price > (xaction_price + trade_fee) and last_xaction == "buy" and share_count > 0:
            # sell
            print(f"SELL at {current_price}")
            net_profit += current_price - trade_fee
            share_count -= 1
            xaction_price = current_price
            last_xaction = "sell"
        elif current_price < (xaction_price - trade_fee) and last_xaction == "sell":
            print(f"BUY at {current_price}")
            net_profit -= current_price + trade_fee
            share_count += 1
            last_xaction = "buy"
            xaction_price = current_price
        if last_net_profit != net_profit:
            print(f"net profit:{net_profit}")
            last_net_profit = net_profit


def method3():
    while True:
        symbol = "btc"
        time.sleep(0.3)
        current_price = upbit.price(symbol)

        candles = upbit.candle_minutes(symbol, unit=5, count=1)
        for i, candle in zip(range(len(candles)), candles):
            print(
                f"[{i}] curr:{current_price} low:{candle['low_price']} high:{candle['high_price']}, trade:{candle['trade_price']}"
            )
