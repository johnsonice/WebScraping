#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 22:15:11 2017

@author: huang
"""

#%%
import ass
import re
import os 
import chardet
from hanziconv import HanziConv
from guess_language import guess_language
from itertools import compress
from functools import partial
from multiprocessing import Pool 

os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%
## get rid of all tags 
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

def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True 
    
## use either gbk or big5 or utf-8
def open_ass(file):

    try:
        with open(file, "r",encoding="gbk") as f:
             doc = ass.parse(f)
        return doc 
    except:
        pass
    try:
        with open(file, "r",encoding="big5") as f:
             doc = ass.parse(f)
        return doc 
    except:
        pass
    try:
        with open(file, "r",encoding="utf-8") as f:
             doc = ass.parse(f)
        return doc 
    except:
        pass
    
    try:
        with open(file, 'rb') as f:
            input_bytes = f.read()
            result = chardet.detect(input_bytes)
            conf = result['confidence']
            res_encoding = result['encoding']
        if conf > 0.95:
            with open(file, "r",encoding=res_encoding) as f:
                doc = ass.parse(f)
            return doc
    except:
        pass
    
    return None

def process_language(ele):
    try:
        text_list = ele.text.split('\\N')
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
        #zh_text = simplify(' '.join(zh_lines))
        zh_text = HanziConv.toSimplified(' '.join(zh_lines))
        #zh_text = ' '.join(zh_lines)
        if len(check_english(zh_text))>0:
            return None
        text_line = en_text + ' | ' + zh_text
        text_line = re.sub(r'\\n',' ',text_line)
        return text_line
    except:
        return None
    
def validate_ass(file):
    subs = open_ass(file)
    if subs is not None:
        subs = subs.events
        languages = [process_language(ele) for ele in subs]
        return languages
    else:
        #print('Can not decode.')
        return None
    
def process_ass(file_ass,results_raw):
    index,ass_file = file_ass
    if index%500 == 0:
        print(index)
    res = validate_ass(ass_file)
    if res is not None: 
        total = len(res)
        #print(total) 
        if total > 0:
            none_values = sum([x is None for x in res ])
            ratio = float(none_values)/float(total)
            if ratio > 0.9:  
                pass         
            else:
                res_short = res[5:-5]
                res_short = [x for x in res_short if x is not None]
                filename, file_extension = os.path.splitext(ass_file)
                fname = filename.split('/')[-1]
                fname = results_raw +fname+'.txt'
                with open(fname, mode='wt', encoding='utf-8') as myfile:
                    myfile.write('\n'.join(res_short))

#%%
if __name__ == '__main__':
    # set up folder path 
    data_folder = 'data/'
    data_ass = data_folder + 'ass/'
    results_raw = data_folder + 'data_results_ass/'
    folders = [data_folder,data_ass,results_raw]
    [check_dir(x) for x in folders]
    
    # get all ass files 
    file_ass = [data_ass + f for f in os.listdir(data_ass)]
    print(len(file_ass))
    
    # process all ass files 
    ## search for srts with both chinese and english in it
    ## and transform them into txt, seperated by |, dump to results raw
    #file_ass = file_ass[:500]

    p = Pool(10)
    partial_ass = partial(process_ass, results_raw = results_raw)
    process_mp = p.map(partial_ass,enumerate(file_ass))
    p.close()
    p.join()
    print('finish')
    
        
