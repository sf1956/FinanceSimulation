from option import Option
from stock import Stock


class Wallet(object):
    def __init__(
        self, amount=0, call_options_sell=None, call_options_buy=None, stocks=None
    ):
        self.amount = amount
        self.call_options_sell = (
            [] if call_options_sell is None else call_options_sell
        )  # Short
        self.call_options_buy = (
            [] if call_options_buy is None else call_options_buy  # Long
        )
        self.stocks = [] if stocks is None else stocks

    def buy_call_option(self, option):
        self.call_options_buy.append(option)
        self.amount -= option.option_price_at_purchase

    def sell_call_option(self, option):
        self.call_options_sell.append(option)
        self.amount += option.option_price_at_purchase

    def realize_sell_call_option(self, ind=0):
        self.amount += self.call_options_sell[ind].strike_price
        del self.call_options_sell[ind]

    def realize_buy_call_option(self, ind=0):
        self.amount -= self.call_options_buy[ind].strike_price
        self.stocks.append(Stock.from_option(self.call_options_buy[ind]))
        del self.call_options_buy[ind]

    def close_sell_call_option(self, price, ind=0):
        self.amount -= price
        del self.call_options_sell[ind]

    def close_buy_call_option(self, price, ind=0):
        self.amount += price
        del self.call_options_buy[ind]

    def __str__(self):
        return f"amount: {self.amount} \n\
call_options_buy: \n<{' | '.join(str(itm) for itm in self.call_options_buy)}> \n\
call_options_sell: \n<{' | '.join(str(itm) for itm in self.call_options_sell)}> \n\
stocks: <{' | '.join(str(itm) for itm in self.stocks)}>"
