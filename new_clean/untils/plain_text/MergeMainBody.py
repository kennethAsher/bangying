#!/usr/bin/python
# encoding: utf-8
'''
@author: kenneth
@license: (C) Copyright 2019-2020, Node Supply Chain Manager Corporation Limited.
@contact: 1131771202@qq.com
@file: MergeMainBody.py
@time: 2020/7/20 4:17 下午
@desc: 合并生成上传至es-裁判文书的文档代码
        id表示(docid), 标题(title), 案件号（caseno），案由(casereason), 审理程序(trialprocedure), 审判年份(judgeyear), 审判月份(judgemonth),审判时间(judgetime), 法院（court），层级（courtlevel），
        省份（province），城市（city），区/县（region）， 案件类型（casetype）， 文书类型（doctype）， 文书内容（plaintext），flag（不知道什么意思）， 审判人员（justices）
'''

import os

class MergeMainBody():
    #初始化所有变量
    def __init__(self):
        super(MergeMainBody, self).__init__()
        #裁判文书所在目录
        self.mainbody_path = '/mnt/disk2/data/minshi/organ_data/'
        #裁判文书补充数据存放目录
        self.add_data_path = '/mnt/disk2/data/sum_data/add_result/minshi/minshi2/'
        #裁判文书合并写出数据
        self.out_path = '/mnt/disk2/data/sum_data/add_result/out_minshi/'

        #裁判补充数据的字典
        self.add_data_mapping = {}

    #获取当前路径下的所有文件名
    def get_names(self, path):
        return os.listdir(path)

    #讲数据写入到补充数据字典中
    def wriet_mapping(self):
        for name in self.get_names(self.add_data_path):
            print('start write file {} to mapping'.format(name))
            with open('{}{}'.format(self.add_data_path, name), 'r', encoding='utf8') as file_open:
                for line in file_open.readlines():
                    fields = line.strip().split('|')
                    doc_id = fields[0]
                    title = fields[1]
                    caseno = fields[7]
                    casereason = fields[18]
                    trialprocedure = fields[10]
                    court = fields[2]
                    courtlevel = fields[6]
                    judgeyear = fields[8]
                    judgemonth = '' if len(fields[9])<2 else fields[9][:-3].replace('-','')
                    judgedate =fields[9]
                    province = fields[3]
                    city = fields[4]
                    region = fields[5]
                    casetype = fields[11]
                    doctype = fields[12]
                    justices = fields[15]
                    value_line = title+'|'+caseno+'|'+casereason+'|'+trialprocedure+'|'+court+'|'+courtlevel+'|'+judgeyear+'|'+judgemonth+'|'+judgedate+'|'+province+'|'+city+'|'+region+'|'+casetype+\
                        '|'+doctype+'|'+justices
                    self.add_data_mapping[doc_id] = value_line
            file_open.close()
        print('processing write mapping is successfully')

    #将组合好的数据写出到指定文件中
    def write_out(self):
        names = self.get_names(self.mainbody_path)
        for name in names:
            print('start read file {}'.format(name))
            with open('{}{}'.format(self.mainbody_path, name), 'r', encoding='utf8') as file_open, open('{}{}'.format(self.out_path, name), 'w', encoding='utf8') as file_write:
                for line in file_open.readlines():
                    fields = line.split('|')
                    if fields[0] in self.add_data_mapping:
                        out_line = fields[0]+'|'+self.add_data_mapping[fields[0]]+'|'+fields[1].replace('。。。。。','。')\
                                   .replace('。。。。','。').replace('。。。','。').replace('。。','。')
                        file_write.write(out_line)
            file_open.close()
            file_write.close()
        print('processing write out is successfully')

    #主运行函数
    def run(self):
        self.wriet_mapping()
        self.write_out()

if __name__ == '__main__':
    merge_demo = MergeMainBody()
    merge_demo.run()