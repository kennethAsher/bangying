#!/usr/bin/python
# encoding: utf-8
'''
@author: kenneth
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: 1131771202@qq.com
@file: es_insert_pg_ws_parsed.py
@time: 2020/7/22 2:38 下午
@desc: 插入裁判文书es文档
'''
#倒入包
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers

#链接es
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)
#输入路径
insert_path = '/mnt/disk2/data/sum_data/add_result/out_minshi/'

#获取路径下文件名称的方法
def get_names(path):
    return os.listdir(path)
lst = []
for name in get_names(insert_path):
    with open('{}{}'.format(insert_path,name), 'r', encoding='utf8') as file_open:
        print('开始执行文件{}'.format(name))
        lines = file_open.readlines()
        k = len(lines)
        flag = 0
        for step,line in enumerate(lines):
            flag += 1
            fields = line.strip().split('|')
            if fields[-1] == '\\N':
                continue
            doc_id = fields[0]
            title = fields[1]
            caseno = fields[2]
            casereason = fields[3]
            trialprocedure = fields[4]
            court = fields[5]
            courtlevel = fields[6]
            judgeyear = fields[7]
            judgemonth = fields[8]
            judgetime = fields[9]
            province = fields[10]
            city = fields[11]
            region = fields[12]
            casetype = fields[13]
            doctype = fields[14]
            plaintext = fields[16]
            try:
                judge_list = []
                if len(fields[15]) > 3:
                    for judge in fields[15].split(','):
                        judge_status = judge.split('-')[0]
                        judge_code = 'JUDGE' if '审判' in judge_status else 'CLERK'
                        judge_name = judge.split('-')[1]
                        judge_list.append({'name':judge_name, 'statuscode':judge_code, 'status':judge_status})
            except:
                judge_list = []
            lst.append([doc_id,title,caseno,casereason,trialprocedure, court, courtlevel, judgeyear, judgemonth, judgetime, province, city, region,
                        casetype,doctype,plaintext,judge_list])
            if len(lst)>999 or k-1 == step:
                # print(lst)
                action = ({
                    "_index": "test_pg_ws_parsed_ken",
                    "_type": "doc",
                    "_source": {
                        'doc_id' : lst_line[0],
                        'title' : lst_line[1],
                        'caseno' : lst_line[2],
                        'casereason' : lst_line[3],
                        'trialprocedure' : lst_line[4],
                        'court' : lst_line[5],
                        'courtlevel' : lst_line[6],
                        'judgeyear' : lst_line[7],
                        'judgemonth' : lst_line[8],
                        'judgetime' : lst_line[9],
                        'province' : lst_line[10],
                        'city' : lst_line[11],
                        'region' : lst_line[12],
                        'casetype' : lst_line[13],
                        'doctype' : lst_line[14],
                        'plaintext' : lst_line[15],
                        'judge_list' : lst_line[16]
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
print('任务执行完成')