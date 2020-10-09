# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/8 11:14 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 取得元数据提供的title，法院，案件类型，案件号，执行年份，执行具体日期
            并且自己清洗法院和案件号，
            并补充判决书类型，审理程序。
'''

import os
import re
import sys
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/get_id.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)

clean_court_pat = re.compile(r'NULL|\+|,|-|\.|0|1|2|3|4|5|6|7|8|9|>|\?|null|VF|_|`|·|ˎ̥|‘|、|【')


# 判断路径是否存在，如果不存在就新建
def exists_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_names(path):
    return os.listdir(path)


def clean_court(court):
    return clean_court_pat.split(court)[-1]


def clean_caseNumber(casenumber):
    casenumber = casenumber.replace('（', '(').replace('）', ')').replace('〔', '(').replace('〕', ')')
    return casenumber


def get_trial_name(case):
    trail = ''
    if '初' in case:
        trail = '一审'
    elif '终' in case:
        trail = '二审'
    elif '特监' in case or '督监' in case:
        trail = '特殊程序'
    elif '再' in case or '申' in case or '监' in case or '抗' in case:
        trail = '再审'
    else:
        trail = '特殊程序'
    return trail


def write_data(label_path, write_minshi, write_xingshi, write_zhixing, write_xingzheng, write_peichang, write_no,
               file_name, step):
    write_minshi = open("{}{}".format(write_minshi, file_name), 'w', encoding='utf8')
    write_xingshi = open("{}{}".format(write_xingshi, file_name), 'w', encoding='utf8')
    write_zhixing = open("{}{}".format(write_zhixing, file_name), 'w', encoding='utf8')
    write_xingzheng = open("{}{}".format(write_xingzheng, file_name), 'w', encoding='utf8')
    write_peichang = open("{}{}".format(write_peichang, file_name), 'w', encoding='utf8')
    write_no = open("{}{}".format(write_no, file_name), 'w', encoding='utf8')
    file_open = open('{}{}'.format(label_path, file_name), 'r', encoding='utf8')
    logging.info('开始写入第{}个文件--{}'.format(step, file_name))
    for line in file_open.readlines():
        fields = line.strip().split('|')
        if len(fields) < 7:
            continue
        doc_id = fields[0]
        title = fields[1]
        court = clean_court(fields[2]) if len(fields[2]) > 5 else ''
        casenumber = clean_caseNumber(fields[4])
        year = fields[5] if len(fields[5]) > 2 else ''
        date = fields[6] if '-' in fields[6] else ''
        trailname = get_trial_name(casenumber)
        casetypedoc = ''
        if '刑事' in fields[3]:
            casetype = '刑事案件'
            if '附带' in title:
                casetypedoc = '刑事附带民事判决书'
            elif '判决' in title:
                casetypedoc = '刑事判决书'
            elif '裁定' in title:
                casetypedoc = '刑事裁定书'
            elif '死刑' in title:
                casetypedoc = '执行死刑命令'
            else:
                casetypedoc = ''
            write_xingshi.write(
                doc_id + '|' + title + '|' + court + '|' + casenumber + '|' + year + '|' + date + '|' + trailname + '|' + casetype + '|' + casetypedoc + '\n')
        elif '行政' in fields[3]:
            casetype = '行政案件'
            if '附带' in title:
                casetypedoc = '行政附带民事判决书'
            elif '赔偿判决' in title:
                casetypedoc = '行政赔偿判决书'
            elif '判决' in title:
                casetypedoc = '行政判决书'
            elif '裁定' in title:
                casetypedoc = '行政裁定书'
            elif '调解' in title:
                casetypedoc = '行政赔偿调解书'
            else:
                casetypedoc = ''
            write_xingzheng.write(
                doc_id + '|' + title + '|' + court + '|' + casenumber + '|' + year + '|' + date + '|' + trailname + '|' + casetype + '|' + casetypedoc + '\n')
        elif '民事' in fields[3]:
            casetype = '民事案件'
            if '判决' in title:
                casetypedoc = '民事判决书'
            elif '裁定' in title:
                casetypedoc = '民事裁定书'
            elif '决定' in title:
                casetypedoc = '民事决定书'
            elif '调解' in title:
                casetypedoc = '民事调解书'
            else:
                casetypedoc = ''
            write_minshi.write(
                doc_id + '|' + title + '|' + court + '|' + casenumber + '|' + year + '|' + date + '|' + trailname + '|' + casetype + '|' + casetypedoc + '\n')
        elif '赔偿' in fields[3]:
            casetype = '赔偿案件'
            write_peichang.write(
                doc_id + '|' + title + '|' + court + '|' + casenumber + '|' + year + '|' + date + '|' + trailname + '|' + casetype + '|' + casetypedoc + '\n')
        elif '执行' in fields[3]:
            casetype = '执行案件'
            if '裁定' in title:
                casetypedoc = '执⾏裁定书'
            write_zhixing.write(
                doc_id + '|' + title + '|' + court + '|' + casenumber + '|' + year + '|' + date + '|' + trailname + '|' + casetype + '|' + casetypedoc + '\n')
        else:
            casetype = ''
            write_no.write(
                doc_id + '|' + title + '|' + court + '|' + casenumber + '|' + year + '|' + date + '|' + trailname + '|' + casetype + '|' + casetypedoc + '\n')

    file_open.close()
    write_minshi.close()
    write_peichang.close()
    write_xingshi.close()
    write_zhixing.close()
    write_xingzheng.close()
    write_no.close()


def run(label_path, write_minshi, write_xingshi, write_zhixing, write_xingzheng, write_peichang, write_no, file_name, step):
    write_data(label_path, write_minshi, write_xingshi, write_zhixing, write_xingzheng, write_peichang, write_no,
               file_name, step)


if __name__ == '__main__':
    # 定义各个文件路径
    label_path = "/mnt/{}/data/organ_data_add/".format(sys.argv[1])
    write_minshi = '/mnt/{}/data/minshi/add_data/'.format(sys.argv[1])
    exists_or_create(write_minshi)
    write_xingshi = '/mnt/{}/data/xingshi/add_data/'.format(sys.argv[1])
    exists_or_create(write_xingshi)
    write_zhixing = '/mnt/{}/data/zhixing/add_data/'.format(sys.argv[1])
    exists_or_create(write_zhixing)
    write_xingzheng = '/mnt/{}/data/xingzheng/add_data/'.format(sys.argv[1])
    exists_or_create(write_xingzheng)
    write_peichang = '/mnt/{}/data/peichang/add_data/'.format(sys.argv[1])
    exists_or_create(write_peichang)
    write_no = '/mnt/{}/data/organ_no_add/'.format(sys.argv[1])
    exists_or_create(write_no)
    for step, file_name in enumerate(os.listdir(label_path)):
        run(label_path, write_minshi, write_xingshi, write_zhixing, write_xingzheng, write_peichang, write_no,
            file_name, step)
