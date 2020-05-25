# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/19 下午5:58
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 测试从mysql数据库直接导入数据到es中
'''

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time

# 连接ES
es = Elasticsearch(
    ['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
    http_auth=('elastic', 'TytxsP^tr!BvCayo'),
    port=9200
)

# 连接MySQL
print("Connect to mysql...")
conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
                       user='pg_db', password='ds930$232aH!@#FD', db='pg_simulate',
                       charset='utf8')
m_cursor = conn.cursor()

try:
    num_id = 0
    while True:
        s = time.time()
        # 查询数据
        sql = "select * from pg_lawyer_socre_3 LIMIT {}, 5000".format(num_id * 5000)

        # 这里假设查询出来的结果为 张三 26 北京
        m_cursor.execute(sql)
        query_results = m_cursor.fetchall()

        if not query_results:
            print("MySQL查询结果为空 num_id=<{}>".format(num_id))
            break
        else:
            actions = []
            for line in query_results:
                cursor = conn.cursor()
                sql_lawyer = "select lawyer_name, organ_name from pg_lawyer where id = {} ".format(int(line[0]))
                cursor.execute(sql_lawyer)
                result = cursor.fetchall()
                # print(result[0][0])
                # 拼接插入数据结构
                action = {
                    "_index": "lawyer_score_ken",
                    "_type": "doc",
                    "_source": {
                        "lawyer_id": int(line[0]),
                        "work_ex": line[1],
                        "ex_soure": line[2],
                        "case1_name": line[3],
                        "case1_count": line[4],
                        "case2_name": line[5],
                        "case2_count": line[6],
                        "case3_name": line[7],
                        "case3_count": line[8],
                        "case4_name": line[9],
                        "case4_count": line[10],
                        "trail_name": line[11],
                        "trail_count": line[12],
                        "doc_count": line[13],
                        "doc_score": line[14],
                        "year_doc_count": line[15],
                        "year_doc_score": line[16],
                        "court_name": line[17],
                        "court_count": line[18],
                        "city_name": line[19],
                        "city_count": line[20],
                        "judent_name": line[21],
                        "judent_count": line[22],
                        "parties_company": line[23],
                        "parties_company_score": line[24],
                        "parties_government": line[25],
                        "parties_government_score": line[26],
                        "parties_private": line[27],
                        "parties_private_score": line[28],
                        "parties_person": line[29],
                        "parties_person_score": line[30],
                        "lawyer_name":result[0][0],
                        "organ_name":result[0][1]
                    }
                }
                # 形成一个长度与查询结果数量相等的列表
                cursor.close()
                actions.append(action)
            # 批量插入
            a = helpers.bulk(es, actions)
            e = time.time()
            print("{} {}s".format(a, e - s))
        num_id += 1

finally:
    m_cursor.close()
    conn.close()
    print("MySQL connection close...")
