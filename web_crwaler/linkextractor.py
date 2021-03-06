import re
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import threading

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.127 Safari/537.36'}


class Webpage:
    def __init__(self, title, site, link):
        self.title = title
        self.link = link
        self.site = site
        self.rank = 0


class LinkExtractor:
    # 원하는 작업을 선택했을 때, 필요한 링크들을 수집
    def __init__(self, role, keyword):
        self.role = role
        self.keyword = keyword
        self.extract_tag = {}
        # 따로 조정 필요한 사이트: yahoo news
        self.can_site = ['CNN', 'CNBC', 'Daily Mail', 'The Guardian', 'ESPN', 'Reuters', 'CBS Sports',
                         'Space.com', 'BBC', 'PEOPLE']
        self.googleNews = {'CNN': 'https\:\/\/www.cnn\.com',
                           'CNBC': 'https\:\/\/www.cnbc\.com',
                           'Daily Mail': 'https\:\/\/www.dailymail\.co\.uk',
                           'The Guardian': 'https\:\/\/www.theguardian\.com',
                           'ESPN': 'https\:\/\/www.espn\.com',
                           'Reuters': 'https\:\/\/www.reuters\.com',
                           'CBS Sports': 'https\:\/\/www.cbssports\.com',
                           'Space.com': 'https\:\/\/www.space\.com',
                           'BBC': 'https\:\/\/www\.bbc\.com',
                           'PEOPLE': 'https\:\/\/people\.com'}
        self.extract_sites = []

    def getLinks(self, number=1):
        if self.role == "youtube":
            self.getYoutubeLinks(self.keyword)
        elif self.role == "news":
            self.getNewsLinkBySearch(self.keyword, number)
        elif self.role == 'wiki':
            self.getWikiSite(self.keyword)
        return self.extract_sites

    def getNewsLinkByTheme(self, keyword):
        return self.extract_sites

    def getYoutubeLinks(self, keyword):
        base_url = 'https://www.google.com/search?q='
        keyword += 'site:youtube.com'
        keyword = re.sub(' ', '%20', keyword)
        url = base_url + keyword
        site = Webpage(title='Youtube link', site='Youtube', link=url)
        self.extract_sites.append(site)

    def getNewsLinkBySearch(self, keyword, number):
        keyword = re.sub(' ', '%20', keyword)
        url = 'https://news.google.com/search?q={}&hl=en-US&gl=US&ceid=US%3Aen'.format(keyword)
        try:
            get_url = requests.get(url=url, headers=header).text
        except HTTPError:
            return
        except URLError:
            return
        bs = BeautifulSoup(get_url, 'lxml')
        articles = bs.find('div', {'class': 'ajwQHc BL5WZb RELBvb'}).find_all('article')
        for article in articles:
            content = article.find('h3')
            if content is None:
                continue
            title = content.text
            link = content.find('a').attrs['href']
            link = re.sub('\.', 'https://news.google.com', link)
            site = article.find('a', {'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).text
            if site in self.can_site:
                self.extract_sites.append(Webpage(title=title, site=site, link=link))
            if len(self.extract_sites) >= number:
                threads = []
                for new_site in self.extract_sites:
                    t = threading.Thread(target=self.convertGoogleNews, args=(new_site, ))
                    t.start()
                    threads.append(t)
                for thread in threads:
                    thread.join()
                return
        if len(self.extract_sites) < number:
            cnn_keyword = 'cnn%20' + keyword
            self.getNewsLinkBySearch(cnn_keyword, number)

    def convertGoogleNews(self, webpage: Webpage):
        link = webpage.link
        get_url = requests.get(url=link, headers=header).text
        bs = BeautifulSoup(get_url, 'lxml')
        new_link = bs.find('a', href=re.compile(self.googleNews[webpage.site])).attrs['href']
        webpage.link = new_link

    def getWikiSite(self, keyword):
        self.extract_sites.append(Webpage('wikipedia', 'wikipedia', keyword))
