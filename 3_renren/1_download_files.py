#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 09:29:36 2017

@author: huang
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import re
from multiprocessing import Pool 

os.getcwd()
os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%
## download 
def download_zip(url,folder,fname):
    try:
        result = requests.get(url)
        res= result.content
        # this line is used to get default name 
        #fname = result.headers['Content-Disposition'].split('"')[1]    
        with open( folder + fname, "wb" ) as f :
                f.write( res )
        return True
    except:
        return False
    
#%%
data_folder = 'data/'
download_folder = data_folder + 'download/'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

df = pd.read_csv('links.csv')


    

