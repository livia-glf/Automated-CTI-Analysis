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

# Use from original browser: 
user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def remove_style_code(soup):
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')] # css
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
#    text = ''.join((c for c in str(soup.text) if ord(c) < 128))
#    text = re.sub('\s*\(\*\)|\s*\d+',' ',text)
    text = soup.text
    text = re.sub('\s{2,}', '\n', text) # delete all spaces more than 2 ws. new line separates sentences

    return text # re.sub('\W+',' ', text)

new_data = {}
if __name__ == '__main__':
    # import json:
    with open('dataset_full.json') as f: 
       data = json.load(f)
    
    for url, url_data in tqdm(data.items()):
        try:
            pdf_text = []
            full_text = ""

            # ********************* PDF Processing: *********************
            if url.__contains__('.pdf') or url.__contains__('download'):
                filename = url.split('/')[-1]
                try:
                    urllib.request.urlretrieve(url, filename)
                    pdfReader = PyPDF2.PdfFileReader(filename)
                    #print(pdfReader.numPages)
                    page = 0
                    while page < pdfReader.numPages: # read all the pages
                        pageObj = pdfReader.getPage(page)
                        pdf_text.append(pageObj.extractText()) # store each page in list
                        page += 1
                    pass
                    pdfReader.close()
                    full_text = ",".join(pdf_text) # separate each page with , and join in full text 
                
                except:
                    
                    raw = parser.from_file(filename)
                    soup = BeautifulSoup(raw['content'], 'html5lib') 
                    full_text = remove_style_code(soup)
                    

                os.remove(filename)
            # ********************* Non-PDF Processing: *********************
            else: 
                user_agent = random.choice(user_agent_list)
                header = {"User-Agent": user_agent, "Accept": "*/*", "Content-Type": "application/json"}
                response = requests.get(url,timeout = 20, headers = header) # increase timeout to load website
                soup = BeautifulSoup(response.content, 'html5lib')
                
                if not soup.text.lower().__contains__('page not found'): # delete all page not found pages 
                    full_text = remove_style_code(soup)
                else:
                    print('\t\t\t  website page not found error')
                    raise Exception()
                
                  
            url_data["text"] = full_text
            new_data[url] = url_data
            
            with open('draft_training_data.json','w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, indent=4)

            
        except KeyboardInterrupt:
            raise
        except BaseException as E:
            print(traceback.format_exc())


 
