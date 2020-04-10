# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/2 下午5:26
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 在裁判文书中清洗律师和审判人员
律师会出现一种情况，在裁判文书中委托代理人并不是律师，是公司员工或者是**服务中心等等，
由于到处的时候将换行符都替换成了'。'
导致切分橘子的时候出现问题，下次再抽取的时候请务必将其替换成'，'
'''

import re

lawyerSpcWordClearPat = re.compile(r'(.*代理[人]?)|(.*辩护[人]?)|([\(（].*?[\)）])|(律师)$|^(代理)')
lawyer_accuser_pat = r'.*委托诉?讼?(代理人|辩护人|代理|辩护)[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'
docSplitPat = re.compile(r'。')
lawyerFilterPat = re.compile(
            r'(.*(事务所|执业证号|援助|法律|中心|公司|一般代理|代理权限|一般授权|特别授权|特别代理|工作单位|专职律师|委托|代理|辩护|上诉|代表|第三人).*)|(^上[述列].*)|(^[该系].*)')
nameGeneralClearPat = re.compile(
            r'(&.{1,7};)|([\(（].*?[\)）])|(<.*?>)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零].*)|�|\+|-|\?|？|([a-zA-Z])|\"|\'|`|、|：|∶|:|;|；|=|［|］|（|）|/|_|／|<|﹤|>|﹥|&|＊|\*|\s|\d|#|○|Ｘ|×|某|丨|被告|原告|统一社会信用代码')
justicePatterns = re.compile(r'^((代理)?审判长)[:：]?(.*)'
                               r'|^((保持队形)?院长)[:：]?(.*)'
                               r'|^((代|代理|助[理]?|人民)?审[判理]?员)[:：]?(.*)'
                               r'|^((代|代理|见习|实习)?书记员)[:：]?(.*)'
                               r'|^((保持队形)?法官助理)[:：]?(.*)'
                               r'|^((保持队形)?执行员)[:：]?(.*)'
                               r'^((人[民员]|代理)?陪[审判]员?)[:：]?(.*)')

juticesPat = re.compile(r'(院长'
                        r'|审判长'
                        r'|审[判理]员|代审[判理]员|代理审[判理]员|助理审[判理]员|人民审[判理]员|助审员'
                        r'|法官助理'
                        r'|执行员|书记员'
                        r'|人[民员]陪[审判]员?|陪[审判]员?|代理陪[审判]员?)[:：]?')  # 员字可能没有

#匹配是否碰到对手
opponents_pat = re.compile(r'被告[人]?|被上诉|被|原审被告|被申请[人]?|被执行[人]?|被异议[人]?|罪犯')

                         # '|书记员|代理书记员|代书记员|实习书记员|见习书记员)[:：]?')     #首次清洗忽略书记员
clearDatePat = re.compile(
    r'(申请执行.*?年)|(逾期不予执行)|((本|此).*?(与|和)原.*?核对无异)|(无异)|([ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零一二三四五六七八九十×xX\d]{1,4}年.*)'
    r'|((一九)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零]).{1,4}年.*)|([一二三四五六七八九十xX\d]{1,2}月[廿一二三四五六七八九十xX\d]{1,3}日)'
    r'|0霞住新乐市新小区西单元|文书日期')

htmlRemovePat = re.compile('>(.*?)<')
#清洗律师事务所开头为系，均系，为等
organ_split_pat = re.compile(r'系|均系|为')

lines = '维持原判。。。二审案件受理费8950元，由江西建工第二建筑有限责任公司负担，，，本判决为终审判决，，，审判长　　王维登，，审判员　　程　鹰，，审判员　　陈红卫，，，，二〇一七年八月二十四日，，书记员　　朱丹'

def get_judges(judge_types, judges):
    fields_type = judge_types.split(',')
    fields_judge = judges.split(',')
    type_judge = ''
    flag = len(fields_judge) if len(fields_judge) < len(fields_type) else len(fields_type)
    for i in range(flag):
        type_judge = type_judge + ',' + fields_type[i] + '-' + fields_judge[i]
    return type_judge[1:]

lines = docSplitPat.split(lines)
judges=''
for line in reversed(lines):
    line = line.strip()
    if juticesPat.findall(line) is not None:
        line = re.sub(r'\s|\\|([\(（].*?[\)）])|(\{.*?\})|([\[【].*?[\]】])|\?|？|　', '', line)
        line = re.sub(r'&middot;', '·', line)
        if ('独任' in line) or ('批示' in line):
            continue
        juticesList = juticesPat.split(line)
        index = 2
        judge_types = ','.join(juticesPat.findall(line))
        # 前面判断过匹配 审判人员，所以结果最少三个，如果存在index 1，就肯定会有2，有3肯定会有4以此类推
        while index < len(juticesList):
            judgeName = juticesList[index]
            if len(judgeName) > 5:  # 为了避免很多没必要的正则匹配。所以名字如果大于5才进行正则判断 ， 因为最不讲究的也得写个 “张三一月一日” 吧。。。。
                judgeName = clearDatePat.sub('', judgeName)
            judgeName = nameGeneralClearPat.sub('', judgeName)
            if len(judgeName) > 0:  # 处理完如果名字时是空的就丢掉吧
                # 有几十个sb写成这种格式“人民人民审判员  罗安树”名字长度大于3防止真有人叫x人民的 14f47031-9390-47a3-a512-a9ac00f79c98
                if len(judgeName) > 3:
                    if '附' == judgeName[3]:
                        judgeName = judgeName.split('附')[0]
                    judgeName = re.sub('(人民|执行|见习|无误)$', '', judgeName)
                if len(judgeName) > 2:
                    if '附' == judgeName[2]:
                        judgeName = judgeName.split('附')[0]
            if len(judgeName) < 4:
                judges += judgeName + ","
            index += 2
        if len(judge_types) < 2:
            continue
        type_judge = get_judges(judge_types, judges[:-1])
        break


print(type_judge)