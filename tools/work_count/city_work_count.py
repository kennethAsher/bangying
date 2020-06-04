#!/usr/bin/python3.6
# -*- conding:utf-8 -*-

"""
@author :       kennethAsher
@fole   :       city_work_count.py
@ctime  :       2020/1/9 15:07
@Email  :       1131771202@qq.com
#content:       主要功能实现了统计每个律师分别在城市打官司的次数，并添加字段is_max（是场次最多的为1，否则为0）
"""

def get_mapping_count():
    mapping = {}
    work_counts = open('D:\\work_count\\no1\\000000_0', 'r', encoding='utf-8')
    for line in work_counts.readlines():
        fields = line.strip().split('|')
        key, value = fields[0], int(fields[4])
        if fields[3] == '空': continue
        if key in mapping:
            mapping[key] = value if value > mapping[key] else mapping[key]
        else:
            mapping[key] = value
    work_counts.close()
    return mapping

def get_is_max(path_in, path_out, mapping):
    file_input = open(path_in, 'r', encoding='utf-8')
    file_out = open(path_out, 'w', encoding='utf-8')
    is_max = 0
    for line in file_input.readlines():
        fields = line.strip().split('|')
        key, value = fields[0], int(fields[4])
        if fields[3] == '空': continue
        is_max = 0 if value < mapping[key] else 1
        file_out.write(line.strip() + '|' + str(is_max) +'\n')
    file_input.close()
    file_out.close()

if __name__ == '__main__':
    mapping = get_mapping_count()
    path_in = 'D:\\work_count\\no1\\000000_0'
    path_out = 'D:\\work_count\\no1_out\\000000_0'
    get_is_max(path_in, path_out, mapping)

