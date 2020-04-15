# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/15 11:11 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 第二份demo文件
'''

import os
import datetime
import time

class Demo():
    def __init__(self):
        self.input_path = '/mnt/disk1/data/doc_data/doc_lawyer_case_out/'
        self.out_file = '/mnt/disk1/data/doc_data/doc_untils/lawyer_date/data'
        self.out_lawyer_date_score = '/mnt/disk1/data/doc_data/doc_untils/lawyer_date/lawyer_score'

    def get_names(self):
        return os.listdir(self.input_path)

    def get_mapping(self):
        file_case = open(self.out_file, 'r', encoding='utf8')
        year_mapping = {}
        for line in file_case.readlines():
            fields = line.strip().split('|')
            # 年份的map
            if fields[0] not in year_mapping:
                year_mapping[fields[0]] = fields[1]
            elif fields[1] < year_mapping[fields[0]]:
                year_mapping[fields[0]] = fields[1]
            else:
                pass
        return year_mapping

    def get_date(self, date):
        now_date = str(datetime.datetime.now().date())
        fields = date.split('-')
        now_fields = now_date.split('-')
        num = int(now_fields[0])-int(fields[0])
        year = 365
        month = int(fields[1])
        day = int(fields[2])
        months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
        sum = months[month - 1]
        sum += day
        leap = 0
        if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
            leap = 1
            year += 1
        if leap == 1 and month > 2:
            sum += 1
        return sum/float(year)+num

    def get_lawyer_date(self):
        names = self.get_names()
        file_write = open(self.out_file, 'w', encoding='utf8')
        for name in names:
            file_open = open('{}{}'.format(self.input_path, name), 'r', encoding='utf8')
            for line in file_open.readlines():
                fields = line.split('|')
                lawyer_id = fields[0]
                date = fields[3]
                out_line = lawyer_id+'|'+date+'\n'
                file_write.write(out_line)
            file_open.close()
        file_write.close()

    def get_date_score(self):
        year_mapping = self.get_mapping()
        lawyer_set = set()
        file_case = open(self.out_file, 'r', encoding='utf8')
        file_out = open(self.out_lawyer_date_score, 'w', encoding='utf8')
        for line in file_case.readlines():
            fields = line.strip().split('|')
            if fields[0] not in lawyer_set:
                lawyer_set.add(fields[0])
                date_num = self.get_date(year_mapping[fields[0]])
                date_score = 0 if date_num <= 2 else (date_num*5-10)/3
                year_score = 5 if date_score > 5 else date_score
                year_line = fields[0] + '|' + str(date_num) + '|' + str(float('%.2f' % year_score))
                file_out.write(year_line+'\n')
        file_case.close()
        file_out.close()
if __name__ == '__main__':
    demo = Demo()
    demo.get_date_score()