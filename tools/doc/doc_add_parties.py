#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/21 9:40 AM 
@Author : kennethAsher
@content: 筛选当事人并且添加到结果中， 筛选出姓名即可
'''

import re

docSplitPat = re.compile(r'\.|。|\n')
partiesSplitPat = re.compile(r',|，|;|；|:|：')
partiesPat_line = '原告[人]?|被告[人]?|第三人|上诉人|被上诉人|原审原告|原审被告|原审第三人|再审申请人|被申请人' \
                  '|申请执行人|被执行人|异议人|被异议人|申请人|起诉人|申报人|罪犯|公诉机关|被告人|原公诉机关|上诉人'
file_open = open('/Users/kenneth-mac/data/000359_0', 'r', encoding='utf8')
file_write = open('/Users/kenneth-mac/data/000359_0_write', 'w', encoding='utf8')

for doc_line in file_open.readlines():
    fields = doc_line.split('|')
    lines = list(filter(None, docSplitPat.split(fields[12])))
    line_num=0
    out_line = ''
    for line in lines:
        line = re.sub(r'\s|\\|&middot', '', line)
        line_num = line_num+1
        for word in partiesPat_line.split('|'):
            patterm = r'^({}([\(（].*?[\)）])?)[:：]?(.*)'.format(word)
            matchResut = re.match(patterm, line)
            if matchResut is not None:
                out_line = matchResut.group(1) + '-' + partiesSplitPat.split(matchResut.group(3))[0]
                break
        if len(out_line.strip()) > 1:
            file_write.write(out_line+'\n')
            break
    if out_line.strip() == '':
        file_write.write(out_line + '\n')
