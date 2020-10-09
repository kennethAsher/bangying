# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/8 11:06 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将裁判文书分类写到各个类型的文件夹中
'''

import os
import sys
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/get_doc.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)


# 判断路径是否存在，如果不存在就新建
def exists_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 获取路径下面的所有的文件名
def get_names(path):
    return os.listdir(path)

# 将每个类别的doc_id存放在不同类别的set中
def get_set(path):
    logging.info('开始读入{}中的doc_id'.format(path.split('/')[4]))
    result = set()
    for name in os.listdir(path):
        file_open = open("{}{}".format(path, name), 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.split('|')
            result.add(fields[0])
        file_open.close()
    return result

# 按照文书类别不同，将文书分别存放在不同的位置
def write_organ_data(names,minshi_set,xingshi_set,xingzheng_set,zhixing_set,prichang_set):
    for step,name in enumerate(names):
        logging.info('开始写入第{}个文件--{}'.format(step,name))
        file_open = open('{}{}'.format(oped_path, name), 'r', encoding='utf8')
        minshi_write = open('{}{}'.format(minshi_path, name), 'w', encoding='utf8')
        xingshi_write = open('{}{}'.format(xingshi_path, name), 'w', encoding='utf8')
        xingzheng_write = open('{}{}'.format(xingzheng_path, name), 'w', encoding='utf8')
        zhixing_write = open('{}{}'.format(zhixing_path, name), 'w', encoding='utf8')
        peichang_write = open('{}{}'.format(peichang_path, name), 'w', encoding='utf8')
        for line in file_open.readlines():
            fields = line.split('|')
            if fields[0] in minshi_set:
                minshi_write.write(line)
            elif fields[0] in xingshi_set:
                xingshi_write.write(line)
            elif fields[0] in xingzheng_set:
                xingzheng_write.write(line)
            elif fields[0] in zhixing_set:
                zhixing_write.write(line)
            elif fields[0] in prichang_set:
                peichang_write.write(line)
        file_open.close()
        minshi_write.close()
        xingshi_write.close()
        xingzheng_write.close()
        zhixing_write.close()
        peichang_write.close()

def run():
    minshi_set = get_set(minshi_dir)
    xingshi_set = get_set(xingshi_dir)
    xingzheng_set = get_set(xingzheng_dir)
    zhixing_set = get_set(zhixing_dir)
    prichang_set = get_set(peichang_dir)
    logging.info('doc_id读取完毕------\n开始执行分割源数据')
    names = get_names(oped_path)
    write_organ_data(names,minshi_set,xingshi_set,xingzheng_set,zhixing_set,prichang_set)


if __name__ == '__main__':
    #定义各个文件路径
    oped_path = '/mnt/{}/data/organ_data/'.format(sys.argv[1])
    minshi_dir = '/mnt/{}/data/minshi/add_data/'.format(sys.argv[1])
    xingshi_dir = '/mnt/{}/data/xingshi/add_data/'.format(sys.argv[1])
    zhixing_dir = '/mnt/{}/data/zhixing/add_data/'.format(sys.argv[1])
    xingzheng_dir = '/mnt/{}/data/xingzheng/add_data/'.format(sys.argv[1])
    peichang_dir = '/mnt/{}/data/peichang/add_data/'.format(sys.argv[1])
    minshi_path = '/mnt/{}/data/minshi/organ_data/'.format(sys.argv[1])
    exists_or_create(minshi_path)
    xingshi_path = '/mnt/{}/data/xingshi/organ_data/'.format(sys.argv[1])
    exists_or_create(xingshi_path)
    zhixing_path = '/mnt/{}/data/zhixing/organ_data/'.format(sys.argv[1])
    exists_or_create(zhixing_path)
    xingzheng_path = '/mnt/{}/data/xingzheng/organ_data/'.format(sys.argv[1])
    exists_or_create(xingzheng_path)
    peichang_path = '/mnt/{}/data/peichang/organ_data/'.format(sys.argv[1])
    exists_or_create(peichang_path)
    run()