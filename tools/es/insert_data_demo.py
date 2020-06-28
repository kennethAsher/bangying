#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/6/16 1:35 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 将单个文书数据插入得es库中
'''

from elasticsearch import Elasticsearch

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)

# test_pg_ws_lawyercase_ken
# data = {
#                         "lawyer_name": '陈立意',
#                         "lawyer_organ_name": '陈立意',
#                         "lawyer_id": 1000806037,
#                         "partners": [{'name':'王力', 'office':'北京市浩天信和律师事务所'}],
#                         "opponents": [],
#                         "docid": '',
#                         "casereason": '侵害商标权纠纷',
#                         "casetype": '民事案件',
#                         "doctype": '民事裁定书',
#                         "trialprocedure": '一审',
#                         "judgeyear": '2019',
#                         "judgemonth": '201912',
#                         "court": '北京市朝阳人民法院',
#                         "courtlevel": '基层',
#                         "province": '北京市',
#                         "city": '北京市',
#                         "region": '朝阳区',
#
#                         "partystatus": '被告',
#                         "partytype": True,
#                         "justices": [{'name':'李一可','status':'审判长','statuscode':'JUDGE'},{'name':'裘晖','status':'审判员','statuscode':'JUDGE'},{'name':'谭雅文','status':'审判员','statuscode':'JUDGE'},{'name':'谢雨佳','status':'书记员','statuscode':'CLERK'}]
#                     }
# result = es.index(index='test_pg_ws_lawyercase_ken', doc_type='doc', body=data)
# print(result)




# test_pg_lawyer_info_attr_ken
data = {
                        "lawyer_id": 1000019184,
                        "lawyer_name": '王力',
                        "lawyer_organ_name": '北京市浩天信和律师事务所',
                        "type_code": 'JUDGE_PERSON',
                        "type_name": '审判人员',
                        "type_param_code": '',
                        "type_param_name": '东城区',
                        "first_year": '2019',
                        "casereason_set": [],
                        "trialprocedure_set": ['一审','特殊程序']
                    }
result = es.index(index='test_pg_lawyer_info_attr_ken', doc_type='doc', body=data)
print(result)