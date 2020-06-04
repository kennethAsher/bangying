# -*- coding:utf-8 -*-

"""
@author: kennethAsher
@fole  : lawyer_add_id.py
@ctime : 2019/12/25 10:37
@Email : 1131771202@qq.com
"""
import re
import os

error_pat = (r'(.*(X|M|H|Ｘ|×|x|m).*)')

def get_mapping(lawyer_id_dir):
    mapping = {}
    lawyer_id = open(lawyer_id_dir, 'r', encoding='utf8')
    for line in lawyer_id.readlines():
        # print(line.strip())
        fields = line.strip().split("|")
        if len(fields) != 3:
            continue
        key = fields[1].strip()+fields[2].strip()
        mapping[key] = fields[0]
    lawyer_id.close()
    return mapping

def add_id(data_name, lawyer_data_int, lawyer_data_out, mapping):
    lawyer_int = open('{}{}'.format(lawyer_data_int,data_name), 'r', encoding='utf8')
    lawyer_out = open('{}{}'.format(lawyer_data_out,data_name), 'w', encoding='utf8')
    for line in lawyer_int.readlines():
        # print(line)
        matcher = re.match(error_pat, line)
        if matcher is not None:
            continue
        fields = line.strip().split("|")
        key = fields[5].strip() + fields[6].strip()
        if mapping[key] is not None:
            lawyer_out.write(mapping[key]+"|"+line)
    lawyer_int.close()
    lawyer_out.close()

if __name__ == '__main__':
    lawyer_id_dir = 'D:\\lawyer\\pg_lawyer_id.txt'
    lawyer_data_int = 'D:\\lawyer\\lawyer_disticnt_data\\'
    lawyer_data_out = 'D:\\lawyer\\lawyer_add_id\\'
    mapping = get_mapping(lawyer_id_dir)
    dirs = os.listdir(lawyer_data_int)
    for dir in dirs:
        add_id(dir, lawyer_data_int, lawyer_data_out, mapping)


