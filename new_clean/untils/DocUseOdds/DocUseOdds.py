#!/usr/bin/python
# encoding: utf-8
'''
@author: kenneth
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: 1131771202@qq.com
@file: DocUseOdds.py
@time: 2020/7/1 2:57 下午
@desc: 通过计算词频来计算文案采用率
        （1为撤回等因素导致，0为计算得到的采用率）
        输出为：doc_id|原告采用率｜标记｜被告采用率｜标记
'''

###倒入包
import os


###定义实现类
class DocUseOdds():
    # 初始化方法
    def __init__(self):
        # 输入路径
        self.input_path = '/Users/kenneth-mac/data/test/appeal_words/'
        # 输出路径
        self.output_path = '/Users/kenneth-mac/data/test/win_dds/'

    # 获取文件名方法
    def get_names(self, path):
        return os.listdir(path)

    # 启动方法
    def run(self):
        # 获得路径下的文件名
        names = self.get_names(self.input_path)
        # 遍历每个文件
        for name in names:
            # 打开文件
            with open('{}{}'.format(self.input_path, name), 'r', encoding='utf8') as file_open, open(
                    '{}{}'.format(self.output_path, name), 'w', encoding='utf8') as file_write:
                # 遍历原文件里面的内容
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    if len(fields) >= 3:
                        # 案件号
                        doc_id = fields[0]
                        if '撤回起诉' in fields[3] or '驳回' in fields[3] or '异议成立' in fields[3] \
                                or '本案移送' in fields[3] or '撤诉' in fields[3] or '中止' in fields[3] \
                                or '准许' in fields[3] or '终结' in fields[3] or '转为普通程序' in fields[3] \
                                or '本院提审' in fields[3]:
                            file_write.write(doc_id + '|' + str(0) + '|' + str(1) + '|' + str(0) + '|' + str(1) + '\n')
                            continue
                        # 原告诉求,按照','分隔的句子
                        plaintiff_text = fields[1]
                        # 原告同法院认为词频出现次数
                        plaintiff_num = 0
                        # 被告诉求,按照','分隔的句子
                        defendant_text = fields[2]
                        # 被告同法院认为词频出现次数
                        defendant_num = 0
                        # 法院认为,按照','分隔的句子
                        court_text = fields[3]
                        
                        # 判断如果原告和被告均无内容，则直接输出
                        if (plaintiff_text == '' and defendant_text == '') or court_text == '':
                            file_write.write(doc_id + '|' + str(0) + '|' + str(0) + '|' + str(0) + '|' + str(0) + '\n')
                            continue
                        # 计算原告诉求词频出现次数
                        for word in plaintiff_text.split(','):
                            if word in court_text:
                                plaintiff_num += 1
                        # 计算被告诉求出现的次数
                        for word in defendant_text.split(','):
                            if word in court_text:
                                defendant_num += 1
                        # 词频出现总和
                        sum = plaintiff_num + defendant_num
                        if sum <= 0 :
                            file_write.write(doc_id + '|' + str(0) + '|' + str(0) + '|' + str(0) + '|' + str(0) + '\n')
                            continue
                        # 计算文案采用率
                        plaintiff_odds = plaintiff_num / sum
                        defendant_odds = defendant_num / sum
                        out_line = doc_id + '|' + str(round(plaintiff_odds, 3)) + '|' + '0' + '|' +\
                                   str(round(defendant_odds, 3)) + '|' + '0'
                        file_write.write(out_line + '\n')



if __name__ == '__main__':
    doc_use = DocUseOdds()
    doc_use.run()

