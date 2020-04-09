#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/12 2:43 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 整理已清洗律师数据民事案件每个类别的占比分别是多少以及数量
'''

def count_num(open_name, out_file):
    open_file = open(open_name, 'r', encoding='utf8')
    out_file = open(out_file, 'w', encoding='utf8')
    casetype_count = 0  #案件类型数量
    sentence_count = 0  #民事判决书数量
    judge_count = 0     #民事裁定书数量
    decision_count = 0  #民事决定书数量
    mediation_count = 0 #民事调解书数量
    other = 0           #其他类型书来弄
    for line in open_file.readlines():
        if casetype_count == 13384571:
            break
        fields = line.split('|')
        if fields[2].strip() == '民事案件':
           # casetype_count += 1
            if '判决书' in fields[1]:
                sentence_count += 1
                casetype_count += 1
            if '裁定书' in fields[1]:
                judge_count += 1
                casetype_count += 1
            if '决定书' in fields[1]:
                decision_count += 1
                casetype_count += 1
            if '调解书' in fields[1]:
                mediation_count += 1
                casetype_count += 1
            if ('调解书' not in fields[1]) and ('裁定书' not in fields[1]) and ('裁定书' not in fields[1]) and ('判决书' not in fields[1]):
                other += 1
                casetype_count += 1
    out_line = '民事判决书'+'-'+str(sentence_count)+'|'+'民事裁定书'+'-'+str(judge_count)+'|'+'民事决定书'+'-'+str(decision_count)+'|'+'民事调解书'+'-'+str(mediation_count)+'|'+'其他'+'-'+str(other)+'|'+'总数'+'-'+str(casetype_count)+'|'
    out_file.write(out_line+'\n')

def run(open_name, out_file):
    count_num(open_name, out_file)

if __name__ == '__main__':
    open_name = '/mnt/disk1/data/utils_data/doc_title/get_doc_title'
    out_file = '/mnt/disk1/data/utils_data/doc_title/doc_title_count'
    run(open_name, out_file)