"""
@author : kennethAsher
@fole   : AddType.py
@ctime  : 2020/5/6 15:39
@Email  : 1131771202@qq.com
@content: 在案由-审判人员数据数据中，添加审判人员的类型
"""

import re

class AddType():

    # 初始化变量函数
    def __init__(self):
        self.party_path = 'C:\\Users\\GG257\\OneDrive\\sublime\\帮瀛\\pg_data\\pg_court\\pg_court.txt'
        self.family_path = 'C:\\Users\\GG257\\OneDrive\\sublime\\帮瀛\\pg_data\\pg_court\\court_map_4.22.txt'
        self.labels_path = 'D:\\judge_data\\organ_data_docid\\'
        self.write_path = 'D:\\judge_data\\judge_add_court\\'
        self.government_pat = re.compile(r'.*(委|办公室|局|会|办|政协|部|政府|党校|部朝阳大街|信|中心|委银州区|厅|史馆|科学院|科院|事馆|处)$')
        self.labels_set = set()
        self.family1_set = set()
        self.family2_set = set()
        self.family3_set = set()


    def get_fields(self, line):
        return line.strip().split('|')

    # 清洗含有（）的客户
    def clean_str(self, word):
        word = word.strip()
        if '（' in word:
            start_index = word.index('（')
            if '）' in word:
                end_index = word.index('）')
                word = word[:start_index] + word[end_index + 1:]
            else:
                word = word[:start_index]
        return word

    def get_set(self):
        family_names_open = open(self.family_path, 'r', encoding='utf8')
        labels_company_open = open(self.labels_path, 'w', encoding='utf8')
        family1_set = set()
        family2_set = set()
        family3_set = set()
        labels_set = set()
        for family in family_names_open.readlines():
            family = family.strip()
            if len(family) == 1:
                family1_set.add(family)
            if len(family) == 2:
                family2_set.add(family)
            if len(family) == 3:
                family3_set.add(family)
        for label in labels_company_open.readlines():
            labels_set.add(self.clean_str(label.strip()))
        return family1_set, family2_set, family3_set, labels_set

    # 获取当事人类型
    def get_type(self, name):
        match = self.government_pat.match(name)
        if name in self.labels_set:
            return '有标签企业'
        elif match is not None:
            return '政府'
        elif (name[:1] in self.family1_set or name[:2] in self.family2_set or name[:3] in self.family3_set) and len(name) <= 5:
            return '个人'
        else:
            return '非上市民营'

    # 将整理好的数据写入到文件中
    def write_party_type(self):
        file_open = open(self.party_path, 'r', encoding='utf8')
        file_write = open(self.family_path, 'r', encoding='utf8')
        for line in file_open.readlines():
            fields = self.get_fields(line)
            if len(fields[2]) > 1:
                partys = fields[2].split(',')
                list = []
                for party in partys:
                    name = party.split('-')[-1]
                    type = self.get_type(name)
                    list.append(party+'-'+type)
                out_line = fields[0]+'|'+fields[1]+'|'+','.join(list)+'\n'
                file_write.write(out_line)





    # 主执行方法
    def run(self):
        self.family1_set,self.family2_set,self.family3_set,self.labels_set = self.get_set()
        self.write_party_type()


if __name__ == '__main__':
    addtype = AddType()
    addtype.run()

