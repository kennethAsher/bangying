#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/24 5:54 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 将入库文件清洗成独立能使用的格式
'''

import os

#清洗含有（）的客户
def clean_str(word):
    word = word.strip()
    if '（' in word:
        start_index = word.index('（')
        if '）' in word:
            end_index = word.index('）')
            word = word[:start_index]+word[end_index+1:]
        else:
            word = word[:start_index]
    return word
def run(name):
    file_open = open('/Users/kenneth-mac/data/lawyer_separate/{}'.format(name), 'r', encoding='utf8')
    print('/Users/kenneth-mac/data/lawyer_separate/{}'.format(name))
    file_write = open('/Users/kenneth-mac/data/lawyer_separate_out/{}'.format(name), 'w', encoding='utf8')
    out_line=''
    k = 0
    print('开始之行')
    for line in file_open.readlines():
        fields = line.strip().split('|')
        judent = fields[9].strip().split(',')
        judents = ''
        # k = k+1
        # if k % 10000 == 0:
        #     print(k)
        if len(judent) > 1:
            for jud in judent:
                if '-' in jud:
                    judents = judents+','+jud.split('-')[1]
        fields[9] = judents[1:]
        parties = clean_str(fields[14].strip())
        fields[14] = parties
        for i in range(15):
            out_line = out_line+'|'+fields[i]
        file_write.write(out_line[1:]+'\n')
        out_line = ''
    file_open.close()
    file_write.close()

base_path = '/Users/kenneth-mac/data/lawyer_separate/'
names = os.listdir(base_path)
for name in names:
    run(name)