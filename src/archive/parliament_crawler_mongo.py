import gc
import os
import re
import requests
import pymongo

from bs4 import BeautifulSoup, SoupStrainer

# Development tools
from memory_profiler import profile


class ParliamentCrawler():
    """
    API to crawl DPR's website
    """

    def __init__(self, root_url = 'https://www.dpr.go.id/', headers = None, crawler_db_host = 'mongodb://localhost:27017'):
        """
        Initiating the crawler
        """
        self.root_url = root_url
        self.headers = headers or {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", 
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

        # Crawler helper
        self.crawl_counter = 0
        self.crawl_child_links = []

        # Database attributes
        self.crawler_db_host = crawler_db_host
        self.mongodb_client = None
        self.mongodb_db = None
        self.mongodb_coll = None


    def init_db(self):
        """
        Initialize external database in local filesystem to store crawled information
        """
        self.mongodb_client = pymongo.MongoClient(self.crawler_db_host)
        self.mongodb_db = self.mongodb_client["crawler_db"]
        self.mongodb_coll = self.mongodb_db["crawler_coll"]


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
        return_docs = self.mongodb_coll.find({"url":url})
        if list(return_docs) == []:
            # If url doesn't exist in MongoDB collection, insert
            row_id = self.mongodb_coll.insert_one(
                {
                    "url": url,
                    "links": links
                }
            )
        else: # update
            row_id = self.mongodb_coll.update_many(
                {"url": url},
                {
                    "$set":{
                        "links": links
                    },
                    "$currentDate":{"lastModified":True}
                }
            )

        print(f"URL {url} inserted to MongoDB collection. Document ID {row_id}")

    
    def crawl_page(self, url):
        """
        Crawl a page and log the result to db
        """
        parsed_html = self.get_page(url)
        links = self.extract_links(parsed_html)
        clean_links = self.cleanup_links(links)
        self.log_links(url, clean_links)

        return url, clean_links


    def is_url_in_db(self, url):
        """
        Check if URL already exists in crawler db.

        True if URL already in db, false if not.
        """
        return_docs = self.mongodb_coll.find({"url":url})
        if list(return_docs) == []:
            return False
        return True
    
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
        _, clean_links = self.crawl_page(url)
        self.crawl_counter += 1

        # Get all child URLs from db
        self.crawl_child_links = list(set(self.crawl_child_links + clean_links))
        next_page = None

        for c in self.crawl_child_links:
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
    crawler = ParliamentCrawler(root_url = 'https://www.dpr.go.id/jdih', crawler_db_host='mongodb://Marukun:marukun@localhost:27017')
    crawler.init_db()
    crawler.start_crawl()