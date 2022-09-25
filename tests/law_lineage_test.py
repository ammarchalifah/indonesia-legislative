from code.law_lineage import IndonesiaLawLineage


client = IndonesiaLawLineage()


def test_extract_pdfs():
    response = client.extract_pdfs(input = 'test_documents')

    assert response == 0