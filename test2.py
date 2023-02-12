# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# from selenium import webdriver
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.firefox.options import Options as FirefoxOptions

# url = "https://jimdaltontrading.com/nyse-volume/"

# options = FirefoxOptions()
# # options.add_argument("--headless")
# # options.add_argument("window-size=1280,800")
# # options.add_argument('proxy-server=106.122.8.54:3128')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

# driver = webdriver.Firefox(options=options)
# driver.get(url)

# table = driver.find_elements(By.ID, 'nysedatatable')

# df = pd.DataFrame(columns=['date', 'vol', 'yday_vol', 'diff'])

# data = []
# for row in table:

#     row_arr = str(row).split(' ')

#     print (row_arr)
#     # data.append(row.text)
#     # print(row.text)


# print(data)
# driver.close()



import yfinance as yf
from datetime import date, timedelta
import pandas as pd

ticker = '^DJI'
tk = yf.Ticker(ticker)
week_data = tk.history(period='2d', interval='30m')

today = date.today()
prev = today - timedelta(days=1)

df = pd.DataFrame(week_data, columns=['Volume'])
df.reset_index(inplace=True)

prev = (df['Datetime'].dt.date == df['Datetime'].min())
prev_df = df.loc[prev]

current = (df['Datetime'].dt.date == df['Datetime'].max())
current_df = df.loc[current]

# print(df)
# blah =current_df.to_frame().join(prev_df)
# print(blah)
print(prev_df['Volume'])
blah = current_df.join(prev_df['Volume'])
print(blah)



# df = df[df.Datetime.str.contains(str(today))]
# print(df.index)

# print(df)




