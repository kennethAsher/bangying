# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : NewLawyerScore.py
@ctime  : 2020/5/22 14:17
@Email  : 1131771202@qq.com
@content: 计算律师分值，直接放进数据库
"""

import os
import logging
import datetime

logging.basicConfig(filename='/mnt/disk1/log/python/untils/get_data/NewLawyerScore.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

class LawyerScore():
    def __init__(self):
        self.input_path = '/mnt/disk2/data/sum_data/lawyer_result/lawyer_score_data_no/'
        self.out_file = '/mnt/disk2/data/sum_data/lawyer_result/lawyer_score'

        self.cause_mapping4_3 = {}
        self.cause_mapping3_2 = {}
        self.cause_mapping2_1 = {}
        self.cause_name = set()
        # 最低的年限
        self.year_mapping = {}
        # 裁判文书的总量
        self.doc_count_mapping = {}
        # 审理程序
        self.trail_mapping = {}
        # 管辖机构
        self.court_mapping = {}
        # 所在市区
        self.city_mapping = {}
        # 审判人员
        self.jud_mapping = {}
        # 争议类型
        self.cause_mapping = {}
        # 客户类型
        self.parties_mapping = {}

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

    def get_year_doc(self, year, doc_count):
        return doc_count / year

    def get_cause_mapping(self):
        cause_file = open('/mnt/disk2/utils_data/pg_sm_cause_of_action.txt', 'r', encoding='utf8')
        for line in cause_file.readlines():
            fields = line.split('|')
            if fields[3].strip() not in self.cause_mapping4_3:
                if fields[3].strip() is not None:
                    self.cause_mapping4_3[fields[3].strip()] = fields[2].strip()
            if fields[2].strip() not in self.cause_mapping3_2:
                if fields[2].strip() is not None:
                    self.cause_mapping3_2[fields[2].strip()] = fields[1].strip()
            if fields[1].strip() not in self.cause_mapping2_1:
                if fields[1].strip() is not None:
                    self.cause_mapping2_1[fields[1].strip()] = fields[0].strip()
            self.cause_name.add(fields[0])
        cause_file.close()

    def get_parties_score(self, num):
        if num < 0.3:
            return 0
        elif num > 0.8:
            return 10
        else:
            return 2 * ((10 * num) - 3)

    def getting_mapping(self,path):
        file_case = open(path, 'r', encoding='utf8')
        for line in file_case.readlines():

            fields = line.strip().split('|')

            # 年份的map--直接存入数值
            try:
                if len(fields[3])>1:
                    data_num = self.get_date(fields[3]) if len(fields[3])>5 else 2020-int(fields[3])
                    if fields[0] not in self.year_mapping and len(fields[3])>1:
                        self.year_mapping[fields[0]] = data_num
                    elif data_num > self.year_mapping[fields[0]]:
                        self.year_mapping[fields[0]] = data_num
                    else:
                        pass

                # 文书总量的map
                if fields[0] not in self.doc_count_mapping:
                    self.doc_count_mapping[fields[0]] = 1
                else:
                    self.doc_count_mapping[fields[0]] = self.doc_count_mapping[fields[0]] + 1

                # 审理程序
                if fields[5].strip() is not None:
                    if fields[0] not in self.trail_mapping:
                        self.trail_mapping[fields[0]] = fields[5].strip()
                    else:
                        self.trail_mapping[fields[0]] = self.trail_mapping[fields[0]] + ',' + fields[5].strip()

                # 管辖机构
                if fields[7].strip() is not None:
                    if fields[0] not in self.court_mapping:
                        self.court_mapping[fields[0]] = fields[7].strip()
                    else:
                        self.court_mapping[fields[0]] = self.court_mapping[fields[0]] + ',' + fields[7].strip()

                # 所在城市
                if fields[8].strip() != '':
                    if fields[0] not in self.city_mapping:
                        self.city_mapping[fields[0]] = fields[8].strip()
                    else:
                        self.city_mapping[fields[0]] = self.city_mapping[fields[0]] + ',' + fields[8].strip()

                # 审判人员
                if fields[9].strip() != '':
                    if fields[0] not in self.jud_mapping:
                        self.jud_mapping[fields[0]] = fields[9].strip()
                    else:
                        self.jud_mapping[fields[0]] = self.jud_mapping[fields[0]] + ',' + fields[9].strip()

                # 案由
                if fields[4].strip() != '':
                    if fields[0] not in self.cause_mapping:
                        self.cause_mapping[fields[0]] = fields[4].strip()
                    else:
                        self.cause_mapping[fields[0]] = self.cause_mapping[fields[0]] + ',' + fields[4].strip()

                # 当事人类型的map
                if fields[6].strip != '':
                    if fields[0] not in self.parties_mapping:
                        self.parties_mapping[fields[0]] = fields[6].strip()
                    else:
                        self.parties_mapping[fields[0]] = self.parties_mapping[fields[0]] + ',' + fields[6].strip()
            except :
                continue
        file_case.close()

    def make_score(self):
        names = os.listdir(self.input_path)
        for name in names:
            path = '{}{}'.format(self.input_path, name)
            logging.info('starting make mapping of file {}'.format(name))
            self.getting_mapping(path)
        lawyer_set = set()
        file_out = open(self.out_file, 'w', encoding='utf8')
        for name in names:
            logging.info('starting writefile of file {}'.format(name))
            file_case = open('{}{}'.format(self.input_path, name), 'r', encoding='utf8')
            for step, line in enumerate(file_case.readlines()):
                fields = line.strip().split('|')
                if fields[0] not in lawyer_set:
                    # 1.1诉讼经验
                    lawyer_set.add(fields[0])
                    if fields[0] in self.year_mapping:
                        year_score = 0 if self.year_mapping[fields[0]] < 3 else (self.year_mapping[fields[0]] * 5 - 10) / 3
                        year_score = 5 if year_score > 5 else year_score
                        year_line = fields[0] + '|' + str(self.year_mapping[fields[0]]) + '|' + str(float('%.2f' % year_score))
                    else:
                        year_line = fields[0]+'||'

                    # 1.2争议类型
                    if fields[0] in self.cause_mapping:
                        cause = self.cause_mapping[fields[0]]
                        cause_fields = cause.strip().split(',')
                        cause_1 = ''
                        cause_2 = ''
                        cause_3 = ''
                        cause_4 = ''

                        for field in cause_fields:
                            if field in self.cause_mapping4_3:
                                cause_4 = cause_4 + ',' + field
                                cause_3 = cause_3 + ',' + self.cause_mapping4_3[field]
                                cause_2 = cause_2 + ',' + self.cause_mapping3_2[self.cause_mapping4_3[field]]
                                cause_1 = cause_1 + ',' + self.cause_mapping2_1[self.cause_mapping3_2[self.cause_mapping4_3[field]]]
                            if field in self.cause_mapping3_2:
                                cause_3 = cause_3 + ',' + field
                                cause_2 = cause_2 + ',' + self.cause_mapping3_2[field]
                                cause_1 = cause_1 + ',' + self.cause_mapping2_1[self.cause_mapping3_2[field]]
                            if field in self.cause_mapping2_1:
                                cause_2 = cause_2 + ',' + field
                                cause_1 = cause_1 + ',' + self.cause_mapping2_1[field]
                            if field in self.cause_name:
                                cause_1 = cause_1 + ',' + field
                        cause_1 = cause_1[1:] if cause_1 is not None else cause_1
                        cause_2 = cause_2[1:] if cause_2 is not None else cause_2
                        cause_3 = cause_3[1:] if cause_3 is not None else cause_3
                        cause_4 = cause_4[1:] if cause_4 is not None else cause_4
                        cause_1_num = 0 if cause_1 == '' else len(cause_1.split(','))
                        cause_2_num = 0 if cause_2 == '' else len(cause_2.split(','))
                        cause_3_num = 0 if cause_3 == '' else len(cause_3.split(','))
                        cause_4_num = 0 if cause_4 == '' else len(cause_4.split(','))
                        cause_line = year_line + '|' + cause_1 + '|' + str(cause_1_num) + '|' + cause_2 + '|' + str(
                            cause_2_num) + '|' + cause_3 + '|' + str(cause_3_num) + '|' + cause_4 + '|' + str(cause_4_num)
                    else:
                        cause_line = year_line + '||||||||'
                    # 1.3审理程序
                    if fields[0] in self.trail_mapping:
                        trail = self.trail_mapping[fields[0]]
                        trail_num = 0 if trail == '' else len(trail.split(','))
                        trail_line = cause_line + '|' + str(self.trail_mapping[fields[0]]) + '|' + str(trail_num)
                    else:
                        trail_line = cause_line + '||'

                    # 2.1文书总量
                    if fields[0] in self.doc_count_mapping:
                        doc_count = self.doc_count_mapping[fields[0]]
                        doc_count_score = 0 if doc_count <= 6 else (doc_count * 5 - 30) / 84
                        doc_count_score = 5 if doc_count_score > 5 else doc_count_score
                        doc_count_line = trail_line + '|' + str(self.doc_count_mapping[fields[0]]) + '|' + str(
                            float('%.2f' % doc_count_score))
                    else:
                        doc_count_line = trail_line + '||'

                    # 2.2年代理量
                    if fields[0] in self.doc_count_mapping:

                        year_doc = self.get_year_doc(self.year_mapping[fields[0]],
                                                self.doc_count_mapping[fields[0]])
                        year_doc_score = 0 if year_doc <= 3 else (year_doc * 5 - 15) / 9
                        year_doc_score = 5 if year_doc_score > 5 else year_doc_score
                        year_doc_line = doc_count_line + '|' + str(year_doc) + '|' + str(float('%.2f' % year_doc_score))
                    else:
                        year_doc_line = doc_count_line + '||'

                    # 2.4管辖机构
                    if fields[0] in self.court_mapping:
                        court = self.court_mapping[fields[0]]
                        court_num = 0 if court == '' else len(court.split(','))
                        court_line = year_doc_line + '|' + court + '|' + str(court_num)
                    else:
                        court_line = year_doc_line + '||'

                    # 2.5所在城市
                    if fields[0] in self.city_mapping:
                        city = self.city_mapping[fields[0]]
                        city_num = 0 if city == '' else len(city.split(','))
                        city_line = court_line + '|' + city + '|' + str(city_num)
                    else:
                        city_line = court_line + '||'

                    # 2.6审判人员
                    jud = '' if fields[0] not in self.jud_mapping else self.jud_mapping[fields[0]]
                    jud_list = []
                    for j in jud:
                        if '-' in j:
                            name = j.split('-')[1]
                            jud_list.append(name)
                    jud_line = city_line + '|' + ','.join(jud_list) + '|' + str(len(jud_list))

                    # 2.3客户类型
                    if fields[0] in self.parties_mapping:
                        parties = self.parties_mapping[fields[0]]
                        # print(parties)
                        parties_company = 0  # 有标签的企业计数
                        parties_company_score = 0  # 有标签的企业分值
                        parties_gevernment = 0  # 政府计数
                        parties_gevernment_score = 0  # 政府分值
                        parties_private = 0  # 非上市民营企业计数
                        parties_private_score = 0  # 非上市民营企业分值
                        parties_person = 0  # 个人计数
                        parties_person_score = 0  # 个人分值
                        parties_list = parties.split(',')
                        count = len(parties_list)
                        if count > 0:
                            for party in parties_list:
                                if '个人' in party:
                                    parties_person = parties_person + 1
                                    continue
                                elif '非上市民营' in party:
                                    parties_private = parties_private + 1
                                    continue
                                elif '有标签企业' in party:
                                    parties_company = parties_company + 1
                                    continue
                                elif '政府' in party:
                                    parties_gevernment = parties_gevernment + 1
                                    continue

                            parties_company_score = str(float('%.2f' % (self.get_parties_score(parties_company / count))))
                            parties_gevernment_score = str(float('%.2f' % (self.get_parties_score(parties_gevernment / count))))
                            parties_private_score = str(float('%.2f' % (self.get_parties_score(parties_private / count))))
                            parties_person_score = str(float('%.2f' % (self.get_parties_score(parties_person / count))))

                        parties_line = jud_line + '|' + str(parties_company) + '|' + parties_company_score + '|' + str(
                            parties_gevernment) + \
                                       '|' + parties_gevernment_score + '|' + str(
                            parties_private) + '|' + parties_private_score + '|' + \
                                       str(parties_person) + '|' + parties_person_score
                    else:
                        parties_line = jud_line + '||||||||'
                    file_out.write(parties_line + '\n')
            file_case.close()
        file_out.close()



    def run(self):
        self.get_cause_mapping()
        self.make_score()



if __name__ == '__main__':
    lawyerscore = LawyerScore()
    lawyerscore.run()