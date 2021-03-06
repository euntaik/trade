from broker.crypto.upbit import Upbit
import os


def test_apis():
    sut = Upbit(access_key=os.environ["UPBIT_OPEN_API_ACCESS_KEY"], secret_key=os.environ["UPBIT_OPEN_API_SECRET_KEY"])
    assert sut.price("btc")
    assert sut.volume_24h("btc")
    assert sut.orderbook_avg("btc")
    assert sut.trade_fee("btc")
    assert sut.possible_orders("btc")
