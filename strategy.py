import pandas as pd
import datetime as dt
from wallet import Wallet
from option import Option


class Strategy(object):
    def __init__(
        self,
        df,
        wallet,
        target_trade_date,
        short_target_dte=30,
        long_target_dte=700,
        short_target_strike_over_stock_prec=1.05,
        long_target_strike_over_stock_prec=1.0,
    ):
        self.df = df
        self.wallet = wallet
        self.target_trade_date = target_trade_date
        self.short_target_dte = short_target_dte
        self.long_target_dte = long_target_dte
        self.short_target_strike_over_stock_prec = short_target_strike_over_stock_prec
        self.long_target_strike_over_stock_prec = long_target_strike_over_stock_prec

        self.open_short_position(
            df=self.df,
            wallet=self.wallet,
            target_trade_date=self.target_trade_date,
            target_dte=self.short_target_dte,
            target_strike_over_stock_prec=self.short_target_strike_over_stock_prec,
        )
        # short = self.find_option_by_dte(df=df, target_dte=short_target_dte)
        # short = self.find_option_by_strike_over_stock(
        #     df=short, target_strike_over_stock_prec=short_target_strike_over_stock_prec
        # )
        # wallet.sell_call_option(Option.from_data_series(short))

        self.open_long_position(
            df=self.df,
            wallet=self.wallet,
            target_trade_date=self.target_trade_date,
            target_dte=self.long_target_dte,
            target_strike_over_stock_prec=self.long_target_strike_over_stock_prec,
        )
        # long = self.find_option_by_dte(df=df, target_dte=long_target_dte)
        # long = self.find_option_by_strike_over_stock(
        #     df=long, target_strike_over_stock_prec=long_target_strike_over_stock_prec
        # )
        # wallet.sell_call_option(Option.from_data_series(long))

    def filter_option_by_trade_date(self, df, target_trade_date):
        df = df.loc[df.QUOTE_DATE >= target_trade_date, :].copy()
        min_trade_date = df.QUOTE_DATE.min()
        df = df.loc[df.QUOTE_DATE == target_trade_date, :].copy()

        if len(df) == 0:
            print(f"No options with trade date <= {target_trade_date}")

        return df

    def filter_option_by_dte(self, df, target_dte=30):
        df = df.loc[df.DTE <= target_dte, :].copy()
        max_dte = df.DTE.max()
        df = df.loc[df.DTE == max_dte, :].copy()

        if len(df) == 0:
            print(f"No options with dte <= {target_dte}")

        return df

    def filter_option_by_strike_over_stock(
        self, df, target_strike_over_stock_prec=1.05
    ):
        df = df.loc[df.STRIKE >= target_strike_over_stock_prec, :].copy()
        min_strike = df.STRIKE.min()
        df = df.loc[df.STRIKE == min_strike, :].copy()

        if len(df) == 0:
            print(
                f"No options with strike over stoke price >= {target_strike_over_stock_prec}"
            )

        return df

    def open_short_position(
        self,
        df,
        wallet,
        target_trade_date,
        target_dte,
        target_strike_over_stock_prec,
    ):
        short = self.filter_option_by_trade_date(
            df=df, target_trade_date=target_trade_date
        )
        short = self.filter_option_by_dte(df=short, target_dte=target_dte)
        short = self.filter_option_by_strike_over_stock(
            df=short, target_strike_over_stock_prec=target_strike_over_stock_prec
        )
        short = short.squeeze()
        # print(short)
        wallet.sell_call_option(Option.from_data_series(short))

    def open_long_position(
        self,
        df,
        wallet,
        target_trade_date,
        target_dte,
        target_strike_over_stock_prec,
    ):
        long = self.filter_option_by_trade_date(
            df=df, target_trade_date=target_trade_date
        )
        long = self.filter_option_by_dte(df=long, target_dte=target_dte)
        long = self.filter_option_by_strike_over_stock(
            df=long, target_strike_over_stock_prec=target_strike_over_stock_prec
        )
        long = long.squeeze()
        # print(long)
        # print(type(long))
        wallet.buy_call_option(Option.from_data_series(long))
