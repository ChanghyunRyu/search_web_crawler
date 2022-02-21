from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import re


class Content:
    def __init__(self, topic, search_result, recommend=None, wiki=None):
        self.topic = topic
        self.search_result = search_result
        self.recommend = recommend
        self.wiki = wiki
        # recommend: 구글 최상단 검색 결과(존재하지 않을 수도 있음), redeem: 구글 우측 정리된 검색결과, 위키백과 검색결과(존재하지 않을 수 있음)

    def save_content_txt(self):
        txtFile = open('storage/{}.txt'.format(self.topic), 'wt+', encoding='utf-8')
        print()

    def print_content(self):
        print("----recommend----")
        print(self.recommend+'\n')
        print('------wiki-------')
        print(self.wiki+'\n')
        print('------result-----')
        for result in self.search_result:
            print(result[0])
            print(result[1]+'\n')



baseurl = "https://www.google.com/search?q="
question = "machine learning"
question = re.sub(' ', '+', question)

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get(baseurl+question)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# recommend 추출(없는 경우 존재)
recommend = soup.find(id='search').find('span', {'class': 'hgKElc'})
if recommend is not None:
    recommend = recommend.text

# 검색 결과 추출
search_results = []
results = soup.find_all('div', {'class': 'g tF2Cxc'})
for result in results:
    link = result.find('a')
    attrs = link.attrs['href']
    title = link.find('h3').text
    search_results.append((title, attrs))
    
# 위키피디아 검색 추출
keyword = "machine learning"
keyword = re.sub(' ', '_', keyword)
html = urlopen('http://en.wikipedia.org/wiki/{}'.format(keyword))
bs = BeautifulSoup(html, 'html.parser')
redeem = bs.find(id='mw-content-text').find('p')
if redeem is not None:
    redeem = redeem.text
    redeem = re.sub('\n|(\[[0-9]*\])|', '', redeem)

content = Content(question, search_result=search_results, recommend=recommend, wiki=redeem)
content.print_content()
