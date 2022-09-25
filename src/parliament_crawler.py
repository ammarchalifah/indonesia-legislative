import gc
import os
import re
import json
import requests

from bs4 import BeautifulSoup, SoupStrainer

# Development tools
from memory_profiler import profile

class ParliamentCrawler():
    """
    API to crawl DPR's website
    """

    def __init__(self, root_url = 'https://www.dpr.go.id/', headers = None, crawler_db = 'crawler_db.json'):
        """
        Initiating the crawler
        """
        self.root_url = root_url
        self.headers = headers or {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", 
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
        self.crawler_db = crawler_db
        self.crawl_counter = 0


    def init_db(self):
        """
        Initialize external database in local filesystem to store crawled information
        """
        file = open(self.crawler_db, 'w')
        json.dump({}, file)
        file.close()
        print("Created a new crawler db at {}".format(self.crawler_db))


    def read_db(self):
        file = open(self.crawler_db, 'r')
        json_object = json.load(file)
        file.close()
        return json_object


    def write_db(self, json_object):
        file = open(self.crawler_db, 'w')
        json.dump(json_object, file)
        file.close()


    def get_page(self, url):
        """
        Get the HTML page from a URL
        """
        response = requests.get(url, headers = self.headers)
        parsed_html = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('a'))
        return parsed_html


    def extract_links(self, parsed_html):
        """
        Extract all links from a parsed HTML
        """
        links = []
        for link in parsed_html:
            if link.has_attr('href'):
                links.append(link['href'])
        return links


    def cleanup_links(self, links):
        """
        Clean-up extracted links
        """
        clean_links = []
        pathRegEx = re.compile(r'^\/.*$')
        for link in links:
            matched_string = pathRegEx.findall(link)
            if matched_string != []:
                clean_links.append(self.root_url + link)
        return clean_links

    
    def log_links(self, url, links):
        """
        Log the links into the crawler db
        """
        json_object = self.read_db()
        json_object[url] = links
        self.write_db(json_object)

    
    def crawl_page(self, url):
        """
        Crawl a page and log the result to db
        """
        parsed_html = self.get_page(url)
        links = self.extract_links(parsed_html)
        clean_links = self.cleanup_links(links)
        self.log_links(url, clean_links)


    def is_url_in_db(self, url):
        """
        Check if URL already exists in crawler db.

        True if URL already in db, false if not.
        """
        json_object = self.read_db()
        if url in json_object:
            return True
        return False

    def get_all_child_links(self):
        """
        Get all child links
        """
        json_object = self.read_db()
        child_links = []
        for key in json_object:
            child_links += json_object[key]
        return list(set(child_links))
    
    @profile
    def start_crawl(self, url = None, stop_count = None):
        """
        Start crawling from root_url
        """

        if url is None:
            url = self.root_url


        if stop_count is not None:
            if stop_count < self.crawl_counter:
                print(f"Crawl finished because of stop count {stop_count}")
                return None
        
        # Start crawling
        self.crawl_page(url)
        self.crawl_counter += 1

        # Get all child URLs from db
        child_links = self.get_all_child_links()
        next_page = None

        for c in child_links:
            if self.is_url_in_db(c):
                continue
            else:
                next_page = c
                break
        
        if next_page is None:
            print("Crawl finished.")
            return None

        self.start_crawl(next_page, stop_count)



if __name__ == "__main__":
    crawler = ParliamentCrawler(root_url = 'https://www.dpr.go.id')
    crawler.init_db()
    crawler.start_crawl(stop_count=15)