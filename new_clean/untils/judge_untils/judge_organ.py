"""
@author : kennethAsher
@fole   : judge_organ.py
@ctime  : 2020/4/22 14:50
@Email  : 1131771202@qq.com
@content: 将审判人员的数据和法院数据对关系，补全审判人员数据
"""

import os

class judge_organ():
    #初始化变量函数
    def __init__(self):
        self.pg_court_path = 'C:\\Users\\GG257\\OneDrive\\sublime\\帮瀛\\pg_data\\pg_court\\pg_court.txt'
        self.court_map_path = 'C:\\Users\\GG257\\OneDrive\\sublime\\帮瀛\\pg_data\\pg_court\\court_map_4.22.txt'
        self.judge_dir = 'D:\\judge_data\\organ_data_docid\\'
        self.judge_info_path = 'D:\\judge_data\\judge_add_court\\'
        self.id_info_map = {}
        self.name_id_map = {}

    #返回路径下的文件名称
    def get_path_names(self, path_dir):
        return os.listdir(path_dir)

    def get_fields(self, line):
        return line.strip().split('|')

    #拿到法院id对应的法院信息
    def get_court_id_info_map(self):
        print('看是写入id_info_map')
        file_open = open(self.pg_court_path, 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = self.get_fields(line)
            id = fields[0]
            value = fields[1]+'|'+fields[2]+'|'+fields[3]+'|'+fields[4]+'|'+fields[5]
            self.id_info_map[id] = value
        file_open.close()

    #拿到法院名称对应的法院id
    def get_court_name_id_map(self):
        print('看是写入name_id_map')
        file_open1 = open(self.pg_court_path, 'r', encoding='utf8')
        file_open2 = open(self.court_map_path, 'r', encoding='utf8')
        for line in file_open1.readlines():
            fields = self.get_fields(line)
            id = fields[0]
            name = fields[1]
            self.name_id_map[name] = id
        for line in file_open2.readlines():
            fields = self.get_fields(line)
            id = fields[0]
            name = fields[1]
            self.name_id_map[name] = id
        file_open1.close()
        file_open2.close()

    #整理审判人员数据，将结果写出到文件中
    def write_judge_info(self):
        names = self.get_path_names(self.judge_dir)
        for name in names:
            file_open = open('{}{}'.format(self.judge_dir,name),'r', encoding='utf8')
            file_write = open('{}{}'.format(self.judge_info_path, name), 'w', encoding='utf8')
            print('开始遍历文件{}'.format(name))
            for line in file_open.readlines():
                fields = self.get_fields(line)
                court = fields[2]
                if court not in self.name_id_map:
                    continue
                id = str(self.name_id_map[court])
                value = self.id_info_map[id]
                out_line = fields[0] +'|'+ fields[1] +'|'+ value +'|'+ fields[3] +'|'+ fields[4] +'|'+ fields[5] + '\n'
                file_write.write(out_line)
            file_open.close()
            file_write.close()


    #主执行方法
    def run(self):
        self.get_court_id_info_map()
        self.get_court_name_id_map()
        self.write_judge_info()


if __name__ == '__main__':
    judge_organ = judge_organ()
    judge_organ.run()
    
