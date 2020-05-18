# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/21 下午5:26
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 测试，往这里写就行了
'''

import re
import jieba
'''
plaintiff_lawsuit_pat = re.compile(r'.*(原审原告|原告人|原告|上诉人|申诉人|再审申请人|申请人|申请执行人|异议人|起诉人|申报人|原审第三人|第三人).*(诉讼|请求|诉请|诉称).*')
# 被告诉求
appellee_lawsuit_pat = re.compile(r'.*((原审被告|被告人|被告|被上诉人|被申诉人|申请再审人|被申请人|被执行人|被异议人)|一审法院).*(答辩|反诉|诉讼|请求|诉请|诉称|认为).*')
# 法院认为中断
court_end_pat = re.compile(r'.*本院认为.*')
# 法院判决
court_lawsuit_pat = re.compile(r'.*(判决如下|裁决如下|裁定如下).*')

line = '原告赵某及委托诉讼代理人李某，被告吕某及恒泰公交公司委托诉讼代理人王某、被告人保泾川支公司委托诉讼代理人张某2均到庭参加了诉讼。'
read_flag = 1
if court_lawsuit_pat.match(line) is not None:
    read_flag = 4
if appellee_lawsuit_pat.match(line) is not None:
    read_flag = 3
if plaintiff_lawsuit_pat.match(line) is not None:
    read_flag = 2
if court_end_pat.match(line) is not None:
    read_flag = 1
if read_flag == 4:
    print(4)
if read_flag == 3:
    print(3)
if read_flag == 2:
    print(2)



'''

# plaintiff_lawsuit_pat = re.compile(r'(原审原告|原告人|原告|上诉人|申诉人|再审申请人|申请人|申请执行人|异议人|起诉人|申报人|原审第三人|第三人).*(诉讼|请求|诉请|诉称)')
# line = '原告赵某向本院提出诉讼请求：'
# print(plaintiff_lawsuit_pat.findall(line))

line = '鉴定费1500.00元'
out = jieba.lcut(line)
print(out)
