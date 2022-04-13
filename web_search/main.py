import webcrawlerapi
import time

start = time.time()
# link = webcrawlerapi.extract_article_link('world')
# link = webcrawlerapi.extract_youtube_link_ex('nothing left to lose')
articles = webcrawlerapi.return_article('world')
for article in articles:
    print(article[0])
    print(article[1])
    print('--------------------------------------')
end = time.time()
# print(link)
print(end-start)
