from option import Option


class Stock(object):
    def __init__(self, symbol="qqq"):
        self.symbol = symbol

    @classmethod
    def from_option(cls, option):
        return cls(symbol=option.symbol)

    def __str__(self):
        return f"stock: {self.symbol}"
