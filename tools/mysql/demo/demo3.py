# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/15 2:59 下午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 更新原本存放律师详情的数据的日期的分值数据
'''

import pymysql

class demo3():
    def __init__(self):
        self.file_path = '/Users/by-webqianduan/Downloads/data'
        self.conn = pymysql.connect(host='39.107.110.141',
                               user='root',
                               password='root',
                               db='pg_data',
                               charset='utf8')


    def read_data(self):
        cursor = self.conn.cursor()
        file_open = open('demo3','r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('|')
            if len(fields)<2:
                continue
            id = fields[0]
            ex = float(fields[1])
            score = float(fields[2])
            # print(line)
            sql = "update pg_lawyer_socre_5 set work_ex={},ex_soure={} where lawyer_id = '{}'".format(ex, score, id)
            cursor.execute(sql)
            self.conn.commit()
        cursor.close()

    def run(self):
        self.read_data()

if __name__ == '__main__':
    demo = demo3()
    demo.run()