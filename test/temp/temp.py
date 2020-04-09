# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/21 下午5:26
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 测试，往这里写就行了
'''

import re
#切分法院的正则
court_split_pat = re.compile(r'/|—||e|;|]|\)|\?|”|号|1|2|3|4|5|6|7|8|9|0|，|：|\+|`|（|＋'
                             r'||－|笔录|A;|判决|纠纷|签发|爱欣|我|意见|存档|判长|易忠东'
                             r'|抄送|期间内|份数|审批栏|判决|底端|年月日|仿宋|宋体|﹥')
court_clean_pat = re.compile(r'　| |SHAPE\*MERGEFORMAT|PAGE|ˎ̥|E\*MERGEFORMAT|_')
data_open = open('/Users/by-webqianduan/data/court/data','r', encoding='utf8')
court_open = open('/Users/by-webqianduan/Documents/pg_data/pg_court.txt','r', encoding='utf8')
data_write = open('/Users/by-webqianduan/data/court/data_write','w', encoding='utf8')

court_set = set()
for line in court_open.readlines():
    court_set.add(line.strip())
flag=0
for line in data_open.readlines():
    clean_court = court_clean_pat.sub('',line.strip().split('|')[0])
    court = court_split_pat.split(clean_court)[-1].replace('黑黑','黑').replace('广广','广')
    if court not in court_set:
        data_write.write(court+'\n')


