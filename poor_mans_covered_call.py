import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


"""
FUNCTIONS Section
"""

def extract_rows_with_columns_equal_to_a_certain_value(df, column_name, value):

  """
  Creates a dataframe of rows with columns equal to a certain value in another.

  Args:
    df: The dataframe to be filtered.
    column_name: The name of the column to be checked for value.
    value: The value to be filtered for.

  Returns:
    A dataframe of the rows in df where the column_name column is equal to value.
  """

  filtered_df = df[df[column_name] == value]
  return filtered_df

##########################################################

def return_min_lt_A_in_col_X(df, A, X):
    
  """

This function calculates the smallest value which is larger than A in column X of a DataFrame.

Args:
    df (pandas.DataFrame): The original DataFrame.
    A (int): The value of A.
    X (str): The name of the column X.

Returns:
    float: The smallest value.
  """

    # Calculate the smallest value in column X that is larger than A.

  sm_lt_A = df[X].where(df[X] > A).min()


# Return the value.

  return sm_lt_A

###################################################

"""
This function creates a DataFrame from an original DataFrame of rows with the smallest value which is larger than A in column X.

Args:
    df (pandas.DataFrame): The original DataFrame.
    A (int): The value of A.
    X (str): The name of the column X.

Returns:
    pandas.DataFrame: The filtered DataFrame.
"""

def create_df_with_smalles_value_larger_then_A_of_column_X(df, A, X):

    # Calculate the smallest value in column X that is larger than A.

    smallest_values = df[X].where(df[X] > A).min()

    # Filter the original DataFrame to only include the rows where the value in column X is equal to the smallest value.
    filtered_df = df[df[X] == smallest_values]

    # Return the filtered DataFrame.
    return filtered_df

############################################################


def calculate_date(date_str, days):

    # Convert the date string to a datetime object.
    date = dt.datetime.strptime(date_str, "%Y-%m-%d")

    # Add the specified number of days to the datetime object.
    new_date = date + dt.timedelta(days=days)

    # Return the new date in the same format as the original date string.
    return new_date.strftime("%Y-%m-%d")

##################################

def save_dataframe_to_csv(df, filename):

    # Save the DataFrame to a CSV file.
    df.to_csv(filename, index=False)

#######################################################

# End FUNCTIONS Section

# read data to DF

df = pd.read_csv('./data/2015/qqq_eod_201501.txt')

df.rename(columns={'[QUOTE_UNIXTIME]':'QUOTE_UNIXTIME', ' [QUOTE_READTIME]':'QUOTE_READTIME', ' [QUOTE_DATE]':'QUOTE_DATE',
       ' [QUOTE_TIME_HOURS]':'QUOTE_TIME_HOURS', ' [UNDERLYING_LAST]':'UNDERLYING_LAST', ' [EXPIRE_DATE]':'EXPIRE_DATE',
       ' [EXPIRE_UNIX]':'EXPIRE_UNIX', ' [DTE]':'DTE', ' [C_DELTA]':'C_DELTA', ' [C_GAMMA]':'C_GAMMA', ' [C_VEGA]':'C_VEGA',
       ' [C_THETA]':'C_THETA', ' [C_RHO]':'C_RHO', ' [C_IV]':'C_IV', ' [C_VOLUME]':'C_VOLUME', ' [C_LAST]':'C_LAST',
       ' [C_SIZE]':'C_SIZE', ' [C_BID]':'C_BID', ' [C_ASK]':'C_ASK', ' [STRIKE]':'STRIKE', ' [P_BID]':'P_BID',
       ' [P_ASK]':'P_ASK', ' [P_SIZE]':'P_SIZE', ' [P_LAST]':'P_LAST', ' [P_DELTA]':'P_DELTA', ' [P_GAMMA]':'P_GAMMA',
       ' [P_VEGA]':'P_VEGA', ' [P_THETA]':'P_VEGA', ' [P_RHO]':'P_RHO', ' [P_IV]':'P_IV', ' [P_VOLUME]':'P_VOLUME',
       ' [STRIKE_DISTANCE]':'STRIKE_DISTANCE', ' [STRIKE_DISTANCE_PCT]':'STRIKE_DISTANCE_PCT'}, inplace=True)

# d_df is a decimated DF with the required columns

d_df = df[['QUOTE_DATE', 'UNDERLYING_LAST', 'EXPIRE_DATE', 'DTE', 'STRIKE', 'C_ASK']]

class Option(object):
      def __init__(self, symbol='qqq', strike_price=100, stock_price=100, option_price=10, expiration_date=dt.date.fromisoformat('2023-12-04')):
        self.symbol = symbol
        self.strike_price = strike_price
        self.stock_price = stock_price
        self.option_price = option_price
        self.expiration_date = expiration_date


# clear white spaces of dates columns

d_df.QUOTE_DATE = d_df.QUOTE_DATE.str.strip()

d_df.EXPIRE_DATE = d_df.EXPIRE_DATE.str.strip()


# change to rolling date !!!!

trade_date = d_df.loc[0, 'QUOTE_DATE']
initial_stock_price = d_df.loc[0, 'UNDERLYING_LAST']

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
""" 
Sell (Write) Call Option Section
"""
# DTE for sell option is the DTE >= value A

# find expiration date

# A is the upper limit of the desired number of days to expiration_date

A=30

DTE = return_min_lt_A_in_col_X(d_df, A, 'DTE')

expiration_date = calculate_date(trade_date, DTE-3)     #check why this is correct!!!!

# extract df with the calculated expiration_date

df_expiration_date = extract_rows_with_columns_equal_to_a_certain_value(d_df, 'EXPIRE_DATE', expiration_date)

#calculate Strike price

Target_strike_stock_price_PCT = 0.05
target_strike_price = initial_stock_price * (1 + Target_strike_stock_price_PCT)
strike_price = return_min_lt_A_in_col_X(df_expiration_date, target_strike_price, 'STRIKE')

# Create df of rows with strike_price in 'STRIKE' column

df_strike = extract_rows_with_columns_equal_to_a_certain_value(df_expiration_date, 'STRIKE', strike_price)

#reset the indec of df_strike

df_strike.reset_index(drop=True, inplace=True)

"""
Option_Sell = Option(strike_price=df_strike.loc[0,'STRIKE'],
                    stock_price=df_strike.loc[0,'UNDERLYING_LAST'],
                    option_price=df_strike.loc[0,'C_LAST'],
                    expiration_date=df_strike.loc[0,'EXPIRE_DATE'])


# Save the DataFrame to a CSV file called "dataframe.csv".
save_dataframe_to_csv(d_df, "./data/dataframe.csv")

"""
"""
plt.plot(df_strike['C_ASK'])
plt.show()
plt.plot(df_strike['UNDERLYING_LAST'])
plt.show()
print(Option_Sell)
"""
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

""" 
Buy Call Option Section
"""
# DTE for sell option is the DTE >= value A

# find expiration date

# A is the upper limit of the desired number of days to expiration_date

A=700

DTE = return_min_lt_A_in_col_X(d_df, A, 'DTE')

expiration_date = calculate_date(trade_date, DTE+28)     #check why this is correct!!!!

# extract df with the calculated expiration_date

df_expiration_date = extract_rows_with_columns_equal_to_a_certain_value(d_df, 'EXPIRE_DATE', expiration_date)

#calculate Strike price

Target_strike_stock_price_PCT = 0
target_strike_price = initial_stock_price * (1 + Target_strike_stock_price_PCT)
strike_price = return_min_lt_A_in_col_X(df_expiration_date, target_strike_price, 'STRIKE')

# Create df of rows with strike_price in 'STRIKE' column

df_strike = extract_rows_with_columns_equal_to_a_certain_value(df_expiration_date, 'STRIKE', strike_price)

#reset the indec of df_strike

df_strike.reset_index(drop=True, inplace=True)


# plot option & stock price

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(df_strike['C_BID'])
axs[0].set_title('Buy Call Option Price')
axs[0].grid(True)
axs[1].plot(df_strike['UNDERLYING_LAST'])
axs[1].set_title('Stock Price')
axs[1].grid(True)
plt.show()



