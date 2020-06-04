# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author : kennethAsher
@fole   : es_insert_ws_judgecase.py
@ctime  : 2020/5/18 17:43
@Email  : 1131771202@qq.com
@content: 将清洗好的judgecase数据上传至es
"""


from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)


path = '/mnt/disk1/data/untils_data/judge_data/ws_judgecase_ext/'
# path = 'D:\\es_data\\ws_judgecase_ext\\'
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
            _id = int(fields[0])
            judge_name = fields[1]
            judge_status = fields[2]
            person_cnt = int(fields[3])
            company_cnt = int(fields[4])
            court = fields[5]
            courtlevel = fields[6]
            docid = fields[7]
            casereason = fields[8]
            casetype = fields[9]
            doctype = fields[10]
            trialprocedure = fields[11]
            judgeyear = fields[12]
            judgemonth = fields[13]
            judgedate = fields[14]
            try:
                lawyer_list = []
                if len(fields[15])>2:
                    lawyers = fields[15].split(',')
                    for l in lawyers:
                        lawyer_list.append({'name':l.split('-')[0], 'office':l.split('-')[1]})
            except:
                lawyer_list = []
            try:
                judge_list = []
                if len(fields[16])>2:
                    judges = fields[16].split(',')
                    for j in judges:
                        judge_list.append(j.split('-')[-1])
            except:
                judge_list = []
            try:
                person_list = []
                if len(fields[17])>1:
                    persons = fields[17][1:].strip().split(',')
                    for p in persons:
                        person_list.append({'name':p.split('-')[1], 'status':p.split('-')[0]})
            except:
                person_list = []
            try:
                company_list = []
                if len(fields[18]) > 1:
                    companies = fields[18][1:].strip().split(',')
                    for c in companies:
                        company_list.append({'name':c.split('-')[1], 'status':c.split('-')[0]})
            except:
                company_list = []

            lst.append([_id,judge_name,judge_status,person_cnt,company_cnt, court, courtlevel,docid, casereason,casetype, doctype, trialprocedure,judgeyear,judgemonth,judgedate,lawyer_list,judge_list,person_list,company_list])
            if len(lst)>999 or k-1 == step:
                # print(lst)
                action = ({
                    "_index": "test_ws_judgecase_ext_ken",
                    "_type": "doc",
                    "_source": {
                        "id": lst_line[0],
                        "judge_name": lst_line[1],
                        "judge_status": lst_line[2],
                        "person_cnt": lst_line[3],
                        "company_cnt": lst_line[4],
                        "court": lst_line[5],
                        "courtlevel": lst_line[6],
                        "docid": lst_line[7],
                        "casereason": lst_line[8],
                        "casetype": lst_line[9],
                        "doctype": lst_line[10],
                        "trialprocedure": lst_line[11],
                        "judgeyear": lst_line[12],
                        "judgemonth": lst_line[13],
                        "judgetime": lst_line[14],
                        "lawyers": lst_line[15],
                        "partners":lst_line[16],
                        "persons":lst_line[17],
                        "companies": lst_line[18]
                    }
                } for lst_line in lst)
                try:
                    helpers.bulk(es, action)
                except :
                    print('出现问题了')
                print('传输了{}条审判人员'.format(str(flag)))
                lst = []
        file_open.close()
        print('上传完成{}'.format(name))