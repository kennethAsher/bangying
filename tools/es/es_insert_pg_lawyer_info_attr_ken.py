# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/5/25 下午4:16
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将清洗好的律师数据上传至es库中的pg_lawyer_info_attr_ken中用来代替原表中的pg_lawyer_info_attr_ext表
'''

from elasticsearch import Elasticsearch

def get_mapping_action(dir_name, i):
    mapping = {}
    actions = open(dir_name, 'r', encoding='utf8')
    for line in actions.readlines():
        mapping[line.strip()] = "CAUSE_OF_ACTION_{}".format(i)
    return mapping

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)


mapping1 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action.txt", 1)
mapping2 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action2.txt", 2)
mapping3 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action3.txt", 3)
mapping4 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action4.txt", 4)
mapping = dict(list(mapping1.items()) + list(mapping2.items()) + list(mapping3.items()) + list(mapping4.items()))

def insert_cause(fields):
    if fields[5] not in mapping:
        return
    data_cause = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": mapping[fields[5]],
                  "type_name": "案由", "type_param_code": fields[5], "type_param_name": fields[5],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_cause)

def insert_court(fields):
    data_court = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": "COURT_OR_ARBITRATION_AGENCY",
                  "type_name": "管辖机构", "type_param_code": fields[3], "type_param_name": fields[3],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_court)

def insert_area(fields):
    data_area = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": "WORK_AREA",
                  "type_name": "地域", "type_param_code": fields[9], "type_param_name": fields[9],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_area)

def insert_proceeding(fields):
    data_proceeding = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": "COURT_PROCEEDING",
                  "type_name": "审理程序", "type_param_code": fields[4], "type_param_name": fields[4],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_proceeding)

def insert_judge(fields):
    if fields[8] == "":
        pass
    if ',' not in fields[8]:
        data_judge = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                           "type_code": "JUDGE_PERSON",
                           "type_name": "审判人员", "type_param_code": fields[8], "type_param_name": fields[8],
                           "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
        es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_judge)
    if ',' in fields[8]:
        lists = fields[8].split(',')
        for i in lists:
            data_judge = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                               "type_code": "JUDGE_PERSON",
                               "type_name": "审判人员", "type_param_code": i, "type_param_name": i,
                               "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
            es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_judge )
file_in = open("D:\\lawyer\\lawyer_add_set\\lawyer_add_set.txt", 'r', encoding='utf8')
k = 0
for line in file_in.readlines():
    if k % 100 == 0:
        print(k)
    k = k+1
    fields = line.strip().split('|')
    fields[10] = fields[10].replace('[',"").replace(']','').replace("'","").split(',')
    fields[11] = fields[11].replace('[', "").replace(']', '').replace("'", "").split(',')
    insert_cause(fields)
    insert_court(fields)
    insert_area(fields)
    insert_proceeding(fields)
    insert_judge(fields)

