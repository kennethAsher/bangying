"""
@author : kennethAsher
@fole   : JudgeRelationAddId.py
@ctime  : 2020/4/27 16:28
@Email  : 1131771202@qq.com
@content: 上面对接数据judge_info_upgrade_file_relation
        将里面的低级法院对应到高级法院的id
"""

file_open_relation = open('D:\\judge_data\\judge_info\\judge_info_upgrade_file_relation', 'r', encoding='utf8')
file_open = open('D:\\judge_data\\judge_info\\judge_info_result', 'r', encoding='utf8')

file_write = open('D:\\judge_data\\judge_info\\judge_info_upgrade_file_relation_id', 'w', encoding='utf8')

mapping = {}

for line in file_open.readlines():
    fields = line.strip().split('|')
    key = fields[1]+'-'+fields[2]
    value = fields[0]
    mapping[key] = value

for line in file_open_relation.readlines():
    fields = line.strip().split('|')
    key = fields[-2]+'-'+fields[-1]
    value = mapping[key]
    file_write.write(line.strip()+'|'+value+'\n')
file_open_relation.close()
file_open.close()
file_write.close()