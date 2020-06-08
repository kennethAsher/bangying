# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/15 11:11 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 开始整那些标的额啦
'''

import re
import os


path = '/mnt/disk1/data/untils_data/lawyer_data/ws_lawyercase/'
names = os.listdir(path)
k = 0
for name in names:
    with open('{}{}'.format(path, name), 'r', encoding='utf8') as file_in:
        for line in file_in.readlines():
            k+=1

print(k)