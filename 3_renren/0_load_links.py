# -*- coding: utf-8 -*-
"""
Spyder Editor

down all renren file links with both chinese and english

"""
#%%
from bs4 import BeautifulSoup
import requests
#import pandas as pd
import os
import re

os.getcwd()
os.chdir('/Volumes/Samsung_T3/Dev/WebScraping/3_renren')
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

## get download link from title link 
def get_down_link(url):
    try:
        result = requests.get(url)
        if result.status_code != 200:
            return None
        c = result.content
        soup = BeautifulSoup(c,"lxml")
        down_link =  soup.find('li',{'class':'li dlsub'}).find('a').get('href')
        return down_link
    except:
        return None
#%%
## send the request
url = "http://www.zmz2017.com/esubtitle"
result = requests.get(url)
page_num = get_page_num(result)
if page_num == None :
    raise ValueError('Bug in getting page num, request failed.')


## get page number

#%%

result = requests.get(url)
if result.status_code != 200:
    raise
c = result.content
soup = BeautifulSoup(c,"lxml")
items = soup.find('div',{'class':'box subtitle-list'}).findAll('li')



