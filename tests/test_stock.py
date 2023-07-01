from stock import Stock
from option import Option


def test_stock_default():
    stock = Stock()
    assert stock.symbol == "qqq"


def test_stock_from_option_default():
    option = Option()
    stock = Stock.from_option(option)
    assert stock.symbol == "qqq"
