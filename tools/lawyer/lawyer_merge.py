"""
@author: kennethAsher
@fole  : lawyer_merge.py
@ctime : 2019/12/26 10:46
@Email : 1131771202@qq.com
"""

import os

dir_input = 'D:\\lawyer\\lawyer_add_province\\'
file_out = open('D:\\lawyer\\lawyer_merge\\lawyer_merge.txt', 'w', encoding='utf8')
dirs = os.listdir(dir_input)
for dir in dirs:
    file_in = open(dir_input+dir, 'r', encoding='utf8')
    for line in file_in.readlines():
        if line == "":
            continue
        file_out.write(line)
    file_in.close()
file_out.close()