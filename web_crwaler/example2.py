import requests
from bs4 import BeautifulSoup
from linkextractor import LinkExtractor
from convertor import Convertor
import time

start = time.time()
linkext = LinkExtractor('news', 'daily mail')
sites = linkext.getLinks(5)
convertor = Convertor()
for site in sites:
    result = convertor.extract_content(site)
    print(site.site)
    print(result)
    break
end = time.time()
print(end-start)
