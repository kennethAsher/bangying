#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/21 2:23 PM 
@Author : kennethAsher
@content: 在解析完全的文档内容里面拿到推荐分值的内容
'''

file_open = open('mulu', 'r', encoding='utf8')
file_write = open('mulu', 'w', encoding='utf8')

for line in file_open.readlines():
    fields = line.split('｜')
    out_line = fields[0]+'|'+fields[1]+'|'+fields[10]+'|'+fields[8]+'|'+fields[9]+'|'+fields[5]+'|'+fields[4]
    +'|' + fields[13]+'|'+fields[14]+'|'+fields[15]+'|'+fields[18]+'|'+fields[19]+'|'+fields[20]+'|'+fields[21]+'|'+fields[22]

    file_write.write(out_line)

file_open.close()
file_write.close()