import pandas as pd
import datetime as dt
from wallet import Wallet
from option import Option


start_date = 0
trading_date = 3
experation_date = 12
future_date = 50

data_path = "./data/2015/qqq_eod_201501.txt"


df = pd.read_csv(data_path)

df.rename(
    columns={
        "[QUOTE_UNIXTIME]": "QUOTE_UNIXTIME",
        " [QUOTE_READTIME]": "QUOTE_READTIME",
        " [QUOTE_DATE]": "QUOTE_DATE",
        " [QUOTE_TIME_HOURS]": "QUOTE_TIME_HOURS",
        " [UNDERLYING_LAST]": "UNDERLYING_LAST",
        " [EXPIRE_DATE]": "EXPIRE_DATE",
        " [EXPIRE_UNIX]": "EXPIRE_UNIX",
        " [DTE]": "DTE",
        " [C_DELTA]": "C_DELTA",
        " [C_GAMMA]": "C_GAMMA",
        " [C_VEGA]": "C_VEGA",
        " [C_THETA]": "C_THETA",
        " [C_RHO]": "C_RHO",
        " [C_IV]": "C_IV",
        " [C_VOLUME]": "C_VOLUME",
        " [C_LAST]": "C_LAST",
        " [C_SIZE]": "C_SIZE",
        " [C_BID]": "C_BID",
        " [C_ASK]": "C_ASK",
        " [STRIKE]": "STRIKE",
        " [P_BID]": "P_BID",
        " [P_ASK]": "P_ASK",
        " [P_SIZE]": "P_SIZE",
        " [P_LAST]": "P_LAST",
        " [P_DELTA]": "P_DELTA",
        " [P_GAMMA]": "P_GAMMA",
        " [P_VEGA]": "P_VEGA",
        " [P_THETA]": "P_VEGA",
        " [P_RHO]": "P_RHO",
        " [P_IV]": "P_IV",
        " [P_VOLUME]": "P_VOLUME",
        " [STRIKE_DISTANCE]": "STRIKE_DISTANCE",
        " [STRIKE_DISTANCE_PCT]": "STRIKE_DISTANCE_PCT",
    },
    inplace=True,
)

d_df = df[["QUOTE_DATE", "UNDERLYING_LAST", "EXPIRE_DATE", "DTE", "STRIKE", "C_ASK"]]


poor_wallet = Wallet()
