"""
@author : kennethAsher
@fole   : judge_merge_name.py
@ctime  : 2020/4/23 16:03
@Email  : 1131771202@qq.com
@content: 合并审判人员的名称，从而对比层级
问题：合并律师，什么会升级到最高级人民法院？
黑小兵|重庆市第四中级人民法院|2013|2014|中级---黑小兵|重庆市高级人民法院|2009|2019|高级？
"""

import os

class merge_name():

    def __init__(self):
        self.input_dir = 'D:\\judge_data\\judge_merge\\judge_court_level\\'
        self.out_level01 = 'D:\\judge_data\\judge_merge\\judge_name_merge\\level01'
        self.out_level12 = 'D:\\judge_data\\judge_merge\\judge_name_merge\\level12'
        self.out_level23 = 'D:\\judge_data\\judge_merge\\judge_name_merge\\level23'

        self.mapping_level_0 = {}
        self.mapping_level_1 = {}
        self.mapping_level_2 = {}
        self.court_mapping = {}

    def get_names(self):
        return os.listdir(self.input_dir)
    
    def get_court_map(self):
        open_file = open('C:\\Users\\GG257\\OneDrive\\sublime\\帮瀛\\pg_data\\pg_court\\pg_court.txt', 'r', encoding='utf8')
        for line in open_file.readlines():
            fields = line.strip().split('|')
            key = fields[1]
            value = fields[2]+'|'+fields[3]
            self.court_mapping[key]=value

    def append_map(self):
        names = self.get_names()
        for step, name in enumerate(names):
            file_open = open('{}{}'.format(self.input_dir, name), 'r', encoding='utf8')
            for line in file_open.readlines():
                key = line[:line.index('|')]
                if step == 0: self.mapping_level_0[key] = line.strip()
                if step == 1: self.mapping_level_1[key] = line.strip()
                if step == 2: self.mapping_level_2[key] = line.strip()
            
    def write_file(self, name, out_file, mapping):
        file_open = open('{}{}'.format(self.input_dir, name), 'r', encoding='utf8')
        file_write = open(out_file, 'w', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('|')
            key = fields[0]
            value = self.court_mapping[fields[1]]
            if key in mapping:
                words = mapping[key].strip().split('|')
                value_word = self.court_mapping[words[1]]
                out_line = mapping[key] + '|' + value_word + '---' + line.strip() + '|' + value +'\n'
                file_write.write(out_line)
        file_open.close()
        file_write.close()


    def run(self):
        self.get_court_map()
        self.append_map()
        self.write_file('level_1', self.out_level01, self.mapping_level_0)
        self.write_file('level_2', self.out_level12, self.mapping_level_1)
        self.write_file('level_3', self.out_level23, self.mapping_level_2)

if __name__ == '__main__':
    merge_name = merge_name()
    merge_name.run()