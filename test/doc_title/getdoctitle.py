#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/12 1:41 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 对律师数据的律师id-裁判文书标题-案件类型获取
'''

import os

def get_content(open_dir, out_dir):
    out_path = open(out_dir, 'w', encoding='utf8')
    names = os.listdir(open_dir)
    for name in names:
        in_path = open('{}{}'.format(open_dir,name), 'r', encoding='utf8')
        for line in in_path.readlines():
            fields = line.strip().split('|')
            out_line = fields[0]+'|'+fields[2]+'|'+fields[10]
            out_path.write(out_line+'\n')
        in_path.close()
    out_path.close()

def run(open_dir, out_dir):
    get_content(open_dir, out_dir)

if __name__ == '__main__':
    open_dir = '/mnt/disk1/data/doc_data/doc_result/result1/'
    out_dir = '/mnt/disk1/data/utils_data/doc_title/get_doc_title'
    run(open_dir, out_dir)
