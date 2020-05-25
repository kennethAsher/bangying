"""
@author : kennethAsher
@fole   : demo4_help.py
@ctime  : 2020/5/20 14:56
@Email  : 1131771202@qq.com
@content:
"""

import re
clean = re.compile('[\(（].*?[\)）]')

path = r'C:\Users\GG257\Desktop\shenzhenlayer.txt'
file_in = open(path, 'r', encoding='utf8')
set_file = open('pg_lawyer.txt', 'r', encoding='utf8')
file_out_up = open('card_temp', 'w', encoding='utf8')
file_out_in = open('name_temp', 'w', encoding='utf8')
new_file = open('new_temp', 'w', encoding='utf8')

card_set = set()
name_set = set()
for line in set_file.readlines():
    fields = line.strip().split('|')
    try:
        name = fields[0]+'-'+fields[2]
        card = fields[1]
        card_set.add(card)
        name_set.add(name)
    except:
        print(line)

for line in file_in.readlines():
    fields = line.strip().split('|')
    #在这里注意每个地区所处理数据的律所不是在同一个位置
    organ_name_orgin = clean.sub('',fields[4])
    if fields[8] in card_set:
        file_out_up.write(line.strip()+'|'+organ_name_orgin+'\n')
    elif fields[1]+'-'+organ_name_orgin in name_set:
        file_out_in.write(line.strip()+'|'+organ_name_orgin+'\n')
    else:
        new_file.write(line.strip()+'|'+organ_name_orgin+'\n')
