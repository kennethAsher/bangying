# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/16 上午10:37
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 
'''

import re

#判断案由
#使用与会报错：本院在审理原告浙江××农村合作银行××星××行诉被告王甲、王乙金融借款合同纠纷一案中
cause_pat = re.compile(r'(.*?)一案')
#分行mainbody的正则
split_pat = re.compile(r'。|\n')
#匹配到当事人
parties_pat = re.compile(r'((原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人'
                         r'|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人)([\(（].*?[\)）])?)[:：]?(.*)')
#切分当事人
parties_split_pat = re.compile(r'原审原告|原审被告|原告人|被告人|原告|被告|被上诉人|上诉人|原审第三人|第三人|被申诉人|申诉人'
                               r'|再审申请人|申请再审人|被申请人|申请人|申请执行人|被执行人|被异议人|异议人|起诉人|申报人')
file_open = open('/Users/by-webqianduan/data/cause/write_mainbody','r', encoding='utf8')
# file_write = open('', 'w', encoding='utf8')
for count_line in file_open.readlines():
    lines = count_line.split('\t')
    fields = split_pat.split(lines[1].strip())
    if len(fields) < 5:
        continue
    split_word = ''
    party_line = ''
    for i in range(0,len(fields)-1):
        result = parties_pat.findall(fields[i])
        if len(result) > 0 and '一案' not in fields[i]:
            #移除括号内的内容
            remove_parent = re.sub(r"[\(（].*?[\)）]", "", fields[i])
            #获取当事人类型
            party_type = parties_split_pat.findall(remove_parent)[0]
            # print(party_type[0])
            # 当事人切分
            split_move = parties_split_pat.split(remove_parent)
            #取得当事人，长度大于2，过滤掉（原告母，原告之父此类）
            if len(split_move[1])>2:
                name = split_move[1].split('，')[0].replace('：','')
                split_word = split_word + '|' + name
            #输出当事人
            # print(party_type+'-'+name)
            party_line = party_line +','+ party_type+'-'+name

        if '一案' in fields[i]:
            cause_line = remove_parent = re.sub(r"[\(（].*?[\)）]", "", fields[i])
            # print(split_word[1:])
            split_word_pat = re.compile(r'{}'.format(split_word[1:]))
            cause = cause_pat.findall(cause_line)
            #输出案由
            # print(split_word_pat.split(cause[0])[-1])
            #写出到文件
            # file_write.write(lines[0].strip()+'|'+party_line[1:]+'|'+cause)
            break

# result = cause_pat.findall(line)
