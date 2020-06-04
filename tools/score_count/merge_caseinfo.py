#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/10 11:47 AM 
@Author : kennethAsher
@content: 
'''

import os

out_caseinfo=open('/Users/kenneth-mac/data/merge_caseinfo', 'w', encoding='utf8')
paths = os.listdir('/Users/kenneth-mac/data/table_case_info/')
for data_path in paths:
    print(data_path)
    in_caseinfo = open('/Users/kenneth-mac/data/table_case_info/{}'.format(data_path), 'r', encoding='utf8')
    for line in in_caseinfo.readlines():
        out_caseinfo.write(line)
    in_caseinfo.close()
out_caseinfo.close()