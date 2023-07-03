import pandas as pd
import datetime as dt
from wallet import Wallet
from option import Option
from filter_utils import filter_option_df
from option_operation import open_short_position_, open_long_position_
from loguru import logger
import sys

# logger.add(sys.stderr, backtrace=True, diagnose=True)


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
        logger.info(
            f"Strategy __init__: target_trade_date:{target_trade_date}, short_target_dte:{short_target_dte}, \
                long_target_dte:{long_target_dte}, short_target_strike_over_stock_prec:{short_target_strike_over_stock_prec}, \
                    long_target_strike_over_stock_prec:{long_target_strike_over_stock_prec}, daily_option_prec:{daily_option_prec}"
        )
        self.df = df
        self.wallet = wallet
        self.target_trade_date = target_trade_date
        self.short_target_dte = short_target_dte
        self.long_target_dte = long_target_dte
        self.short_target_strike_over_stock_prec = short_target_strike_over_stock_prec
        self.long_target_strike_over_stock_prec = long_target_strike_over_stock_prec
        self.daily_option_prec = daily_option_prec

        open_short_position_(
            df=self.df,
            wallet=self.wallet,
            target_trade_date=self.target_trade_date,
            target_dte=self.short_target_dte,
            target_strike_over_stock_prec=self.short_target_strike_over_stock_prec,
        )

        open_long_position_(
            df=self.df,
            wallet=self.wallet,
            target_trade_date=self.target_trade_date,
            target_dte=self.long_target_dte,
            target_strike_over_stock_prec=self.long_target_strike_over_stock_prec,
        )

    def daily_roll(self, df, target_trade_date, ind=0):
        orig_option = self.wallet.call_options_buy[ind]
        orig_option_price_at_purchase = orig_option.option_price_at_purchase
        orig_option_expiration_date = orig_option.expiration_date
        orig_option_strike_price = orig_option.strike_price

        new_option = Option.from_data_series(
            filter_option_df(
                df=df,
                target_trade_date=target_trade_date,
                target_dte=self.short_target_dte,
                target_strike=orig_option_strike_price,
            )
        )

        updated_option = Option.from_data_series(
            filter_option_df(
                df=df,
                target_trade_date=target_trade_date,
                target_expiration_date=orig_option_expiration_date,
                target_strike=orig_option_strike_price,
            )
        )
        logger.info(
            f"updated_option.option_price_at_purchase:{updated_option.option_price_at_purchase}"
        )
        logger.info(f"orig_option_price_at_purchase:{orig_option_price_at_purchase}")
        logger.info(f"self.daily_option_prec:{self.daily_option_prec}")
        if (  # TODO: check condition!
            updated_option.option_price_at_purchase
            <= orig_option_price_at_purchase * self.daily_option_prec
        ):
            logger.info(f"rolling option")
            self.wallet.roll_buy_call_option(
                new_option=new_option, update_option=updated_option, ind=ind
            )
        else:
            logger.info("not rolling option")
