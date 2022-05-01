from linkextractor import Webpage
import re
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError


class Convertor:
    # 링크 한 개에서 필요한 내용을 긁어오는 것
    def __init__(self):
        cnn_extract_tag = {'role': 'article', 'title': '', 'content': ''}
        cnbc_extract_tag = {'role': 'article', 'title': '', 'content': ''}
        dm_extract_tag = {'role': 'article', 'title': '', 'content': ''}
        guardian_extract_tag = {'role': 'article', 'title': '', 'content': ''}
        espn_extract_tag = {'role': 'article', 'title': '', 'content': ''}
        youtube_extract_tag = {'role': 'youtube', 'content': '#search'}
        self.extract_tag = {'Youtube': youtube_extract_tag,
                            'CNN': cnn_extract_tag,
                            'CNBC': cnbc_extract_tag,
                            'Daily Mail': dm_extract_tag,
                            'The Guardian': guardian_extract_tag,
                            'ESPN': espn_extract_tag}

    def extract_content(self, webpage: Webpage):

        return
