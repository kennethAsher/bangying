#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/3/5 7:17 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 将律师姓名-律所 替换称为lawyer_id
'''

def get_id_mapping():
    id_mapping = {}
    open_lawyer_id = open('/mnt/disk1/data/pg_data/pg_lawyer_id.txt', 'r', encoding='utf8')
    for line in open_lawyer_id.readlines():
        split = line.strip().split('|')
        key = split[1]+'-'+split[2]
        value = split[0]
        id_mapping[key] = value
    return id_mapping

def run(file_open, file_write):
    id_mapping = get_id_mapping()
    for line in file_open.readlines():
        fields = line.strip().split('|')
        result_lawyer_id = ''
        if fields[1] != '':
            lawyers = fields[1].split(',')
            for lawyer in lawyers:
                try:
                    id = id_mapping[lawyer]
                    result_lawyer_id = result_lawyer_id+','+id
                except :
                    print(lawyer)
            file_write.write(fields[0] + '|' + result_lawyer_id[1:] + '\n')
            continue
        file_write.write(line)



if __name__ == '__main__':
    file_open = open('/mnt/disk1/data/utils_data/lawyer_opponent/opponent_count/opponent_count', 'r', encoding='utf8')
    file_write = open('/mnt/disk1/data/utils_data/lawyer_opponent/truncate_opponent/truncate_opponent', 'w', encoding='utf8')
    run(file_open, file_write)