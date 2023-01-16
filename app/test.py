import yfinance as yf
import json
import pandas as pd
import numpy as np
import datetime
from table2ascii import table2ascii as t2a, PresetStyle


def clean_up_field(field, round_field: int = 2) -> str:
    return round((field[0]), round_field)

ticker = 'META'
tk = yf.Ticker(ticker)

todayData = tk.history(period='1d')

exps = list(tk.options)

print(exps)

blah = []
for index, e in enumerate(exps):
    if (index == 0):
        blah.append(e)

exps = exps[0]

options = pd.DataFrame()
for e in blah:
    opt = tk.option_chain(e)
    limit = 5
    current = clean_up_field(todayData['Close'])

    # get closet strike to current close
    closest_strike_calls = opt.calls.iloc[(opt.calls['strike']-round(current)).abs().argsort()[:1]].index.values.astype(int)[0]
    limited_calls = opt.calls.iloc[closest_strike_calls-limit:closest_strike_calls+limit]

    closest_strike_puts = opt.puts.iloc[(opt.puts['strike']-round(current)).abs().argsort()[:1]].index.values.astype(int)[0]
    limited_puts = opt.puts.iloc[closest_strike_puts-limit:closest_strike_puts+limit]

    opt = pd.concat([limited_calls, limited_puts])

    print(opt.shape)
    opt['expirationDate'] = e
    options = pd.concat([opt], ignore_index=True)
    
    # yfinance returns incorrect date, add 1 day for correct exp
    options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days=1)

    options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
    options['CALL'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)

    # mid-point
    options['mark'] = (options['bid'] + options['ask']) / 2 
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'lastTradeDate', 'lastPrice'])

    # print(options.to_markdown(index=False))



o = clean_up_field(todayData['Open'])
h = clean_up_field(todayData['High'])
l = clean_up_field(todayData['Low'])
c = clean_up_field(todayData['Close'])
current = clean_up_field(todayData['Close'])
output = t2a(
    header=["Instrument", "Current", "Open", "High", "Low", "Close"],
    body=[[ticker, current, o, h, l, c]],
    first_col_heading=True
)

# print(f"```\n{output}\n```")

# print(json.dumps(getFb.info, indent=3))

# print(getFb.history(period='1d'))

