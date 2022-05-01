import requests
from bs4 import BeautifulSoup

site = 'https://www.cnbc.com/2022/04/30/russia-ukraine-live-updates.html'
get_url = requests.get(url=site).text
bs = BeautifulSoup(get_url, 'html.parser')
print(bs)
