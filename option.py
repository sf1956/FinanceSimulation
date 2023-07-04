import datetime as dt
import pandas as pd
from logger import logger, logger_wraps


class Option(object):
    @logger_wraps()
    def __init__(
        self,
        symbol="qqq",
        strike_price=100,
        stock_price_at_purchase=100,
        option_price_at_purchase=10,
        expiration_date=pd.Timestamp("2023-12-04"),
    ):
        self.symbol = symbol
        self.strike_price = strike_price
        self.stock_price_at_purchase = stock_price_at_purchase
        self.option_price_at_purchase = option_price_at_purchase
        self.expiration_date = expiration_date

    @classmethod
    @logger_wraps()
    def from_data_series(cls, series, symbol="qqq"):
        return cls(
            symbol=symbol,
            strike_price=series.STRIKE,
            stock_price_at_purchase=series.UNDERLYING_LAST,
            option_price_at_purchase=series.C_LAST
            if series.C_LAST > 0
            else ((series.C_ASK + series.C_BID) / 2),  # series.C_ASK
            expiration_date=series.EXPIRE_DATE,
            # expiration_date=pd.Timestamp(dt.date.fromisoformat(series.EXPIRE_DATE)),
        )

    def __str__(self):
        return f"option: {self.symbol}:\n strike:{self.strike_price}\n expiration:{self.expiration_date}\n (option at purchase:{self.option_price_at_purchase},\n stock at purchase:{self.stock_price_at_purchase})"

    def __eq__(self, other):
        return (self.symbol, self.strike_price, self.expiration_date) == (
            other.symbol,
            other.strike_price,
            other.expiration_date,
        )
