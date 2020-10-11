#!/usr/bin/python
# encoding: utf-8
'''
@Author:        kennethAsher
@Contact:       1131771202@qq.com
@ClassName:     merge_judge_add.py
@Time:          2020/10/11 10:11 上午
@Desc:          //TODO 合并审判人员，审理时间，审理程序
'''

import os
import sys
import logging

_type = sys.argv[1]
_disk = sys.argv[2]

logging.basicConfig(filename='/mnt/disk1/log/python/{}/merge_judge_add.log'.format(_type),
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

# 判断路径是否存在，如果不存在就新建
def exists_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)

#返回路径下的文件名称集合
def get_names(input_path):
    return os.listdir(input_path)

#拿到add_path的map，返回日期，法院，审理程序
def get_add_map(add_path, add_map):
    names = get_names(add_path)
    for name in names:
        file_open = open('{}{}'.format(add_path, name), 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('|')
            out_line = fields[2]+'|'+fields[4]+'|'+fields[5]+'|'+fields[6]
            key = fields[0]
            add_map[key] = out_line
        file_open.close()

#拿到judge_path的map,返回审判人员的名称以及对应的法院，（书记员要排除）
def get_judge_map(judge_path, judge_map):
    names = get_names(judge_path)
    for name in names:
        file_open = open('{}{}'.format(judge_path, name), 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('|')
            judge = ''
            judge_names = fields[3].split(',')
            for judge_name in judge_names:
                words = judge_name.split('-')
                if '书记员' in words[0]:
                    break
                if len(words) < 2:
                    continue
                judge = judge + words[1] + ','
            out_line = judge[:-1] if len(judge)>1 else ""
            key = fields[0]
            judge_map[key] = out_line
        file_open.close()

#将审判人员数据写出
def write_judge_case(output_path, add_path, add_map, judge_map):
    names = get_names(add_path)
    for step, name in enumerate(names):
        logging.info("开始执行第{}个文件{}".format(str(step), name))
        file_open = open('{}{}'.format(add_path, name), 'r', encoding='utf8')
        file_out = open('{}{}'.format(output_path, name), 'w', encoding='utf8')
        for line in file_open.readlines():
            key = line.strip().split('|')[0]
            if key not in judge_map:
                continue
            judges = judge_map[key]
            if len(judges) > 0:
                names = judges.split(',')
                for name in names:
                    out_line = key + '|' + name+'|'+add_map[key]+'\n'
                    file_out.write(out_line)
        file_open.close()
        file_out.close()


#执行函数
def run(judge_path, add_path, output_path, add_map, judge_map):
    print('开始导入add_map')
    get_add_map(add_path, add_map)
    print('导入完成add_map,并且开始导入judge_map')
    get_judge_map(judge_path, judge_map)
    print('导入完成judge_map，并且开始写出到最后文件中')
    write_judge_case(output_path, add_path, add_map, judge_map)
    print('执行完成')

if __name__ == '__main__':
    judge_path = '/mnt/{}/data/{}/lawyer_judge/'.format(_disk, _type)
    add_path = '/mnt/{}/data/{}/add_data/'.format(_disk, _type)
    output_path = '/mnt/{}/data/{}/judge_case/'.format(_disk, _type)
    exists_or_create(output_path)
    add_map = {}
    judge_map = {}
    run(judge_path, add_path, output_path, add_map, judge_map)
