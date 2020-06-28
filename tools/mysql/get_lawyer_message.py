#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/18 9:18 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 通过律师的id查询出律师的信息并保存,下面的是将已经查询到的数据放在es中的ken表中
'''

import pymysql

# file_openn = open('lawyer_id.txt', 'r', encoding='utf8')
# file_write = open('lawyer_write.txt', 'w', encoding='utf8')
#
# conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com', user='pg_db', password='ds930$232aH!@#FD', db='pg_simulate', charset='utf8')
# cursor = conn.cursor()
# for line in file_openn.readlines():
#     word = line.strip()
#     sql = "select id, lawyer_name, organ_name,province, city from pg_lawyer where id = {}".format(word)
#     cursor.execute(sql)
#     data = cursor.fetchone()
#     out_line = ''
#     for i in range(5):
#         if i == 0:
#             out_line = out_line + str(data[i])+'|'
#             continue
#         else:
#             if data[i] is None:
#                 out_line += '|'
#                 continue
#         out_line = out_line + data[i]+ '|'
#
#     file_write.write(out_line[:-1]+'\n')




import re
from elasticsearch import Elasticsearch
final_city_pat = re.compile(r'北京|上海|天津|重庆')
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

file_open = open('lawyer_write.txt', 'r', encoding='utf8')
for line in file_open.readlines():
    fields = line.strip().split('|')
    if fields[4] == '':
        if fields[3] == '':
            data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2]}
            es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)
        else:
            data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                    "type_code":"WORK_PROVINCE", "type_param_code":fields[3]}
            es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)
    else:
        if fields[3] == "":
            match = final_city_pat.match(fields[4])
            if match is not None:
                data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                        "type_code": "WORK_PROVINCE", "type_param_code": fields[4]}
                es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)
                data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                        "type_code": "WORK_CITY", "type_param_code": fields[4]}
                es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)
            else:
                data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                        "type_code": "WORK_CITY", "type_param_code": fields[4]}
                es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)
        else:
            data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                    "type_code": "WORK_PROVINCE", "type_param_code": fields[3]}
            es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)
            data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                    "type_code": "WORK_CITY", "type_param_code": fields[4]}
            es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data)