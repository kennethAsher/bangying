# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/10 10:45 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将已经补充好id的法院添加到法院对应关系表中
'''

import logging
import pymysql

logging.basicConfig(filename='../../../log/mysql/demo/demo2.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",
                    level=logging.INFO)

class demo2():
    def __init__(self):
        self.file_path = 'C:\\Users\\GG257\\OneDrive\\sublime\\帮瀛\\pg_data\\new_pg_court.txt'
        self.conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
                               user='pg_db',
                               password='ds930$232aH!@#FD',
                               db='pg_test',
                               charset='utf8')

    def get_conn(self):
        # 阿里云测试使用
        # conn = pymysql.connect(host='39.107.110.141',
        #                        user='root',
        #                        password='root',
        #                        db='pg_data',
        #                        charset='utf8')
        # 模拟数据库

        cursor = self.conn.cursor()
        return cursor

    def read_data(self):
        cursor = self.get_conn()
        file_open = open(self.file_path,'r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('|')
            if len(fields)<2:
                continue
            try:
                court_id = int(fields[1])
                court_name = fields[0]
                # print(line)
                sql = "insert into court_map(court_id, court_map_name) values('{}','{}')".format(court_id, court_name)
                cursor.execute(sql)
                self.conn.commit()
            except:
                print(line)

        cursor.close()

    def run(self):
        self.read_data()

if __name__ == '__main__':
    demo = demo2()
    demo.run()