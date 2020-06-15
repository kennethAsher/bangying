#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/6/10 10:11 AM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 清洗官费内容
'''

import os
import re


#去掉括号已经括号里面的内容
remove_parent = re.compile(r'[\(（].*?[\)）]')
#检测是否减半收取
havle_accept_pat = re.compile(r'减半')
#费用类型
cost_type_pat = re.compile(r'(保全保险费|评估费|反诉受理费|诉讼保全费|财产保全费|保全费|公告费)(.*?)元')
#未知费用类型
cost_no_pat = re.compile(r'费(.*?)元')
#判断是否由附加费用，合计
merge_pat = re.compile(r'费(.*?)元(.*?)计(.*?)元')
#承担人员
person_pat = re.compile(r'(原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人)(.*?)(自行负担|自行承担|共同负担|承担|负担|担负|均担|担)(.*?)元')
person_pat1 = re.compile(r'(原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人)(自行负担|自行承担|共同负担|承担|负担|担负|均担|担)(.*?)元')
person_pat2 = re.compile(r'[由]?(.*?)(自行负担|自行承担|共同负担|承担|负担|担负|均担|担)(.*?)元')
person_pat3 = re.compile(r'[由]?(原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人)(.*?)(自行负担|自行承担|共同负担|承担|负担|担负|均担|担)')
person_pat4 = re.compile(r'[由]?(.*?)(自行负担|自行承担|共同负担|承担|负担|担负|均担|担)')

class CleanPublicExpense():
    #调用类时启动函数
    def __init__(self):
        #文件输入路径
        self.input_path='/Users/kenneth-mac/data/test/Public_expense/'
        #文件输出
        self.out_path = '/Users/kenneth-mac/data/test/'

    # 清洗出承担人
    def clean_person(self, accept_cost, cost_line, line):
        if cost_line.endswith('均'):
            cost_line = cost_line.replace('均','')
        # 判断是否符合person_pat的正则判断，如果是，则直接返回line
        if len(person_pat.findall(line)) > 0:
            return line
        # 判断是否符合person_pat1的正则判断，如果是，则直接返回line
        if len(person_pat1.findall(line)) > 0:
            return line
        # 判断是否符合person_pat2的正则判断，如果是，则直接返回line
        if len(person_pat2.findall(line)) > 0:
            return line
        # 判断是否符合person_pat3的正则判断，如果是，则进入判断
        if len(person_pat3.findall(line)) > 0:
            # 判断是否有额外费用，判断长度，满足则意味着没有其他，直接返回承担者+受理费用
            if len(cost_line) < 2:
                return line + str(accept_cost) + '元'
            # 存在额外费用，检测是否为
            if len(merge_pat.findall(cost_line)) > 0:
                money = merge_pat.findall(cost_line)
                money = money[-1][-1]
                return line + money + '元'
            # 判断减半收取的费用
            if '减半' in cost_line:
                return line + str(accept_cost / 2) + '元'
        # 判断是否符合person_pat3的正则判断，如果是，则进入判断
        if len(person_pat4.findall(line)) > 0:
            # 判断是否有额外费用，判断长度，满足则意味着没有其他，直接返回承担者+受理费用
            if len(cost_line) < 2:
                return line + str(accept_cost) + '元'
            # 存在额外费用，检测是否为
            if len(merge_pat.findall(cost_line)) > 0:
                money = merge_pat.findall(cost_line)
                money = money[-1][-1]
                return line + money + '元'
            # 判断减半收取的费用
            if '减半' in cost_line:
                return line + str(accept_cost / 2) + '元'
            return line + str(accept_cost) + '元'
        print(line)

    #将费用分类，承担者，承担金额返回
    def clean_line(self, accept_cost, line):
        # 括号备注内容  由原告负担409元，由被告韩永平、曹华芬负担357元（于支付上述款项时一并支付原告）
        line = remove_parent.sub('', line)
        # 或裁判如下等等
        if '如下' in line:
            words = line.split('案件受理')
            line = '案件受理' + words[-1]

        # 不服   由被告陈东负担 如不服本判决，可在判决书送达之日起十五日内向本院递交上诉状，并按对方当事人人数提出副本，上诉于江苏省常州市中级人民法院418.75元
        if '不服' in line:
            if '如不服' in line:
                words = line.split('如不服')
                line = line.replace('如不服'+words[-1],'').strip()
            words = line.split('不服')
            line = line.replace('不服'+words[-1], '').strip()

        # 审判
        if '审判' in line:
            words = line.split('审判')
            line = line.replace('审判' + words[-1], '').strip()

        # 接下来操作去掉判决生效这一段话和
        if '判决' in line or '生效' in line:
            words = line.split('，')
            line = line.replace(words[-1], '')[:-1]

        if '由' in line:
            index = line.index('由')
            cost_line = line[0:index]
            person_line = line[index:]
        else:
            cost_line = ''
            person_line = line
        person = self.clean_person(accept_cost, cost_line, person_line)
        return str(cost_line), str(person)

    #读取数据和写出数据
    def write_out(self):
        names = os.listdir(self.input_path)
        for name in names:
            with open('{}{}'.format(self.input_path, name), 'r', encoding='utf8') as file_open, open('{}{}'.format(self.out_path, name), 'w', encoding='utf8') as file_out:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    if len(fields)==4:
                        if len(fields[3])>2 :
                            # 案件受理费用
                            accept_cost = float(fields[2].split('-')[-1]) if len(fields[2])>2 else 0
                            # 承担详情费用
                            cost_line,person = self.clean_line(accept_cost, fields[3])
                            file_out.write(line.strip()+'|'+cost_line+person+'\n')
            file_open.close()
            file_out.close()

    #启动函数
    def run(self):
        self.write_out()


if __name__ == '__main__':
    clean_public_expense = CleanPublicExpense()
    clean_public_expense.run()
