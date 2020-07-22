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

# 原告正则
plaintiff_pat = re.compile(r'.*(原审原告|原告人|原告|上诉人|申诉人|再审申请人|申请再审人|申请执行人|申请人|异议人|起诉人|申报人).*')
# 被告正则
defendant_pat = re.compile(r'.*(原审被告|被告人|被告|被上诉人|被申诉人|被申请人|被执行人|被异议人).*')
# 获取金额的正则
money_pat = re.compile(r'.*?(负担)(.*?)元.*?(负担)(.*?)元')


class SplitAppealType():

    # 创建类时初始化变量
    def __init__(self):
        # 输入路径
        self.input_path = '/mnt/disk1/data/minshi/appeal_data/'
        # 输出路径
        self.output_path = '/mnt/disk1/data/minshi/appeal_win_odds/'
        # 官费输入路径，此刻做金额类使用
        self.win_input_path = '/mnt/disk1/data/minshi/public_expense/'

        # 金额胜诉率的mapping
        self.win_mapping = {}

    # 获得路径下的所有文件名称
    def get_names(self, path):
        return os.listdir(path)

    # 获得金额胜诉率的mapping
    def get_win_mapping(self):
        for name in self.get_names(self.win_input_path):
            with open('{}{}'.format(self.win_input_path, name), 'r', encoding='utf8') as file_open:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    if len(fields) > 4:
                        if plaintiff_pat.match(fields[2]) is not None and defendant_pat.match(fields[2]) is not None:
                            try:
                                money = money_pat.findall(fields[2])
                                yuan_money = int(money[0][1])
                                bei_money = int(money[0][3])
                                sum = yuan_money + bei_money
                                yuan_odds = round(yuan_money/sum, 2)
                                bei_odds = round(bei_money/sum, 2)
                                value_line = str(yuan_odds)+'｜0｜'+str(bei_odds)+'|0'
                                self.win_mapping[fields[0]] = value_line
                                continue
                            except:
                                value_line = '0.50|1|0.50|1'
                                self.win_mapping[fields[0]] = value_line
                                continue
                        elif plaintiff_pat.match(fields[2]) is not None:
                            value_line = '0.00|0|1.00|0'
                            self.win_mapping[fields[0]] = value_line
                        elif defendant_pat.match(fields[2]) is not None:
                            value_line = '1.00|0|0.00|0'
                            self.win_mapping[fields[0]] = value_line
                        else:
                            value_line = '0.50|1|0.50|1'
                            self.win_mapping[fields[0]] = value_line
            file_open.close()

    # 读取写出每个文件
    def write_file(self, input_path, output_path, name):
        with open('{}{}'.format(input_path, name), 'r', encoding='utf8') as file_in, \
                open('{}{}'.format(output_path, name), 'w', encoding='utf8') as file_out:
            for line in file_in.readlines():
                fields = line.split('|')
                doc_id = fields[0]
                # 判断当前数据为有4个字段并且法院存在法院判定
                if len(fields) > 3 and len(fields[3]) > 10:
                    # 判断是否符合特殊审判阶段的
                    if '撤诉' in fields[3] or '撤回起诉' in fields[3] or '终结' in fields[3] or '准许' in fields[3] or '本案移送' in \
                            fields[3]:
                        file_out.write(doc_id + '|0.50|1|0.50|1\n')
                        continue
                    elif '驳回' in fields[3]:
                        if plaintiff_pat.match(fields[3]) is not None:
                            file_out.write(doc_id + '|0.00|1|1.00|1\n')
                            continue
                        else:
                            file_out.write(doc_id + '|1.00|1|0.00|1\n')
                            continue
                    elif '本院提审' in fields[3] or '转为普通程序' in fields[3] or '中止' in fields[3]:
                        file_out.write(doc_id + '｜0.00｜1|0.00|1\n')
                        continue
                    elif '异议成立' in fields[3]:
                        if plaintiff_pat.match(fields[3]) is not None:
                            file_out.write(doc_id + '|1.00|1|0.00|1\n')
                            continue
                        else:
                            file_out.write(doc_id + '|0.00|1|1.00|1\n')
                            continue

                    # 判断是否符合金额比例
                    if doc_id in self.win_mapping:
                        file_out.write(doc_id + '|' + self.win_mapping[doc_id] + '\n')
                        continue

    # 启动入口
    def run(self):
        self.get_win_mapping()
        names = self.get_names(self.input_path)
        for name in names:
            self.write_file(self.input_path, self.output_path, name)
