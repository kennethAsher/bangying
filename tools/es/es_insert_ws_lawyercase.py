# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : es_insert_ws_lawyercase.py
@ctime  : 2020/5/27 17:04
@Email  : 1131771202@qq.com
@content: 将清洗好的数据存放在es中的ws_lawyercase表中
"""


from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)


path = '/mnt/disk1/data/untils_data/lawyer_data/ws_lawyercase/'

names = os.listdir(path)
lst = []
for name in names:
    with open('{}{}'.format(path,name), 'r', encoding='utf8') as file_open:
        print('开始执行文件{}'.format(name))
        lines = file_open.readlines()
        k = len(lines)
        flag = 0
        for step,line in enumerate(lines):
            flag += 1
            fields = line.strip().split('|')
            lawyer_name = fields[2]
            organ_name = fields[3]
            lawyer_id = int(fields[1])
            partner_list = []
            if len(fields[4]) > 5:
                partners = fields[4].split(',')
                for partner in partners:
                    if '-' in partner:
                        words = partner.split('-')
                        partner_list.append({"name":words[0],"office":words[1]})
            opponent_list = []
            if len(fields[5]) > 5:
                opponents = fields[5].split(',')
                for opponent in opponents:
                    if '-' in opponent:
                        words = opponent.split('-')
                        opponent_list.append({"name":words[0],"office":words[1]})
            docid = fields[6]
            casereason = fields[7]
            casetype = fields[8]
            doctype = fields[9]
            trail = fields[10]
            judge_year = fields[11]
            judge_month = fields[12].replace('-','')
            court = fields[13]
            court_level = fields[14]
            province = fields[15]
            city = fields[16]
            region = fields[17]
            partystatus = '原告'
            partytype = True
            if fields[0] != '1':
                partystatus = '被告'
                if '个人' in fields[-2].split(',')[-1]:
                    partytype = False
            else:
                if '个人' in fields[-2].split(',')[0]:
                    partytype = False
            judge_list = []
            if len(fields[-1]) > 3:
                judges = fields[-1].split(',')
                for judge in judges:
                    if '-' in judge:
                        words = judge.split('-')
                        judge_code = ''
                        if '审判' in words[0]:
                            judge_code = 'JUDGE'
                        elif '陪审' in words[0]:
                            judge_code = 'JUROR'
                        elif '助理' in words[0] or '法官' in words[0]:
                            judge_code = 'ASSISTANT'
                        else:
                            judge_code = 'CLERK'
                        judge_list.append({'name': words[1], 'status': words[0], 'statuscode':judge_code})
            lst.append(
                [lawyer_name, organ_name, lawyer_id, partner_list, opponent_list, docid, casereason, casetype, doctype,
                 trail, judge_year, judge_month, court, court_level, province, city, region, partystatus, partytype,
                 judge_list])
            #nested
            if len(lst) > 999 or k - 1 == step:
                # action = ({
                #     "_index": "test_pg_ws_lawyercase_ken",
                #     "_type": "doc",
                #     "_source": {
                #         "lawyer_name": lst_line[0],
                #         "lawyer_organ_name": lst_line[1],
                #         "lawyer_id": lst_line[2],
                #         "partners": lst_line[3],
                #         "opponents": lst_line[4],
                #         "docid": lst_line[5],
                #         "casereason": lst_line[6],
                #         "casetype": lst_line[7],
                #         "doctype": lst_line[8],
                #         "trialprocedure": lst_line[9],
                #         "judgeyear": lst_line[10],
                #         "judgemonth": lst_line[11],
                #         "court": lst_line[12],
                #         "courtlevel": lst_line[13],
                #         "province": lst_line[14],
                #         "city": lst_line[15],
                #         "region": lst_line[16],
                #         "partystatus": lst_line[17],
                #         "partytype": lst_line[18],
                #         "justices": lst_line[19]
                #     }
                action = ({
                    "_index": "test_pg_ws_lawyercase_ken",
                    "_type": "doc",
                    "_source": {
                        "lawyer_name": lst_line[0],
                        "lawyer_organ_name": lst_line[1],
                        "lawyer_id": lst_line[2],
                        "partners": lst_line[3],
                        "opponents": lst_line[4],
                        "docid": lst_line[5],
                        "casereason": lst_line[6],
                        "casetype": lst_line[7],
                        "doctype": lst_line[8],
                        "trialprocedure": lst_line[9],
                        "judgeyear": lst_line[10],
                        "judgemonth": lst_line[11],
                        "court": lst_line[12],
                        "courtlevel": lst_line[13],
                        "province": lst_line[14],
                        "city": lst_line[15],
                        "region": lst_line[16],
                        "partystatus": lst_line[17],
                        "partytype": lst_line[18],
                        "justices": lst_line[19]
                    }
                } for lst_line in lst)
                try:
                    helpers.bulk(es, action)
                except:
                    print('出现问题了')
                print('传输了{}条律师数据'.format(str(flag)))
                lst = []
        file_open.close()
        print('上传完成{}'.format(name))
print('任务执行完成')
