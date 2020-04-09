# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/27 上午9:59
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 清洗court_demo中法院，案号和裁定书结果，统一整理格式

未解决问题：裁定书还有一些格式没有洗清楚---distinct（裁定书）
法院还有一些问题没有洗清楚-------distinct（法院名称）
'''

import re

clean_type_pat = re.compile(r'|h2alig=quot;|ceterquot;|y#ex2YC|&bull;|h2gt;|&#xB;|STRONG|alt|#xA;|&amp;|宋体加黑'
                            r'|void|《|，|厦门市|亅|eqoad||\'|hidde;|&#x;|&#2;|&shy;'
                            r'|||amp;|bsp;|hgt;|lt;|pt;|&gt;\[|（稿）|ሓ'
                            r'|】|=|”|	|）|Z|（| ||、|　|\)||,|\?|＋|》|u|］|\+|﹤|／|P|­|\{|`'
                            r'|H|&|;|%|h|0|7|1|3|8|4|5|6|9|2|\(|n|/|_|×|○|}|·|~|‘|\.|﹥|p|丨|b|’|X|j')
clean_type_split_pat = re.compile(r'日|审|的|：|合同|赔偿|案|纠纷|理|法|年|:|稿纸|发|原稿|征收|庭|第|-|告'
                                  r'|吗|事由|呈签|附带|错误|他|强制|文稿|执行令|监外|居民|看|人民|不用|福'
                                  r'|名称|补正|施罪|查|驾驶|恢复|未按|指定|磅')

#整理裁定书类型
def clean_type(open_dir):
    file_open = open(open_dir, 'r', encoding='utf8')
    l = 0
    k = 0
    for line in file_open.readlines():
        line = clean_type_pat.sub('', line.strip())
        line = clean_type_split_pat.split(line)[-1].replace('裁裁','裁').replace('民事民事','民事')\
            .replace('事裁定','裁定').replace('刑事附带民事刑事','刑事').replace('刑事民事','民事').replace('个人书','书')\
            .replace('刑事附带民事','民事')
        l+=1
        if len(line)==5:
            k+=1
            continue
        print(line)

    print(l)
    print('*'*20)
    print(k)

#整理法院名称
def clean_court(open_dir):
    file_open = open(open_dir, 'r', encoding='utf8')

def run(open_dir):
    # clean_type(open_dir)
    clean_court(open_dir)

if __name__ == '__main__':
    open_dir = '/Users/by-webqianduan/data/court/write_data'
    run(open_dir)