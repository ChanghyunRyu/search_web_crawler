from linkextractor import LinkExtractor

linkext = LinkExtractor('news', 'champions league')
print(linkext.getLinks(5))
