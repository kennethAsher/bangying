# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/16 上午10:00
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 从裁判文书的标题中清洗出案由等
select title, mainbody from tods_judrisk_lawsui where casetype_name = '民事案件' limit 2000;
'''

import os
import re
case_type_pat = re.compile(r'民事|刑事|执行|行政|赔偿')
cause_action_pat = re.compile(r'一审|二审|再审|撤销|特别')
#首先将本地的裁判文书文件中拿到所有的title


def get_names(input_path):
    return os.listdir(input_path)

#将title写入到单独文件中
def write_title(open_orgin_dir, write_title_data):
    names = get_names(open_orgin_dir)
    write_data = open(write_title_data, 'w', encoding='utf8')
    for name in names:
        input_data = open('{}{}'.format(open_orgin_dir, name), 'r', encoding='utf8')
        for line in input_data.readlines():
            fields = line.split('|')
            title = fields[2]
            write_data.write(title+'\n')
        input_data.close()
    write_data.close()

#清洗裁判文书标题数据
def clean_title(write_title_data, write_clean_data, cause_names):
    
    clean_data = open(write_clean_data, 'w', encoding='utf8')
    title_data = open(write_title_data, 'r', encoding='utf8')
    for line in title_data.readlines():
        flag = 0
        cause_name = open(cause_names, 'r', encoding='utf8')
        for cause in cause_name.readlines():
            cause = cause.strip()
            if cause in line:
                clean_data.write(cause+'\n')
                flag = 1
                break
        if flag == 0:
            print(line)
            # try:
            #     case_type = case_type_pat.findall(line)
            #     case_name = case_type[0]+'案件'
            # except :
            #     case_name = '其它案件'
            # try:
            #     cause_action = cause_action_pat.findall(line)
            #     cause_name = cause_action[0]
            # except :
            #     cause_name = '其它'





def run(open_orgin_dir, write_title_data, write_clean_data, cause_dir):
    # write_title(open_orgin_dir, write_title_data)
    clean_title(write_title_data, write_clean_data, cause_dir)


if __name__ == '__main__':
    open_orgin_dir = '/Users/by-webqianduan/data/doc_add_province/'
    write_title_data = '/Users/by-webqianduan/data/test_title/title.txt'
    write_clean_data = '/Users/by-webqianduan/data/test_title/desc_title.txt'
    cause_dir = '/Users/by-webqianduan/Documents/pg_data/cause_name/cause_names'
    run(open_orgin_dir, write_title_data, write_clean_data, cause_dir)