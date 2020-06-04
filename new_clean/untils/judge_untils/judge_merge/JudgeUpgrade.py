"""
@author : kennethAsher
@fole   : JudgeUpgrade.py
@ctime  : 2020/4/24 13:52
@Email  : 1131771202@qq.com
@content:
        上面对应着各层次名称合并之后的数据
        将升级的审判人员数据（即名称相同的数据）单独输出
        然后将符合条件升级的审判人员单独输出至文件judge_upgrade中
"""

import os

class JudgeUpgrade():
    def __init__(self):
        self.input_path = 'D:\\judge_data\\judge_merge\\judge_name_merge\\'
        self.output_file = open('D:\\judge_data\\judge_merge\\judge_upgrade\\judge_upgrade', 'w', encoding='utf8')

    def get_names(self, input_path):
        return os.listdir(input_path)

    def get_judge(self, name, type):
        file_open = open('{}{}'.format(self.input_path, name), 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = line.strip().split('---')
            if len(fields) < 1:
                continue
            words_1 = fields[0].split('|')
            words_2 = fields[1].split('|')
            if type != 4:
                if (words_1[type] == words_2[type]) and (words_1[3]<words_2[2]):
                    self.output_file.write(line)
            else:
                if words_1[3]<words_2[2]:
                    self.output_file.write(line)

    def run(self):
        self.get_judge('level01',6)
        self.get_judge('level12',5)
        self.get_judge('level23', 4)


if __name__ == '__main__':
    judge_upgrade = JudgeUpgrade()
    judge_upgrade.run()