import requests
import pymongo
import pandas as pd
from http_utils import TimeoutHTTPAdapter, DefaultRetryStrategy
from bs4 import BeautifulSoup


adapter = TimeoutHTTPAdapter(max_retries=DefaultRetryStrategy)
http = requests.Session()
http.mount("http://", adapter)
http.mount("https://", adapter)


class ParliamentCrawler():
    """
    API to crawl DPR's website
    """

    field_mapper = {
            '_id': '_id', 
            'id': 'id', 
            'document_title':'document_title', 
            'lastModified':'lastModified',
            'document_attributes.Nomor':'document_number', 
            'document_attributes.Tanggal Disahkan':'document_ratification_date',
            'document_attributes.Tanggal Diundangkan':'document_promulgation_date', 
            'document_attributes.LN':'document_LN',
            'document_attributes.TLN':'document_TLN', 
            'document_attributes.File':'document_pdf_url',
            'document_attributes.Referensi RUU':'document_ruu_reference'
            }

    def __init__(self, 
                    root_url = 'https://www.dpr.go.id/', 
                    headers = None, 
                    crawler_db_host = 'mongodb://localhost:27017'
                    ):
        """
        Initiating the crawler
        """
        self.root_url = root_url
        self.headers = headers or {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

        # Crawler helper
        self.crawl_counter = 1
        self.crawl_child_links = []

        # Database attributes
        self.crawler_db_host = crawler_db_host
        self.mongodb_client = None
        self.mongodb_db = None
        self.mongodb_coll = None


    def init_db(self, 
                    remove_existing = False,
                    allow_duplicate = False):
        """
        Initialize external database in local filesystem to store crawled information
        """
        self.mongodb_client = pymongo.MongoClient(self.crawler_db_host)
        if remove_existing:
            self.mongodb_client.drop_database("crawler_db")
        self.mongodb_db = self.mongodb_client["crawler_db"]
        self.mongodb_coll = self.mongodb_db["crawler_coll"]
        self.allow_duplicate = allow_duplicate


    def cleanup_db(self, 
        remove_empty_document = True
        ):
        """
        Functions to clean the MongoDB
        """
        if remove_empty_document:
            self.mongodb_coll.delete_many({"document_title":""})

    def export_db(self,
        path
        ):
        """
        Function to convert 
        """
        cursor = self.mongodb_coll.find()
        df = pd.json_normalize(cursor)
        new_column_name = []
        for c in df.columns:
            try:
                c_ = self.field_mapper[c]
                new_column_name.append(c_)
            except:
                new_column_name.append(c)
        df.columns = new_column_name
        df.to_csv(path)

    def get_page(self, url):
        """
        Get the HTML page from a URL
        """
        response = http.get(url, headers = self.headers, timeout=1)
        parsed_html = BeautifulSoup(response.content, "html.parser")
        return parsed_html

    
    def extract_dict(self, parsed_html):
        """
        Extract dictionary from parsed HTML
        """
        document_title = parsed_html.findAll('h3', {'class': 'text-center'})[0].text

        document_attributes_list = parsed_html.findAll('div', {'class': 'keterangan'})[0].findAll('div', {'class':'clearfix'})
        document_attributes = {}

        for da in document_attributes_list:
            if da.find('div', {'class':'input pull-left'}).find('a') is not None:
                document_attributes[da.find('div', {'class':'ket-title pull-left'}).text] = da.find('div', {'class':'input pull-left'}).text.lstrip(': ') + da.find('div', {'class':'input pull-left'}).find('a')['href']
            else:
                document_attributes[da.find('div', {'class':'ket-title pull-left'}).text] = da.find('div', {'class':'input pull-left'}).text.lstrip(': ')

        extracted_dict = {
            "id": self.crawl_counter,
            "document_title": document_title,
            "document_attributes":document_attributes
        }
        return extracted_dict

    
    def log_dict(self, dict):
        """
        Log the extracted dict to MongoDB
        """
        if self.allow_duplicate:
            row_id = self.mongodb_coll.insert_one(
                dict
            )
        else:
            # Check content in the DB and do upsert if there is a duplicate
            return_docs = self.mongodb_coll.find({"id":self.crawl_counter})
            if list(return_docs) == []:
                # If url doesn't exist in MongoDB collection, insert
                row_id = self.mongodb_coll.insert_one(
                    dict
                )
            else: # update
                row_id = self.mongodb_coll.update_many(
                    {"id": self.crawl_counter},
                    {
                        "$set": dict,
                        "$currentDate":{"lastModified":True}
                    }
                )
        print("New row inserted to MongoDB collection. Document ID {}, id {}".format(row_id, dict["id"]))

    
    def crawl_page(self, url):
        """
        Crawl a page and log the result to db
        """
        try:
            parsed_html = self.get_page(url)
            extracted_dict = self.extract_dict(parsed_html)
            self.log_dict(extracted_dict)
        except KeyboardInterrupt:
            raise Exception("KeyboardInterrupt. Raising exception")
        except:
            print("Failed to crawl {}".format(url))


    def start_crawl(self, start_crawl = None, stop_count = None):
        """
        Start crawling from root_url
        """

        url = self.root_url

        if start_crawl is not None:
            self.crawl_counter = start_crawl

        if stop_count is not None:
            if stop_count < self.crawl_counter:
                print(f"Crawl finished because of stop count {stop_count}")
                return None
        
        # Start crawling
        self.crawl_page(url+str(self.crawl_counter))
        self.crawl_counter += 1

        self.start_crawl(stop_count = stop_count)



if __name__ == "__main__":
    crawler = ParliamentCrawler(root_url = 'https://www.dpr.go.id/jdih/index/id/', 
        crawler_db_host='mongodb://Marukun:marukun@localhost:27017'
        )
    crawler.init_db(remove_existing = False)
    # crawler.start_crawl(1, 10)
    crawler.cleanup_db()
    crawler.export_db("src/artifacts/legislative_docs.csv")