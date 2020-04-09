# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/18 下午4:59
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @region  : 因为我忘记了是不是使用的新的数据库去对照的id
# @Content : 本篇内容主要是将原本筛选好的lawyer中的id和律师姓名-律所名称拿出来，
             去数据库里面进行对照，从而验证是否正确
'''

import logging
logging.basicConfig(filename='/mnt/disk1/log/python/root/demo/demo1.log',filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

file_open = open('/mnt/disk1/data/utils_data/lawyer_case_data/merge_caseinfo', 'r', encoding='utf8')
file_write = open('/mnt/disk1/data/utils_data/lawyer_case_data/get_id', 'w', encoding='utf8')
i = 0
for line in file_open.readlines():
    fields = line.strip().split('|')
    out_line = fields[0]+'|'+fields[7]+'|'+fields[8]
    i = i+1
    if i%10000 ==0:
        logging.info('this line is {}'.format(str(i)))
    file_write.write(out_line+'\n')

file_open.close()
file_write.close()