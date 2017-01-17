#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 20:10:50 2017

@author: johnsonice
"""

#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os 
import json 

os.getcwd()
os.chdir('/home/johnsonice/Desktop/temp/webScrap')

url = "https://www.ted.com/talks?language=zh-cn&sort=newest"
result = requests.get(url)

