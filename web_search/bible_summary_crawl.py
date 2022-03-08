import warnings
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re

base_url = 'https://biblesummary.info/'
bible_page = ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges',
              'ruth', '1-samuel', '2-samuel', '1-kings', '2-kings', '1-chronicles', '2-chronicles',
              'ezra', 'nehemiah', 'esther', 'job', 'psalms', 'proverbs', 'ecclesiastes', 'song-of-songs',
              'isaiah', 'jeremiah', 'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah',
              'jonah', 'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai',
              'zechariah', 'malachi', 'matthew', 'mark', 'luke', 'john', 'acts', 'romans', '1-corinthians',
              '2-corinthians', 'galatians', 'ephesians', 'philippians', 'colossians', '1-thessalonians',
              '2-thessalonians', '1-timothy', '2-timothy', 'titus', 'philemon', 'hebrews', 'james', '1-peter',
              '2-peter', '1-john', '2-john', '3-john', 'jude', 'revelation']
warnings.filterwarnings(action='ignore')
driver = webdriver.Chrome()

chapters = []
summarys = []
documents = []
for page in bible_page:
    # 성경 html 크롤링
    driver.get(base_url + page)
    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')
    # 각 장 크롤링
    tweets = bs.find('div', {'class': 'column_main page_content'}).findAll('div', {'class': 'tweet'})
    for tweet in tweets:
        # extraction start
        summary = tweet.find('p', {'class': 'tweet_content'})
        summary = summary.text
        summary = re.split(':', summary)
        chapter = summary[0]
        chapter = chapter.replace('\n', '')
        summary = ':'.join(summary[1:])
        # full version 추출
        full_url = tweet.find('p', {'class': 'tweet_details'}).find('a', href=re.compile(
            '^(https?:\/\/)([^\/]*)(\.)(biblegateway\.com)(.*)'))
        full_url = full_url.attrs['href']
        driver.get(full_url)
        full_html = driver.page_source
        full_bs = BeautifulSoup(full_html, 'html.parser')
        document = full_bs.find('div', {'class': 'std-text'})
        # 텍스트 가공, (), [], 순수 번호 제거 제거
        document = document.text
        document = document.replace('\xa0', ' ')
        document = re.sub('\([A-Za-z0-9]+\)|(^[0-9]+)|\[[A-Za-z0-9]+\]', '', document)
        chapters.append(chapter)
        documents.append(document)
        summarys.append(summary)

dataframe = pd.DataFrame({'chapter': chapters, 'document': documents, 'summary': summarys})
dataframe.to_csv('storage/bible_summary.csv', encoding='utf-8')
driver.delete_all_cookies()
driver.close()
