# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/14 10:00 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 从裁判文书中提取诉讼请求，以及法院的判决结果
            案号|原告|被告|法院
'''



import re
import os
import logging

logging.basicConfig(filename='/Users/kenneth-mac/OneDrive/pycharm/bangying/log/clean_oc/民事/clean_text.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

docSplitPat = re.compile(r'。')
htmlRemovePat = re.compile('>(.*?)<')
#清洗律师事务所开头为系，均系，为等
organ_split_pat = re.compile(r'系|均系|为')
#原告诉求判断
plaintiff_lawsuit_pat = re.compile(r'(原审原告|原告人|原告|上诉人|申诉人|再审申请人|申请人|申请执行人|异议人|起诉人|申报人|原审第三人|第三人).*(诉讼请求|诉讼|请求|诉请|诉称)')
# 被告诉求
appellee_lawsuit_pat = re.compile(r'((原审被告|被告人|被告|被上诉人|被申诉人|申请再审人|被申请人|被执行人|被异议人)|一审法院).*(答辩|反诉|诉讼|请求|诉请|诉称|认为)')
# 法院认为中断
court_end_pat = re.compile(r'.*本院认为.*')
# 法院判决
court_lawsuit_pat = re.compile(r'.*(判决如下|裁决如下|裁定如下).*')
# 审判人员
justicePatterns = re.compile(r'^((代理)?审判长)[:：]?(.*)'
                               r'|^((保持队形)?院长)[:：]?(.*)'
                               r'|^((代|代理|助[理]?|人民)?审[判理]?员)[:：]?(.*)'
                               r'|^((代|代理|见习|实习)?书记员)[:：]?(.*)'
                               r'|^((保持队形)?法官助理)[:：]?(.*)'
                               r'|^((保持队形)?执行员)[:：]?(.*)'
                               r'^((人[民员]|代理)?陪[审判]员?)[:：]?(.*)')


def get_judges(judge_types, judges):
    fields_type = judge_types.split(',')
    fields_judge = judges.split(',')
    type_judge = ''
    flag = len(fields_judge) if len(fields_judge) < len(fields_type) else len(fields_type)
    for i in range(flag):
        if len(fields_judge[i])<2:
            continue
        type_judge = type_judge + ',' + fields_type[i] + '-' + fields_judge[i]
    return type_judge[1:]

def write_lawyer_judge(open_dir, write_dir):
    file_write = open(write_dir, 'w', encoding='utf8')
    file_open = open(open_dir, 'r', encoding='utf-8')
    for line in file_open.readlines():
        plaintiff_lawsuit = ''
        appellee_lawsuit = ''
        court_lawsuit = ''
        #因为提取的时候将换行替换成了了'。'，所以在文书可能连续出现多个句号，此处需要将这些替换掉
        line = htmlRemovePat.sub('', line)
        line = line.replace('。。。。。', '').replace('。。。。', '').replace('。。。', '').replace('。。', '').replace('\n','')
        doc_num = line.split('|')[0]
        lines = docSplitPat.split(line)
        #过滤出现'一案'之前内容的标识，之前的数据主要是原告、被告、律师、案由等信息
        read_flag = 0
        for line in lines:
            if '不服从本' in line or '不服本' in line or '调解方式结案' in line or '调解协议' in line or justicePatterns.match(line) is not None:
                break
            if '一案' in line:
                read_flag = 1
                continue
            if '到庭' in line:
                continue
            if read_flag > 0:
                if court_end_pat.match(line) is not None:
                    read_flag = 1
                if plaintiff_lawsuit_pat.match(line) is not None:
                    read_flag = 2
                if appellee_lawsuit_pat.match(line) is not None:
                    read_flag = 3
                if court_lawsuit_pat.match(line) is not None:
                    read_flag = 4
                if read_flag == 2:
                    if '均到庭' in line or '审理终结' in line:
                        continue
                    plaintiff_lawsuit = plaintiff_lawsuit + '。' + line
                if read_flag == 3:
                    appellee_lawsuit = appellee_lawsuit + '。' + line
                if read_flag == 4:
                    court_lawsuit = court_lawsuit + '。' + line

        plaintiff_lawsuit = plaintiff_lawsuit[1:] if len(plaintiff_lawsuit) > 1 else ''
        appellee_lawsuit = appellee_lawsuit[1:] if len(appellee_lawsuit) > 1 else ''
        court_lawsuit = court_lawsuit[1:] if len(court_lawsuit) > 1 else ''

        file_write.write(doc_num+'|'+plaintiff_lawsuit+'|'+appellee_lawsuit+'|'+court_lawsuit+'\n')
        file_open.close()
    file_write.close()



def run(open_dir, write_dir):
    names = os.listdir(input_path)
    for name in names:
        logging.info('start reading file of {}'.format(name))
        write_lawyer_judge(open_dir+name, write_dir+name)
        logging.info('end reading file of {}'.format(name))
    logging.info('全部文件执行完成')

if __name__ == '__main__':
    input_path = '/Users/kenneth-mac/data/test/mainbody_test/'
    out_path = '/Users/kenneth-mac/data/test/'
    run(input_path, out_path)
