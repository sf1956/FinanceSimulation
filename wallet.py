from option import Option
from stock import Stock
from logger import logger


class Wallet(object):
    def __init__(
        self, amount=0, call_options_sell=None, call_options_buy=None, stocks=None
    ):
        self.amount = amount
        self.call_options_sell = (  # Short
            [] if call_options_sell is None else call_options_sell
        )
        self.call_options_buy = (  # Long
            [] if call_options_buy is None else call_options_buy
        )
        self.stocks = [] if stocks is None else stocks

    def buy_call_option(self, option):
        self.call_options_buy.append(option)
        logger.debug(
            f"buy_call_option: amount({self.amount}) - option price({option.option_price_at_purchase}) = new amount({self.amount - option.option_price_at_purchase})"
        )
        self.amount -= option.option_price_at_purchase

    def sell_call_option(self, option):
        self.call_options_sell.append(option)
        logger.debug(
            f"sell_call_option: amount({self.amount}) + option price({option.option_price_at_purchase}) = new amount({self.amount + option.option_price_at_purchase})"
        )
        self.amount += option.option_price_at_purchase

    def realize_sell_call_option(self, ind=0):
        self.amount += self.call_options_sell[ind].strike_price
        del self.call_options_sell[ind]

    def realize_buy_call_option(self, ind=0):
        self.amount -= self.call_options_buy[ind].strike_price
        self.stocks.append(Stock.from_option(self.call_options_buy[ind]))
        del self.call_options_buy[ind]

    def close_sell_call_option(
        self, updated_price, ind=0
    ):  # buy a call option to cancel out the call option you sold
        logger.debug(
            f"close_sell_call_option: amount({self.amount}) - updated_price({updated_price}) = new amount({self.amount - updated_price})"
        )
        self.amount -= updated_price
        del self.call_options_sell[ind]

    def close_buy_call_option(
        self, updated_price, ind=0
    ):  # sell the call option you bought
        logger.debug(
            f"close_buy_call_option: amount({self.amount}) + updated_price({updated_price}) = new amount({self.amount + updated_price})"
        )
        self.amount += updated_price
        del self.call_options_buy[ind]

    def roll_sell_call_option(self, new_option, update_option, ind=0):
        self.close_sell_call_option(
            updated_price=update_option.option_price_at_purchase, ind=ind
        )
        self.sell_call_option(new_option)

    def roll_buy_call_option(self, new_option, update_option, ind=0):
        self.close_buy_call_option(
            updated_price=update_option.option_price_at_purchase, ind=ind
        )
        self.buy_call_option(new_option)

    def __str__(self):
        return f"amount: {self.amount} \n\
call_options_buy: \n<{' | '.join(str(itm) for itm in self.call_options_buy)}> \n\
call_options_sell: \n<{' | '.join(str(itm) for itm in self.call_options_sell)}> \n\
stocks: <{' | '.join(str(itm) for itm in self.stocks)}>"
