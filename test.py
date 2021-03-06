from broker.broker import Broker

broker = Broker("coinone")

print(broker.price("ada"))
