import crawler
import time

start = time.time()
crawler = crawler.Crawler()
results = crawler.startCrawl('news ko', '검수완박', 100)
# crawler.startCrawl('news en', 'champions league', 10)
for result in results:
    print(result)
print(time.time() - start)
