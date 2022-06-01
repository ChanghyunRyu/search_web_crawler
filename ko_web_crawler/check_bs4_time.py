from bs4 import BeautifulSoup
import time
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.127 Safari/537.36'}

start = time.time()
keyword = 'who is the president of korea'
url = 'https://news.google.com/search?q={}&hl=en-US&gl=US&ceid=US%3Aen'.format(keyword)
get_url = requests.get(url=url, headers=header).text
bs = BeautifulSoup(get_url, 'lxml')
bodys = bs.find('div', {'class': 'ajwQHc BL5WZb RELBvb'}).find_all('article')
for body in bodys:
    content = body.find('h3')
    if content is not None:
        print(content.text)
end = time.time()
print('Time is get: {}'.format(end-start))