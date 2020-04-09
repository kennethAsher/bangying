# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/19 上午10:15
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 给单个文件去重
'''

file_open = open('get_id', 'r', encoding='utf8')
file_write = open('distinct_id', 'w', encoding='utf8')

id_set = set()
for line in file_open.readlines():
    id_set.add(line.strip())
for key in id_set:
    file_write.write(key+'\n')
    