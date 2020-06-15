'''
@Time   : 2020/2/3 1:19 PM 
@Author : kennethAsher
@content: 
'''

from elasticsearch import Elasticsearch
import os

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

def insert_agent_num(input_path):
    input_file = open(input_path, 'r', encoding='utf8')
    k = 0
    for line in input_file.readlines():
        if k%100 == 0:
            print(k)
        k = k+1
        fields = line.strip().split('|')
        num = 0 if int(fields[3]) < 7 else (5*int(fields[3])-30)/84
        score = float('%.2f' % num)
        data = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[1], "lawyer_organ_name": fields[2],
                'agent_num': int(fields[3]), 'agent_score': score}
        es.index(index='pg_lawyer_agent_num_ken', doc_type='doc', body=data)
    input_file.close()
base_dir = '/mnt/disk1/data/table/table_agent_num'
paths = os.listdir(base_dir)
for _path in paths:
    path = base_dir+'/'+_path
    print('the file {} starting upload'.format(_path))
    insert_agent_num(path)
    print('the file {} is uploaded'.format(_path))
