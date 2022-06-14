import json
import PyPDF2
import requests 
from bs4 import BeautifulSoup
import time, random
import urllib.request
from PyPDF2 import PdfFileReader
from collections import defaultdict
import re
from bs4 import Comment

def remove_style_code(soup):
    #styleclean = re.compile('<style>.*?</style>')
    #js_clean = re.sub(styleclean, '', data)
    #javascript = re.compile('<script>.*?</script>')
    #cleandata = re.sub(javascript, '',js_clean )
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
    #return re.sub('\W+',' ', cleandata)
    return re.sub('\W+',' ', soup.text)

if __name__ == '__main__':
    
    # import json:
    with open('ent_dataset.json') as f: 
       data = json.load(f)
    pass  

    url_list = []
    url_keywords = []
    for k, v in data.items():
        if not k.endswith('.zip'):
            url_keywords.append(v)
            url_list.append(k)
        pass
    pass
    
    link = 0 
    while link < len(url_list):
        pdf_key = defaultdict(list)
        main_Data = []
        remain = len(url_list) - (link + 1)
        print('loading: {} & remaining: {}'.format(link + 1, remain - 1))
        
        try:
            full_text = ""
            if url_list[link].__contains__('.pdf'):
                filename = url_list[link].split('/')[-1]
                urllib.request.urlretrieve(url_list[link], filename)
                
                pdfReader = PyPDF2.PdfFileReader(filename)
                print(pdfReader.numPages)

                page = 0
                pdf_text = []
                while page < pdfReader.numPages: # read all the pages
                    pageObj = pdfReader.getPage(page)
                    pdf_text.append(pageObj.extractText()) # store each page in list
                    page += 1
                pass

                full_text = ",".join(pdf_text) # separate each page with , and join in full text 
                
                pdfReader.close()

            # other files: 
            else: 
                response = requests.get(url_list[link])
                soup = BeautifulSoup(response.content, 'html5lib')  # need to clean some of the scripts (ex: css and javascript)
                #full_text = remove_style_code(soup.text.strip())
                #full_text = remove_style_code(soup.find("body").text.strip())
                full_text = remove_style_code(soup)
            pass
            
            pdf_key["text"] = full_text
            pdf_key["keywords"] = url_keywords[link]
            main_Data.append(pdf_key)
            try:
                with open('training_data.json','a', encoding='utf-8') as outfile:
                    json.dump(main_Data, outfile)
                pass
                print('\t\t\t  Data Save Successfully  ')
            except BaseException as E:
                print(E)
            pass

        except BaseException as E:
            print(E)
        pass
        
        # PDF files: 
        
        time.sleep(random.randint(5,10)) # pick random number between 5 and 10 to sleep 
        link += 1

    pass
    print(url_list)
