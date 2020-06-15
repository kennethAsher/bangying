# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/8 11:06 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将裁判文书分类写到各个类型的文件夹中
'''

import os
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/get_doc.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)


class Get_Doc():
    def __init__(self):
        self.oped_path = '/mnt/disk2/data/organ_data/'
        self.minshi_dir = '/mnt/disk2/data/minshi/add_data/data'
        self.xingshi_dir = '/mnt/disk2/data/xingshi/add_data/data'
        self.zhixing_dir = '/mnt/disk2/data/zhixing/add_data/data'
        self.xingzheng_dir = '/mnt/disk2/data/xingzheng/add_data/data'
        self.peichang_dir = '/mnt/disk2/data/peichang/add_data/data'
        self.minshi_path = '/mnt/disk2/data/minshi/organ_data/'
        self.xingshi_path = '/mnt/disk2/data/xingshi/organ_data/'
        self.zhixing_path = '/mnt/disk2/data/zhixing/organ_data/'
        self.xingzheng_path = '/mnt/disk2/data/xingzheng/organ_data/'
        self.peichang_path = '/mnt/disk2/data/peichang/organ_data/'

    def get_names(self, path):
        return os.listdir(path)

    def get_set(self, path):
        logging.info('开始读入{}中的doc_id'.format(path.split('/')[4]))
        result = set()
        file_open = open(path, 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.split('|')
            result.add(fields[0])
        file_open.close()
        return result

    def write_organ_data(self, names,minshi_set,xingshi_set,xingzheng_set,zhixing_set,prichang_set):
        for step,name in enumerate(names):
            logging.info('开始写入第{}个文件--{}'.format(step,name))
            file_open = open('{}{}'.format(self.oped_path, name), 'r', encoding='utf8')
            minshi_write = open('{}{}'.format(self.minshi_path, name), 'w', encoding='utf8')
            xingshi_write = open('{}{}'.format(self.xingshi_path, name), 'w', encoding='utf8')
            xingzheng_write = open('{}{}'.format(self.xingzheng_path, name), 'w', encoding='utf8')
            zhixing_write = open('{}{}'.format(self.zhixing_path, name), 'w', encoding='utf8')
            peichang_write = open('{}{}'.format(self.peichang_path, name), 'w', encoding='utf8')
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

    def run(self):
        minshi_set = self.get_set(self.minshi_dir)
        xingshi_set = self.get_set(self.xingshi_dir)
        xingzheng_set = self.get_set(self.xingzheng_dir)
        zhixing_set = self.get_set(self.zhixing_dir)
        prichang_set = self.get_set(self.peichang_dir)
        logging.info('doc_id读取完毕------\n开始执行分割源数据')
        names = self.get_names(self.oped_path)
        self.write_organ_data(names,minshi_set,xingshi_set,xingzheng_set,zhixing_set,prichang_set)


if __name__ == '__main__':
    #定义各个文件路径
    get_demo = Get_Doc()
    get_demo.run()