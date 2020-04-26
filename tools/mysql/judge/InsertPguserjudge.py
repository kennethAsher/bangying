"""
@author : kennethAsher
@fole   : InsertPguserjudge.py
@ctime  : 2020/4/26 14:43
@Email  : 1131771202@qq.com
@content: 上接清洗整理好的审判人员数据，将所有数据插入到pg_test下的pg_user_judge中
"""

import pymysql

file_open = open('D:\\judge_data\\judge_info\\judge_info_out', 'r', encoding='utf-8')
conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com', user='pg_db', password='ds930$232aH!@#FD', db='pg_test', charset='utf8')
cursor = conn.cursor()

for line in file_open.readlines():
    fields = line.strip().split('|')
    trail = fields[-1].replace('-', '|')
    sql = "insert into pg_user_judge_copy1(court, name, court_level, earliest_year, judicial_doc_cnt,last_year_judicial_cnt, court_proceeding_type) " \
          "values( '{}', '{}', '{}', '{}', {},{}, '{}')".format(fields[1], fields[0], fields[2], fields[3], int(fields[5]), int(fields[6]),trail)
    cursor.execute(sql)
    conn.commit()
cursor.close()
conn.close()