#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 20:34:51 2017

@author: huang
"""

#%%
import os 
from shutil import copyfile
os.getcwd()
os.chdir('/Users/huang/Dev/projects/WebScraping/3_renren/')
#%%

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
    
def assign_files(data_unpack):
    unpack_links = []
    unpack_names = []
    for path, subdirs, files in os.walk(data_unpack):
        for name in files:
            unpack_links.append(os.path.join(path, name))
            unpack_names.append(name)
    
    #unpack_links = os.listdir(data_unpack)
    pair = list(zip(unpack_links,unpack_names))
    asss = [f for f in pair if check_ass(f[0])]
    srts = [f for f in pair if check_srt(f[0])]
    print(len(asss))
    print(len(srts))
    if len(asss)>0:
        [copyfile(f[0],data_ass+f[1]) for f in asss]
    if len(srts)>0:
        [copyfile(f[0],data_srt+f[1]) for f in srts]
    print('finish copy files')

    
#%%
if __name__ == '__main__':
    data_folder = 'data/'
    data_raw = data_folder + 'download/'
    data_unpack = data_folder + 'unpack/'
    data_srt = data_folder + 'srt/'
    data_ass = data_folder + 'ass/'
    folders = [data_folder,data_raw,data_unpack,data_srt,data_ass]
    [check_dir(x) for x in folders]
    
    assign_files(data_unpack)

