# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/5/25 下午4:16
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将清洗好的律师数据上传至es库中的pg_lawyer_info_attr_ken中用来代替原表中的pg_lawyer_info_attr_ext表
'''

import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers


es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

# 构建方法使得案由为key，案由层级为value的字典
def get_mapping_action(dir_name, i):
    mapping = {}
    actions = open(dir_name, 'r', encoding='utf8')
    for line in actions.readlines():
        mapping[line.strip()] = "CAUSE_OF_ACTION_{}".format(i)
    actions.close()
    return mapping
# 构建字典存放所有的案由层级
mapping1 = get_mapping_action("/mnt/disk1/data/pg_data/cause_of_action/cause_of_action.txt", 1)
mapping2 = get_mapping_action("/mnt/disk1/data/pg_data/cause_of_action/cause_of_action2.txt", 2)
mapping3 = get_mapping_action("/mnt/disk1/data/pg_data/cause_of_action/cause_of_action3.txt", 3)
mapping4 = get_mapping_action("/mnt/disk1/data/pg_data/cause_of_action/cause_of_action4.txt", 4)
mapping = dict(list(mapping1.items()) + list(mapping2.items()) + list(mapping3.items()) + list(mapping4.items()))




#在计算好的律师数据中得到causelist和triallist
def get_list_mapping():
    cause_mapping = {}
    trail_mapping = {}
    with open('/mnt/disk1/data/untils_data/lawyer_data/lawyer_score', 'r', encoding='utf8') as file_open:
        for line in file_open.readlines():
            fields = line.strip().split('|')
            try:
                cause_mapping[fields[0]] = list(set(fields[5].split(',')))
                trail_mapping[fields[0]] = list(set(fields[11].split(',')))
            except :
                continue
    file_open.close()
    return cause_mapping, trail_mapping

#获得省市县的字典
def get_mapping_area():
    province_mapping = {}
    city_mapping = {}
    region_mapping = {}
    areas = open('/mnt/disk1/data/pg_data/pg_court.txt','r',encoding='utf-8')
    for line in areas.readlines():
        fields = line.split('|')
        if len(fields) < 8:
            continue
        province_mapping[fields[1]] = fields[2]
        city_mapping[fields[1]] = fields[7]
        region_mapping[fields[1]] = fields[8]
    areas.close()
    return province_mapping, city_mapping, region_mapping

if __name__ == '__main__':
    input_path = '/mnt/disk1/data/untils_data/lawyer_data/lawyer_score_data_no/'
    names = os.listdir(input_path)
    lst = []
    cause_mapping, trail_mapping = get_list_mapping()
    province_mapping, city_mapping, region_mapping = get_mapping_area()
    for name in names:
        print('开始执行文件{}'.format(name))
        with open('{}{}'.format(input_path, name), 'r', encoding='utf8') as file_open:
            lines = file_open.readlines()
            k = len(lines)
            for step, line in enumerate(lines):
                fields = line.strip().split('|')
                cause_list = ''
                if fields[0] in cause_mapping:
                    cause_list = cause_mapping[fields[0]]
                trail_list = ''
                if fields[0] in trail_mapping:
                    trail_list = trail_mapping[fields[0]]
                if len(fields[4]) > 0 and fields[4] in mapping:
                    lst.append([int(fields[0]), fields[1], fields[2], mapping[fields[4]], "案由", fields[4], fields[4],fields[3][:4], cause_list, trail_list])
                if fields[7] in province_mapping:
                    if len(fields[7]) > 0:
                        lst.append([int(fields[0]), fields[1], fields[2], "COURT_OR_ARBITRATION_AGENCY", "管辖机构", fields[7], fields[7],fields[3][:4], cause_list, trail_list])
                    if len(province_mapping[fields[7]]) > 0:
                        lst.append([int(fields[0]), fields[1], fields[2], "WORK_PROVINCE", "工作省份", province_mapping[fields[7]], province_mapping[fields[7]],fields[3][:4], cause_list, trail_list])
                    if len(city_mapping[fields[7]]) > 0:
                        lst.append([int(fields[0]), fields[1], fields[2], "WORK_CITY", "工作城市", city_mapping[fields[7]], city_mapping[fields[7]],fields[3][:4], cause_list, trail_list])
                    if len(region_mapping[fields[7]]) > 0:
                        lst.append([int(fields[0]), fields[1], fields[2], "WORK_REGION", "工作区域", region_mapping[fields[7]], region_mapping[fields[7]],fields[3][:4], cause_list, trail_list])
                if len(fields[5]) > 0:
                    lst.append([int(fields[0]), fields[1], fields[2], "COURT_PROCEEDING", "审理程序", fields[5], fields[5],fields[3][:4], cause_list, trail_list])
                if len(fields[9]) > 4:
                    judges = fields[9].split(',')
                    for judge in judges:
                        if '-' in judge and '书记员' not in judge:
                            judge_name = judge.split('-')[-1]
                            lst.append([int(fields[0]), fields[1], fields[2], "JUDGE_PERSON", "审判人员", judge_name, fields[7],fields[3][:4], cause_list, trail_list])

                if len(lst)>999 or k-1 == step:
                    action = ({
                    "_index": "test_pg_lawyer_info_attr_ken",
                    "_type": "doc",
                    "_source": {
                        "lawyer_id": lst_line[0],
                        "lawyer_name": lst_line[1],
                        "lawyer_organ_name": lst_line[2],
                        "type_code": lst_line[3],
                        "type_name": lst_line[4],
                        "type_param_code": lst_line[5],
                        "type_param_name": lst_line[6],
                        "first_year": lst_line[7],
                        "casereason_set": lst_line[8],
                        "trialprocedure_set": lst_line[9]
                    }
                } for lst_line in lst)
                    try:
                        helpers.bulk(es, action)
                    except:
                        print('出现问题了')
                    print('传输了{}条律师数据'.format(str(step+1)))
                    lst = []
            print('执行完成文件{}'.format(name))
            file_open.close()
    print('程序执行完成')
