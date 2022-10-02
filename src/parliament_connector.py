import os
from turtle import title
import requests
import pandas as pd

from bs4 import BeautifulSoup

class ParliamentConnector():
    """
    API to interact with DPR's resources
    """

    supported_documents = ['uu']

    def __init__(self, conn = 'local', path = "artifacts/legislative_docs.csv"):
        """
        Initializing the class object.
        """
        if conn == 'local':
            self.df = pd.read_csv(path)
        else:
            raise Exception("Only conn == 'local' is supported.")
    

    def is_correct_type(self, input, type):
        """
        Check if input has the correct type
        """
        if isinstance(input, list):
            if all(isinstance(elem, type) for elem in input):
                return True, list
            else:
                raise Exception("Wrong type of input {}".format(input))
        elif isinstance(input, type):
            return True, type
        else:
            raise Exception("Wrong type of input {}".format(input))


    def find_documents(
        self,
        title_contains = None, 
        document_number = None, 
        document_LN = None, 
        document_TLN = None, 
        document_ratification_year = None, 
        document_promulgation_year = None,
        document_type = None):
        """
        Function to find list of documents based on user query.
        """

        df_return = self.df.copy()

        if title_contains:
            type_bool, data_type = self.is_correct_type(title_contains, str)
