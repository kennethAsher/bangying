# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/1 下午4:49
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 清洗已经分离出来的民事判决书中的法院，并且提取出文书年份和审理程序
'''

import re
#切分法院的正则
court_split_pat = re.compile(r'/|—||e|;|]|\)|\?|”|号|1|2|3|4|5|6|7|8|9|0|，|：|\+|`|（|＋'
                             r'||－|笔录|A;|判决|纠纷|签发|爱欣|我|意见|存档|判长|易忠东'
                             r'|抄送|期间内|份数|审批栏|判决|底端|年月日|仿宋|宋体|﹥')
#清洗法院的正则
court_clean_pat = re.compile(r'　| |SHAPE\*MERGEFORMAT|PAGE|ˎ̥|E\*MERGEFORMAT|_')


data_open = open('/mnt/disk2/data/mspjs/court_type_case/data','r', encoding='utf8')
data_write = open('/mnt/disk2/data/mspjs/court_type_case/data_write','w', encoding='utf8')

for line in data_open.readlines():
    fields = line.strip().split('|')
    clean_court = court_clean_pat.sub('',fields[1])
    court = court_split_pat.split(clean_court)[-1].replace('黑黑','黑').replace('广广','广')

    year = fields[3][fields[3].index('(')+1:fields[3].index('(')+5] if '(' in fields[3] else ""
    if '初' in fields[3]:
        trail = '一审'
    elif '终' in fields[3]:
        trail = '二审'
    elif '再' in fields[3] or '申' in fields[3] or '监' in fields[3] or '抗' in fields[3]:
        trail = '再审'
    else:
        trail = '特殊程序'
    out_line = fields[0]+'|'+court+'|'+fields[2]+'|民事案件|判决书|'+fields[3]+'|'+year+'|'+trail+'\n'
    data_write.write(out_line)