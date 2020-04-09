# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/20 下午6:14
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 替换文件中的字符，将|替换成|
'''

file_open = open('court_relation', 'r', encoding='utf8')
file_write = open('court_relation_out', 'w', encoding='utf8')

for line in file_open.readlines():
    line = line.strip()
    if '｜' in line:
        line = line.replace('｜','|')
    file_write.write(line +'\n')