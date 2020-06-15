# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/24 上午9:54
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将审判人员数据合并，求得维度，（文书总量、经验年份、案由）
'''


def get_mapping():
    file_open = open('/Users/by-webqianduan/data/doc/000245_0_out_id', 'r', encoding='utf8')
    # 最低的年限
    year_mapping = {}
    # 裁判文书的总量
    doc_count_mapping = {}
    # 审理程序
    trail_mapping = {}

    for line in file_open.readlines():
        fields = line.strip().split('|')

        #年份
        if fields[0] not in year_mapping:
            year_mapping[fields[0]] = int(fields[4])
        elif int(fields[4]) < year_mapping[fields[0]]:
            year_mapping[fields[0]] = int(fields[4])
        else:
            pass

        #文书总量
        if fields[0] not in doc_count_mapping:
            doc_count_mapping[fields[0]] = 1
        else:
            doc_count_mapping[fields[0]] = doc_count_mapping[fields[0]] + 1

        #审理程序
        if fields[0] not in trail_mapping:
            trail_mapping[fields[0]] = fields[3]
        else:
            trail_mapping[fields[0]] = trail_mapping[fields[0]]+','+fields[3]

    return year_mapping,doc_count_mapping,trail_mapping


if __name__ == '__main__':
    year_mapping,doc_count_mapping,trail_mapping = get_mapping()
    judge_set = set()
    file_open = open('/Users/by-webqianduan/data/doc/000245_0_out_id', 'r', encoding='utf8')
    file_write = open('/Users/by-webqianduan/data/doc/000245_0_out_count', 'w', encoding='utf8')
    for line in file_open.readlines():
        fields = line.strip().split('|')
        if fields[0] not in judge_set:
            year = str(year_mapping[fields[0]])
            doc_count = str(doc_count_mapping[fields[0]])
            trail = set()
            for key in trail_mapping[fields[0]].split(','):
                trail.add(key)
            trail = ','.join(trail)
            out_line = fields[0]+'|'+fields[1]+'|'+fields[5]+'|'+fields[6]+'|'+year+'|'+doc_count+'|'+trail
            judge_set.add(fields[0])
            file_write.write(out_line+'\n')

