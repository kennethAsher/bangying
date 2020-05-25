#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/12 2:43 PM
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 整理全部数据民事案件每个类别的占比分别是多少以及数量
'''

import os

def count_num(open_dir, out_file):
    out_file = open(out_file, 'w', encoding='utf8')
    names = os.listdir(open_dir)
    casetype_count = 0  #案件类型数量
    sentence_count = 0  #民事判决书数量
    judge_count = 0     #民事裁定书数量
    decision_count = 0  #民事决定书数量
    mediation_count = 0 #民事调解书数量
    other = 0           #其他类型书来弄
    for name in names:
        open_file = open('{}{}'.format(open_dir,name), 'r', encoding='utf8')
        for line in open_file.readlines():
            if casetype_count == 49824981:
                break
            fields = line.split('|')
            if fields[10].strip() == '民事案件':
                # casetype_count += 1
                if '判决书' in fields[2]:
                    sentence_count += 1
                    casetype_count += 1
                if '裁定书' in fields[2]:
                    judge_count += 1
                    casetype_count += 1
                if '决定书' in fields[2]:
                    decision_count += 1
                    casetype_count += 1
                if '调解书' in fields[2]:
                    mediation_count += 1
                    casetype_count += 1
                if ('调解书' not in fields[2]) and ('裁定书' not in fields[2]) and ('裁定书' not in fields[2]) and ('判决书' not in fields[2]):
                    other += 1
                    casetype_count += 1
    out_line = '民事判决书'+'-'+str(sentence_count)+'|'+'民事裁定书'+'-'+str(judge_count)+'|'+'民事决定书'+'-'+str(decision_count)+'|'+'民事调解书'+'-'+str(mediation_count)+'|'+'其他'+'-'+str(other)+'|'+'总数'+'-'+str(casetype_count)+'|'
    out_file.write(out_line+'\n')

def run(open_dir, out_file):
    count_num(open_dir, out_file)

if __name__ == '__main__':
    open_dir = '/mnt/disk1/data/doc_data/doc_result/result1/'
    out_file = '/mnt/disk1/data/utils_data/doc_title/doc_title_count_total'
    run(open_dir, out_file)