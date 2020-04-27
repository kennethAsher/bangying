"""
@author : kennethAsher
@fole   : InsertJudgeRelation.py
@ctime  : 2020/4/27 17:24
@Email  : 1131771202@qq.com
@content:
            上街审判人员映射关系数据：judge_info_upgrade_file_relation_id
            将文件内容上传至mysql中的关系映射表：judge_map
"""

import pymysql

file_open = open('D:\\judge_data\\judge_info\\judge_info_upgrade_file_relation_id', 'r', encoding='utf8')
conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com', user='pg_db', password='ds930$232aH!@#FD', db='pg_test', charset='utf8')
cursor = conn.cursor()

for line in file_open.readlines():
    fields = line.strip().split('|')
    trail = fields[7].replace('-', '|')
    sql = "insert into judge_map(court, name, court_level, earliest_year, judicial_doc_cnt,last_year_judicial_cnt, court_proceeding_type, update_court, update_id) " \
          "values('{}', '{}', '{}', '{}', {},{}, '{}', '{}', {})".format(fields[1], fields[0], fields[2],
                                                                   fields[3], int(fields[5]), int(fields[6]), trail, fields[-2], int(fields[-1]))
    cursor.execute(sql)
    conn.commit()
cursor.close()
conn.close()