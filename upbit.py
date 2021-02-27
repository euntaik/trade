import os
import requests
import json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
from decorators import private_api, public_api
from broker import BaseBroker, Order

ACCESS_KEY = os.environ["UPBIT_OPEN_API_ACCESS_KEY"]
SECRET_KEY = os.environ["UPBIT_OPEN_API_SECRET_KEY"]


class Upbit(BaseBroker):
    def __init__(self, version=1):
        self.server_url = "https://api.upbit.com"
        self.api_url = f"{self.server_url}/v{version}"
        self.market = {}

    def request(self, api, payload=None, headers=None, method="GET"):
        method = requests.post if method == "POST" else requests.get
        url = f"{self.server_url}{api}"
        response = method(url, params=payload, headers=headers)
        return response.json()

    def request_public(self, api, payload=None, headers=None, method="GET"):
        return self.request(api, payload, headers=headers, method=method)

    def request_private(self, api, payload=None, headers=None, method="GET"):
        return self.request(api, payload, headers=headers, method=method)

    def markets(self):
        if not self.market:
            url = f"{self.api_url}/market/all"
            detail = "true" if True else "flase"
            querystring = {"isDetails": detail}
            response = requests.request("GET", url, params=querystring)
            results = json.loads(response.text)
            for entry in results:
                self.market[entry.get("market")] = entry

        return self.market

    def __symbol(self, symbol):
        symbol = f"KRW-{symbol.upper()}" if "-" not in symbol else symbol
        return symbol

    @private_api
    def account_balance(self):
        payload = {"access_key": ACCESS_KEY, "nonce": str(uuid.uuid4())}
        jwt_token = jwt.encode(payload, SECRET_KEY)
        authorize_token = "Bearer {}".format(jwt_token)
        print(authorize_token)
        headers = {"Authorization": authorize_token}

        return self.request_private("/v1/accounts", headers=headers)

    @private_api
    def _order(self, order_type: Order, symbol, price, qty):
        if order_type == Order.BUY:
            order = "bid"
        elif order_type == Order.SELL:
            order = "ask"
        query = {
            "market": symbol,
            "side": order,
            "volume": qty,
            "price": price,
            "ord_type": "limit",
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            "access_key": ACCESS_KEY,
            "nonce": str(uuid.uuid4()),
            "query_hash": query_hash,
            "query_hash_alg": "SHA512",
        }

        jwt_token = jwt.encode(payload, SECRET_KEY)
        authorize_token = "Bearer {}".format(jwt_token)
        headers = {"Authorization": authorize_token}
        return self.request_private(
            "/v1/orders", payload=query, headers=headers, method="POST"
        )

    @private_api
    def buy(self, symbol, price, qty, safety_check=True):
        symbol = self.__symbol(symbol)
        if safety_check:
            if not self.check_buy_price(symbol, price):
                return
        return self._order(Order.BUY, symbol, price, qty)

    @private_api
    def sell(self, symbol, price, qty, safety_check=True):
        symbol = self.__symbol(symbol)
        if safety_check:
            if not self.check_sell_price(symbol, price):
                return
        return self._order(Order.SELL, symbol, price, qty)

    @public_api
    def ticker(self, symbol):
        payload = {"markets": {self.__symbol(symbol)}}
        data = self.request("/v1/ticker", payload=payload)
        return data[0]

    @public_api
    def volume_24h(self, symbol):
        return self.ticker(symbol).get("acc_trade_volume")

    @public_api
    def price(self, symbol, detail=False):
        payload = {"markets": {self.__symbol(symbol)}}
        data = self.request("/v1/ticker", payload=payload)
        data = data[0] if type(data) is list else data
        return data.get("trade_price") if not detail else data

    @public_api
    def candle_minutes(self, symbol, unit=1, to="", count=1):
        return self.candle(symbol, "minutes", unit=unit, to=to, count=count)

    @public_api
    def candle(self, symbol, timespan, unit=1, to="", count=1):
        """
        parameters:
            symbol : 마켓 코드 (ex. KRW-BTC, BTC-BCC)
            duration : minutes, days, weeks, months
            unit : only valid for minute type. 분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240
            to : 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX or yyyy-MM-dd HH:mm:ss. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수
        """
        symbol = self.__symbol(symbol)
        timespans = ["minutes", "days", "weeks", "months"]
        if timespan not in timespans:
            raise ValueError
        api = f"/v1/candles/{timespan}"
        api = f"{api}/{unit}" if timespan == "minutes" else api
        payload = {"market": symbol, "count": count}
        return self.request(api, payload=payload)

    @public_api
    def orderbook(self, symbol):
        """
        returns: 
        {
            "market": "KRW-BTC",
            "timestamp": 1529910247984,
            "total_ask_size": 8.83621228,
            "total_bid_size": 2.43976741,
            "orderbook_units": [
                {} # 1 호가
                {} # 2 호가
                ...
                {} # 15 호가
            ]
        }
        """
        symbol = self.__symbol(symbol)
        payload = {"markets": symbol}
        ret = self.request("/v1/orderbook", payload=payload)
        if type(ret) is list:
            return ret[0]
        return ret

    @public_api
    def possible_orders(self, symbol):
        query = {"market": self.__symbol(symbol)}
        print("@@@", query)
        query_string = urlencode(query).encode()

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            "access_key": ACCESS_KEY,
            "nonce": str(uuid.uuid4()),
            "query_hash": query_hash,
            "query_hash_alg": "SHA512",
        }

        jwt_token = jwt.encode(payload, SECRET_KEY)
        authorize_token = "Bearer {}".format(jwt_token)
        headers = {"Authorization": authorize_token}
        return self.request("/v1/orders/chance", payload=query, headers=headers)


if __name__ == "__main__":
    upbit = Upbit()
    print(upbit.price("ada"))

    # ret = upbit.markets()
    # print(ret)
    # ret = upbit.price('ADA')
    # print(ret)
    print(upbit.candle("ada", "minutes"))
    # print(ret)

    print(upbit.orderbook("ada"))

    print(upbit.account_balance())
    print(upbit.possible_orders("ada"))

    print(upbit.price("ada"))
    print(upbit.buy("ada", 1580, 10))
