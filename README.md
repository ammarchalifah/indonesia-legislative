# Indonesia Legislative Analytics

This project aims to make Indonesia's legislative system more transparent and clear. 

The first part of the project is data collection of legislative documents, using web crawler to crawl & log data from DPR's website.

The second part is making a connector to DPR website based on the crawled data. The objective is to develop an easy to use API to access legislative document.

The third part is text extraction from PDF and text processing with NLP. The objective is to transform legislative data (unstructured data, PDF format) to semi-structure data (JSON, with clear document name, number, articles, and upstream documents).

The fourth part is analytics: graph analytics to see the networks of legislative documents and text analytics to search clauses.
***
## Web Crawler
If you want to build your own index & use it as the basis for the API, run your own crawler by following this guide.

To run the crawler, run MongoDB container locally. MongoDB is a non-relational database that is suitable to store crawled data. In this example, MongoDB will run inside a Docker container locally.
```
docker-compose up -d
```
Ensure the MongoDB container is running by executing `docker ps`

After MongoDB container is running, start the crawler
```
python src/parliament_crawler.py
```
Then, start the crawler
```
python src/parliament_crawler.py
```
## GraphQL - API
After the crawler finished crawling and storing the data to the MongoDB database, start the GraphQL web interface to interact with the data easily.
```
python src/parliament_app.py
```
Access GraphQL's web UI in `https://localhost:5000`