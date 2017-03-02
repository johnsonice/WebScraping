#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 09:26:14 2017

@author: huang
"""

#import chardet
import re
import pandas as pd
import os 

os.chdir('/Users/huang/Dev/projects/WebScraping/4_dictionary/')
    
#%%
## define some functions 

def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True 
    
def clean_doc(line_str):
    line_str = re.sub(r'\/.*?\/','',line_str)
    line_str = re.sub(r'\【.*?\】','',line_str)
    line_str = re.sub(r'\[.*?\]','',line_str)
    return line_str
def split_line(line):
    line = line.split('\t')
    key = line[0]
    val = line[1]
    val = val.split('\\n')
    val = [delete_adj(x) for x in val]
    res = []
    for i in val:
        temp = re.split(', |; ',i)
        res.extend(temp)
    res = [clean_up(x) for x in res if clean_up(x) is not None]
    return (key,res)


def delete_adj(line):
    line = re.sub(r'\w+\.\s+','',line).strip()
    return line

def clean_up(text):
    text = text.strip()
    s = '相关词组'
    if len(check_chinese(text))>0:
        if s in text:
            return None
        else:
            return text
    else:
        return None
    
def item_list(text):
    try:
        key,val = split_line(text)
        #line_list = [str(key)+ '| ' + str(x) for x in val]
        line_list = [(key,x) for x in val]
        return line_list
    except:
        return None

def check_chinese(text):
    ch = re.findall(r'[\u4e00-\u9fff]+', text)
    return ch

def check_english(text):
    en = re.findall(r"[A-Za-z]+", text)
    return en

#%%

## create folder structure

data_folder = 'data/'
raw_data_folder = data_folder + 'raw_data/'
processed_data_folder = data_folder + 'processed_data/yinhandictionary/'
result_data_folder = data_folder + 'result_data/yinhandictionary/' 
folders = [data_folder,raw_data_folder,processed_data_folder,result_data_folder]
[check_dir(x) for x in folders]

#%%
## read data 
file = raw_data_folder + '简明英汉字典.txt'

#with open(file, 'rb') as f:
#    input_bytes = f.read()
#    result = chardet.detect(input_bytes)
#    conf = result['confidence']
#    res_encoding = result['encoding']
#print(conf)
#print(res_encoding)

res_encoding ='GB2312'

with open(file, "r",encoding=res_encoding,errors = 'ignore') as f:
    doc = [line.strip() for line in f]
#%%
## process data 
doc_clean = [clean_doc(x) for x in doc]
res = []   ## storing result tuples 
doc_res = [item_list(x) for x in doc_clean]
doc_res = [res.extend(x) for x in doc_res if x is not None]


#%%
##export data to processed

fname = processed_data_folder +'yinhanzidian'+'.csv'
df = pd.DataFrame(res,columns=['en','cn'])
df.to_csv(fname,index=False,sep='|',header=False)

## export to result 
fname_res_cn =result_data_folder +'yinhanzidian_cn'+'.txt'
fname_res_en =result_data_folder  +'yinhanzidian_en'+'.txt'

df.en.to_csv(fname_res_en,index=False,header=False)
df.cn.to_csv(fname_res_cn,index=False,header=False)

print('finish')