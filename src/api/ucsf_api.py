from dataclasses import dataclass
import re
import requests
import polars as pl
    

@dataclass
class IndustryDocsSearch:
    """
    UCSF Industry Documents Library Solr API Wrapper Class.

    API Documentation found here: https://www.industrydocuments.ucsf.edu/wp-content/uploads/2020/08/IndustryDocumentsDataAPI_v7.pdf
    """
    base_url = "https://metadata.idl.ucsf.edu/solr/ltdl3/"
    results = []
    
    def _create_query(self, q: str, wt: str, cursor_mark: str, sort: str) -> str:
        """Constructs parametrized query"""
        return f'{self.base_url}query?q={q}&wt={wt}&cursorMark={cursor_mark}&sort={sort}'
    
    def _loop_results(self, q: str, wt: str, cursor_mark: str, sort: str) -> None:
        """Iteratively retrieves documents with cursor_mark for Solr deep paging"""
        next_cursor = cursor_mark
        current_cursor = None 
        while next_cursor != current_cursor:
            current_cursor = next_cursor
            q_url = self._create_query(q, wt, current_cursor, sort)
            r = requests.get(q_url).json()
            self.results.extend(r['response']['docs'])
            next_cursor = r['nextCursorMark'] 
            print(f"{len(self.results)}/{r['response']['numFound']} documents collected")
                
        return
    
    def _create_links(self) -> None:
        """Adds links to documents"""
        for doc in self.results:
            doc['url'] = f'https://www.industrydocuments.ucsf.edu/tobacco/docs/#id={doc['id']}'
    
    def _ocr_content(self, doc_id: str):
        """
        Pulls OCR content based on document ID
        
        example: https://download.industrydocuments.ucsf.edu/m/x/h/p/mxhp0288/mxhp0288.ocr
        """
        base_url = 'https://download.industrydocuments.ucsf.edu/'
        folders = '/'.join([x for x in re.search(r'[a-z]+(?=[0-9])', doc_id)[0]])
        full_url = f'{base_url}{folders}/{doc_id}/{doc_id}.ocr'
        try: 
            return requests.get(full_url).content
        except:
            return 
        
    def _obtain_ocr_content(self) -> None:
        """Iterates over results and pulls OCR content for each"""
        for i, doc in enumerate(self.results):
            doc['ocr_content'] = self._ocr_content(doc['id'])
            print(f'{i}/{len(self.results)}')
    
    # TODO: add functionality for /select/* queries for specific fields
    def query(self, q='(case:"State of North Carolina" AND collection:"JUUL Labs Collection")', wt='json', cursor_mark='*', sort="id%20asc", ocr=False) -> None:
        """Queries the UCSF Industry Documents Solr Library for documents"""
        self._loop_results(q=q, wt=wt, cursor_mark=cursor_mark, sort=sort)
        print('Adding URLs to query results')
        self._create_links()
        if ocr:
            print('Pulling OCR content from query results')
            self._obtain_ocr_content()

    def load(self, filename: str) -> pl.DataFrame:
        """Reads results from a local CSV or JSON"""
        if not filename.lower().endswith('.parquet'):
            raise Exception("Only parquet format supported currently.")
        self.results = pl.read_parquet(filename)
        
    def save(self, filename: str) -> None:
        """Writes previously queried or read results in parquet format"""
        if not filename.lower().endswith('.parquet'):
            raise Exception("Only parquet format supported currently.")
        df = pl.DataFrame(self.results, nan_to_null=True)
        df.write_parquet(filename)
        