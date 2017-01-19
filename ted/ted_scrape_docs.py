
# coding: utf-8

# #### 2 TED read individual transcrapt 

# In[6]:

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os 
import json 

#os.getcwd()
#os.chdir('/home/johnsonice/Desktop/temp/webScrap')


# In[7]:

def retrieve_doc(url,lang):
    ## send request 
    result = requests.get(url)
    if result.status_code == 200:       ## check if url successfully loaded
        #print('200, Request successful')
        pass
    else:
        #raise ValueError('Request Response is not 200,check url.')
        print('Request Response is not 200,check url.')
        
    ## scrap data 
    c = result.content
    soup = BeautifulSoup(c,"lxml")
    doc={}
    doc_mata= soup.find('div', { 'class' : 'media__message'})
    doc['author'] = doc_mata.find('h4',{'class':'h12 talk-link__speaker'}).getText().replace('\n','')
    doc['title'] = doc_mata.find('h4',{'class':'h9'}).getText().replace('\n','')
    doc['date'] = doc_mata.find('div').find('span').find('span').getText().replace('\n','')
    
    data = {'time':[],'text_'+lang:[]}
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
            s = s.strip(' \t\n\r').replace('\n',' ')
            text += s
        
        data['time'].append(time)
        data['text_'+lang].append(text)
    #    print(time)
    #    print(text)
    doc['data']= data
    
    ## return data object 
    return doc


# In[8]:

def check(raw_url,language):
    result_cn = requests.get(raw_url+language['chinese'])
    result_en = requests.get(raw_url+language['english'])
    
    if result_cn.status_code == 200 and result_en.status_code == 200:
        return True
    else:
        return False 


# In[9]:

def scrap(raw_url,folder):

    language = {'chinese':'/transcript?language=zh-cn','english':'/transcript?language=en'}
    #raw_url = "https://www.ted.com/talks/kevin_kelly_how_ai_can_bring_on_a_second_industrial_revolution"

    available = check(raw_url,language)

    if available == True:
        english = retrieve_doc(raw_url+language['english'],'en')
        chinese = retrieve_doc(raw_url+language['chinese'],'cn')

        ## merge english and chinese, and export it 
        fname = folder + chinese['title'] + '.txt'
        df_en = pd.DataFrame(english['data'])
        df_cn = pd.DataFrame(chinese['data'])
        df_merge = pd.concat([df_en['text_en'],df_cn['text_cn']],axis=1)
        df_merge.to_csv(fname,sep='|')
        return True
    else:
        print('translation is not available')
        return False



# In[10]:




# In[ ]:

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

