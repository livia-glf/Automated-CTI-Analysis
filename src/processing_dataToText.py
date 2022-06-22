#******************************************************************************
        # This code is used to scrape the 'dataset full' json file to retrieve
        # every url and extract the text from it - whether HTML or PDF
        # It then stores it in a file named 'training data'
#****************************************************************************** 


import json
from wsgiref import headers
import PyPDF2
import requests 
from bs4 import BeautifulSoup
import time, random
import urllib.request
from PyPDF2 import PdfFileReader
from collections import defaultdict
import re
from bs4 import Comment
from tika import parser
import os
from tqdm import tqdm
import traceback

import warnings
warnings.filterwarnings("ignore")

# Use from original browser: 
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

def remove_style_code(soup):
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')] # css
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
    
    return soup.text # re.sub('\W+',' ', text)

output_file_name = 'dataset_full_text.json'

if os.path.exists(output_file_name):
    with open(output_file_name) as f: 
       new_data = json.load(f)
else:
    new_data = {}


if __name__ == '__main__':
    # import json:
    with open('dataset_full.json') as f: 
       data = json.load(f)
    
    for url, url_data in tqdm(data.items()):
        if url in new_data:
            continue
        
        try:
            pdf_text = []
            full_text = ""
            
            header = {"User-Agent": user_agent, "Accept": "*/*", "Content-Type": "application/json"}
            response = requests.get(url,timeout = 20, headers = header, verify=False) # increase timeout to load website
            pdf = False
            with open('tmp.pdf', 'wb') as f:
                f.write(response.content)
            
            # ********************* PDF Processing: *********************
            if url.__contains__('.pdf') or url.__contains__('download'):
            
                try:
                    pdfReader = PyPDF2.PdfFileReader('tmp.pdf')
                    page = 0
                    while page < pdfReader.numPages: # read all the pages
                        pageObj = pdfReader.getPage(page)
                        pdf_text.append(pageObj.extractText()) # store each page in list
                        page += 1
                    
                    full_text = ",".join(pdf_text) # separate each page with , and join in full text 
                    pdf = True
                except:
                    pass
            if not pdf:
                soup = BeautifulSoup(response.content, 'html5lib')
                
                if not soup.text.lower().__contains__('page not found'): # delete all page not found pages 
                    full_text = remove_style_code(soup)
                else:
                    raise Exception('website page not found error')
                    
            full_text = re.sub('\s{2,}', '\n', full_text) # delete all spaces more than 2 ws. new line separates sentences
            url_data["text"] = full_text
            new_data[url] = url_data
            
            with open('dataset_full_text.json','w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, indent=4)

            
        except KeyboardInterrupt:
            raise
        except BaseException as E:
            print(url)
            print(traceback.format_exc())


 
