#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/6/23 5:37 PM 
@Author : kennethAsher
@Email  ：1131771202@qq.com
@content: 将诉求进行分词
'''

import os
import jieba

class SplitLine():
    #初始化方法
    def __init__(self):
        super(SplitLine, self).__init__()
        #文件输入路径
        self.input_path = '/mnt/disk1/data/minshi/appeal_data/'
        #文件输出路径
        self.output_path = '/mnt/disk1/data/minshi/split_words/'
        #停用此所在路径
        self.stop_words_file = '/mnt/disk1/data/pg_data/stop_words'
        #存放停用此的set
        self.stop_words = set()

    #将停用此补充至set的方法
    def load_stop_words(self):
        with open(self.stop_words_file, 'r', encoding='utf8') as file_open:
            for line in file_open.readlines():
                self.stop_words.add(line.strip())

    #将去掉停用词的词语写出至输出目录中
    def write_words(self):
        names = os.listdir(self.input_path)
        for name in names:
            print('开始执行文件{}'.format(name))
            with open('{}{}'.format(self.input_path, name), 'r', encoding='utf8') as file_open, open('{}{}'.format(self.output_path, name), 'w', encoding='utf8') as file_out:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    doc_id = fields[0]
                    plaintiff_words = ''
                    if len(fields[1]) > 2:
                        plaintiff_words = ','.join([x for x in jieba.lcut(fields[1]) if x not in self.stop_words])
                    defendant_words = ''
                    if len(fields[2]) > 2:
                        defendant_words = ','.join([x for x in jieba.lcut(fields[2]) if x not in self.stop_words])
                    court_words = ''
                    if len(fields[3]) > 2:
                        court_words = ','.join([x for x in jieba.lcut(fields[3]) if x not in self.stop_words])
                    out_line = doc_id+'|'+plaintiff_words+'|'+defendant_words+'|'+court_words+'\n'
                    file_out.write(out_line)
                file_open.close()
                file_out.close()
        print('本程序执行结束')

    def run(self):
        self.load_stop_words()
        self.write_words()


if __name__ == '__main__':
    split_line = SplitLine()
    split_line.run()