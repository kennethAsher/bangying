"""
@author : kennethAsher
@fole   : LawyerAddData.py
@ctime  : 2020/5/7 15:51
@Email  : 1131771202@qq.com
@content:
            上接律师审判人员数据，附加数据
            根据docid将两者数据合并
"""

import os

class LawyerAddData():
    def __init__(self):
        self.add_data_path = '/mnt/disk2/data/sum_data/add_data/'
        self.cause_party_path = '/mnt/disk2/data/sum_data/cause_party/'
        self.lawyer_judge_path = '/mnt/disk2/data/sum_data/lawyer_judge/'
        self.pg_court_path = '/mnt/disk2/utils_data/court/pg_court.txt'
        self.court_map_path = '/mnt/disk2/utils_data/court/court_map_4.22.txt'
        self.write_file = '/mnt/disk2/data/sum_data/add_data_result/'
        self.lawyer_judge_mapping = {}
        self.cause_party_mapping = {}
        self.id_info_map = {}
        self.name_id_map = {}

    def get_names(self, path):
        return os.listdir(path)

    def get_fields(self, line):
        return line.strip().split('|')

    # 拿到法院id对应的法院信息
    def get_court_id_info_map(self):
        print('开始写入id_info_map')
        file_open = open(self.pg_court_path, 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = self.get_fields(line)
            id = fields[0]
            value = fields[1] + '|' + fields[2] + '|' + fields[3] + '|' + fields[4] + '|' + fields[5]
            self.id_info_map[id] = value
        file_open.close()

    # 拿到法院名称对应的法院id
    def get_court_name_id_map(self):
        print('开始写入name_id_map')
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

    def get_map(self):
        add_data_names = self.get_names(self.lawyer_judge_path)
        print('starting read file lawyer_judge for making lawyer_judge_mapping')
        for name in add_data_names:
            add_data_open = open('{}{}'.format(self.lawyer_judge_path, name), 'r', encoding='utf8')
            print('starting read file lawyer_judge for making lawyer_judge_mapping of {}'.format(name))
            for line in add_data_open.readlines():
                fields = self.get_fields(line)
                lawyer_name = fields[1]
                lawyer_organ = fields[2]
                judge = fields[3]
                friend = fields[4]
                opponent = fields[5]
                value = lawyer_name+'|'+lawyer_organ+'|'+judge+'|'+friend+'|'+opponent
                self.lawyer_judge_mapping[fields[0]] = value
            add_data_open.close()
        print('ending read file lawyer_judge for making lawyer_judge_mapping')


    def write_result(self):
        names = self.get_names(self.add_data_path)
        for name in names:
            print('starting read file for {}'.format(name))
            add_data_open = open('{}{}'.format(self.add_data_path, name), 'r', encoding='utf8')
            write_result = open('{}{}'.format(self.write_file, name), 'w', encoding='utf8')
            for line in add_data_open.readlines():
                fields = self.get_fields(line)
                if len(fields)<2:
                    continue
                title = fields[1]
                try:
                    court_value = self.id_info_map[str(self.name_id_map[fields[2]])]
                except :
                    court_value = '||||'
                lawyer_judge = self.lawyer_judge_mapping[fields[0]] if fields[0] in self.lawyer_judge_mapping else '||||'
                doc_number = fields[3]
                year = fields[4]
                date = fields[5]
                trail = fields[6]
                doc_type = fields[7]
                book_type = fields[8]
                value =fields[0]+'|'+ title +'|'+court_value+'|'+doc_number+'|'+year+'|'+date+'|'+trail+'|'+doc_type+'|'+book_type
                out_line = value+'|'+lawyer_judge+'\n'
                write_result.write(out_line)
            add_data_open.close()
            write_result.close()

    def run(self):
        self.get_court_id_info_map()
        self.get_court_name_id_map()
        self.get_map()
        self.write_result()


if __name__ == '__main__':
    demo = LawyerAddData()
    demo.run()