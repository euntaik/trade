from enum import Enum, auto
from abc import *
from dataclasses import dataclass

from broker.common.types import *
from broker.crypto import *


def Broker(broker: str, access_key=None, secret_key=None):
    """
    Factory method for creating a broker of choice
    """
    try:
        return eval(broker.title())(access_key=access_key, secret_key=secret_key)
    except:
        raise Exception(f"{broker} is not available")
