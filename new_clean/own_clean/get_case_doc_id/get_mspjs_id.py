# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/27 下午1:22
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 通过判断文书种类的民事判决书和民判决书，找到对应的id
'''

import os

def get_id(open_file, write_file, write_file2):
    print('开始获取民事判决书的id')
    map_set = set()
    file_open = open(open_file, 'r', encoding='utf8')
    file_write = open(write_file, 'w', encoding='utf8')
    file_write2 = open(write_file2, 'w', encoding='utf8')
    print('开始写出民事判决书法院，案号')
    for line in file_open.readlines():
        fields = line.strip().split('|')
        if fields[2] == '民事判决书' or fields[2] == '民判决书':
            file_write.write(line)
            map_set.add(fields[0].strip())
        else:
            file_write2.write(line)
    print('完成写出民事判决书法院，案号')
    print('获取id成功')
    return map_set

def get_organ_data(oped_dir, write_dir, map_set):
    names = os.listdir(oped_dir)
    k = 0
    for name in names:
        print('开始写入第{}个文件--{}'.format(k,name))
        file_open = open('{}{}'.format(oped_dir, name), 'r', encoding='utf8')
        file_write = open('{}{}'.format(write_dir, name), 'w', encoding='utf8')
        for line in file_open.readlines():
            fields = line.split('|')
            if fields[0] in map_set:
                file_write.write(line)
        file_open.close()
        file_write.close()

def run(oped_dir, write_dir, open_file, write_file, write_file2):
    map_set = get_id(open_file, write_file, write_file2)
    get_organ_data(oped_dir, write_dir, map_set)

if __name__ == '__main__':
    #定义各个文件路径
    oped_dir = '/mnt/disk2/data/organ_data/'
    write_dir = '/mnt/disk2/data/mspjs/organ_data/'
    open_file = '/mnt/disk2/data/organ_data_court_1/add_court_clean'
    write_file = '/mnt/disk2/data/mspjs/court_type_case/data'
    write_file2 = '/mnt/disk2/data/organ_data_court_1/add_court_clean_new'
    run(oped_dir, write_dir, open_file, write_file, write_file2)