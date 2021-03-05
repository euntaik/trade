from enum import Enum, auto


class Order(Enum):
    BUY = auto()
    SELL = auto()


class BaseBroker:
    def check_buy_price(self, symbol, price):
        current_price = self.price(symbol)
        if float(price) > float(current_price):
            print(
                f"You were trying to BUY {symbol} at price({price}) higher than the current price({current_price})!"
            )
            return False
        return True

    def check_sell_price(self, symbol, price):
        current_price = self.price(symbol)
        if float(price) < float(current_price):
            print(
                f"You were trying to SELL {symbol} at price({price}) higher than the current price({current_price})!"
            )
            return False
        return True
