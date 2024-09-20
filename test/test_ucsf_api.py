from src.api.ucsf_api import IndustryDocsSearch

class TestIndustryDocsSearch:   
    
    def test_create_query(self):
        wrapper = IndustryDocsSearch()
        
        assert wrapper._create_query(q='vape') == 'https://metadata.idl.ucsf.edu/solr/ltdl3/query?q=vape&wt=json&cursorMark=*&sort=id%20asc'

    # TODO
    def test_query(self):
        return
    
    # TODO 
    def test_load(self):
        return
    
    # TODO
    def test_load(self):
        return

