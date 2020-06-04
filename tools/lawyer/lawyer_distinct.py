# -*- coding:utf-8 -*-
"""
@author: kennethAsher
@fole  : lawyer_distinct.py
@ctime : 2019/12/25 9:57
@Email : 1131771202@qq.com
"""

import os
import re

dir_input = 'D:\\lawyer\\lawyer_out\\'
dir_output = 'D:\\lawyer\\lawyer_disticnt_data\\'
def distince_text(test_name, dir_input, dir_output):
    a=0
    readDir = "{}{}".format(dir_input, test_name)  #old
    writeDir = "{}{}".format(dir_output, test_name) #new
    lines_seen = set()
    outfile = open(writeDir, "w", encoding='utf8')
    f = open(readDir, "r", encoding='utf8')
    for line in f:
        if line not in lines_seen:
            a+=1
            outfile.write(line)
            lines_seen.add(line)
            if a%10000==0:
                print(a)
    outfile.close()
    print("success")

dirs = os.listdir(dir_input)
for dir in dirs:
    distince_text(dir, dir_input, dir_output)