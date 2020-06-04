"""
@author : kennethAsher
@fole   : demo8.py
@ctime  : 2020/4/26 13:31
@Email  : 1131771202@qq.com
@content: 文件去重
"""

file_open = open('D:\\judge_data\\judge_info\\judge_info', 'r', encoding='utf8')
file_write = open('D:\\judge_data\\judge_info\\1', 'w', encoding='utf8')

x = set()

for line in file_open.readlines():
    x.add(line)

for line in x:
    file_write.write(line)