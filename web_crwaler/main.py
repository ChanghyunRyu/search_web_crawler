import webscraper
import time
from selenium import webdriver
import chromedriver_autoinstaller as AutoChrome


start = time.time()
extract = webscraper.LinkExtractor('news', 'champions league')
print(extract.getLinks(5))
crawler = webscraper.Crawler()

end = time.time()
print(end-start)

