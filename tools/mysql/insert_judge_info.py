# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/24 下午1:03
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将清洗好的审判人员数据插入到表中
'''


import pymysql

file_open = open('test', 'r', encoding='utf-8')
conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com', user='pg_db', password='ds930$232aH!@#FD', db='pg_simulate', charset='utf8')
cursor = conn.cursor()

for line in file_open.readlines():
    fields = line.strip().split('|')
    trail = fields[6].replace(',', '|')
    sql = "insert into pg_user_judge_copy1(id, court, name, court_level, earliest_year, judicial_doc_cnt, court_proceeding_type) " \
          "values({}, '{}', '{}', '{}', '{}', {}, '{}')".format(int(fields[0]), fields[2], fields[1], fields[3], fields[4], int(fields[5]), trail)
    cursor.execute(sql)
    conn.commit()
cursor.close()
conn.close()
