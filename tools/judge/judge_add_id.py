# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/23 下午8:06
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将清洗好的judge数据按照数据库中存在的id来添加id，如果存在则取出来，如果不存在则添加一个新的
'''

id_open = open('/Users/by-webqianduan/Desktop/pg_user_judge.txt', 'r', encoding='utf8')
file_open = open('/Users/by-webqianduan/data/doc/000245_0_out', 'r', encoding='utf8')
file_write = open('/Users/by-webqianduan/data/doc/000245_0_out_id', 'w', encoding='utf8')

id = 11400000

mapping = {}
out_id = ''
for line in id_open.readlines():
    fields = line.strip().split('|')
    key = fields[2]+'-'+fields[1]
    mapping[key] = fields[0]
for line in file_open.readlines():
    fields = line.strip().split('|')
    if len(fields) < 5:
        continue
    key = fields[0]+'-'+fields[4]
    if key in mapping:
        out_id = mapping[key]
    else:
        out_id = str(id)
        id += 1
        mapping[key] = out_id
    file_write.write(out_id +'|'+ line)

