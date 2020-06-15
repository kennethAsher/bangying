# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/21 下午5:18
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将计算好分值的数据批量插入到es中
'''

import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)




def load_data(lines, name):
    print('loading... file')
    file_open = open('data/{}'.format(name), 'r', encoding='utf8')
    for line in file_open.readlines():
        lines.append(line.strip().split('|'))
    print('load file over')
    return lines

def batch_data(lines):
    """ 批量写入数据 """
    while len(lines) > 0:
        the_lines = []
        for i in range(0, 1000):
            if len(lines) == 0:
                break
            the_lines.append(lines.pop(0))
        action = ({
            "_index": "lawyer_score_ken",
            "_type": "doc",
            "_source": {
                "lawyer_id": int(fields[0]),
                "lawyer_name":fields[1],
                "organ_name": fields[2],
                "type_action": fields[3],
                "type_name": fields[4],
                "type_value":fields[5],
                "type_param_name":fields[6],
                "type_param_value":float(fields[7])
            }
        } for fields in the_lines)
        helpers.bulk(es, action)
        print('传输了1000条')

if __name__ == '__main__':
    names = os.listdir('data/')
    for name in names:
        lines = []
        lines = load_data(lines, name)
        print('开始...')
        batch_data(lines)
        print('{}传输完成'.format(name))
