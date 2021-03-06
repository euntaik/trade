from abc import *
from broker.common.types import *


class BrokerBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, access_key=None, secret_key=None):
        ...

    @abstractmethod
    def buy(self, symbol, price, qty, safety_check=True, sync=True, timeout=0) -> XactResult:
        ...

    @abstractmethod
    def sell(self, symbol, price, qty, safety_check=True, sync=True, timeout=0) -> XactResult:
        ...

    @abstractmethod
    def ticker(self, symbol) -> dict:
        ...

    @abstractmethod
    def price(self, symbol, detail=False) -> float:
        ...

    @abstractmethod
    def orderbook(self, symbol) -> dict:
        ...

    @abstractmethod
    def orderbook_avg(self, symbol) -> float:
        ...

    @abstractmethod
    def volume_24h(self, symbol) -> float:
        ...

    @abstractmethod
    def trade_fee(self, symbol) -> float:
        ...

    def check_buy_price(self, symbol, price):
        current_price = self.price(symbol)
        if float(price) > float(current_price):
            print(f"You were trying to BUY {symbol} at price({price}) higher than the current price({current_price})!")
            return False
        return True

    def check_sell_price(self, symbol, price):
        current_price = self.price(symbol)
        if float(price) < float(current_price):
            print(f"You were trying to SELL {symbol} at price({price}) lower than the current price({current_price})!")
            return False
        return True
