# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/23 下午4:47
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 从已经统计好分数的文书中计算审判人员的维度


'''

import re
import os


def get_mapping(map_open):
    court_mapping = {}
    for line in map_open.readlines():
        fields = line.split('|')
        court_mapping[fields[0]] = fields[1]
    return court_mapping

def write_result(open_dir, write_data, court_mapping):
    names = os.listdir(open_dir)
    file_write = open(write_data, 'r', encoding='utf8')
    for name in names:
        file_open = open('{}{}'.format(open_dir, name), 'w', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('|')
            judges_party = fields[15].strip().split(',')
            if ',' in fields[4]:
                fields[4] = fields[4].split(',')[0]
            if '再审' in fields[5]:
                fields[5] = '再审'
            if fields[9] in court_mapping:
                fields[9] = court_mapping[fields[9]]
            for judges in judges_party:
                judge = judges.split('-')
                if len(judge)>1:
                    if len(judge[1]) < 5 or len(judge[1]) > 7:
                        if judge[1].startswith('员') or judge[1].startswith('长') or judge[1].startswith('判长') or judge[1].startswith('判员') or judge[1].startswith('记员'):
                            judge[1] = re.sub(r'员|长|判长|判员|记员', '', judge[1])
                        out_line = judge[1]+'|'+ fields[4]+'|'+ fields[5]+'|'+ fields[6]+'|'+ fields[9]+'\n'
                        file_write.write(out_line)

        file_open.close()
    file_write.close()

def run(open_dir, write_data, map_open):
    court_map = get_mapping(map_open)
    write_result(open_dir, write_data, court_map)

if __name__ == '__main__':
    open_dir = '/mnt/disk1/data/doc_data/doc_result/result1/'
    write_data = '/mnt/disk1/data/utils_data/judge_data/judge_info/judge_info_case'
    map_open = open('/mnt/disk1/data/pg_data/court_relation', 'r', encoding='utf8')
    run(open_dir, write_data, map_open)