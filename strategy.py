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

    def filter_option_by_trade_date(self, df, target_trade_date):
        df = df.loc[df.QUOTE_DATE >= target_trade_date, :].copy()
        min_trade_date = df.QUOTE_DATE.min()
        df = df.loc[df.QUOTE_DATE == min_trade_date, :].copy()

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

    def filter_option_by_expiration_date(self, df, target_expiration_date):
        df = df.loc[df.EXPIRE_DATE == target_expiration_date, :].copy()

        if len(df) == 0:
            print(f"No options with expiration date == {target_expiration_date}")

        return df

    def filter_option_by_strike(self, df, target_strike):
        df = df.loc[df.STRIKE == target_strike, :].copy()

        if len(df) == 0:
            print(f"No options with strike == {target_strike}")

        return df

    def filter_option_by_strike_over_stock(
        self, df, target_strike_over_stock_prec=1.05
    ):
        df = df.loc[
            df.STRIKE >= target_strike_over_stock_prec * df.STRIKE / df.UNDERLYING_LAST,
            :,
        ].copy()
        min_strike = df.STRIKE.min()
        df = df.loc[df.STRIKE == min_strike, :].copy()

        if len(df) == 0:
            print(
                f"No options with strike over stock price >= {target_strike_over_stock_prec}"
            )

        return df

    def filter_option(
        self,
        df,
        target_trade_date,
        target_strike_over_stock_prec=None,
        target_strike=None,
        target_dte=None,
        target_expiration_date=None,
    ):
        out = self.filter_option_by_trade_date(
            df=df, target_trade_date=target_trade_date
        )
        if target_dte is not None:
            out = self.filter_option_by_dte(df=out, target_dte=target_dte)
        if target_expiration_date is not None:
            out = self.filter_option_by_expiration_date(
                df=out, target_expiration_date=target_expiration_date
            )
        if target_strike_over_stock_prec is not None:
            out = self.filter_option_by_strike_over_stock(
                df=out, target_strike_over_stock_prec=target_strike_over_stock_prec
            )
        if target_strike is not None:
            out = self.filter_option_by_strike(df=out, target_strike=target_strike)
        out = out.squeeze()
        return out

    def open_short_position(
        self,
        df,
        wallet,
        target_trade_date,
        target_dte,
        target_strike_over_stock_prec,
    ):
        short = self.filter_option(
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
        long = self.filter_option(
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

        updated_option = self.filter_option(
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
