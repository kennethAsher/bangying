# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/14 10:00 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 从裁判文书中提取诉讼请求，以及法院的判决结果
'''

#如果没有检测到受理费，则跳过

import re
docAcceptCossPat = re.compile(r'.*受理费[用]?[:：]?(.*)元.*')
accept_cost_pat = re.compile(r'受理费[费本院实际全额依法预缴应收用共计由已因适用按简易普通程序（(减半)收取）计算后交缴纳征收取计即为合计人民币元各到]{0,20}(\d+(\.\d+)?[万]?)[元减半收取0-9]{0,10}[元]?')
rescue_cost_pat = re.compile(r'保全费(\d+(\.\d+)?)元')

person_pat = re.compile(r'[由](.*)[负承]担')
person_pat2 = re.compile(r'[被原告](.*)负担(.*)元')
bear_pat = re.compile(r'诉讼.*?元|司法鉴定.*?元')



def get_accept_cost(line):
    line = line.replace(',', '').replace('，', '')
    money_match = accept_cost_pat.findall(line)
    accept_cost = '空'
    if len(money_match) > 0:
        accept_cost = money_match[0][0]
        if '万' in accept_cost:
            accept_cost=str(float(accept_cost.replace('万', ''))*10000)
    return accept_cost

line = '案件受理费300元，被告赵建忠、赵浩勋、范书云负担150元，原告刘永琰负担100元，被告李雪珍负担50元'
money = get_accept_cost(line)
print(money)
person = person_pat.findall(line)
print(person)
out = bear_pat.findall(line)
print(out)
out2 = person_pat2.findall(line)
print(out2)
