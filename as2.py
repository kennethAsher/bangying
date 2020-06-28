# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/15 11:11 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 开始整那些标的额啦
'''

import re
import os
from elasticsearch import Elasticsearch
import re

file_open = open('/Users/kenneth-mac/data/test/zagk', 'r', encoding='utf8')
file_write = open('/Users/kenneth-mac/data/test/zagk_out', 'w', encoding='utf8')

for line in file_open.readlines():
    fields = line.strip().split('|')
    if 50>len(fields[3])>1:
        file_write.write(fields[0]+'|'+fields[3]+'\n')
file_open.close()
file_write.close()