import pandas as pd
from logger import logger, logger_wraps


@logger_wraps()
def filter_option_df_by_trade_date(df, target_trade_date):
    df = df.loc[df.QUOTE_DATE >= target_trade_date, :].copy()
    min_trade_date = df.QUOTE_DATE.min()
    df = df.loc[df.QUOTE_DATE == min_trade_date, :].copy()
    logger.debug(
        f"filter_option_df_by_trade_date: min_trade_date:{min_trade_date}, target_trade_date:{target_trade_date}"
    )
    logger.debug(f"len(df):{len(df)}")

    if len(df) == 0:
        logger.debug(f"No options with trade date <= {target_trade_date}")

    return df


@logger_wraps()
def filter_option_df_by_dte(df, target_dte=30):
    df = df.loc[df.DTE <= target_dte, :].copy()
    max_dte = df.DTE.max()
    df = df.loc[df.DTE == max_dte, :].copy()
    logger.debug(f"filter_option_df_by_dte: max_dte:{max_dte}, target_dte:{target_dte}")
    logger.debug(f"len(df):{len(df)}")

    if len(df) == 0:
        logger.debug(f"No options with dte <= {target_dte}")

    return df


@logger_wraps()
def filter_option_df_by_expiration_date(df, target_expiration_date):
    df = df.loc[df.EXPIRE_DATE == target_expiration_date, :].copy()
    logger.debug(
        f"filter_option_df_by_expiration_date: target_expiration_date:{target_expiration_date}"
    )
    logger.debug(f"len(df):{len(df)}")

    if len(df) == 0:
        logger.debug(f"No options with expiration date == {target_expiration_date}")

    return df


@logger_wraps()
def filter_option_df_by_strike(df, target_strike):
    df = df.loc[df.STRIKE == target_strike, :].copy()
    logger.debug(f"filter_option_df_by_strike: target_strike:{target_strike}")
    logger.debug(f"len(df):{len(df)}")

    if len(df) == 0:
        logger.debug(f"No options with strike == {target_strike}")

    return df


@logger_wraps()
def filter_option_df_by_strike_over_stock(df, target_strike_over_stock_prec=1.05):
    df = df.loc[
        df.STRIKE >= target_strike_over_stock_prec * df.UNDERLYING_LAST,
        :,
    ].copy()
    min_strike = df.STRIKE.min()
    df = df.loc[df.STRIKE == min_strike, :].copy()
    logger.debug(
        f"filter_option_df_by_strike_over_stock: min_strike:{min_strike}, target_strike_over_stock_prec:{target_strike_over_stock_prec}"
    )
    logger.debug(f"len(df):{len(df)}")

    if len(df) == 0:
        logger.debug(
            f"No options with strike over stock price >= {target_strike_over_stock_prec}"
        )

    return df


@logger_wraps()
def filter_option_df(
    df,
    target_trade_date,
    target_strike_over_stock_prec=None,
    target_strike=None,
    target_dte=None,
    target_expiration_date=None,
):
    out = filter_option_df_by_trade_date(df=df, target_trade_date=target_trade_date)
    if target_dte is not None:
        out = filter_option_df_by_dte(df=out, target_dte=target_dte)
    if target_expiration_date is not None:
        out = filter_option_df_by_expiration_date(
            df=out, target_expiration_date=target_expiration_date
        )
    if target_strike_over_stock_prec is not None:
        out = filter_option_df_by_strike_over_stock(
            df=out, target_strike_over_stock_prec=target_strike_over_stock_prec
        )
    if target_strike is not None:
        out = filter_option_df_by_strike(df=out, target_strike=target_strike)
    out = out.squeeze()
    # logger.debug(f"df:{out}")
    return out
