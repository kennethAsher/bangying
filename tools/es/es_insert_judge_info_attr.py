"""
@author : kennethAsher
@fole   : es_insert_judge_info_attr.py
@ctime  : 2020/5/15 9:47
@Email  : 1131771202@qq.com
@content: 将清洗好的judge_info_attr数据放进es中
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)

#将某一维度字段拆解成多条放进list
path = r'D:\judge_info_attr'
with open(path, 'r', encoding='utf8') as judge_info_attr_file:
    lst = []
    flag = 0
    for line in judge_info_attr_file.readlines():
        flag += 1
        fields = line.strip().split('|')
        judge_id = int(fields[2])
        judge_name = fields[0]
        court_name = fields[1]
        all_cnt = int(fields[4])
        if len(fields[3])>2:
            causes = fields[3].split(',')
            for cause in causes:
                words = cause.split('-')
                lst.append([judge_id, judge_name, court_name, 'CAUSE_OF_ACTION_2', '案由', words[0],words[0], all_cnt, int(words[1])])
        if len(fields[5])>2:
            trails = fields[5].split(',')
            for trail in trails:
                words = trail.split('-')
                lst.append([judge_id, judge_name, court_name, 'COURT_PROCEEDING', '审理程序', words[0],words[0], all_cnt, int(words[1])])
        if len(fields[6])>2:
            parties = fields[6].split(',')
            for party in parties:
                words = party.split('-')
                lst.append([judge_id, judge_name, court_name, 'PARTY_TYPE', '当事人类型', words[0],words[0], all_cnt, int(words[1])])
        if len(fields[7]) > 2:
            print('审判人员iod', judge_id)
            lawyers = fields[7].split(',')
            for lawyer in lawyers:
                words = lawyer.split('-')
                lst.append([judge_id, judge_name, court_name, 'RELATED_LAWYER', '关联律师', words[0], words[1], all_cnt,
                            int(words[-1])])
        if len(fields[8])>2:
            judges = fields[8].split(',')
            for judge in judges:
                words = judge.split('-')
                lst.append([judge_id, judge_name, court_name, 'COOPERATE_JUDGE', '合作法官', words[0],words[1], all_cnt, int(words[-1])])

        if len(lst)>1000:
            action = ({
                "_index": "test_pg_judge_info_attr_ken",
                "_type": "doc",
                "_source": {
                    "judge_id": lst_line[0],
                    "judge_name": lst_line[1],
                    "court": lst_line[2],
                    "type_code": lst_line[3],
                    "type_name": lst_line[4],
                    "type_param_code": lst_line[5],
                    "type_param_name": lst_line[6],
                    "all_cnt": lst_line[7],
                    "cnt": lst_line[8]
                }
            } for lst_line in lst)
            helpers.bulk(es, action)
            print('传输了{}条审判人员'.format(str(flag)))
            lst = []



print('上传完成')
