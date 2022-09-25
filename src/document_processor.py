from pdfminer.high_level import extract_text

class DocumentProcessor():
    """
    Module to process fetched documents.
    """


    def __init__(self):
        pass


    def extract_pdf(self, input, output = None):
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

        text = extract_text(input)
        if output is not None:
            with open(output, 'w', encoding = 'utf-8') as f:
                f.write(text)

        return 0

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