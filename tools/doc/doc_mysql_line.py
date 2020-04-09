#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/24 3:54 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 将数据格式修改成mysql能使用的格式
'''

file_open = open('/Users/kenneth-mac/data/merge_out', 'r', encoding='utf8')
file_write = open('/Users/kenneth-mac/data/merge_out1', 'w', encoding='utf8')
for line in file_open.readlines():
    fields = line.split('|')

    case1_count = 0 if fields[3].strip() == '' else len(fields[3].strip().split(','))
    case2_count = 0 if fields[4].strip() == '' else len(fields[4].strip().split(','))
    case3_count = 0 if fields[5].strip() == '' else len(fields[5].strip().split(','))
    case4_count = 0 if fields[6].strip() == '' else len(fields[6].strip().split(','))
    trail_count = 0 if fields[7].strip() == '' else len(fields[7].strip().split(','))
    court_count = 0 if fields[12].strip() == '' else len(fields[12].strip().split(','))
    city_count = 0 if fields[13].strip() == '' else len(fields[13].strip().split(','))
    judent_count = 0 if fields[14].strip() == '' else len(fields[14].strip().split(','))

    out_line = fields[0]+'|'+fields[1]+'|'+fields[2]+'|'+fields[3]+'|'+str(case1_count)+'|'+fields[4]+'|'+str(case2_count)+'|'+fields[5]+'|'+str(case3_count)+ \
               '|' +fields[6]+'|'+str(case4_count)+'|'+fields[7]+'|'+str(trail_count)+'|'+fields[8]+'|'+fields[9]+'|'+fields[10]+'|'+fields[11]+'|'+fields[12]+'|'+str(court_count)+ \
               '|' +fields[13].strip()+'|'+str(city_count)+'|'+fields[14].strip()+'|'+str(judent_count)+'\n'

    file_write.write(out_line)

file_open.close()
file_write.close()