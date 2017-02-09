#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 09:29:36 2017

@author: huang
"""

#from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from functools import partial
#import re
from multiprocessing import Pool 

os.getcwd()
os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%
## download 
def download_zip(f,folder):
    index,row = f 
    url = row['links']
    fname = row['name']
    try:
        result = requests.get(url)
        res= result.content
        # this line is used to get default name 
        #fname = result.headers['Content-Disposition'].split('"')[1]    
        with open( folder + fname, "wb" ) as f :
                f.write( res )
        if index % 50 == 0 :
            print(index)
            
        return True
    except:
        return False


    
#%%
if __name__ == '__main__':
    data_folder = 'data/'
    download_folder = data_folder + 'download/'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    ## read download links from previous csv file 
    df = pd.read_csv('links.csv')
    ## download files from renren 
    ## multi process 
    p = Pool(20)
    partial_download = partial(download_zip, folder = download_folder)
    all_links_mp = p.map(partial_download,df.iterrows())
    p.close()
    p.join()
    print('finish')
    
    ## single process 
#==============================================================================
#for x in df.iterrows():
#    if x[0]> 10:
#        break
#    print(download_zip(x,download_folder))
#==============================================================================
#%%



