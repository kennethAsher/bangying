# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/23 下午4:18
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将法院名称清洗干净然后去重，重新写入到新文件中
'''

import re

clean_court_pat = re.compile(r'NULL|\+|,|-|\.|0|1|2|3|4|5|6|7|8|9|>|\?|null|VF|_|`|·|ˎ̥|‘|、|【')


file_open = open('/Users/by-webqianduan/data/court/organ_court','r',encoding='utf8')
file_write = open('/Users/by-webqianduan/data/court/organ_couct_clean', 'w', encoding='utf8')

court_set = set()

for line in file_open.readlines():
    if clean_court_pat.findall(line) is not None:
        line = clean_court_pat.split(line)[-1]
    court_set.add(line)

for court in court_set:
    file_write.write(court)

file_open.close()
file_write.close()
