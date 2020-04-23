"""
@author : kennethAsher
@fole   : judge_name_merge.py
@ctime  : 2020/4/23 13:14
@Email  : 1131771202@qq.com
@content: 整理审判人员，最终得到直接放入pg_user_judge的数据
"""

import os


class judge_name_merge():
    def __init__(self):
        self.input_path = 'D:\\judge_data\\judge_add_court\\'
        self.output_path = 'D:\\judge_data\\judge_info\\judge_info'
        self.mapping_start = {}
        self.mapping_end = {}
        self.mapping_count = {}
        self.mapping_trial = {}
        self.mapping_last_count = {}

    def get_fields(self, line):
        return line.strip().split('|')

    def get_names(self, input_path):
        return os.listdir(input_path)

    def get_mapping(self):
        names = self.get_names(self.input_path)
        for name in names:
            file_open = open('{}{}'.format(self.input_path,name), 'r', encoding='utf8')
            print('string file {} to mapping'.format(name))
            for line in file_open.readlines():
                fields = self.get_fields(line)
                key = fields[1]+'|'+fields[2]
                if key not in self.mapping_start:
                    self.mapping_start[key] = fields[7]
                    self.mapping_end[key] = fields[7]
                    self.mapping_count[key] = 1
                    self.mapping_trial[key] = fields[-1]
                    self.mapping_last_count[key] = 1 if fields[7] == '2020' else 0
                else:
                    if fields[7]<self.mapping_start[key]:
                        self.mapping_start[key] = fields[7]
                    if fields[7]>self.mapping_end[key]:
                        self.mapping_end[key] = fields[7]
                    if fields[-1] not in self.mapping_trial[key]:
                        self.mapping_trial[key] = self.mapping_trial[key]+'-'+fields[-1]
                    if fields[7] == '2020':
                        self.mapping_last_count[key] = self.mapping_last_count[key]+1
                    self.mapping_count[key] = self.mapping_count[key]+1
            file_open.close()


    def write_file(self):
        names = self.get_names(self.input_path)
        file_write = open(self.output_path, 'w', encoding='utf8')
        for name in names:
            file_open_now = open('{}{}'.format(self.input_path, name), 'r', encoding='utf8')
            print('writing out file {} to file'.format(name))
            _set = set()
            for line in file_open_now.readlines():
                fields = self.get_fields(line)
                key = fields[1] + '|' + fields[2]
                level = fields[6]
                if key not in _set:
                    start_year = self.mapping_start[key]
                    end_year = self.mapping_end[key]
                    count = self.mapping_count[key]
                    trail = self.mapping_trial[key]
                    last_count = self.mapping_last_count[key]
                    out_line = key + '|' + level + '|' + start_year + '|' + end_year + '|' + str(count) + '|' + str(
                        last_count) + '|' + trail + '\n'
                    if count > 3:
                        file_write.write(out_line)
                    _set.add(key)
            file_open_now.close()
        file_write.close()



    def run(self):
        self.get_mapping()
        self.write_file()

if __name__ == '__main__':
    judge_name_merge = judge_name_merge()
    judge_name_merge.run()
