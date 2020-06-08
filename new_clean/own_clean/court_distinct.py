# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/1 下午1:53
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 在清洗好的裁判文书中找到不同名称的法院并单独抽取出来补全数据库
'''

file_open = open('data', 'r', encoding='utf8')
file_write = open('write_data','w',encoding='utf8')

court_set = set()

for line in file_open.readlines():
    fields = line.strip().split('|')
    court_set.add(fields)[1]

for court in court_set:
    file_write.write(court+'\n')
file_open.close()
file_write.close()