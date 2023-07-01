from strategy import Strategy
from data_gen import get_option_data
from wallet import Wallet
import pandas as pd
import pytest
from option import Option


@pytest.fixture
def example_long_option():
    return Option(
        symbol="qqq",
        strike_price=55.0,
        stock_price_at_purchase=103.06,
        option_price_at_purchase=50.51,
        expiration_date=pd.Timestamp("2017-01-20"),
    )


@pytest.fixture
def example_short_option():
    return Option(
        symbol="qqq",
        strike_price=70.0,
        stock_price_at_purchase=103.06,
        option_price_at_purchase=33.11,
        expiration_date=pd.Timestamp("2015-01-30"),
    )


def test_strategy(example_long_option, example_short_option):
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

    assert strategy.wallet.amount == -17.4
    assert strategy.wallet.call_options_buy[0] == example_long_option
    assert strategy.wallet.call_options_sell[0] == example_short_option
