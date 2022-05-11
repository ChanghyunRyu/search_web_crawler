from linkextractor import Webpage
import re
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import wikipediaapi
import threading

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.127 Safari/537.36'}


class Convertor:
    # 링크 한 개에서 필요한 내용을 긁어오는 것
    def __init__(self):
        self.not_extract = ['See also', 'References', 'Sources', 'Further reading', 'External links']
        self.wiki_en = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
        cnn_extract_tag = {'role': 'article',
                           'title': 'body > div.pg-right-rail-tall.pg-wrapper > article > div.l-container > h1',
                           'content': '#body-text'}
        cnbc_extract_tag = {'role': 'article',
                            'title': '#main-article-header > div > div.ArticleHeader-wrapperHeroNoImage.ArticleHeader'
                                     '-wrapperHero.ArticleHeader-wrapper.ArticleHeader-wrapperNoImage > '
                                     'div:nth-child(2) > h1',
                            'content': '#RegularArticle-ArticleBody-5'}
        dm_extract_tag = {'role': 'article',
                          'title': '#js-article-text > h2',
                          'content': '#js-article-text'}
        guardian_extract_tag = {'role': 'article',
                                'title': 'body > main > article > div > div > div.dcr-1nupfq9',
                                'content': 'body > main > article > div > div > div.dcr-185kcx9'}
        espn_extract_tag = {'role': 'article',
                            'title': '#article-feed > article:nth-child(1) > div > header',
                            'content': '#article-feed > article:nth-child(1) > div > div.article-body > p'}
        reuters_extract_tag = {'role': 'article',
                               'title': '#main-content > article > div > header > div > '
                                        'div.article-header__heading__15OpQ > h1',
                               'content': '#main-content > article > div > div > div > '
                                          'div.article-body__content__17Yit.paywall-article > p'}
        cbssports_extract_tag = {'role': 'article',
                                 'title': '#article0 > article > div.Article-head > h1',
                                 'content': '#Article-body > div.Article-bodyContent > p'}
        spacecom_extract_tag = {'role': 'article',
                                'title': '#main > article > header > h1',
                                'content': '#article-body > p'}
        bbc_extract_tag = {'role': 'article',
                           'title': '#main-heading',
                           'content': '#main-content > div.ssrcss-1ocoo3l-Wrap.e42f8511 > div > '
                                      'div.ssrcss-rgov1k-MainColumn.e1sbfw0p0 > article'}
        people_extract_tag = {'role': 'article',
                              'title': 'body > div.container-full-width.clearfix.template-two-col.karma-below-banner'
                                       '.with-sidebar-right.karma-below-banner.karma-site-container > main > article '
                                       '> div.articleContainer.karma-sticky-grid > div.articleContainer__header > div '
                                       '> div.intro.article-info > div > h1',
                              'content': 'body > div.container-full-width.clearfix.template-two-col.karma-below'
                                         '-banner.with-sidebar-right.karma-below-banner.karma-site-container > main > '
                                         'article > div.articleContainer.karma-sticky-grid'}

        youtube_extract_tag = {'role': 'youtube', 'content': '#search'}
        wiki_extract_tag = {'role': 'wiki'}
        self.extract_tag_en = {'Youtube': youtube_extract_tag,
                               'CNN': cnn_extract_tag,
                               'CNBC': cnbc_extract_tag,
                               'Daily Mail': dm_extract_tag,
                               'The Guardian': guardian_extract_tag,
                               'ESPN': espn_extract_tag,
                               'Reuters': reuters_extract_tag,
                               'CBS Sports': cbssports_extract_tag,
                               'Space.com': spacecom_extract_tag,
                               'BBC': bbc_extract_tag,
                               'PEOPLE': people_extract_tag}

    def extract_content(self, webpage: Webpage):
        try:
            get_url = requests.get(url=webpage.link, headers=header).text
        except HTTPError or URLError:
            return
        bs = BeautifulSoup(get_url, 'lxml')
        extract_tag = self.extract_tag_en[webpage.site]
        if extract_tag['role'] == 'article':
            title = bs.select(extract_tag['title'])
            bodies = bs.select(extract_tag['content'])
            if webpage.site == 'Daily mail':
                bodies = bodies[0].find('div', {'itemprop': 'articleBody'}).find_all('p')
            elif webpage.site == 'BBC':
                divs = bodies[0].find_all('div', {'data-component': 'text-block'})
                bodies = []
                for div in divs:
                    bodies.append(div.find('p'))
            elif webpage.site == 'PEOPLE':
                divs = bodies[0].find_all('div', {'class': 'articleContainer__content'})
                bodies = []
                for div in divs:
                    ps = div.find_all('p')
                    if len(ps) == 0:
                        continue
                    for p in ps:
                        bodies.append(p)
            if len(title) == 0 or len(bodies) == 0:
                return
            title = title[0].text
            content = ''
            for body in bodies:
                content += body.text + ' '
            content = self.preprocessingArticle(content)
            title = self.preprocessingArticle(title)
            return {'site': webpage.site, 'title': title, 'content': content}
        elif extract_tag['role'] == 'youtube':
            content = bs.select(extract_tag['content'])
            content = content[0].find('a', href=re.compile('https\:\/\/www.youtube\.com'))
            return content.attrs['href']
        elif extract_tag['role'] == 'wiki':
            return self.extract_wikipedia(webpage)

    # 추출한 기사 본문의 쓸모 없는 내용 가공(미구현)
    @staticmethod
    def preprocessingArticle(content):
        content = re.sub('\n|\xa0|\t', '', content)
        content = re.sub('  ', '', content)
        content.replace("\\", "")
        return content

    def extract_wikipedia(self, webpage: Webpage):
        keyword = webpage.link
        page = self.wiki_en.page(keyword)
        if page.exists():
            if self.check_multi_meaning(page.summary):
                link_list = self.extract_link_wiki(keyword)
                paragraph = self.return_wiki_summary(link_list)
                return paragraph
            else:
                sessions = page.sections
                paragraph = []
                for s in sessions:
                    if s.title not in self.not_extract:
                        paragraph.append(page.section_by_title(s.title).text)
                    paragraph = '. '.join(paragraph)
                    return paragraph

    def check_multi_meaning(self, keyword_summary):
        return keyword_summary.endswith('may refer to:')

    def extract_link_wiki(self, keyword):
        result = []
        html = requests(url='https://en.wikipedia.org/wiki/' + keyword, headers=header)
        bs = BeautifulSoup(html, 'lxml')
        links = bs.find(id='mw-content-text').findAll('a', href=re.compile('^(/wiki/)'))
        for link in links:
            link = link.attrs['href']
            link = re.sub('/wiki/', '', link)
            result.append(link)
        return result

    def return_wiki_summary(self, keywords):
        summarys = []
        threads = []
        for keyword in keywords:
            t = threading.Thread(target=self.extract_wiki_summary, args=(keyword, summarys))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        return summarys

    def extract_wiki_summary(self, keyword, paragraphs):
        keyword = re.sub(' ', '_', keyword)
        page = self.wiki_en.page(keyword)
        if page.exists():
            if self.check_multi_meaning(page.summary):
                link_list = self.extract_link_wiki(keyword)
                paragraph = self.return_wiki_summary(link_list)
                paragraphs.append(paragraph)
            else:
                summary = page.summary
                paragraphs.append(summary)
