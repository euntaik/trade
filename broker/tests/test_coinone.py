from broker.crypto.coinone import Coinone


def test_apis():
    sut = Coinone()
    assert sut.price("btc")
    assert sut.volume_24h("btc")
    assert sut.orderbook_avg("btc")
    assert sut.trade_fee("btc")
