# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : WsLawyerCase.py
@ctime  : 2020/5/27 10:45
@Email  : 1131771202@qq.com
@content: 从原始数据中拿到lawyercase表所需要的字段
        partytype在库中表示，如果是不为个人使用true，是个人的话使用false
"""

import os
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/untils/get_data/ws_lawyercase.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)


class LawyerCase():
    # 初始化方法
    def __init__(self):
        self.input_path = '/mnt/disk2/data/sum_data/add_result/'  # 数据的输入路径
        self.laweyr_id_file = '/mnt/disk2/utils_data/pg_lawyer.txt'  # lawyer_id所在的路径
        self.out_path = '/mnt/disk2/data/sum_data/result/ws_lawyercase/'  # 输出数据的路径
        self.lawyer_friend_path = '/mnt/disk2/data/sum_data/lawyer_judge/'  # 律师以及对手律师的路径

        self.lawyer_id_mapping = {}  # 存放律师id的mapping
        self.plaintiff_mapping = {}  # 存放原告律师的mapping

    # 补充存放律师id的mapping
    def get_lawyer_mapping(self):
        logging.info('starting write data to lawyer_id_mapping')
        with open(self.laweyr_id_file, 'r', encoding='utf8') as file_open:
            for line in file_open.readlines():
                fields = line.strip().split('|')
                try:
                    key = fields[1] + '-' + fields[3]
                    value = fields[0]
                    self.lawyer_id_mapping[key] = value
                except :
                    print('脏数据')
        file_open.close()
        logging.info('ending write data to lawyer_id_mapping')

    # 补充原告律师和被告律师的mapping   1代表原告，0代表被告
    def get_friend_opponent_mapping(self):
        names = os.listdir(self.lawyer_friend_path)
        for name in names:
            logging.info('starting write data to friend_opponent_mapping of file {}'.format(name))
            flag = 1
            flag_str = ''
            with open('{}{}'.format(self.lawyer_friend_path, name), 'r', encoding='utf8') as file_in:
                for line in file_in.readlines():
                    fields = line.strip().split('|')
                    if len(fields[1]) > 1 and len(fields[2]) > 1:
                        if fields[0] in self.plaintiff_mapping:
                            if fields[5] != flag_str:
                                flag = 0
                            out = str(flag) + '|' + fields[1] + '|' + fields[2] + '|' + fields[4] + '|' + fields[5]
                            self.plaintiff_mapping[fields[0]] = self.plaintiff_mapping[fields[0]]+'=='+out
                        else:
                            out = str(flag) + '|' + fields[1] + '|' + fields[2] + '|' + fields[4] + '|' + fields[5]
                            self.plaintiff_mapping[fields[0]] = out
                            flag = 1
                            flag_str = fields[5]
            file_in.close()
        logging.info('ending write data to friend_opponent_mapping')

    # 从原数据中获取到需要格式的日期
    def get_year_and_month(self, fields):
        if len(fields[9]) > 5:
            return fields[9][:4], fields[9][:7]
        if len(fields[8]) > 2:
            return fields[8][:4], ''
        return '', ''

    # 整理写出文件过程
    def write_lawyercase(self):
        names = os.listdir(self.input_path)
        for name in names:
            logging.info('Start reading the file named {}'.format(name))
            with open("{}{}".format(self.input_path, name), 'r', encoding='utf8') as file_open, open(
                    "{}{}".format(self.out_path, name), 'w', encoding='utf8') as file_write:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    doc_id = fields[0]
                    cause_name = fields[-2]
                    case_type = fields[11]
                    doc_type = fields[12]
                    trail = fields[10]
                    judges = fields[15]
                    judge_year, judge_month = self.get_year_and_month(fields)
                    court = fields[2]
                    court_level = fields[6]
                    province = fields[3]
                    city = fields[4]
                    region = fields[5]
                    party = fields[-1]
                    if fields[0] in self.plaintiff_mapping:
                        lawyers = self.plaintiff_mapping[fields[0]]
                        for lawyer in lawyers.split('=='):
                            if len(lawyer) > 4:
                                out_line = lawyer+'|'+doc_id + '|' + cause_name + '|' + case_type + '|' + doc_type + '|' + trail +'|' + judge_year + '|' + judge_month + '|' + court + '|' + court_level + '|' + province + '|' + city + '|' + region + '|' + party+ '|' + judges + '\n'
                                file_write.write(out_line)

    # 运行的主函数
    def run(self):
        self.get_lawyer_mapping()
        self.get_friend_opponent_mapping()
        self.write_lawyercase()


if __name__ == '__main__':
    lawyer = LawyerCase()
    lawyer.run()