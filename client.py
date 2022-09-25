from document_processor import DocumentProcessor

client = DocumentProcessor()

client.extract_pdf(input='inputs/uu_2021_01.pdf', output='outputs/uu_2021_01.txt')