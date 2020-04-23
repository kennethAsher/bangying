"""
@author : kennethAsher
@fole   : judge_court_level.py
@ctime  : 2020/4/22 19:22
@Email  : 1131771202@qq.com
@content: 将审判人员按照法院层级分类，并且最终保留层级，日期，法院名称字段
"""

import os

class judge_court_level():
    def __init__(self):
        self.input_dir = 'D:\\judge_data\\judge_add_court\\'
        self.level_0 = 'D:\\judge_data\\judge_court_level\\level_0'
        self.level_1 = 'D:\\judge_data\\judge_court_level\\level_1'
        self.level_2 = 'D:\\judge_data\\judge_court_level\\level_2'
        self.level_3 = 'D:\\judge_data\\judge_court_level\\level_3'

    def get_names(self, input_dir):
        return os.listdir(input_dir)

    def write_level_file(self):
        names = self.get_names(self.input_dir)
        write_level_0 = open(self.level_0, 'w', encoding='utf8')
        write_level_1 = open(self.level_1, 'w', encoding='utf8')
        write_level_2 = open(self.level_2, 'w', encoding='utf8')
        write_level_3 = open(self.level_3, 'w', encoding='utf8')
        for name in names:
            file_open = open('{}{}'.format(self.input_dir, name), 'r', encoding='utf8')
            for line in file_open.readlines():
                fields = line.strip().split('|')
                if len(fields)<3:
                    continue
                judge_name = fields[0]
                court_name = fields[1]
                year = fields[2]
                date = fields[3]
                level = fields[8]
                out_line = judge_name+'|'+court_name+'|'+year+'|'+date+'|'+level+'\n'

                if '最高' in level:
                    write_level_3.write(out_line)
                elif '高级' in level:
                    write_level_2.write(out_line)
                elif '中级' in level:
                    write_level_1.write(out_line)
                else:
                    write_level_0.write(out_line)
            file_open.close()
        write_level_0.close()
        write_level_1.close()
        write_level_2.close()
        write_level_3.close()

    def run(self):
        self.write_level_file()


if __name__ == '__main__':
    judge_court_level = judge_court_level()
    judge_court_level.run()
