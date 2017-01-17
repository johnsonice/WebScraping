# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
from bs4 import BeautifulSoup
import requests
#import pandas as pd
import os 
import json 

os.getcwd()
os.chdir('/home/johnsonice/Desktop/temp/webScrap')


#%%
def retrieve_doc(url):
    ## send request 
    result = requests.get(url)
    if result.status_code == 200:       ## check if url successfully loaded
        print('200, Request successful')
    else:
        raise ValueError('Request Response is not 200,check url.')

    ## scrap data 
    c = result.content
    soup = BeautifulSoup(c,"lxml")
    doc={}
    doc_mata= soup.find('div', { 'class' : 'media__message'})
    doc['author'] = doc_mata.find('h4',{'class':'h12 talk-link__speaker'}).getText().replace('\n','')
    doc['title'] = doc_mata.find('h4',{'class':'h9'}).getText().replace('\n','')
    doc['date'] = doc_mata.find('div').find('span').find('span').getText().replace('\n','')
    
    data = {'time':[],'text':[]}
    rows = soup.find('div',{'class':'talk-article__body'}).findAll('p')
    for row in rows:    
        #get time stamp
        time = row.find('data').getText()
        time = time.strip(' \t\n\r')       ## trim space and line break
        # get text 
        para = row.find('span').findAll('span')
        text = ''
        for p in para:
            s = p.getText()
            s = s.strip(' \t\n\r').replace('\n','')
            text += s
        
        data['time'].append(time)
        data['text'].append(text)
    #    print(time)
    #    print(text)
    doc['data']= data
    
    ## return data object 
    return doc
#%%

def check(raw_url,language):
    result_cn = requests.get(raw_url+language['chinese'])
    result_en = requests.get(raw_url+language['english'])
    
    if result_cn.status_code == 200 and result_en.status_code == 200:
        return True
    else:
        return False 
    
#%%
language = {'chinese':'/transcript?language=zh-cn','english':'/transcript?language=en'}
raw_url = "https://www.ted.com/talks/kevin_kelly_how_ai_can_bring_on_a_second_industrial_revolution"

available = check(raw_url,language)

if available == True:
    document = {}
    document['english'] = retrieve_doc(raw_url+language['english'])
    document['chinese'] = retrieve_doc(raw_url+language['chinese'])
    # save to file:
    fname = document['english']['title'] + '.json'
    with open('../data/'+fname, 'w') as f:
        json.dump(document, f)
else:
    print('translation is not available')



#==============================================================================
#     # load from file:
# with open('my_file.json', 'r') as f:
#     try:
#         data2 = json.load(f)
#         print(data2)
#     # if the file is empty the ValueError will be thrown
#     except ValueError:
#         data2 = {}
#==============================================================================

    
        