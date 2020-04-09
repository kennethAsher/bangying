# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/23 上午11:03
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将数据库法院和清洗出的法院关系对应表建立，
'''

import pymysql
import logging

logging.basicConfig(filename='../../../log/mysql/demo/demo1.log',
                    filemode="w", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%M-%Y %H:%M:%S",
                    level=logging.INFO)

# conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
#                        user='pg_db',
#                        password='ds930$232aH!@#FD',
#                        db='pg_simulate',
#                        charset='utf8')

conn = pymysql.connect(host='39.107.110.141',
                       user='root',
                       password='root',
                       db='pg_data',
                       charset='utf8')
cursor = conn.cursor()

file_open = open('/Users/by-webqianduan/Documents/法院关系', 'r', encoding='utf8')

k = 0
for line in file_open.readlines():
    logging.info('已经传输了{}条'.format(k))
    k = k+1
    cursor = conn.cursor()
    fileds = line.strip().split('|')
    if len(fileds)<2:
        print(line)
        break
    try:
        sql = "select id from pg_court where name like '%{}%'".format(fileds[1])
        cursor.execute(sql)
        data = cursor.fetchone()


        sql1 = "insert into court_map(court_id, court_map_name) values('{}','{}')".format(int(data[0]), fileds[0])
        cursor.execute(sql1)
        conn.commit()
    except:
        logging.warning('错误数据：'+line)
    cursor.close()


conn.close()