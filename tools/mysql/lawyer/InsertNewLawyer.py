# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : InsertNewLawyer.py
@ctime  : 2020/5/22 9:58
@Email  : 1131771202@qq.com
@content: 添加新的lawyer以及律所并补充律师id
"""

import pymysql

input_file = '/mnt/disk1/data/untils_data/lawyer_data/in_file'
file_open = open(input_file, 'r', encoding='utf8')

conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
                               user='pg_db',
                               password='ds930$232aH!@#FD',
                               db='pg_test',
                               charset='utf8')
cursor = conn.cursor()

for line in file_open.readlines():
    fields = line.strip().split('|')
    lawyer_id = int(fields[0])
    name = fields[1]
    court = fields[2]
    if len(fields)==3:
        sql = "insert into pg_lawyer(id, lawyer_name, organ_name, organ_name_orgin) values({},'{}','{}','{}')"\
            .format(lawyer_id, name, court, court)
        cursor.execute(sql)
    conn.commit()
cursor.close()
conn.close()