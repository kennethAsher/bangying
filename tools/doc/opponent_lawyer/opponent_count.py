#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/4 5:15 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 将律师所有的对手合并
'''


import os

def get_mapping(open_dir):
    opponent_mapping = {}
    names = os.listdir(open_dir)
    for name in names:
        file_opener = open('{}{}'.format(open_dir, name), 'r', encoding='utf-8')
        for line in file_opener.readlines():
            fields = line.split('|')
            if fields[0] not in opponent_mapping:
                opponent_mapping[fields[0]] = fields[1].strip()
            else:
                opponent_mapping[fields[0]] = opponent_mapping[fields[0]] + fields[1].strip()
    return opponent_mapping

def opponent_count(opponent_mapping, input_dir, out_dir):
    opponent_set = set()
    names = os.listdir(input_dir)
    file_write = open(out_dir, 'w', encoding='utf-8')
    for name in names:
        file_open = open('{}{}'.format(input_dir, name), 'r', encoding='utf-8')
        for line in file_open.readlines():
            fields = line.split('|')
            if fields[0] not in opponent_set:
                opponent_set.add(fields[0])
                words = opponent_mapping[fields[0]] if opponent_mapping[fields[0]]=='' else opponent_mapping[fields[0]][:-1]
                out_line = fields[0] + '|' + words
                file_write.write(out_line+'\n')
        file_open.close()
    file_write.close()

def run(open_dir, input_dir, out_dir):
    opponent_mapping = get_mapping(open_dir)
    opponent_count(opponent_mapping, input_dir, out_dir)


if __name__ == '__main__':
    open_dir = '/mnt/disk1/data/utils_data/lawyer_opponent/write_opponent/'
    input_dir = '/mnt/disk1/data/utils_data/lawyer_opponent/write_opponent/'
    out_dir = '/mnt/disk1/data/utils_data/lawyer_opponent/opponent_count/opponent_count'
    run(open_dir, input_dir, out_dir)
