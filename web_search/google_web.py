from bs4 import BeautifulSoup
from selenium import webdriver
import re


class Content:
    def __init__(self, topic, search_result, recommend=None, redeem=None):
        self.topic = topic
        self.search_result = search_result
        self.recommend = recommend
        self.redeem = redeem
        # recommend: 구글 최상단 검색 결과(존재하지 않을 수도 있음), redeem: 구글 우측 정리된 검색결과, 위키백과 검색결과(존재하지 않을 수 있음)

    def save_content_txt(self):
        txtFile = open('storage/{}.txt'.format(self.topic), 'wt+', encoding='utf-8')
        print()

    def print_content(self):
        print("----recommend----")
        if self.recommend is not None:
            print(self.recommend)
        else:
            print('None')
        print('\n-----redeem-------')
        if self.redeem is not None:
            print(self.redeem)
        else:
            print('None')
        print('\n------result-----')
        for result in self.search_result:
            print(result[0])
            print(result[1]+'\n')


if __name__ == '__main__':
    baseurl = "https://www.google.com/search?q="
    question = 'what is captain america?'
    question = re.sub(' ', '+', question)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(baseurl + question)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # recommend 추출(없는 경우 존재)
    recommend = soup.find(id='search').find('div', {'data-tts': 'answers'})
    if recommend is not None:
        recommend = recommend.text
    elif soup.find(id='search').find('div', {'role': 'heading'}) is not None:
        recommend = soup.find(id='search').find('div', {'role': 'heading'})
        recommend = recommend.text
    else:
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

    # 오른쪽 검색 추출
    redeem = soup.find('div', {'class': 'SzZmKb'})
    if redeem is not None:
        redeem = redeem.find('h2')
        redeem = redeem.text

    content = Content(question, search_result=search_results, recommend=recommend, redeem=redeem)
    content.print_content()
    # 정답출력에 대한 생각: redeem -> 단답형이 정답, recommend-> 설명이 정답(단 recommend 에서도 간단한 답이 정답인 경우가 있음.)
    # 만약 해당 자료형을 만들 수 있다면, 이진 분류기 학습을 시키는 것이 가능할 것으로 보임(json 파일).
    # json 데이터의 경우, 단답형 답변이 대부분을 차지하는 것으로 보임. -> 데이터셋이 편향될 것.
    # redeem 과 recommend 가 둘다 존재할 때, recommend 가 정답인 경우: recommend 가 redeem 의 설명인 경우
