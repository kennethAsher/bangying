# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/10 12:49 下午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将数据库中目前不存在的法院清洗出来
'''

court_open = open('/Users/by-webqianduan/data/court/organ_couct_clean','r', encoding='utf8')
old_court_open=open('/Users/by-webqianduan/Documents/pg_data/pg_court.txt','r', encoding='utf8')

file_write = open('/Users/by-webqianduan/data/court/data_new.txt','w',encoding='utf8')

court_set = set()

for line in old_court_open.readlines():
    court_set.add(line)

for line in court_open.readlines():
    if line not in court_set:
        file_write.write(line)