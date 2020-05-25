# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : InsertLawyerScore.py
@ctime  : 2020/5/25 10:01
@Email  : 1131771202@qq.com
@content: 将计算好分值的律师数据存放至lawyerscore表中
"""

import pymysql

file_open = open('/mnt/disk1/data/untils_data/lawyer_data//lawyer_score')
no_open = open('/mnt/disk1/data/pg_data//pg_lawyer.txt')


conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
                               user='pg_db',
                               password='ds930$232aH!@#FD',
                               db='pg_test',
                               charset='utf8')

no_mapping = {}
for line in no_open.readlines():
    fields = line.strip().split('|')
    try:
        key = fields[0]
        value = fields[2]
        if len(value)> 5:
            no_mapping[key] = value
    except :
        continue
no_open.close()


cursor = conn.cursor()
for line in file_open.readlines():
    fields = line.strip().split('|')
    no_id = ''
    if fields[0] in no_mapping:
        no_id = no_mapping[fields[0]]
    fields[1] = fields[1] if fields[1] != '' else 0
    fields[2] = fields[2] if fields[2] != '' else 0
    fields[4] = fields[4] if fields[4] != '' else 0
    fields[6] = fields[6] if fields[6] != '' else 0
    fields[8] = fields[8] if fields[8] != '' else 0
    fields[10] = fields[10] if fields[10] != '' else 0
    fields[12] = fields[12] if fields[12] != '' else 0
    fields[13] = fields[13] if fields[13] != '' else 0
    fields[14] = fields[14] if fields[14] != '' else 0
    fields[15] = fields[15] if fields[15] != '' else 0
    fields[16] = fields[16] if fields[16] != '' else 0
    fields[18] = fields[18] if fields[18] != '' else 0
    fields[20] = fields[20] if fields[20] != '' else 0
    fields[22] = fields[22] if fields[22] != '' else 0
    fields[23] = fields[23] if fields[23] != '' else 0
    fields[24] = fields[24] if fields[24] != '' else 0
    fields[25] = fields[25] if fields[25] != '' else 0
    fields[26] = fields[26] if fields[26] != '' else 0
    fields[27] = fields[27] if fields[27] != '' else 0
    fields[28] = fields[28] if fields[28] != '' else 0
    fields[29] = fields[29] if fields[29] != '' else 0
    fields[30] = fields[30] if fields[30] != '' else 0
    sql = 'insert into `pg_lawyer_socre` ( `lawyer_id`, `work_ex`,`ex_soure`,`case1_name`,`case1_count`,`case2_name`,`case2_count`,' \
          '`case3_name`,`case3_count`,`case4_name`,`case4_count`,`trail_name`,`trail_count`,`doc_count`,`doc_score`,`year_doc_count`,' \
          '`year_doc_score`,`court_name`,`court_count`,`city_name`,`city_count`,`judent_name`,`judent_count`,`parties_company`,`parties_company_score`,' \
          '`parties_government`,`parties_government_score`,`parties_private`,`parties_private_score`,`parties_person`,`parties_person_score`,`lawyer_license_no`) values ("{}",{},{},"{}",' \
          '{},"{}",{},"{}",{},"{}",{},"{}",{},{},{},{},{},"{}",{},"{}",{},"{}",{},{},{},{},{},{},{},{},{},"{}")'.format(
        fields[0], float(fields[1]), float(fields[2]),
        fields[3], int(fields[4]), fields[5], int(fields[6]), fields[7], int(fields[8]), fields[9], int(fields[10]),
        fields[11], int(fields[12]),
        int(fields[13]), float(fields[14]), float(fields[15]), float(fields[16]), fields[17], int(fields[18]),
        fields[19], int(fields[20]),
        fields[21], int(fields[22]), int(fields[23]), float(fields[24]), int(fields[25]), float(fields[26]),
        int(fields[27]), float(fields[28]), int(fields[29]), float(fields[30]), no_id)
    cursor.execute(sql)
    conn.commit()
file_open.close()
cursor.close()
conn.close()