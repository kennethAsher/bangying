#！/usr/bin/python3.6
# -*- coding:utf8 -*-

"""
@author : kennethAsher
@fole   : local_add_acceptance.py
@ctime  : 2020/1/13 9:53
@Email  : 1131771202@qq.com
@content: 追加本案的标的额，以及受理费用，类型，有什么人承担，身份，数值
          标的额|受理费，金额=保全费，金额==谁，身份，承担金额-
"""

import os
import re
'''
    1.不超过1万元的，每件交纳50元；                            50
　　2.超过1万元至10万元的部分，按照2.5％交纳；                 50<50+(x-10000)*0.025<2300
　　3.超过10万元至20万元的部分，按照2％交纳；                  2300 + (x-100000)*0.02<4300
　　4.超过20万元至50万元的部分，按照1.5％交纳；                4300+(x-200000)*0.015<8800
　　5.超过50万元至100万元的部分，按照1％交纳；                 8800 + (x-500000)*0.01 < 13800
　　6.超过100万元至200万元的部分，按照0.9％交纳；              13800 + (x-1000000)*0.009 < 22800
　　7.超过200万元至500万元的部分，按照0.8％交纳；              22800 + (x-2000000)*0.008 < 46800
　　8.超过500万元至1000万元的部分，按照0.7％交纳；             46800 + (x-5000000)*0.007 < 81800 
　　9.超过1000万元至2000万元的部分，按照0.6％交纳；            ...                        <141800
　　10.超过2000万元的部分，按照0.5％交纳。                      ...
'''
#根据受理费计算标的额
def acceptCost_2_subjectCost(cost):
    if '空' in cost:
        return '空'
    money = float(cost)
    if money <= 50:
        return 10000
    if money <= 2300:
        return (money-50)/0.025 + 10000
    if money <= 4300:
        return (money-2300)/0.02 + 100000
    if money <= 8800:
        return (money-4300)/0.015 + 200000
    if money <= 13800:
        return (money-8800)/0.01 + 500000
    if money <= 22800:
        return (money-13800)/0.009 + 1000000
    if money <= 46800:
        return (money-22800)/0.008 + 2000000
    if money <= 81800:
        return (money - 46800) / 0.007 + 5000000
    if money <= 141800:
        return (money - 81800) / 0.006 + 10000000
    if money > 141800:
        return (money - 141800) / 0.005 + 20000000

docSplitPat = re.compile(r'。|\n|；')
#判断是否存在可挖去的价值
docAcceptCossPat = re.compile(r'.*受理费[用]?[:：]?(.*)元.*')
accept_cost_pat = re.compile(r'受理费[费本院实际全额依法预缴应收用共计由已因适用按简易普通程序（(减半)收取）计算后交缴纳征收取计即为合计人民币元各到]{0,20}(\d+(\.\d+)?[万]?)[元减半收取0-9]{0,10}[元]?')
rescue_cost_pat = re.compile(r'保全费(\d+(\.\d+)?)元')
# judgmemt = '案件受理费2935元，由被告童某某、江西宜春汽车运输股份有限公司高安分公司承担'
file_in = open('D:\\doc_data\\region_data_out\\000355_0_new1', 'r', encoding='utf-8')
file_out = open('D:\\doc_data\\region_data_out\\000355_0_new3', 'w', encoding='utf-8')

# 检测是否有受理费，并返回
def get_accept_cost(line):
    line = line.replace(',', '').replace('，', '')
    money_match = accept_cost_pat.findall(line)
    accept_cost = '空'
    if len(money_match) > 0:
        accept_cost = money_match[0][0]
        if '万' in accept_cost:
            accept_cost=str(float(accept_cost.replace('万', ''))*10000)
    return accept_cost

def get_detail(line):
    pass

#检测是否有保全费并返回
def get_rescue_cost(line):
    line = line.replace(',', '').replace('，', '')
    rescue_cost = '空'
    rescue_cost_match = rescue_cost_pat.findall(line)
    if len(rescue_cost_match) > 0 :
        rescue_cost=str(rescue_cost_match[0][0])
    return rescue_cost

for judgmemt in file_in.readlines():
    line = judgmemt.strip()
    accept_cost = get_accept_cost(line)
    subject_cost = acceptCost_2_subjectCost(accept_cost)
    rescue_cost = get_rescue_cost(line)
    #如果是减半收取的话标注出来
    remark = ""
    if '减半' in line and accept_cost != '空':
        remark = '(减半收取{})'.format(str(float(accept_cost)/2))
    file_out.write('{}|{}|受理费,{}=保全费,{}\n'.format(line, str(subject_cost), accept_cost+remark, rescue_cost))