import crawler
import time

start = time.time()
crawler = crawler.Crawler()
# 한국 기사 크롤 예시
# results = crawler.startCrawl('news ko', '검수완박', 10)
# 해외 기사 크롤 예시
# results = crawler.startCrawl('news en', 'golden boots winner in news', 15)
# 유튜브 예시
# result = crawler.startCrawl('youtube', 'Hall of Fame')
# 구글 검색 예시
results = crawler.startCrawl('google search', 'what is transformer bert')
for result in results:
    print(result)
print(time.time() - start)
