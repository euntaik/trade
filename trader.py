from coinone import Coinone
from upbit import Upbit

coinone = Coinone()
upbit = Upbit()


# print(coinone.orderbook('ada'))
coinone_volume = coinone.volume_24h("ada")
upbit_volume = upbit.volume_24h("ada")


print(coinone_volume)
print(upbit_volume)

outstading_orders = upbit.orderbook("ada")
sum_sell_price = 0
sum_sell_count = 0
sum_buy_price = 0
sum_buy_count = 0
for orders in outstading_orders["orderbook_units"]:
    sum_sell_price += orders["ask_price"] * orders["ask_size"]
    sum_sell_count += orders["ask_size"]
    sum_buy_price += orders["bid_price"] * orders["bid_size"]
    sum_buy_count += orders["bid_size"]

orderers_price = (sum_sell_price + sum_buy_price) / (sum_sell_count + sum_buy_count)

print(orderers_price)
print(upbit.price("ada"))
