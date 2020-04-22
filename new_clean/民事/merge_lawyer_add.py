"""
@author : kennethAsher
@fole   : merge_lawyer_add.py
@ctime  : 2020/4/21 19:52
@Email  : 1131771202@qq.com
@content: 合并审判人员数据
"""


import os

class demo():
    #初始化
    def __init__(self):
        self.judge_path = '/mnt/disk2/data/minshi/lawyer_judge/'
        self.add_path = '/mnt/disk2/data/minshi/add_data/'
        self.output_path = '/mnt/disk2/data/minshi/judge_case/judge_case'
        self.add_map = {}
        self.judge_map = {}

    #返回路径下的文件名称集合
    def get_names(self, input_path):
        return os.listdir(input_path)

    #拿到add_path的map，返回日期，法院，审理程序
    def get_add_map(self):
        names = self.get_names(self.add_path)
        for name in names:
            file_open = open('{}{}'.format(self.add_path, name), 'r', encoding='utf8')
            for line in file_open.readlines():
                fields = line.strip().split('|')
                out_line = fields[2]+'|'+fields[4]+'|'+fields[5]+'|'+fields[6]
                key = fields[0]
                self.add_map[key] = out_line
            file_open.close()

    #拿到judge_path的map,返回审判人员的名称以及对应的法院，（书记员要排除）
    def get_judge_map(self):
        names = self.get_names(self.judge_path)
        for name in names:
            file_open = open('{}{}'.format(self.judge_path, name), 'r', encoding='utf8')
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
                self.judge_map[key] = out_line
            file_open.close()

    #将审判人员数据写出
    def write_judge_case(self):
        file_out = open(self.output_path, 'w', encoding='utf8')
        names = self.get_names(self.add_path)
        for name in names:
            file_open = open('{}{}'.format(self.add_path, name), 'r', encoding='utf8')
            for line in file_open.readlines():
                key = line.strip().split('|')[0]
                if key not in self.judge_map:
                    continue
                judges = self.judge_map[key]
                if len(judges) > 0:
                    names = judges.split(',')
                    for name in names:
                        out_line = key + '|' + name+'|'+self.add_map[key]+'\n'
                        file_out.write(out_line)
            file_open.close()
        file_out.close()


    #执行函数
    def run(self):
        print('开始导入add_map')
        self.get_add_map()
        print('导入完成add_map,并且开始导入judge_map')
        self.get_judge_map()
        print('导入完成judge_map，并且开始写出到最后文件中')
        self.write_judge_case()
        print('执行完成')

if __name__ == '__main__':
    demo = demo()
    demo.run()

