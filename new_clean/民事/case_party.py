# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/16 上午10:37
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 清洗民事判决书，代码能够实现从裁判文书中找到原告，被告，以及案由--针对民事裁定书
清洗出来的当事人有的为空，处理的时候需要注意一下
清洗出来会有当事人为委托人，注意一下"被上诉人-共同委托诉讼代理人欧"
存在乱码需要处理        ：为离���纠纷
本次操作将有乱码的数据直接舍弃

'''

import re
import os
import logging

# logging.basicConfig(filename='D:\\cause_data\\cause_party.log',
logging.basicConfig(filename='/mnt/disk1/log/python/minshi/cause_party.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

# 判断案由
# 使用与会报错：本院在审理原告浙江××农村合作银行××星××行诉被告王甲、王乙金融借款合同纠纷一案中
# 分行mainbody的正则
split_pat = re.compile(r'。|\n')
# 判断是否符合案由所在句子
cause_pat = re.compile(r'(.*?)一案')
# 在完整句子中切分出当事人
name_split = re.compile(r',|，')
# 清洗当事人名称
clean_party_pat = re.compile(r'：|\?|:|˙|；|1|2|3|4|5|6|7|8|9')
# 匹配到当事人
parties_pat = re.compile(r'((原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人'
                         r'|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人)([\(（].*?[\)）])?)[:：]?(.*)')
# 切分当事人
parties_split_pat = re.compile(r'原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人'
                               r'|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人')
#清除标签内容
htmlRemovePat = re.compile('>(.*?)<')

def get_set():
    # file_o = open('D:\\cause_data\\pg_sm_cause_of_action.txt', 'r', encoding='utf8')
    file_o = open('/mnt/disk2/utils_data/pg_sm_cause_of_action.txt', 'r', encoding='utf8')
    set1 = set()
    set2 = set()
    set3 = set()
    set4 = set()
    for line in file_o.readlines():
        fields = line.strip().split('|')
        if fields[3] != '':
            set4.add(fields[3])
        if fields[2] != '':
            set3.add(fields[2])
        if fields[1] != '':
            set2.add(fields[1])
        if fields[0] != '':
            set1.add(fields[0])
    file_o.close()
    return set1,set2,set3,set4
set1, set2, set3, set4 = get_set()

def get_cause(cause_name):
    for set_4 in set4:
        if cause_name in set_4 or set_4 in cause_name:
            return set_4
    for set_3 in set3:
        if cause_name in set_3 or set_3 in cause_name:
            return set_3
    for set_2 in set2:
        if cause_name in set_2 or set_2 in cause_name:
            return set_2
    for set_1 in set1:
        if cause_name in set_1 or set_1 in cause_name:
            return set_1
    return cause_name

def write_result(open_dir, write_path, names):
    file_write = open(write_path, 'w', encoding='utf8')
    k=1
    for file_name in names:
        file_open = open('{}{}'.format(open_dir, file_name), 'r', encoding='utf8')
        for count_line in file_open.readlines():
            lines = count_line.split('|')
            fields = split_pat.split(htmlRemovePat.sub('',lines[1].strip()))
            if len(fields)<3:
                file_write.write(lines[0]+'||\n')
                continue
            split_word = ''
            party_line = ''
            for i in range(0, len(fields) - 1):
                # 移除括号内的内容
                remove_parent = re.sub(r"[\(（].*?[\)）]", "", fields[i])
                result = parties_pat.findall(remove_parent)
                if len(result) > 0 and '一案' not in fields[i]:
                    party_type = parties_split_pat.findall(remove_parent)[0]
                    # 当事人切分
                    split_move = parties_split_pat.split(remove_parent)
                    # 取得当事人，长度大于2，过滤掉（原告母，原告之父此类）
                    if len(split_move[1]) > 2:
                        name = clean_party_pat.sub('', split_move[1].split('，')[0])
                        if '(' in name:
                            name = name[:name.index('(')]
                        if len(name) > 20 and '分公司' not in name and '支行' not in name:
                            name = name.split('公司')[0] + '公司'
                        split_word = split_word + '|' + name
                    if name.endswith('户') and len(name) > 2:
                        name = name.replace('户', '')
                    if ',' in name :
                        name = name.split(',')[0]
                    #有的会多余显示被告人张三、李四、王五共同上诉（在前面已经显示完成的情况下）
                    #有的会显示被告人：共同委托代理人XXX
                    if '、' in name or '委托' in name or '诉讼' in name or '代理人' in name or '��' in name or 'Ｘ' in name or '职工' in name or len(name)>30:
                        continue
                    party_line = party_line + ',' + party_type + '-' + name
                if '一案' in fields[i]:
                    try:
                        split_word_pat = re.compile(r'{}'.format(split_word[1:]))
                        cause = cause_pat.findall(remove_parent)
                        if len(cause) == 0 or '姓名或名称' in fields[i] :
                            cause_name = ''
                        else:
                            cause_name = split_word_pat.split(cause[0])[-1]
                            cause_name = cause_name[1:] if (cause_name.startswith('为') and cause_name.endswith('纠纷')) else cause_name
                            cause_name = get_cause(cause_name) if '��' not in cause_name else ''
                    except:
                        if len(party_line)>2:
                            file_write.write(lines[0]+'||'+party_line[1:]+'\n')
                        else:
                            file_write.write(lines[0] + '||\n')
                        break
                    file_write.write(lines[0]+'|'+cause_name+'|'+party_line[1:]+'\n')
                    break
        file_open.close()
        logging.info('第{}个文件{}执行完毕了'.format(k,file_name))
        k = k+1
    file_write.close()

def list_name(open_dir):
    return os.listdir(open_dir)

def run(open_dir, write_path):
    names = list_name(open_dir)
    write_result(open_dir, write_path, names)

if __name__ == '__main__':
    open_dir = '/mnt/disk2/data/minshi/organ_data/'
    write_path = '/mnt/disk2/data/minshi/cause_party/cause_party_case'
    # open_dir = 'D:\\cause_data\\organ_data\\'
    # write_path = 'D:\\cause_data\\cause_party\\cause_party_case'
    run(open_dir, write_path)