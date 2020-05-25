"""
@author : kennethAsher
@fole   : JudgeUpdateInfo.py
@ctime  : 2020/4/24 14:37
@Email  : 1131771202@qq.com
@content: 已经分离出来的升级的人员具体的数量
"""

mapping_upgrade = set()
mapping_upgrate_end = set()
file_open = open('D:\\judge_data\\judge_info\\judge_info', 'r', encoding='utf8')
file_open_upgrade = open('D:\\judge_data\\judge_merge\\judge_upgrade\\judge_upgrade', 'r', encoding='utf8')
file_write_info = open('D:\\judge_data\\judge_info\\judge_info_out', 'w', encoding='utf8')
file_write_upgrade = open('D:\\judge_data\\judge_info\\judge_info_upgrade', 'w', encoding='utf8')
file_write_upgrade_end = open('D:\\judge_data\\judge_info\\judge_info_upgrade_end', 'w', encoding='utf8')
k = 0
for line in file_open_upgrade.readlines():
    fields = line.strip().split('---')
    words_upgrade = fields[0].split('|')
    words_upgrade_end = fields[1].split('|')
    key_upgrade = words_upgrade[0]+'|'+words_upgrade[1]
    key_upgrade_end = words_upgrade_end[0]+'|'+words_upgrade_end[1]
    mapping_upgrade.add(key_upgrade)
    mapping_upgrate_end.add(key_upgrade_end)
    k = k+1
print(k)
print(len(mapping_upgrade))
print(len(mapping_upgrate_end))
for line in file_open.readlines():
    fields = line.strip().split('|')
    key = fields[0]+'|'+fields[1]
    flag = 0
    if key in mapping_upgrade:
        file_write_upgrade.write(line)
        flag = 1
    if key in mapping_upgrate_end:
        file_write_upgrade_end.write(line)
        flag = 1
    if flag == 0:
        file_write_info.write(line)


