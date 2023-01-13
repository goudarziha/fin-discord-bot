import requests
from bs4 import BeautifulSoup

FOREX_FACTORY_URL = 'https://www.forexfactory.com'

page = requests.get(FOREX_FACTORY_URL)
print(page)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("table")

print(results)