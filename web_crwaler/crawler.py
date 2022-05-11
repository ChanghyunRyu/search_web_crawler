from linkextractor import LinkExtractor, Webpage
from convertor import Convertor
import threading


class Crawler:
    def __init__(self):
        self.results = []

    def startCrawl(self, role, keyword, number=1):
        self.results = []
        threads = []
        webpages = LinkExtractor(role, keyword).getLinks(number)
        for webpage in webpages:
            t = threading.Thread(target=self.startConvertor, args=(webpage, ))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        return self.results

    def startConvertor(self, webpage: Webpage):
        convertor = Convertor()
        self.results.append(convertor.extract_content(webpage))
