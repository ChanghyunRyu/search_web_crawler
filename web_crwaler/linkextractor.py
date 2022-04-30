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
    # 원하는 작업을 선택했을 때, 필요한 링크들을 수집
    def __init__(self, role, keyword):
        self.role = role
        self.keyword = keyword
        self.links = set()
        self.extract_tag = {}

