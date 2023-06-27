from option import Option
from stock import Stock


class Wallet(object):
    def __init__(self, amount=0, options_sold=None, options_bought=None, stocks=None):
        self.amount = amount
        self.options_sold = [] if options_sold is None else options_sold
        self.options_bought = [] if options_bought is None else options_bought
        self.stocks = [] if stocks is None else stocks

    def buy_option(self, option):
        self.options_bought.append(option)
        self.amount -= option.option_price

    def sell_option(self, option):
        self.options_sold.append(option)
        self.amount += option.option_price

    def realize_sold_option(self, ind=0):
        self.amount += self.options_sold[ind].strike_price
        del self.options_sold[ind]

    def realize_bought_option(self, ind=0):
        self.amount -= self.options_bought[ind].strike_price
        self.stocks.append(Stock.from_option(self.options_bought[ind]))
        del self.options_bought[ind]

    def __str__(self):
        return f"amount: {self.amount} \n\
    options_bought: {' | '.join(str(itm) for itm in self.options_bought)} \n\
    options_sold: {' | '.join(str(itm) for itm in self.options_sold)} \n\
    stocks: {' | '.join(str(itm) for itm in self.stocks)}"
