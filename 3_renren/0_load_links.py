# -*- coding: utf-8 -*-
"""
Spyder Editor

down all renren file links with both chinese and english

"""
#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import re
from multiprocessing import Pool 

os.getcwd()
os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren')
#%%
## get page number 
def get_page_num(result):
    if result.status_code != 200:
        return None
    c=result.content
    soup = BeautifulSoup(c,"lxml")
    pages =  soup.find('div',{'class':'pages'}).findAll('a')
    page_num = pages[-1].getText()
    page_num = int(re.findall(r'\d+',page_num)[0])
    #print('Total Page number is: ' + str(page_num))
    return page_num

def extract_link(link):
    result_sub = requests.get(link)
    if result_sub.status_code != 200:
        raise
    c = result_sub.content
    soup = BeautifulSoup(c,"lxml")
    down_item = soup.find('div',{'class':'subtitle-links tc'}).find('h3').find('a')
    #print(down_item)
    d_link = down_item.get('href')
    d_name = down_item.getText().strip()
    
    return (d_link,d_name)

def check_sub_language(item):
    language = item.find('dd').findAll('span')[0].getText()
    if '中英' in language:
        return True
    else:
        return False
    
## get download link from title link 
def get_down_link(item):
    if check_sub_language(item):
        link = domin + item.find('dt').find('a').get('href')
        d_link,d_name = extract_link(link)
        return (d_link,d_name)
    else:
        return False
    
def get_all_links(pn):
    print('running page: ',pn)
    page_url = 'http://www.zmz2017.com/esubtitle?page=' + str(pn)
    result = requests.get(page_url)
    if result.status_code != 200:
        raise ValueError('Did not get correct response from server!')
    c = result.content
    soup = BeautifulSoup(c,"lxml")
    items = soup.find('div',{'class':'box subtitle-list'}).findAll('li')
    res = [get_down_link(x) for x in items]
    res = [x for x in res if x != False]
    return res

#%%

#%%
if __name__ == '__main__':
    ## send the request
    url = "http://www.zmz2017.com/esubtitle"
    domin = "http://www.zmz2017.com"
    result = requests.get(url)
    page_num = get_page_num(result)
    if page_num == None :
        raise ValueError('Bug in getting page num, request failed.')
    ## get page number

    p = Pool(10)
    all_links_mp = p.map(get_all_links,range(1,page_num))
    p.close()
    p.join()
    print(len(all_links_mp))
    
    #all_links = []
    #
    #for pn in range(1,3):
    #    res = get_all_links(pn)
    #    all_links.extend(res)
    #
    #print(len(all_links))
    # 
    all_docs = []
    [all_docs.extend(x) for x in all_links_mp]
    down_link, name = zip(*all_docs)
    docs = {'name': name,'links':down_link}
    df = pd.DataFrame(docs)    
    df.to_csv('links.csv')
    print('finish')

#%%





