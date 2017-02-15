#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 22:23:13 2017

@author: huang
"""
#%%

import os 
#from os import path
from itertools import compress
import pandas as pd
import re

os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%
##############################
#### define some functions ###
##############################
def check(f):
    filename, file_extension = os.path.splitext(f)
    if file_extension == '.txt':
        return True
    else:
        return False
def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True

def check_length(e,c):
    if len(e)==len(c):
        return True
    else:
        return False

def check_chinese(line_str):
    cn = re.findall(r'[\u4e00-\u9fff]+',line_str)
    if len(cn)>0:
        return True
    else:
        return False
def check_english(line_str):
    en = re.findall(r"[A-Za-z]+", line_str)
    if len(en)>0:
        return True
    else:
        return False
    
def retrieve_punc(line_str):
    #line_str = "想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8 0. ！“”？  8 6 。0.  2。 3  《    有,惊,喜,哦"  
    #reg_filter1=re.compile(r'[\uff00-\uffef]+')
    reg_filter2 = re.compile(r'[￥·×—‘’“”…、。《》『』【】！（），：；？]+|[\uff00-\uffef]+')
    #r1 = reg_filter1.findall(line_str)
    r2 = reg_filter2.findall(line_str)
    if len(r2)==0:
        return False 
    else:
        return True

def replace_punc(line_str):
    mapping=[('—','-'),('，',','),("‘","'"),("’","'"),('、',','),('“','"'),('”','"'),('。','.'),('（','('),('）',')'),('：',':'),('；',';'),('？','?'),('…','...'),('《',''),('》','')]
    for k,v in mapping:
        line_str=line_str.replace(k,v)
    return line_str

def replace_special(line_str):
    line_str = re.sub(r'[『』【】「」♫．#♪]','',line_str)
    line_str = re.sub(r'\{.*?\}','',line_str)
    line_str = re.sub(r'\<.*?\>','',line_str)
    return line_str

#%%


## define some global folder path 
f_type = 'ass/'
data_folder = 'data/'
results_txt = data_folder + 'data_results_'+f_type
result_folder_cn = data_folder + 'data_final/'+f_type+'cn/'
result_folder_en = data_folder + 'data_final/'+f_type+'en/'

folders = [data_folder,results_txt,result_folder_cn,result_folder_en]
[check_dir(x) for x in folders]

## check if extension is .srt
txts = [results_txt + f for f in os.listdir(results_txt) if check(f)]
print(len(txts))

doc_list ={'title':[],'status':[]}
txt_list = txts
for index,txt in enumerate(txt_list):
    try:
        if index % 100 == 0 :
            print (len(txt_list),index+1)
            
        with open(txt, 'r') as f:
            myFile = [line.strip() for line in f]
        myFile = [replace_special(x) for x in myFile if x != '']
        sp = [s.split('|') for s in myFile]
        en =[ele[0].strip() for ele in sp]
        cn = [ele[1].strip() for ele in sp]
        cn = [replace_punc(x) for x in cn]
        filename, file_extension = os.path.splitext(txt)
        fname = str(index) + "_" +filename.split('/')[-1]
        doc_list['title'].append(fname)
        if check_length(en,cn):
            with open(result_folder_cn + fname + '.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(cn))
            with open(result_folder_en + fname + '.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(en))            
            doc_list['status'].append('Success')
        else:
            doc_list['status'].append('Failed')
    except:
        pass
    
#%%
df = pd.DataFrame(doc_list)
df_problem=df[df.status=='Failed']
print(df_problem.head())
print(df.head())
print('finish')