from ast import parse
import os
import requests

from bs4 import BeautifulSoup, SoupStrainer

class ParliamentCrawler():
    """
    API to crawl DPR's website
    """

    def __init__(self, url = 'https://www.dpr.go.id/', headers = None):
        """
        Initiating the crawler
        """
        self.url = url
        self.headers = headers or {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", 
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}


    def get_page(self, url):
        """
        Get the HTML page from a URL
        """
        response = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('a'))

        for link in soup:
            if link.has_attr('href'):
                print(link['href'])


if __name__ == "__main__":
    crawler = ParliamentCrawler()
    crawler.get_page('https://www.dpr.go.id')