from crawler import Crawler
import time

start = time.time()
crawl = Crawler()
results = crawl.startCrawl('news', 'champions league arsenal', 5)
for result in results:
    print(result)
end = time.time()
print(end-start)
