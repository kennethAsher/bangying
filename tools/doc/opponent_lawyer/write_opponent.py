#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/4 4:09 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 从完整数据中抽取每个律师对应的对手律师
'''

import os
def write_opponent(input_dir,out_dir,name):
    file_open = open('{}{}'.format(input_dir,name), 'r', encoding='utf-8')
    file_write = open('{}{}'.format(out_dir,name), 'w', encoding='utf-8')
    for line in file_open.readlines():
        fields = line.split('|')
        out_line = fields[0] +'|'+ fields[17]
        file_write.write(out_line+'\n')
    file_open.close()
    file_write.close()

def get_names(open_dir):
    names = os.listdir(open_dir)
    return names

def run(open_dir,input_dir,out_dir):
    names = get_names(open_dir)
    for name in names:
        write_opponent(input_dir,out_dir,name)

if __name__ == '__main__':
    open_dir = '/mnt/disk1/data/doc_data/doc_result/result1/'
    input_dir = '/mnt/disk1/data/doc_data/doc_result/result1/'
    out_dir = '/mnt/disk1/data/utils_data/lawyer_opponent/write_opponent/'
    run(open_dir,input_dir,out_dir)
