import pandas as pd
import datetime as dt


def get_option_data(month=1, year=2015, cols=None):
    cols = (
        ["QUOTE_DATE", "UNDERLYING_LAST", "EXPIRE_DATE", "DTE", "STRIKE", "C_ASK"]
        if cols is None
        else cols
    )
    data_path = f"./data/{year}/qqq_eod_{year}{month:02}.txt"

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

    # d_df is a decim   ated DF with the required columns

    d_df = df[cols]

    d_df.loc[:, "QUOTE_DATE"] = d_df.QUOTE_DATE.str.strip().copy()

    d_df.loc[:, "EXPIRE_DATE"] = d_df.EXPIRE_DATE.str.strip().copy()

    return d_df
