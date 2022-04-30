# 사이트별 특화 (룰기반 스크래핑 <- 현재 하고 있는 부분, DOM, 링크 분석)
# 교수님 comment news 크롤러
# 1. 신문, 잡지 등에 있는 기사 제목을 우선 순위로 읽어줌-> 제목 추출
# 2. 3번째 관련 기사 읽어줘-> 본문 추출 + a(Electra)
# 3. 관련기사 10개 정도 분석 -> 관련된 기사 추가 크롤링 or 특정 키워드 기사 검색을 원하는 수에 맞춰서 크롤링
# + a (특정 토픽에 대하여 크롤링 또한 가능하면 괜찮고
# and 한두 사이트에서 긁어오는 것은 크게 좋아하시는 것 같지는 않다 -> 많은 사이트 수작업?)

# 기타 마이크로 서비스
# 정의를 묻는 경우: wiki 앞부분
# 그 외: 구글 크롤링 후 첫 사이트 내용 추출(범용적인 html 가공 생각)
import re
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.127 Safari/537.36'}


class Article:
    def __init__(self, title, link, body=None):
        self.title = title
        self.link = link
        self.body = body
        self.rank = 0


class LinkExtractor:
    # 원하는 작업을 선택했을 때, 필요한 링크들을 수집하는 것이 목적
    def __init__(self, role, keyword):
        self.role = role
        self.keyword = keyword
        self.links = set()
        self.extract_tag = {'cnn': ('body > div.pg-search.pg-wrapper > div.pg-no-rail.pg-wrapper > div > '
                                    'div.l-container > div.cnn-search__right > div > div.cnn-search__results-list > li',
                                    ''),
                            'newyorks': ('https://www.nytimes.com/search?query=',
                                         '#site-content > div > div:nth-child(2) > div.css-46b038 > ol > li'
                                         , 'https://www.nytimes.com')}

    def getLinks(self, number=1):
        if self.role == "youtube":
            self.getYoutubeLinks(self.keyword)
        if self.role == "news":
            self.getNewsLink_bySearch(self.keyword, number)
        return self.links

    def getYoutubeLinks(self, keyword):
        base_url = 'https://www.google.com/search?q='
        keyword += 'site:youtube.com'
        keyword = re.sub(' ', '%20', keyword)
        url = base_url + keyword
        self.links.add(url)

    def getNewsLink_bySearch(self, keyword, number):
        articles = []
        base_url = self.extract_tag['newyorks'][0]
        tag = self.extract_tag['newyorks'][1]
        keyword = re.sub(' ', '%20', keyword)
        url = base_url+keyword
        try:
            get_url = requests.get(url=url, headers=header).text
        except HTTPError as e:
            return
        except URLError as e:
            return
        bs = BeautifulSoup(get_url, 'lxml')
        contents = bs.select(tag)
        for content in contents:
            link = content.find('a').attrs['href']
            title = content.find('h4')
            if link is None or title is None:
                continue
            link = self.extract_tag['newyorks'][2] + link
            title = title.text
            articles.append(Article(title, link))

        # 모아놓은 기사들을 이후, rank 기준으로 정렬 -> 숫자만큼 link 추출
        for article in articles:
            if len(self.links) == number:
                break
            self.links.add(article.link)

    # cnn 백업용
    def getNewsLink_bySearch_cnn(self, keyword, number):
        base_url = 'https://edition.cnn.com/search?size={}&q='.format(number * 2)
        keyword = re.sub(' ', '%20', keyword)
        cnn_header = header
        cnn_header['referer'] = 'https://edition.cnn.com/'
        url = base_url + keyword
        try:
            session = requests.Session()
            session.post(url=url, headers=cnn_header)
            get_url = session.get(url=url).text
        except HTTPError as e:
            return
        except URLError as e:
            return
        bs = BeautifulSoup(get_url, 'html.parser')
        tag = self.extract_tag['cnn']
        contents = bs.select(tag[0])[0]
        print(contents)
        articles = []
        for content in contents:
            link = content.find('a', href=re.compile('\/\/www.cnn.com|^((?!\/videos\/).)*$'))
            if link is None:
                continue
            title = content.find('h3').text
            article = Article(title, link)
            article.append(article)
        for article in articles:
            self.links.add(article.link)


class Convertor:
    # 링크 한 개에서 필요한 내용을 긁어오는 것
    def __init__(self):
        self.extract_tag = {'youtube': ('#search', 'www.youtube.com')}

    def extract_content(self, link, role):
        try:
            get_url = requests.get(url=link, headers=header).text
        except HTTPError as e:
            return
        except URLError as e:
            return
        bs = BeautifulSoup(get_url, 'lxml')
        content = bs.select(self.extract_tag[role][0])
        if role == 'youtube':
            content = content[0].find('a', href=re.compile('https\:\/\/www.youtube\.com'))
            result = content.attrs['href']
        elif role == 'news':
            content = ''
        return result


class Crawler:
    def startCrawl(self, role, keyword, number=1):
        # 링크 추출
        extractor = LinkExtractor(role, keyword, number)
        links = extractor.getLinks(role, keyword, number)
        results = []
        # 링크마다 결과를 저장하여 반환
        for link in links:
            print('추출 링크: {}'.format(link))
            convertor = Convertor()
            results.append(convertor.extract_content(link, role))
        return results
