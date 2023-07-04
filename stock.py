from option import Option
from logger import logger, logger_wraps


class Stock(object):
    @logger_wraps()
    def __init__(self, symbol="qqq"):
        self.symbol = symbol

    @classmethod
    @logger_wraps()
    def from_option(cls, option):
        return cls(symbol=option.symbol)

    def __str__(self):
        return f"stock: {self.symbol}"
