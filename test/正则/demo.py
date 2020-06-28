1#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/18 9:45 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 测试正则表达式
'''



import re
final_city_pat = re.compile(r'北京|上海|天津|重庆')

line = ''
match = final_city_pat.match(line)
if match is not None:
    print('yes')