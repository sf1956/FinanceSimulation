import pandas as pd
import datetime as dt
from wallet import Wallet
from option import Option


class Strategy(object):
    def __init__(
        self,
        trade_day_df,
        wallet,
        short_target_dte=30,
        long_target_dte=700,
        short_target_strike_over_stock_prec=1.05,
        long_target_strike_over_stock_prec=1.0,
    ):
        trade_day_df = trade_day_df
        wallet = wallet
        self.short_target_dte = short_target_dte
        self.long_target_dte = long_target_dte
        self.short_target_strike_over_stock_prec = short_target_strike_over_stock_prec
        self.long_target_strike_over_stock_prec = long_target_strike_over_stock_prec

        short_series = self.find_option_by_dte_strike_over_stock(
            trade_day_df=trade_day_df,
            target_dte=short_target_dte,
            target_strike_over_stock_prec=short_target_strike_over_stock_prec,
        )
        wallet.sell_call_option(Option.from_data_series(short_series))

        long_series = self.find_option_by_dte_strike_over_stock(
            trade_day_df=trade_day_df,
            target_dte=long_target_dte,
            target_strike_over_stock_prec=long_target_strike_over_stock_prec,
        )
        wallet.buy_call_option(Option.from_data_series(long_series))

    def find_option_by_dte_strike_over_stock(
        self, trade_day_df, target_dte=30, target_strike_over_stock_prec=1.05
    ):
        df = trade_day_df.loc[trade_day_df.DTE <= target_dte, :].copy()
        max_dte = df.DTE.max()
        df = df.loc[df.DTE == max_dte, :].copy()

        if len(df) == 0:
            print(f"No options with dte <= {target_dte}")

        df = df.loc[df.STRIKE >= target_strike_over_stock_prec, :].copy()
        min_strike = df.STRIKE.max()
        df = df.loc[df.STRIKE == min_strike, :].copy()

        if len(df) == 0:
            print(
                f"No options with strike over stoke price >= {target_strike_over_stock_prec}"
            )

        return df
