import webcrawlerapi
import time

start = time.time()
# link = webcrawlerapi.extract_article_link('world')
# link = webcrawlerapi.extract_youtube_link_ex('nothing left to lose')
link = webcrawlerapi.return_paragraph(['machine learning'])
end = time.time()
print(link)
print(end-start)
