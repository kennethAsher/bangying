"""
@author : kennethAsher
@fole   : JudgeMerge.py
@ctime  : 2020/4/24 15:19
@Email  : 1131771202@qq.com
@content: 将已经分离的审判人员进行合并,将得到的upgrede_write_file追加至judge_info即可得到完整的审判人员，
          upgrade_write_file_relation将线索替换成为id，添加到关系库中
"""

relation_open = open('D:\\judge_data\\judge_merge\\judge_upgrade\\judge_upgrade','r',encoding='utf8')
upgrade_open = open('D:\\judge_data\\judge_info\\judge_info_upgrade', 'r', encoding='utf8')
upgrade_open_end = open('D:\\judge_data\\judge_info\\judge_info_upgrade_end', 'r', encoding='utf8')
upgrede_write_file = open('D:\\judge_data\\judge_info\\judge_info_upgrade_file','w', encoding='utf8')
upgrade_write_file_relation = open('D:\\judge_data\\judge_info\\judge_info_upgrade_file_relation','w', encoding='utf8')
mapping_relation = {}
mapping_upgrade = {}
mapping_upgrade_end = {}

# 将映射关系存放至mapping_relation
for line in relation_open.readlines():
    fields = line.strip().split('---')
    words_upgrade = fields[0].split('|')
    words_upgrade_end = fields[1].split('|')
    key = words_upgrade[0] + '-' + words_upgrade[1]
    value = words_upgrade_end[0] + '-' + words_upgrade_end[1]
    mapping_relation[key] = value

# 将升级后的审判人员放置于mapping_upgrade_end表中
for line in upgrade_open_end.readlines():
    fields = line.strip().split('|')
    key = fields[0]+'-'+fields[1]
    mapping_upgrade_end[key] = line.strip()

for line in upgrade_open.readlines():
    fields = line.strip().split('|')
    key = fields[0] + '-' + fields[1]
    values = mapping_upgrade_end[mapping_relation[key]].split('|')
    all_cnt = str(int(fields[5]) + int(values[5]))
    last_cnt = str(int(fields[6]) + int(values[6]))
    set_trail = set()
    for v in fields[7].split('-'):
        set_trail.add(v)
    for v in values[7].split('-'):
        set_trail.add(v)
    trail = '-'.join(set_trail)
    out_line = values[0]+'|'+values[1]+'|'+values[2]+'|'+fields[3]+'|'+values[4]+'|'+all_cnt+'|'+last_cnt+'|'+trail
    out_line_relation = out_line + '|' + fields[0] + '|' + fields[1]
    upgrede_write_file.write(out_line+'\n')
    upgrade_write_file_relation.write(out_line_relation + '\n')
