# Indonesia Legislative Analytics

This project aims to make Indonesia's legislative system more transparent and clear. 

The first part of the project is data collection of legislative documents, using web crawler to crawl & log data from DPR's website.

The second part is making a connector to DPR website based on the crawled data. The objective is to develop an easy to use API to access legislative document.

The third part is text extraction from PDF and text processing with NLP. The objective is to transform legislative data (unstructured data, PDF format) to semi-structure data (JSON, with clear document name, number, articles, and upstream documents).

The fourth part is analytics: graph analytics to see the networks of legislative documents and text analytics to search clauses.