"""
@author : kennethAsher
@fole   : JudgeInfoResult.py
@ctime  : 2020/4/22 19:22
@Email  : 1131771202@qq.com
@content:
        上面承接数据清洗好的审判人员数据：judge_info_out；和数据库中原本存放的数据：pg_user_judge_20200427.txt
        将已经整理好的审判人员文档，与原本数据库中存在的审判人员文档合并，相同的追加id，没有相同的需要追加id
        输出已经加上id的数据：judge_info_result
"""

id_open = open('D:\\judge_data\\mysql_data\\pg_user_judge_20200427.txt', 'r', encoding='utf8')
file_open = open('D:\\judge_data\\judge_info\\judge_info_out', 'r', encoding='utf8')
file_write = open('D:\\judge_data\\judge_info\\judge_info_result', 'w', encoding='utf8')

id = 11693932

mapping = {}
out_id = ''
for line in id_open.readlines():
    fields = line.strip().split('|')
    key = fields[2]+'-'+fields[1]
    mapping[key] = fields[0]
for line in file_open.readlines():
    fields = line.strip().split('|')
    if len(fields) < 5:
        continue
    key = fields[0]+'-'+fields[1]
    if key in mapping:
        out_id = mapping[key]
    else:
        out_id = str(id)
        id += 1
    file_write.write(out_id +'|'+ line)