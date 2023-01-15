import sqlite3
from datetime import date
import utils
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By

# init db, create if not created
con = sqlite3.connect("bot.db")

# create calender table
cur = con.cursor()
try:
    cur.execute("CREATE TABLE calender(date, time, currency, news, actual, forecast, previous)")
except Exception as e:
    print('already exists')

today = date.today()

driver = webdriver.Firefox()
try:
    driver.get("http://www.forexfactory.com")
    # Get the table
    table = driver.find_element(By.CLASS_NAME, "calendar__table")
    # Iterate over each table row
    for row in table.find_elements(By.TAG_NAME, "tr"):
        # list comprehension to get each cell's data and filter out empty cells
        row_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))
        if row_data == []:
            continue

        if 'USD' in row_data:
            prev_time = '0'
            # data is messed up, look for numbers in first i of arr
            if utils.has_numbers(row_data[0]):
                time = row_data[0]
                prev_time = time
            else:
                time = prev_time
            
            news = row_data[2]
            previous = row_data[len(row_data) - 1]

            # check for forecast
            if utils.has_numbers(row_data[len(row_data) - 2]):
                forecast = row_data[len(row_data) - 2]

            print(time)
            print(news)
            print(forecast)
            print(previous)
except Exception as e:
    print(e)
finally:
    driver.quit()