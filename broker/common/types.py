from enum import Enum, auto
from dataclasses import dataclass


class Order(Enum):
    BUY = auto()
    SELL = auto()


class Status(Enum):
    SUCCESS = auto()
    WAITING = auto()
    FAIL = auto()


@dataclass
class XactResult:
    status: Status
    detail: dict
