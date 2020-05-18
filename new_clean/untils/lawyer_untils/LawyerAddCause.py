"""
@author : kennethAsher
@fole   : LawyerAddCause.py
@ctime  : 2020/5/9 17:34
@Email  : 1131771202@qq.com
@content:
            对接已经添加数据完成的数据和案由数据
            将二者数据根据docid合并
"""

import os

class LawyerAddCause():
    def __init__(self):
        self.cause_party_path = '/mnt/disk2/data/sum_data/cause_party/'
        self.data_file = '/mnt/disk2/data/sum_data/add_data_result/'
        self.write_file = '/mnt/disk2/data/sum_data/add_result/'
        self.cause_party_mapping = {}

    def get_names(self, path):
        return os.listdir(path)

    def get_fields(self, line):
        return line.strip().split('|')

    def get_map(self):
        cause_party_names = self.get_names(self.cause_party_path)
        for name in cause_party_names:
            cause_party_open = open('{}{}'.format(self.cause_party_path, name), 'r', encoding='utf8')
            print('starting read file cause_party for making cause_party_mapping of {}'.format(name))
            for line in cause_party_open.readlines():
                fields = self.get_fields(line)
                cause_name = fields[1]
                party = fields[2]
                value = cause_name + '|' + party
                self.cause_party_mapping[fields[0]] = value
            cause_party_open.close()
        print('ending read file cause_party for making cause_party_mapping')

    def write_func(self):
        names = self.get_names(self.data_file)
        for name in names:
            print('starting read file for {}'.format(name))
            add_data_open = open('{}{}'.format(self.data_file, name), 'r', encoding='utf8')
            write_result = open('{}{}'.format(self.write_file, name), 'w', encoding='utf8')
            for line in add_data_open.readlines():
                fields = self.get_fields(line)
                cause_party = self.cause_party_mapping[fields[0]]
                out_line = line.strip()+'|'+cause_party+'\n'
                write_result.write(out_line)
            add_data_open.close()
            write_result.close()

    def run(self):
        self.get_map()
        self.write_func()

if __name__ == '__main__':
    demo = LawyerAddCause()
    demo.run()