# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/24 下午4:16
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将清洗计算好的judge数据存放至es的pg_judge_info_ken表中
'''

from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)

def load_data(lines, path):
    print('loading... file')
    file_open = open(path, 'r', encoding='utf8')
    for line in file_open.readlines():
        lines.append(line.strip().split('|'))
    print('load file over')
    return lines

def batch_data(lines,k):
    """ 批量写入数据 """
    while len(lines) > 0:
        the_lines = []
        for i in range(0, 1000):
            if len(lines) == 0:
                break
            the_lines.append(lines.pop(0))
        action = ({
            "_index": "test_pg_judge_info_ken",
            "_type": "doc",
            "_source": {
                "id": int(fields[0]),
                "name":fields[1],
                "court": fields[2],
                "court_level": fields[3],
                "earliest_year": fields[4],
                "judicial_doc_cnt":int(fields[6]),
                "last_year_judicial_cnt":int(fields[7]),
                "data_source":0,
                "court_proceeding_type":fields[8].replace('-','|')
            }
        } for fields in the_lines)
        helpers.bulk(es, action)
        k +=1000
        print('传输了{}条'.format(k))

if __name__ == '__main__':
    k = 0
    lines = []
    # path = '/mnt/disk1/data/utils_data/judge_data/judge_count/judge_count'
    path = 'D:\\judge_data\\judge_info\\judge_info_result'
    lines = load_data(lines, path)
    print('开始...')
    batch_data(lines,k)
    print('上传完成')