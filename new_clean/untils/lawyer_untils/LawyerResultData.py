"""
@author : kennethAsher
@fole   : LawyerResultData.py
@ctime  : 2020/5/21 16:38
@Email  : 1131771202@qq.com
@content: 从添加好各个维度的数据中提取所有律师的数据
"""

import os
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/untils/get_data/LawyerResultData.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

class LawyerResultData():
    def __init__(self):
        self.input_path = '/mnt/disk2/data/sum_data/add_result/'
        self.out_path = '/mnt/disk2/data/sum_data/lawyer_result/lawyer_score_data/'

    def get_path_names(self, path):
        return os.listdir(path)
    #获取日期
    def get_date(self, fields):
        if len(fields[9])>2:
            return fields[9]
        if len(fields[8])>2:
            return fields[8]
        return ''

    def write_out_data(self):
        names = os.listdir(path=self.input_path)
        for name in names:
            logging.info('starting to write data {}'.format(name))
            with open('{}{}'.format(self.input_path, name), 'r', encoding='utf8') as file_open, open('{}{}'.format(self.out_path, name), 'w', encoding='utf8') as file_write:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    date = self.get_date(fields)
                    cause = fields[18]
                    trail = fields[10]
                    party = fields[-1]
                    court = fields[2]
                    city = fields[4]
                    judge = fields[15]
                    if len(fields[13])>1 and len(fields[14])>1:
                        name = fields[13]
                        organ = fields[14]
                        out_line = name+'|'+organ+'|'+date+'|'+cause+'|'+trail+'|'+party+'|'+court+'|'+city+'|'+judge+'\n'
                        file_write.write(out_line)
                    if len(fields[16])>2:
                        for lawyer in fields[16].split(','):
                            try:
                                name = lawyer.split('-')[0]
                                organ = lawyer.split('-')[1]
                                out_line = name + '|' + organ + '|' + date + '|' + cause + '|' + trail + '|' + party + '|' + court + '|' + city + '|' + judge + '\n'
                                file_write.write(out_line)
                            except:
                                logging.info('不理他')
                    if len(fields[17])>2:
                        for lawyer in fields[17].split(','):
                            try:
                                name = lawyer.split('-')[0]
                                organ = lawyer.split('-')[1]
                                out_line = name + '|' + organ + '|' + date + '|' + cause + '|' + trail + '|' + party + '|' + court + '|' + city + '|' + judge + '\n'
                                file_write.write(out_line)
                            except:
                                logging.info('不理他')
            file_open.close()
            file_write.close()

    def run(self):
        self.write_out_data()


if __name__ == '__main__':
    lawyer_result = LawyerResultData()
    lawyer_result.run()