#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:59:11 2017

@author: huang
"""
import re
import pandas as pd
import os 

os.chdir('/Users/huang/Dev/projects/WebScraping/4_dictionary/')

#%%
def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True 

def clean_doc(line_str):
    line_str = re.sub(r'\（.*?\）','',line_str) ## get rid of (...)
    return line_str

#%%
data_folder = 'data/'
raw_data_folder = data_folder + 'raw_data/'
processed_data_folder = data_folder + 'processed_data/youdao/'
result_data_folder = data_folder + 'result_data/youdao/' 
folders = [data_folder,raw_data_folder,processed_data_folder,result_data_folder]
[check_dir(x) for x in folders]

#%%
file = raw_data_folder + 'youdao.xlsx'
df = pd.read_excel(file)
df['en-us'] = df['en-us'].apply(lambda x:x.replace('\\"','"'))
df['zh-cn'] = df['zh-cn'].apply(lambda x:clean_doc(x))
df = df[['en-us','zh-cn']]
##export data to processed

fname = processed_data_folder +'youdao'+'.csv'
df.to_csv(fname,index=False,sep='|',header=False)

## export to result 
fname_res_cn =result_data_folder +'youdao_cn'+'.txt'
fname_res_en =result_data_folder  +'youdao_en'+'.txt'

df['en-us'].to_csv(fname_res_en,index=False,header=False)
df['zh-cn'].to_csv(fname_res_cn,index=False,header=False)

print('finish')