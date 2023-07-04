from wallet import Wallet
from strategy import Strategy
from data_gen import get_option_data
from option import Option
import pandas as pd
from logger import logger, logger_wraps
import datetime as dt


d_df = get_option_data()

start_date = d_df.QUOTE_DATE.min()

end_date = start_date = d_df.QUOTE_DATE.max()


class StrategyRunner(object):
    @logger_wraps()
    def __init__(
        self,
        short_target_dte=30,
        long_target_dte=700,
        short_target_strike_over_stock_prec=1.05,
        long_target_strike_over_stock_prec=1.0,
        daily_option_prec=0.5,
    ):
        self.d_df = get_option_data()
        self.start_date = self.d_df.QUOTE_DATE.min()
        self.end_date = self.d_df.QUOTE_DATE.max()
        self.trading_date = self.start_date
        self.strategy = Strategy(
            self.d_df,
            Wallet(),
            self.trading_date,
            short_target_dte=short_target_dte,
            long_target_dte=long_target_dte,
            short_target_strike_over_stock_prec=short_target_strike_over_stock_prec,
            long_target_strike_over_stock_prec=long_target_strike_over_stock_prec,
            daily_option_prec=daily_option_prec,
        )
        logger.info(f"\nTrading date:{self.trading_date}")
        logger.debug(f"ֿ\n{self.strategy.wallet}")

    @logger_wraps()
    def next_trading_day(self):
        self.trading_date = self.trading_date + dt.timedelta(days=1)
        if self.trading_date > self.end_date:
            logger.info("Passed last availible trading day")
            return
        self.strategy.daily_roll(self.d_df, self.trading_date)
        logger.info(f"\nTrading date:{self.trading_date}")
        logger.debug(f"{self.strategy.wallet}")
