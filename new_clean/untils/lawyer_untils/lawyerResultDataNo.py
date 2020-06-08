"""
@author : kennethAsher
@fole   : lawyerResultDataNo.py
@ctime  : 2020/5/21 19:44
@Email  : 1131771202@qq.com
@content:
            将律师数据补充id,将没有找到的律师单独存放，补充到律师数据中

"""

import os

class LawyerResultDataNo():
    def __init__(self):
        self.input_path = '/mnt/disk2/data/sum_data/lawyer_result/lawyer_score_data/'
        self.output_path = '/mnt/disk2/data/sum_data/lawyer_result/lawyer_score_data_no/'
        self.family_file = '/mnt/disk2/utils_data/lawyer_score/family_names.txt'
        self.id_file = '/mnt/disk2/utils_data/pg_lawyer.txt'
        self.need_in_file = '/mnt/disk2/data/sum_data/lawyer_result/in_file'

        self.flag_set = set()
        self.family_set = set()
        self.id_mapping = {}


    def get_mapping(self):
        with open(self.id_file, 'r', encoding='utf8') as open_file:
            for line in open_file.readlines():
                fields = line.strip().split('|')
                if len(fields)>3:
                     name = fields[1]
                     organ = fields[3]
                     key = name +'-'+organ
                     self.id_mapping[key] = fields[0]
        open_file.close()

    def get_set(self):
        with open(self.family_file, 'r', encoding='utf8') as family_open:
            for line in family_open.readlines():
                self.family_set.add(line.strip())

    def write_file(self):
        names = os.listdir(self.input_path)
        num = 1001059850
        need_id = open(self.need_in_file, 'w', encoding='utf8')
        for name in names:
            print('正在执行文件{}'.format(name))
            with open('{}{}'.format(self.input_path, name),'r', encoding='utf8') as file_open, open('{}{}'.format(self.output_path, name),'w', encoding='utf8') as file_out:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    name = fields[0]
                    organ = fields[1]
                    key = name+'-'+organ
                    if key in self.id_mapping:
                        out_line = self.id_mapping[key]+'|'+line
                        file_out.write(out_line)
                    else:
                        if key not in self.flag_set:
                            num = num+1
                            self.flag_set.add(key)
                            if len(name)>1:
                                if (name[0] in self.family_set or name[:2] in self.family_set) and len(name)<5:
                                    out_line = str(num) +'|'+ line
                                    file_out.write(out_line)
                                    out_id_line = str(num)+'|'+name+'|'+organ+'\n'
                                    need_id.write(out_id_line)
            file_open.close()
            file_out.close()
        need_id.close()

    def run(self):
        self.get_set()
        self.get_mapping()
        self.write_file()
        print('执行结束')

if __name__ == '__main__':
    demo = LawyerResultDataNo()
    demo.run()
