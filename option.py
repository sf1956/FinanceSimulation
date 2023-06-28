import datetime as dt
import pandas as pd


class Option(object):
    def __init__(
        self,
        symbol="qqq",
        strike_price=100,
        # stock_price=100,
        option_price=10,
        expiration_date=pd.Timestamp("2023-12-04"),
    ):
        self.symbol = symbol
        self.strike_price = strike_price
        #  self.stock_price = stock_price
        self.option_price = option_price
        self.expiration_date = expiration_date

    @classmethod
    def from_data_series(cls, series, symbol="qqq"):
        return cls(
            symbol=symbol,
            strike_price=series.STRIKE,
            option_price=series.C_ASK,
            expiration_date=series.EXPIRE_DATE,
            # expiration_date=pd.Timestamp(dt.date.fromisoformat(series.EXPIRE_DATE)),
        )

    def __str__(self):
        return (
            f"option: {self.symbol}: strike={self.strike_price} {self.expiration_date}"
        )
