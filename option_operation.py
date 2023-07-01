from wallet import Wallet
from option import Option
from filter_utils import filter_option_df


def open_short_position_(
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


def open_long_position_(
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
