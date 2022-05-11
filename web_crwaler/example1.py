from linkextractor import LinkExtractor
import time

start = time.time()
linkext = LinkExtractor('news', 'champions league')
sites = linkext.getLinks(5)
for site in sites:
    print(site.title)
    print(site.link)
end = time.time()
print(end-start)
