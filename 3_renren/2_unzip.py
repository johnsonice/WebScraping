#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:03:49 2017

@author: huang
"""
#%%
#from bs4 import BeautifulSoup
import os
from functools import partial
from multiprocessing import Pool 
from pyunpack import Archive  # for unpacking

os.getcwd()
os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%
def check(f):
    filename, file_extension = os.path.splitext(f)
    if file_extension == '.zip' or file_extension == '.rar' or file_extension == '.7z':
        return True
    else:
        return False
    
def check_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)        # If not create the directory, inside their home directory
        return True

def check_srt(f):
    filename, file_extension = os.path.splitext(f)
    if file_extension == '.srt':
        return True
    else:
        return False
    
def check_ass(f):
    filename, file_extension = os.path.splitext(f)
    if file_extension == '.ass':
        return True
    else:
        return False
    
def unpack_zip(file,unpack_folder):
    try:
        index,f = file
        Archive(f).extractall(unpack_folder)
        if index % 50==0:
            print(index)
    except:
        pass

#%%

if __name__ == '__main__':
    data_folder = 'data/'
    data_raw = data_folder + 'download/'
    data_unpack = data_folder + 'unpack/'
    data_srt = data_folder + 'srt/'
    data_ass = data_folder + 'ass/'
    
    folders = [data_folder,data_raw,data_unpack,data_srt,data_ass]
    [check_dir(x) for x in folders]
    
    links = os.listdir(data_raw)
    files = [data_raw + f for f in links if check(f)]
    print(len(files))
    # test a small amount first 
    ## files = files[0:100]
    
    #multi process unpacking
    p = Pool(20)
    partial_unpack = partial(unpack_zip, unpack_folder = data_unpack)
    unpack_mp = p.map(partial_unpack,enumerate(files))
    p.close()
    p.join()
    print('finish')
    ## unpack all the data
    
    ## single process
#    for index,f in enumerate(files):
#        try:
#            #f_name,f_ext = os.path.splitext(f)
#            Archive(data_raw+f).extractall(data_unpack)
#        except:
#            pass
