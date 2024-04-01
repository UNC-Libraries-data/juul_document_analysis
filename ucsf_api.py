import requests
import json
import re
import csv
import os
import pandas as pd

# UCSF Industry Documents Library Solar API: https://www.industrydocuments.ucsf.edu/wp-content/uploads/2020/08/IndustryDocumentsDataAPI_v7.pdf

class IndustryDocsSearch:
    def __init__(self):
         self.base_url = "https://metadata.idl.ucsf.edu/solr/ltdl3/"
         self.q = ""
         self.wt = "xml"
         self.cursorMark = "*"
         self.sort = "id%20asc"
         self.results = []    
    
    # construct single query request
    def create_query(self):
        return f'{self.base_url}query?q={self.q}&wt={self.wt}&cursorMark={self.cursorMark}&sort={self.sort}'
    
    # loop through results using cursorMark
    def loop_results(self):
        q_url = self.create_query()
        r = requests.get(q_url).json()
        
        # add response to response list
        self.results.extend(r['response']['docs'])
        
        # check to see if cursor marks match to make another request or not
        if r['nextCursorMark'] == self.cursorMark:
            print('Results are done!')
            return
        else:
            # set next cursor mark
            self.cursorMark = r['nextCursorMark']
            self.loop_results()
    
    # starts the query process
    def query(self, q=None, wt='xml'):
        self.q = q
        self.wt = wt
        self.loop_results()

    # saves results as a json file
    def save_json(self):
        results_json = {'results': self.results}
        
        with open(f'./{self.q}_results.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(results_json))
    
    # saves results as a CSV file
    def save_csv(self):
        with open(f'./{self.q}_results.csv', 'w', encoding='utf-8') as f:
            f.write(','.join(self.results[0].keys()))
            f.write('\n')
            for r in self.results:
                f.write(','.join(str(x) for x in r.values()))
                f.write('\n')
                
    # TO-DO save results as a XML file
