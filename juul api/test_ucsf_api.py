from ucsf_api import *


class TestWrapper:   
    
    def test_create_query(self):
        wrapper = IndustryDocsSearch()
        wrapper.q = 'vape'
        wrapper.wt = 'json'
        
        assert wrapper.create_query() == 'https://metadata.idl.ucsf.edu/solr/ltdl3/query?q=vape&wt=json&cursorMark=*&sort=id%20asc'
    
    # TO DO 
    def test_read(self):
        

