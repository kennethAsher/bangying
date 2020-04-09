"""
@author: kennethAsher
@fole  : jueties.py
@ctime : 2019/12/30 17:25
@Email : 1131771202@qq.com
"""

import re


lawyerSpcWordClearPat = re.compile(r'(.*代理[人]?)|(.*辩护[人]?)|([\(（].*?[\)）])|(律师)$|^(代理)')
lawyer_accuser_pat = r'委托诉?讼?(代理人|辩护人|代理|辩护)[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'
docSplitPat = re.compile(r'\.|。|\n')
lawyerFilterPat = re.compile(
            r'(.*(事务所|执业证号|援助|法律|中心|公司|一般代理|代理权限|一般授权|特别授权|特别代理|工作单位|专职律师|委托|代理|辩护|上诉|代表|第三人).*)|(^上[述列].*)|(^[该系].*)')
nameGeneralClearPat = re.compile(
            r'(&.{1,7};)|([\(（].*?[\)）])|(<.*?>)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零].*)|�|\+|-|\?|？|([a-zA-Z])|\"|\'|`|、|：|∶|:|;|；|=|［|］|（|）|/|_|／|<|﹤|>|﹥|&|＊|\*|\s|\d|#|○|Ｘ|×|某|丨')
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
                        r'|执行员'
                        r'|人[民员]陪[审判]员?|陪[审判]员?|代理陪[审判]员?'
                        r'|书记[员]?|代理书记[员]?|代书记[员]?|实习书记[员]?|见习书记[员]?)[:：]?')  # 员字可能没有

                         # '|书记员|代理书记员|代书记员|实习书记员|见习书记员)[:：]?')     #首次清洗忽略书记员
clearDatePat = re.compile(
    r'(申请执行.*?年)|(逾期不予执行)|((本|此).*?(与|和)原.*?核对无异)|(无异)|([ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零一二三四五六七八九十×xX\d]{1,4}年.*)'
    r'|((一九)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零]).{1,4}年.*)|([一二三四五六七八九十xX\d]{1,2}月[廿一二三四五六七八九十xX\d]{1,3}日)'
    r'|0霞住新乐市新小区西单元|文书日期')

file_open = open("D:\\lawyer\\lawyers_data\\part_01.txt", 'r', encoding='utf-8')
file_out = open("D:\\part_00_out1.txt", 'w', encoding='utf-8')
k =1
for line in file_open.readlines():
    judges =""
    friends = ""
    opponents = ""
    k = k + 1
    if k % 10000 == 0:
        print(k)
    if '\\N' in line:
        continue
    fields = line.split('\t')
    if len(fields[0]) < 3:
        fields[0] = fields[0] + "案件"
    lines = list(filter(None, docSplitPat.split(fields[1])))
    if len(lines) < 3:
        continue
    line = re.sub(r'\s|\\|([\(（].*?[\)）])|(\{.*?\})|([\[【].*?[\]】])|\?|？', '', lines[-1])
    # print(line)
    line = re.sub(r'&middot;', '·', line)
    # matchResult = justicePatterns.match(line)
    if ('独任' in line) or ('批示' in line):
        continue
    juticesList = juticesPat.split(line)
    # print(juticesList)
    index = 1
    # 前面判断过匹配 审判人员，所以结果最少三个，如果存在index 1，就肯定会有2，有3肯定会有4以此类推
    while index < len(juticesList):
        judgeName = juticesList[index]
        if len(judgeName) > 5:  # 为了避免很多没必要的正则匹配。所以名字如果大于5才进行正则判断 ， 因为最不讲究的也得写个 “张三一月一日” 吧。。。。
            judgeName = clearDatePat.sub('', judgeName)
        judgeName = nameGeneralClearPat.sub('', judgeName)
        if len(judgeName) > 0:  # 处理完如果名字时是空的就丢掉吧
            # 有几十个sb写成这种格式“人民人民审判员  罗安树”名字长度大于3防止真有人叫x人民的 14f47031-9390-47a3-a512-a9ac00f79c98
            if len(judgeName) > 3:
                judgeName = re.sub('(人民|执行|见习|无误)$', '', judgeName)
        if len(judgeName) < 4:
            if juticesPat.match(judgeName) is not None:
                judges += judgeName + "-"
            else:
                judges += judgeName + ","
            # print(s)
        index += 1
    file_out.write(judges + '\n')