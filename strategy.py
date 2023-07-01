import pandas as pd
import datetime as dt
from wallet import Wallet
from option import Option
from filter_utils import filter_option_df


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
        daily_option_prec=0.5,
    ):
        self.df = df
        self.wallet = wallet
        self.target_trade_date = target_trade_date
        self.short_target_dte = short_target_dte
        self.long_target_dte = long_target_dte
        self.short_target_strike_over_stock_prec = short_target_strike_over_stock_prec
        self.long_target_strike_over_stock_prec = long_target_strike_over_stock_prec
        self.daily_option_prec = daily_option_prec

        self.open_short_position(
            df=self.df,
            wallet=self.wallet,
            target_trade_date=self.target_trade_date,
            target_dte=self.short_target_dte,
            target_strike_over_stock_prec=self.short_target_strike_over_stock_prec,
        )

        self.open_long_position(
            df=self.df,
            wallet=self.wallet,
            target_trade_date=self.target_trade_date,
            target_dte=self.long_target_dte,
            target_strike_over_stock_prec=self.long_target_strike_over_stock_prec,
        )

    def open_short_position(
        self,
        df,
        wallet,
        target_trade_date,
        target_dte,
        target_strike_over_stock_prec,
    ):
        short = filter_option_df(
            df=df,
            target_trade_date=target_trade_date,
            target_dte=target_dte,
            target_strike_over_stock_prec=target_strike_over_stock_prec,
        )

        wallet.sell_call_option(Option.from_data_series(short))

    def open_long_position(
        self,
        df,
        wallet,
        target_trade_date,
        target_dte,
        target_strike_over_stock_prec,
    ):
        long = filter_option_df(
            df=df,
            target_trade_date=target_trade_date,
            target_dte=target_dte,
            target_strike_over_stock_prec=target_strike_over_stock_prec,
        )

        wallet.buy_call_option(Option.from_data_series(long))

    def daily_roll(self, df, target_trade_date, ind=0):
        orig_option = self.wallet.call_options_sell[ind]
        orig_option_price_at_purchase = orig_option.option_price_at_purchase
        orig_option_expiration_date = orig_option.expiration_date
        orig_option_strike_price = orig_option.strike_price

        updated_option = filter_option_df(
            df=df,
            target_trade_date=target_trade_date,
            target_expiration_date=orig_option_expiration_date,
            target_strike=orig_option_strike_price,
        )

        if (
            updated_option.option_price_at_purchase
            <= orig_option_price_at_purchase * self.daily_option_prec
        ):
            self.wallet.close_sell_call_option(
                updated_option.option_price_at_purchase, ind=ind
            )
