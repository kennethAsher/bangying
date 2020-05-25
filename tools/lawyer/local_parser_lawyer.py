#-*- coding:utf-8 -*-
"""
@author: kennethAsher
@fole  : local_parser_lawyer.py
@ctime : 2019/12/19 17:07
@Email : 1131771202@qq.com
"""
import re
import os

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
                        r'|人[民员]陪[审判]员?|陪[审判]员?|代理陪[审判]员?)[:：]?')  # 员字可能没有

                         # '|书记员|代理书记员|代书记员|实习书记员|见习书记员)[:：]?')     #首次清洗忽略书记员
clearDatePat = re.compile(
    r'(申请执行.*?年)|(逾期不予执行)|((本|此).*?(与|和)原.*?核对无异)|(无异)|([ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零一二三四五六七八九十×xX\d]{1,4}年.*)'
    r'|((一九)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零]).{1,4}年.*)|([一二三四五六七八九十xX\d]{1,2}月[廿一二三四五六七八九十xX\d]{1,3}日)'
    r'|0霞住新乐市新小区西单元|文书日期')


def parser_lawyer(name):
    file_open = open("D:\\lawyer\\lawyers_data\{}.txt".format(name), 'r', encoding='utf-8')
    file_out = open("D:\\lawyer\\lawyer_out\\{}_out.txt".format(name), 'w', encoding='utf-8')
    k =1

    for line in file_open.readlines():
        judges = ''
        k = k + 1
        if k % 10000 == 0:
            print(k)
        # 处理的是导出的数据
        if '\\N' in line:
            continue
        fields = line.split('\t')
        if len(fields) < 6:
            continue
        if len(fields[0]) < 3:
            fields[0] = fields[0]+"案件"
        lines = list(filter(None, docSplitPat.split(fields[1])))
        if len(lines) < 3:
            continue
        # 清洗审判人员
        line = re.sub(r'\s|\\|([\(（].*?[\)）])|(\{.*?\})|([\[【].*?[\]】])|\?|？', '', lines[-1])
        # print(line)
        line = re.sub(r'&middot;', '·', line)
        # matchResult = justicePatterns.match(line)
        if ('独任' in line) or ('批示' in line):
            continue
        juticesList = juticesPat.split(line)
        # print(juticesList)
        index = 2
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
                judges += judgeName + ","
                # print(s)
            index += 2

        # print(judges)
        # 清洗律师
        for line in lines:
            if line == '':
                continue
            line = re.sub(r'\s|\\', '', line)
            matchResut = re.match(lawyer_accuser_pat, line)
            if matchResut is not None:
                lawyerStr = re.sub(r'[\(（].*?[\)）]', '', matchResut.group(0))
                lawyers = list(filter(None, re.split(r'\,|，|、|;|；|：|：', lawyerStr)))
                if len(lawyers) == 0:
                    break
                # lawyers[-1] = re.sub(r'(分别|均|都)?(系|为|是)|(律师)?(及|和|、)?(实习|助理|执业|兼职|专职|职业|指派|指定)?律师$|法律工作者$|执行$|专职$|(.*(援助|服务|中心|指定).*)|(.*(X|M|H|Ｘ|×|x|m).*)|省|市', '', lawyers[-1])
                lawyers[-1] = re.sub(r'执行$|(律师)?专职$|律师$|(.*(援助|服务|中心|法律工作者|实习|助理|执业|兼职|职业|指派|指定|某).*)|(.*(X|M|H|Ｘ|×|x|m).*)|省|市', '', lawyers[-1])
                lawyers[-1] = re.sub(r'律师事务$|律师律事务$', '律师事务所', lawyers[-1])
                if ('律师事务所' not in lawyers[-1]) or (len(lawyers[-1])<3) or ('事务' in lawyers[0]) :
                    break
                if len(lawyers) > 1:
                    for x in lawyers[0:-1]:
                        if x == '男' or x == '女':
                            break
                        if re.match(r'.*[1-9].*', x) is not None or re.match(r'.*年.*月.*日.*', x) is not None:
                            break
                        lawyerName = x
                        if len(lawyerName) > 3 :
                            if lawyerFilterPat.match(lawyerName) is not None:
                                # print(lawyerName)
                                lawyerName = lawyerFilterPat.sub('', lawyerName)
                                # print(lawyerName)
                        lawyerName = nameGeneralClearPat.sub('', lawyerName)
                            # print(lawyerName)
                        if len(lawyerName) > 1 :
                            file_out.write(fields[0].strip()+'|'+fields[2].strip()+'|'+fields[3].strip()+'|'+fields[4].strip()+'|'+fields[5].strip()+'|'+lawyerName+'|'+lawyers[-1]+ '|' + judges[:-1] +'\n')
    file_open.close()
    file_out.close()

# parser_lawyer('part_00')

data_dir = 'D:\\lawyer\\lawyers_data'

dirs = os.listdir(data_dir)
for dir in dirs:
    parser_lawyer(dir[:-4])




