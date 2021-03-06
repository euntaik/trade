from broker.broker import Broker
import pytest


def test_broker():
    pytest.raises(Exception, Broker, "NonexistingBroker")
    assert Broker("upbit")
    assert Broker("UPBIT")
    assert Broker("coinone")
    assert Broker("COINONE")
