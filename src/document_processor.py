import io

import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from pdfminer.high_level import extract_text
import argparse

class DocumentProcessor():
    """
    Module to process fetched documents.
    """


    def __init__(self):
        pass


    def extract_pdf(self, input):

        # Perform layout analysis for all text
        laparams = pdfminer.layout.LAParams()
        setattr(laparams, 'all_texts', True)

        """
        Extract text from PDF files. Write output 

        Keyword arguments:
        > input (string): PDF filepath
        > output (string): filepath for output (txt)
        """
        if input.split('.')[-1] != 'pdf':
            raise Exception("Input must be a pdf file")
        
        if output.split('.')[-1] != 'txt':
            raise Exception("Output must be a txt file")

        resource_manager = PDFResourceManager()
        fake_handler = io.StringIO()

        converter = TextConverter(resource_manager, fake_handler, laparams=laparams)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(input, 'rb') as f :
            for page in PDFPage.get_pages(f, caching=True, check_extractable=True) :
                page_interpreter.process_page(page)

            text = fake_handler.getvalue()

        converter.close()
        fake_handler.close()

        return text

    def extract_document_title(self, input):
        """
        Extract document title from txt file.

        Keyword arguments:
        > input (string): filepath of txt input file

        Return a dict of the document tile, containing:
        > document_type (string)
        > document_number (int)
        > year (int)
        > title (string)
        > article_number (int): total number of articles in the document
        > upstream_documents (list): list of upstream documents
        """
        pass

    def extract_article(self, input, article_number):
        """
        Extract article from a txt file.

        Keyword arguments:
        > input (string): filepath of txt input file
        > article_number: article number to be extracted

        Return a dict of sections:
        > section_number & content tuple (int, string)
        """
        pass

def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    parser.add_argument("--output", "-o", type=str, required=True)

    args = parser.parse_args()
    processor = DocumentProcessor()
    text = processor.extract_pdf(args.input, args.output)
    with open(output, "w") as f :
        f.write(text)

if __name__ == "__main__" :
    main()


