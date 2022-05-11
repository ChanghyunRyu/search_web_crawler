import requests
import re
from bs4 import BeautifulSoup
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.127 Safari/537.36'}
link = 'https://news.google.com/articles/CAIiEN6VPO8A0nhjVJ603BhYCy4qGQgEKhAIACoHCAowocv1CjCSptoCM' \
       'PvTpgU?uo=CAUicmh0dHBzOi8vd3d3LmNubi5jb20vMjAyMi8wNC8yNy9mb290YmFsbC9tYW5jaGVzdGVyLWNpdHktcmVhbC1tY' \
       'WRyaWQtY2hhbXBpb25zLWxlYWd1ZS1zZW1pZmluYWwtc3B0LWludGwvaW5kZXguaHRtbNIBAA&hl=en-US&gl=US&ceid=US%3Aen'

start = time.time()
get_url = requests.get(url=link, headers=header).text
bs = BeautifulSoup(get_url, 'lxml')
link = bs.find('a', href=re.compile('https\:\/\/www.cnn\.com')).attrs['href']
print(link)
print(time.time() - start)
