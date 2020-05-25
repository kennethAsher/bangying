#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/24 11:35 AM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 
'''

import pymysql

file_open = open('/Users/kenneth-mac/data/merge_out1', 'r', encoding='utf-8')
conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com', user='pg_db', password='ds930$232aH!@#FD', db='pg_simulate', charset='utf8')
cursor = conn.cursor()
i = 0
for line in file_open.readlines():
    fields = line.strip().split('|')
    # sql = 'select id from pg_lawyer_copy2 where lawyer_name="{}" and organ_name_orgin="{}"'.format(fields[6], fields[7])
    # cursor.execute(sql)
    # info1 = cursor.fetchone()
    # if info1 is None:
    #     # id = id + 1
    # item = (fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],fields[8],fields[9],fields[10],fields[11],fields[12],fields[13],fields[14],fields[15],fields[16],fields[17],fields[18],fields[19],fields[20],fields[21],fields[22])
    sql = 'insert into `pg_lawyer_socre` ( `lawyer_id`, `work_ex`,`ex_soure`,`case1_name`,`case1_count`,`case2_name`,`case2_count`,' \
          '`case3_name`,`case3_count`,`case4_name`,`case4_count`,`trail_name`,`trail_count`,`doc_count`,`doc_score`,`year_doc_count`,' \
          '`year_doc_score`,`court_name`,`court_count`,`city_name`,`city_count`,`judent_name`,`judent_count`,`parties_company`,`parties_company_score`,' \
          '`parties_government`,`parties_government_score`,`parties_private`,`parties_private_score`,`parties_person`,`parties_person_score`) values ("{}",{},{},"{}",' \
          '{},"{}",{},"{}",{},"{}",{},"{}",{},{},{},{},{},"{}",{},"{}",{},"{}",{},{},{},{},{},{},{},{},{})'.format(fields[0], int(fields[1]),float(fields[2]),
            fields[3],int(fields[4]),fields[5],int(fields[6]),fields[7],int(fields[8]),fields[9],int(fields[10]),fields[11],int(fields[12]),
            int(fields[13]),float(fields[14]),float(fields[15]),float(fields[16]),fields[17],int(fields[18]),fields[19],int(fields[20]),
            fields[21],int(fields[22]),int(fields[23]),float(fields[24]),int(fields[25]),float(fields[26]),int(fields[27]),float(fields[28]),int(fields[29]),float(fields[30]))
    cursor.execute(sql)

    #没有提交成功是因为插入语句没有commit
    conn.commit()
cursor.close()
conn.close()