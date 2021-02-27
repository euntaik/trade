from coinone import Coinone
from upbit import Upbit

coinone = Coinone()
upbit = Upbit()


#print(coinone.orderbook('ada'))
coinone_volume = coinone.volume_24h('ada')
upbit_volume = upbit.volume_24h('ada')


print(coinone_volume)
print(upbit_volume)


