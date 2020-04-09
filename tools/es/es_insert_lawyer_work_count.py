#!/usr/bin/python3.6
# -*- conding:utf-8 -*-

"""
@author : kennethAsher
@fole   : es_insert_lawyer_work_count.py
@ctime  : 2020/1/9 15:40
@Email  : 1131771202@qq.com
@comment: 将律师在城市的工作次数添加至es的pg_lawyer_work_city_counts
"""

from elasticsearch import Elasticsearch
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

#创建表
# result = es.indices.create(index='pg_lawyer_work_city_counts', ignore=400)
# print(result)

work_counts = open('D:\\work_count\\no1_out\\000000_0', 'r', encoding='utf-8')
k = 0
for line in work_counts:
    k = k + 1
    fields = line.strip().split('|')
    lawyer_id = int(fields[0])
    lawyer_name = fields[1]
    organ_name = fields[2]
    work_city = fields[3]
    work_count = int(fields[4])
    is_max = int(fields[5])
    data = {'lawyer_id':lawyer_id, 'lawyer_name':lawyer_name, 'organ_name':organ_name, 'work_city':work_city, 'work_count':work_count, 'is_max':is_max}
    es.index(index='pg_lawyer_work_city_counts', doc_type='doc', body=data)
    if k % 100 == 0: print(k)

