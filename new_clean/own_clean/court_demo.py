# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/17 下午3:18
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 首先执行实现从文中找到，法院，案号和裁定书结果（第一步需要执行）
'''

import re
import os

#判断案由
#使用与会报错：本院在审理原告浙江××农村合作银行××星××行诉被告王甲、王乙金融借款合同纠纷一案中
cause_pat = re.compile(r'(.*?)一案')
#分行mainbody的正则
split_pat = re.compile(r'。|\n')
#匹配到当事人

parties_pat = re.compile(r'((原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人'
                         r'|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人)([\(（].*?[\)）])?)[:：]?(.*)')

clean_symbol_pat = re.compile(r'&#xD;|&#xa0;|&#x1F;|&mdash;|&middot;')

#法院匹配
court_pat = re.compile(r'(.*?院)(.*?书|.*?令)(.*?号)')
court_clean_pat = re.compile(r'}|书|）|案|国|内容|员|x|\.')
type_pat = re.compile(r'院|号')
case_no_pat = re.compile(r'书|的|打印|}|用）|稿）|稿件）')
#切分当事人
parties_split_pat = re.compile(r'原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人'
                               r'|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人')

def clean_data(open_dir, short_data, error_data, write_data):
    file_write = open(write_data, 'w', encoding='utf8')
    short_write = open(short_data, 'w', encoding='utf8')
    error_write = open(error_data, 'w', encoding='utf8')
    flag = 0
    names = os.listdir(open_dir)
    for name in names:
        print('开始执行第{}个文件'.format(flag))
        file_open = open('{}{}'.format(open_dir,name),'r', encoding='utf8')
        for line in file_open.readlines():
            line = clean_symbol_pat.sub('',line)
            fields = split_pat.split(line.split('|')[1])
            if len(fields) < 5:
                short_write.write(line)
                continue
            for i in range(0, len(fields)):
                if i == 0:
                    if court_pat.match(fields[i]) is not None:
                        results = court_pat.findall(fields[i])
                        try:
                            court = re.sub(r'-|·|.*>','',court_clean_pat.split(results[0][0])[-1])
                            type = re.sub('（驳回起诉用）|.*>','',type_pat.split(results[0][1])[-1])
                            case_no = re.sub(r'\?\?|.*>','',case_no_pat.split(results[0][2])[-1])\
                                .replace('（','(').replace('）',')').replace('〕',')').replace('〔','(')
                            if '简易程序' in case_no:
                                case_no = '简易程序案号'
                            if len(type) < 3:
                                type = '民事判决书'
                            if '(' not in case_no:
                                case_no = "(2012)"+case_no
                            if '之一' in case_no:
                                case_no = case_no.split('之一')[0]+'之一号'
                            #测试验证不符合的输出结果
                            """if len(court)>20 or len(type)>20 or len(case_no)>20:
                                out_line = court + '|' + type + '|' + case_no
                                file_test.write(out_line+'\n')
                                continue"""
                            out_line = line.split('|')[0]+'|'+court+'|'+type+'|'+case_no
                            file_write.write(out_line+'\n')
                        except :
                            error_write.write(line)
        print('第{}个文件执行结束'.format(flag))
        flag += 1

def run(open_dir, short_data, error_data, write_data):
    clean_data(open_dir, short_data, error_data, write_data)

if __name__ == '__main__':
    open_dir = '/mnt/disk2/data/organ_data/'
    short_data = '/mnt/disk2/data/short_data'
    error_data = '/mnt/disk2/data/error_data'
    write_data = '/mnt/disk2/data/organ_data_court_1/data_court'
    run(open_dir, short_data, error_data, write_data)