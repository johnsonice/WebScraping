#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:18:40 2017

@author: huang
"""

#%%

import os 
import re
import pysrt
from mafan import simplify
from guess_language import guess_language
from itertools import compress
from functools import partial
from multiprocessing import Pool 

os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%
def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True

## use either gbk or big5 or utf-8
def open_srt(f):
    try:
        some_subs = pysrt.open(f,encoding = 'gbk') 
        return some_subs
    except:
        pass
    try:
        some_subs = pysrt.open(f,encoding = 'big5') 
        return some_subs
    except:
        pass
    try:
        some_subs = pysrt.open(f) 
        return some_subs
    except:
        pass
    
    return None

def validate(srt):
    subs = open_srt(srt) 
    if subs is not None:
        languages = [process_language(ele) for ele in subs]
        return languages
    else:
        #print('Can not decode.')
        return None
    
def replace_special(line_str):
    line_str = re.sub('[『』【】「」♫．#♪]','',line_str)
    line_str = re.sub(r'\{.*?\}','',line_str)     # non greedy match 
    line_str = re.sub(r'\<.*?\>','',line_str)     # non greedy match 
    return line_str 

def check_chinese(text):
    ch = re.findall(r'[\u4e00-\u9fff]+', text)
    return ch
def check_english(text):
    en = re.findall(r"[A-Za-z]+", text)
    return en

def process_language(ele):
    try:
        text_list = ele.text.split('\n')
        text_list = [replace_special(x) for x in text_list]
        languages = [guess_language(l) for l in text_list]
        en_index = [l=='en' for l in languages]
        zh_index = [l=='zh' for l in languages]
        en_lines = list(compress(text_list,en_index))
        zh_lines = list(compress(text_list,zh_index))
        if len(en_lines)==0 or len(zh_lines)==0:
            return None
        en_text = ' '.join(en_lines)
        if len(check_chinese(en_text)) > 0:
            return None 
        zh_text = simplify(' '.join(zh_lines))
        if len(check_english(zh_text))>0:
            return None
        text_line = en_text + ' | ' + zh_text
        return text_line
    except:
        return None
    
def process_srts(f,results_raw):
    index, srt = f
    res = validate(srt)
    if res is not None: 
        total = len(res)
        ## we only gonna to use files with both english and chinese in it 
        if total > 0:
            none_values = sum([x is None for x in res ])
            ratio = float(none_values)/float(total)
            if ratio > 0.9:  
                pass         
            else:
                res = res[5:-5]
                res = [x for x in res if x is not None]
                filename, file_extension = os.path.splitext(srt)
                fname = filename.split('/')[-1]
                fname = results_raw+fname+'.txt'
                with open(fname, mode='wt', encoding='utf-8') as myfile:
                    myfile.write('\n'.join(res))
                #print(res)
                if index%100 == 0:
                    print(index)
#%%

if __name__ == '__main__':
    data_folder = 'data/'
    data_srt = data_folder + 'srt/'
    data_ass = data_folder + 'ass/'
    results_raw = data_folder+'data_results_srt/'
    
    folders = [data_folder,data_srt,data_ass,results_raw]
    [check_dir(x) for x in folders]
    
    ## search for srts with both chinese and english in it
    ## and transform them into txt, seperated by |, dump to results raw
    data_srts = [data_srt + f for f in os.listdir(data_srt)]
    
    #multi process unpacking
    p = Pool(10)
    partial_unpack = partial(process_srts, results_raw = results_raw)
    process_mp = p.map(partial_unpack,enumerate(data_srts))
    p.close()
    p.join()
    print('finish')

    
    