import wikipediaapi
import threading
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import chromedriver_autoinstaller as AutoChrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# selenium option.
AutoChrome.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('disable-gpu')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-extensions')
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins' : 2, 'popups': 2,
                                                    'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2,
                                                    'fullscreen': 2, 'mouselock' : 2, 'mixed_script': 2,
                                                    'media_stream': 2, 'media_stream_mic': 2, 'media_stream_camera': 2,
                                                    'protocol_handlers': 2, 'ppapi_broker': 2, 'automatic_downloads': 2,
                                                    'midi_sysex': 2, 'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                    'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
chrome_options.add_experimental_option('prefs', prefs)
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = 'eager'

not_extract = ['See also', 'References', 'Sources', 'Further reading', 'External links']
wiki_en = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
article_tag = {'sport': ('http://edition.cnn.com/', ['div.zone__inner'], ''),
               'entertainment': ('http://edition.cnn.com/', ['#entertainment-zone-1', '#entertainment-zone-2'],
                                 'http://edition.cnn.com'),
               'tech': ('http://edition.cnn.com/business/', ['#tech-zone-1', '#tech-zone-2'], 'https://edition.cnn.com'),
               'business': ('http://edition.cnn.com/',
                            ['#us-zone-1 > div.l-container > div > div.column.zn__column--idx-1',
                             '#us-zone-1 > div.l-container > div > div.column.zn__column--idx-0'],
                            'http://edition.cnn.com'),
               'health': ('http://edition.cnn.com/',
                          ['#health-zone-1 > div.l-container > div > div.column.zn__column--idx-1'],
                          'http://edition.cnn.com'),
               'world': ('https://edition.cnn.com/', ['#world-zone-1',
                                                      '#world-zone-2'], 'https://edition.cnn.com')}


# wikipedia crawling
def extract_paragraph(keyword, paragraphs):
    keyword = re.sub(' ', '_', keyword)
    page = wiki_en.page(keyword)
    if page.exists():
        # 여러 뜻이 존재하는지 체크
        if check_multi_meaning(page.summary):
            link_list = extract_link(keyword)
            paragraph = return_summary(link_list)
            paragraphs.append(paragraph)
        else:
            sessions = page.sections
            paragraph = []
            for s in sessions:
                if s.title not in not_extract:
                    paragraph.append(page.section_by_title(s.title).text)
            paragraph = '. '.join(paragraph)
            paragraphs.append(paragraph)


def extract_summary(keyword, paragraphs):
    keyword = re.sub(' ', '_', keyword)
    page = wiki_en.page(keyword)
    if page.exists():
        if check_multi_meaning(page.summary):
            link_list = extract_link(keyword)
            paragraph = return_summary(link_list)
            paragraphs.append(paragraph)
        else:
            summary = page.summary
            paragraphs.append(summary)


def return_paragraph(keywords):
    # input: keyword list ex)['Bible', 'machine learning', 'key']
    # output: ['paragraph', 'paragraph', ['summary', 'summary', ...](뜻이 여러개인 경우)]
    paragraphs = []
    threads = []
    for keyword in keywords:
        t = threading.Thread(target=extract_paragraph, args=(keyword, paragraphs))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    return paragraphs


def return_summary(keywords):
    # 여러 키워드의 summary 반환
    # input: keyword list ex)['Bible', 'machine learning', 'key']
    # output: ['summary', 'summary', ['summary', 'summary', ...](뜻이 여러개인 경우)]
    summarys = []
    threads = []
    for keyword in keywords:
        t = threading.Thread(target=extract_summary, args=(keyword, summarys))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    return summarys


def check_multi_meaning(keyword_summary):
    # 뜻이 여러개인지 체크
    return keyword_summary.endswith('may refer to:')


def extract_link(keyword):
    # 뜻이 여러개인 keyword 입력 시 해당 링크 리스트를 반환
    result = []
    html = urlopen('https://en.wikipedia.org/wiki/'+keyword)
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find(id='mw-content-text').findAll('a', href=re.compile('^(/wiki/)'))
    for link in links:
        link = link.attrs['href']
        link = re.sub('/wiki/', '', link)
        result.append(link)
    return result


# youtube crawling
def extract_youtube_link(search_word):
    search_word = re.sub(' ', '+', search_word)
    url = 'https://www.youtube.com/results?search_query='+search_word
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options, desired_capabilities=caps)
    driver.get(url)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    search_results = bs.find('div', id='contents').find('ytd-video-renderer')
    result = search_results.find('a', id='thumbnail').attrs['href']
    result = 'https://www.youtube.com'+result
    driver.quit()
    return result


# News crawling(CNN)
def return_article(subject):
    link_list = extract_article_link(subject)
    articles = []
    threads = []
    for link in link_list:
        t = threading.Thread(target=extract_article_cnn, args=(link, articles))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    return articles


def extract_article_cnn(link, article_list):
    try:
        html = urlopen(link)
    except HTTPError as e:
        print(e)
        return
    except URLError:
        return
    bs = BeautifulSoup(html, 'lxml')
    title = bs.find('h1', {'class': 'pg-headline'}).text
    article = bs.find('div', {'itemprop': 'articleBody'}).find('section', {'id': 'body-text'}).text
    article_list.append((title, article))
    return


def extract_article_link(subject, num=5):
    base_url = article_tag[subject][0]
    link_list = set()
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options, desired_capabilities=caps)
    driver.get(base_url+subject)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    tags = article_tag[subject][1]
    plus_site = article_tag[subject][2]
    flag = False
    for tag in tags:
        temp_list = bs.select(tag)
        for temp in temp_list[0].findAll('a'):
            if 'href' in temp.attrs:
                site = plus_site+temp.attrs['href']
                if not site == base_url+subject:
                    link_list.add(site)
                if len(link_list) == num:
                    flag = True
                if flag:
                    break
        if flag:
            break
    driver.quit()
    link_list = list(link_list)
    return link_list


def return_article_by_keyword(keyword):
    base_url = 'https://edition.cnn.com/search?q='

    return
