import os
import requests

from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup

class IndonesiaLawLineage():
    """
    Module of Indonesia's law lineage.
    """


    def __init__(self):
        pass


    def pdf_downloader(self, type = None, year = None, output = 'input', config = 'config.json'):
        """
        Download PDF documents from http://dpr.go.id
        """
        pass


    def extract_pdfs(self, input, output = None):
        """
        Extract text from PDF files.
        """
        inputs = os.listdir('input')

        for i in inputs:
            text = extract_text('input/'+i)
            if output is not None:
                with open('output/'+i.replace('.pdf', '.txt'), 'w', encoding = 'utf-8') as f:
                    f.write(text)

        return 0