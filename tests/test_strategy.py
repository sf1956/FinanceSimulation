from strategy import Strategy
from data_gen import get_option_data
from wallet import Wallet
import pandas as pd
import pytest
from option import Option
from loguru import logger


@pytest.fixture
def example_long_option():
    return Option(
        symbol="qqq",
        strike_price=104.0,
        stock_price_at_purchase=103.06,
        option_price_at_purchase=11.1,
        expiration_date=pd.Timestamp("2017-01-20"),
    )


@pytest.fixture
def example_short_option():
    return Option(
        symbol="qqq",
        strike_price=108.5,
        stock_price_at_purchase=103.06,
        option_price_at_purchase=0.13,
        expiration_date=pd.Timestamp("2015-01-30"),
    )


def test_strategy(example_long_option: Option, example_short_option: Option):
    d_df = get_option_data()
    poor_wallet = Wallet()
    strategy = Strategy(
        d_df,
        poor_wallet,
        pd.Timestamp("2015-01-02"),
        short_target_dte=30,
        long_target_dte=750,
        short_target_strike_over_stock_prec=1.05,
        long_target_strike_over_stock_prec=1.0,
        daily_option_prec=0.5,
    )

    assert strategy.wallet.amount == pytest.approx(-11.1 + 0.13, 0.05)
    logger.info(
        f"strategy.wallet.call_options_buy[0]:{strategy.wallet.call_options_buy[0]}"
    )
    logger.info(f"example_long_option:{example_long_option}")
    assert strategy.wallet.call_options_buy[0] == example_long_option
    assert strategy.wallet.call_options_sell[0] == example_short_option
