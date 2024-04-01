import os
import re
import csv
import json
import requests
import tempfile
import pandas as pd
import urllib

# UCSF Industry Documents Library Solar API: https://www.industrydocuments.ucsf.edu/wp-content/uploads/2020/08/IndustryDocumentsDataAPI_v7.pdf


### TO DO ###
# 1. Save results as a XML file
# 2. Read the attached OCR of the files that are being pulled
# 3. Fix save_csv method -- partially done: successfully converts dict objects to csv
# 4. add parameter in query for cursormark
# 5. add method to save cursormark as txt file

class IndustryDocsSearch:
    def __init__(self):
         self.base_url = "https://metadata.idl.ucsf.edu/solr/ltdl3/"
         self.q = ""
         self.wt = "xml"
         self.cursorMark = "*"
         self.sort = "id%20asc"
         self.results = []
         self.keys = []    
    
    # construct single query request
    def create_query(self):
        return f'{self.base_url}query?q={self.q}&wt={self.wt}&cursorMark={self.cursorMark}&sort={self.sort}'
    
    # # loop through results using cursorMark
    # def loop_results(self):
    #     q_url = self.create_query()
    #     r = requests.get(q_url).json()
        
    #     # add response to response list
    #     self.results.extend(r['response']['docs'])
        
    #     # check to see if cursor marks match to make another request or not
    #     if r['nextCursorMark'] == self.cursorMark:
    #         print('Results are done!')
    #         return
    #     else:
    #         # set next cursor mark
    #         self.cursorMark = r['nextCursorMark']
    #         self.loop_results()
    
    # loop through results using cursorMark
    def loop_results(self):
        done = False
        while done != True:
            q_url = self.create_query()
            r = requests.get(q_url).json()

            if len(self.results) == 0:
                print(r['response']['numFound'])

            # print(len(r['response']['docs']))
            # add response to response list
            self.results.extend(r['response']['docs'])
            print(len(self.results))
            # check to see if cursor marks match to make another request or not
            if r['nextCursorMark'] == self.cursorMark:
                print('Results are done!')
                done = True
            else:
                # set next cursor mark
                self.cursorMark = r['nextCursorMark']
                
        return
    
    # starts the query process
    def query(self, q=None, wt='xml'):
        self.q = q
        self.wt = wt.lower()
        self.loop_results()

    # Read in results -- currently only reads in CSV or JSON
    def read(self, file):
        if file.lower().endswith('.csv'):
            self.results = pd.read_csv(file, encoding='utf-8')
        elif file.lower().endswith('.json'):
            self.results = pd.read_json(file, orient='records')

    # saves results as a json file
    def save_json(self):
        # results_json = {'results': self.results}
        
        with open(f'./{self.q}_results.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.results))
    
    # saves results as a CSV file
    def save_csv(self):
        with open(f'./{self.q}_results.csv', 'w', encoding='utf-8') as f:
            # f.write(','.join(self.results[0].keys()))
            # f.write('\n')
            # for r in self.results:
            #     f.write(','.join(str(x) for x in r.values()))
            #     f.write('\n')
            self.find_keys()
            f.write(','.join(self.keys()))
            f.write('\n')
            for r in self.results:
                for k in self.keys():
                    try:
                        f.write(f'{r[k]},')
                    except:
                        f.write(',')
                f.write('\n')
    
    # finds keys in list of results -- only needed if the query returns a JSON object and the user wants to save results as a CSV
    def find_keys(self):
        if self.wt == 'json':
            for r in self.results[0]:
                for k in r.keys():
                    if k not in self.keys:
                        self.keys.append(k)
    
    # presents the results as a Pandas datatable
    def as_datatable(self):
        if pd.isnull(self.results):
            raise ValueError("Please run a query. No data available to create a datatable.")
        
        if self.wt == 'json':
            return pd.DataFrame.from_dict(self.results, orient='records')
        
        elif self.wt == 'csv':
            return pd.read_csv(self.results, encoding='utf-8')
    
    def save_cursormark(self):
        with open('last_cursormark.txt', 'rw') as f:
            f.write(self.cursorMark)
    
    def ocr_url(self, doc_id):
        # EXAMPLE URL: https://download.industrydocuments.ucsf.edu/m/x/h/p/mxhp0288/mxhp0288.ocr
        base_url = 'https://download.industrydocuments.ucsf.edu/'
        folders = re.search(r'[a-z]+', doc_id)[0].split('')
        folders = '/'.join(folders)
        full_url = f'{base_url}{folders}/{doc_id}/{doc_id}.ocr'
        return full_url
    
    def obtain_ocr_content(self):
        
        # create array of ids
        urls = [self.ocr_url(doc.id) for doc in self.results]
        
        # with tempfile.TemporaryDirectory() as temp_dir:
        
        
    
        
        
        
        
        
            
        
    
        
