#!/usr/bin/python
# encoding: utf-8
'''
@author: kenneth
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: 1131771202@qq.com
@file: WinAppealOdds.py
@time: 2020/7/6 4:38 下午
@desc: 将切分好的文书诉求分称为驳回撤诉、有金额比对、无金额比对（1为撤回等因素导致，0为计算得到的采用率）
'''

import os
import re
import logging

# 原告正则
plaintiff_pat = re.compile(r'.*(原审原告|原告人|原告|上诉人|申诉人|再审申请人|申请再审人|申请执行人|申请人|异议人|起诉人|申报人).*')
# 被告正则
defendant_pat = re.compile(r'.*(原审被告|被告人|被告|被上诉人|被申诉人|被申请人|被执行人|被异议人).*')
# 获取金额的正则
money_pat = re.compile(r'.*?(负担|承担).*?([0-9\.,，]{2,10})元.*?(负担|承担).*?([0-9\.,，]{2,10})元')

logging.basicConfig(filename='win_appeal_odds.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

class WinAppealOdds():

    # 创建类时初始化变量
    def __init__(self):
        # 输出路径
        self.output_path = '/mnt/disk1/data/minshi/appeal_win_odds/'
        # 官费输入路径，此刻做金额类使用
        self.win_input_path = '/mnt/disk1/data/minshi/public_expense/'
        # 文案采用率输入路径
        self.doc_use_path = '/mnt/disk1/data/minshi/doc_use_odds/'

        # 金额胜诉率的mapping
        self.win_mapping = {}
        # 文案采用率
        self.doc_use_mapping = {}

    # 获得路径下的所有文件名称
    def get_names(self, path):
        return os.listdir(path)

    # 获得金额胜诉率的mapping
    def get_win_mapping(self):
        logging.info("开始执行get_win_mapping方法,将胜诉率写入至mapping中")
        for name in self.get_names(self.win_input_path):
            logging.info("开始执行文件{}...".format(name))
            with open('{}{}'.format(self.win_input_path, name), 'r', encoding='utf8') as file_open:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    if len(fields) > 4:
                        if plaintiff_pat.match(fields[4]) is not None and defendant_pat.match(fields[4]) is not None:
                            try:
                                money = money_pat.findall(fields[4])
                                if len(money) < 1:
                                    value_line = '0.50|0|0.50|0'
                                    self.win_mapping[fields[0]] = value_line
                                    continue
                                if len(money[0][3].split(".")) > 2: continue
                                yuan_money = float(money[0][1].replace(',','').replace('，',''))
                                bei_money = float(money[0][3].replace(',','').replace('，',''))
                                sum = yuan_money + bei_money
                                yuan_odds = round(yuan_money/sum, 2)
                                bei_odds = round(bei_money/sum, 2)
                                value_line = str(yuan_odds)+'|0|'+str(bei_odds)+'|0'
                                self.win_mapping[fields[0]] = value_line
                                continue
                            except:
                                value_line = '0.50|1|0.50|1'
                                self.win_mapping[fields[0]] = value_line
                                continue
                        elif plaintiff_pat.match(fields[4]) is not None:
                            value_line = '0.00|0|1.00|0'
                            self.win_mapping[fields[0]] = value_line
                        elif defendant_pat.match(fields[4]) is not None:
                            value_line = '1.00|0|0.00|0'
                            self.win_mapping[fields[0]] = value_line
                        else:
                            value_line = '0.50|1|0.50|1'
                            self.win_mapping[fields[0]] = value_line
            file_open.close()

    # 获得文案采用率的mapping
    def get_doc_use_function(self):
        logging.info("开始执行get_doc_use_function方法,将文案采用率写入至mapping中")
        for name in self.get_names(self.doc_use_path):
            logging.info("开始执行文件{}...".format(name))
            file_open = open('{}{}'.format(self.doc_use_path, name), 'r', encoding='utf-8')
            for line in file_open.readlines():
                fields = line.strip().split('|')
                self.doc_use_mapping[fields[0]] = '|'.join(fields[1:])
            file_open.close()


    # 读取写出每个文件
    def write_file(self, input_path, output_path, name):
        with open('{}{}'.format(input_path, name), 'r', encoding='utf8') as file_in, \
                open('{}{}'.format(output_path, name), 'w', encoding='utf8') as file_out:
            for line in file_in.readlines():
                fields = line.split('|')
                doc_id = fields[0]
                # 判断当前数据为有4个字段并且法院存在法院判定
                if len(fields) > 3 and len(fields[3]) > 5:
                    # 判断是否符合特殊审判阶段的
                    if '撤诉' in fields[3] or '撤回起诉' in fields[3] or '终结' in fields[3] or '准许' in fields[3] or '本案移送' in \
                            fields[3]:
                        file_out.write("0-"+doc_id + '|0.50|1|0.50|1\n')
                        continue
                    elif '驳回' in fields[3]:
                        if plaintiff_pat.match(fields[3]) is not None:
                            file_out.write("0-"+doc_id + '|0.00|1|1.00|1\n')
                            continue
                        else:
                            file_out.write("0-"+doc_id + '|1.00|1|0.00|1\n')
                            continue
                    elif '本院提审' in fields[3] or '转为普通程序' in fields[3] or '中止' in fields[3]:
                        file_out.write("0-"+doc_id + '|0.00|1|0.00|1\n')
                        continue
                    elif '异议成立' in fields[3]:
                        if plaintiff_pat.match(fields[3]) is not None:
                            file_out.write("0-"+doc_id + '|1.00|1|0.00|1\n')
                            continue
                        else:
                            file_out.write("0-"+doc_id + '|0.00|1|1.00|1\n')
                            continue

                    # 判断是否符合金额比例
                    elif doc_id in self.win_mapping:
                        file_out.write("1-"+doc_id + '|' + self.win_mapping[doc_id] + '\n')
                        continue

                    # 判断是否符合没有金额比例（使用文案采用率代替胜诉率）
                    else:
                        file_out.write("2-"+doc_id + '|' + self.doc_use_mapping[doc_id] + '\n')
                        continue
        file_in.close()
        file_out.close()


    # 启动入口
    def run(self):
        self.get_win_mapping()
        self.get_doc_use_function()
        names = self.get_names(self.win_input_path)
        logging.info("开始写出胜诉率")
        for name in names:
            logging.info("开始写出至文件{}".format(name))
            self.write_file(self.win_input_path, self.output_path, name)

if __name__ == '__main__':
    win_class = WinAppealOdds()
    win_class.run()
    logging.info("任务执行结束")