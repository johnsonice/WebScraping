#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 22:39:36 2017

@author: johnsonice
"""

import pysrt
import os 
import string
from os import path

pwd = os.getcwd()
file = 'G.srt'
subs = pysrt.open(file,'gbk','ignore')

subs
