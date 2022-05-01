from linkextractor import LinkExtractor
import time

start = time.time()
linkext = LinkExtractor('news', 'ryan Gosling')
sites = linkext.getNewsLinkBySearch('champions league', 1)
for site in sites:
    print(site.title)
end = time.time()
print(end-start)
