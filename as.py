# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/14 10:00 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 从裁判文书中提取诉讼请求，以及法院的判决结果
'''

#如果没有检测到受理费，则跳过

import re
import jieba

line = '审　判　长　　胡悠悠人民陪审员　　胡芝华人民陪审员　　梅凌霄二〇一九年十一月二十一日代书　记员　　陈亚琪'
justicePatterns = re.compile(r'((代理)?审判长)[:：]?(.*)'
                               r'|((保持队形)?院长)[:：]?(.*)'
                               r'|((代|代理|助[理]?|人民)?审[判理]?员)[:：]?(.*)'
                               r'|((代|代理|见习|实习)?书记员)[:：]?(.*)'
                               r'|((保持队形)?法官助理)[:：]?(.*)'
                               r'|((保持队形)?执行员)[:：]?(.*)'
                               r'|((人[民员]|代理)?陪[审判]员?)[:：]?(.*)')
if justicePatterns.findall(line) is not None:
    print(justicePatterns.findall(line))

