"""
@author : kennethAsher
@fole   : MergeJudgeInfoAttr.py
@ctime  : 2020/5/14 17:54
@Email  : 1131771202@qq.com
@content: 上接已经清洗完成的judgeinfo数据集，现在将两者进行合并，最终数据上传至es
"""


class MergeInfo():
    def __init__(self):
        self.insert_x_file = ''
        self.insert_file = ''
        self.merge_file_path = ''
        self.mapping = {}

    def get_fields(self, line):
        return line.strip().split('|')

    def get_mapping(self):
        with open(self.insert_file, 'r', encoding='utf8') as file_open:
            for line in file_open.readlines():
                fields = self.get_fields(line)
                self.mapping[fields[3]] = line.strip()
            file_open.close()

    def get_merge_fields(self, x_filename, filename):
        field = ''
        if len(x_filename)>len(filename)==0 or len(filename)>len(x_filename)==0:
            field = x_filename if len(x_filename)>len(filename)==0 else filename
            return field
        if len(x_filename)>0 and len(filename)>0:
            x_words = x_filename.split(',')
            words = filename.split(',')




    def merge_file(self):
        merge_file_out = open(self.merge_file_path, 'w', encoding='utf8')
        with open(self.insert_x_file, 'r', encoding='utf8') as x_file_open:
            for line in x_file_open.readlines():
                x_fields = self.get_fields(line)
                if x_fields[3] not in self.mapping:
                    merge_file_out.write(line)
                    continue
                fields = self.get_fields(self.mapping[x_fields[3]])
                judge_name = x_fields[0]
                court = x_fields[1]
                judge_id = x_fields[2]




        pass

    def run(self):
        self.get_mapping()
        self.merge_file()
