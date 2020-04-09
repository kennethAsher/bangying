#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
@brief :
@author: kennethAsher
@content  : 清洗裁判文书
@ctime : Tue Dec 17 16:56:33 CST 2019
"""


import re
from pyspark.sql import SparkSession
import json
from pyspark.sql.types import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 个人信息
class Lawyer(object):

    def __init__(self, name, office):
        # 律师姓名
        self.name = name
        # 律所
        self.office = office

    def __str__(self):
        return '{{"name":"{}","office":"{}"}}'.format(self.name, self.office)


# 审判人员信息
class Jutice(object):
    def __init__(self, name, status, statusCode):
        self.name = name
        self.status = status
        self.statusCode = statusCode

    def __str__(self):
        return '{{"name":"{}","status":"{}","statusCode":"{}"}}'.format(self.name, self.status, self.statusCode)

class Party(object):
    """
    """

    def __init__(self):
        # 当事人名称
        self.name = ""
        # 当事人诉讼地位
        self.status = ""
        # 当事人诉讼地位编码
        self.statusCode = ""
        # 公司 or 个人
        self.isCompany = False;
        # 委托带了人
        self.lawyer = []

    def __str__(self):
        # json 里boolean 应该是 true or false，而python 是True False
        return '{{"name":"{}","status":"{}","statusCode":"{}","isCompany":{},"lawyer":[{}]}}'. \
            format(self.name, self.status, self.statusCode, str(self.isCompany).lower(),
                   ",".join([str(x) for x in self.lawyer]))

class LawsuitParser(object):
    def __init__(self):
        # 民事案件当事人身份 ,认定1肯定是先于2出现的，如果已经出现2了，再出现的1就是无效，用户解析正文
        self.civilStatus = {'原告': ('YG', 1),
                            '被告[人]?': ('BG', 2),
                            '第三人': ('DSR', 2),
                            '上诉人': ('SSR', 1),
                            '被上诉人': ('BSSR', 2),
                            '原审原告': ('YYYG', 2),
                            '原审被告': ('YYBG', 2),
                            '原审第三人': ('YSDSR', 2),
                            '再审申请人': ('ZSSQR', 1),
                            '被申请人': ('BSQR', 2),
                            '申请执行人': ('SQZXR', 1),
                            '被执行人': ('BZXR', 2),
                            '异议人': ('YYR', 1),
                            '被异议人': ('BYYR', 2),
                            '申请人': ('SQR', 1),
                            '起诉人': ('QSR', 1),
                            '申报人': ('SBR', 2)}
        # 刑事案件当事人身份
        self.criminalStatus = {'罪犯': ('ZF', 3),
                               '公诉机关': ('GSJG', 1),
                               '被告人': ('BGR', 2),
                               '原公诉机关': ('YGSJG', 1),
                               '上诉人': ('SSR', 2)}

        # 1.1 如果 r'^委托诉?讼?代理人([\(（].*[\)）])?[:：]?(.*律师)'，匹配的话，那种“xxx律师事务所”后面没有律师的会解错
        # 光写“委托诉讼代理人人 xxx”，多写个人的的就有几百个，都是sb吗 54dcc64c-5287-4154-bdb3-8ddd8dd398fa
        self.civilLawyerExpr = r'^委托诉?讼?代理[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'
        self.criminalLawyerExpr = r'^辩护人[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'

        # 解析审判人员的正则表达式  这块文字中间有可能有中英文的空格和tab,dict的value用来表示是法官还是其他身份
        # 解析之前要把空格 tab啥的都去掉
        # 有些修饰词是没用的。为了保持group以后的格式一致
        self.justicePatterns = [(re.compile(r'^((代理)?审判长)[:：]?(.*)'), 'JUDGE'),
                                (re.compile(r'^((保持队形)?院长)[:：]?(.*)'), 'JUDGE'),
                                (re.compile(r'^((代|代理|助[理]?|人民)?审[判理]?员)[:：]?(.*)'), 'JUDGE'),
                                (re.compile(r'^((代|代理|见习|实习)?书记员)[:：]?(.*)'), 'CLERK'),
                                (re.compile(r'^((保持队形)?法官助理)[:：]?(.*)'), 'ASSISTANT'),
                                (re.compile(r'^((保持队形)?执行员)[:：]?(.*)'), 'EXECUTOR'),
                                (re.compile(r'^((人[民员]|代理)?陪[审判]员?)[:：]?(.*)'), 'JUROR'),  # 有可能没有员
                                ]
        self.juticesPat = re.compile('(院长'
                                     '|审判长'
                                     '|审[判理]员|代审[判理]员|代理审[判理]员|助理审[判理]员|人民审[判理]员|助审员'
                                     '|法官助理'
                                     '|执行员'
                                     '|人[民员]陪[审判]员?|陪[审判]员?|代理陪[审判]员?'  # 员字可能没有
                                     '|书记员|代理书记员|代书记员|实习书记员|见习书记员)[:：]?')

        # 很多年月日跟在审判人员后面，需要把这个时间去掉，还有这句话 ‘本件与原本核对无异’ 还有‘本年与原本核对无异’
        # 发现有很多时间写的不正规，不是XXXX年XX月XX日这种格式。。。。10条里有一条。。。。尝试替换掉
        # 零的写法大概有一万种吧 你妹啊
        # “二О二О一七年三月十七日”，“二О十七年” 操⃝
        # 0霞住新乐市新小区西单元 这个特殊的错误，只能这么搞了。。主要有很多案例都带这个。
        self.clearDatePat = re.compile(
            r'(申请执行.*?年)|(逾期不予执行)|((本|此).*?(与|和)原.*?核对无异)|(无异)|([ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零一二三四五六七八九十×xX\d]{1,4}年.*)'
            r'|((一九)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零]).{1,4}年.*)|([一二三四五六七八九十xX\d]{1,2}月[廿一二三四五六七八九十xX\d]{1,3}日)'
            r'|0霞住新乐市新小区西单元|文书日期')

        # 去除html
        self.htmlRemovePat = re.compile('>(.*?)<')

        # 文书分段
        self.docSplitPat = re.compile(r'\.|。|\n')

        # 用来去除一些特殊字符
        self.spcSigClearPat = re.compile(r'(&.{1,7};)|�')

        # 律师错误名字过滤  ，前提字符多于4个字
        self.lawyerFilterPat = re.compile(
            r'(.*(事务所|执业证号|援助|法律|中心|公司|一般代理|代理权限|一般授权|特别授权|特别代理|工作单位|专职律师).*)|(^上[述列].*)|(^[该系].*)')

        # 修正类错误 “及附带民事诉讼代理人何智勇”
        # 修正 “辩护人辩护人王增林，贵州红连天律师事务所律师” 多个辩护人，这种错居然能一大堆。。e561346b-7630-4c5c-84dd-a84a01742f5d
        self.lawyerSpcWordClearPat = re.compile('(.*代理人)|(.*辩护人)|([\(（].*?[\)）])|(律师)$|^(代理)')

        # 用来去除姓名中的一些特殊字符
        self.nameGeneralClearPat = re.compile(
            r'(&.{1,7};)|([\(（].*?[\)）])|(<.*?>)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零].*)|�|\+|-|\?|？|([a-zA-Z])|\"|\'|`|、|：|∶|:|;|；|=|［|］|（|）|/|_|／|<|﹤|>|﹥|&|＊|\*|\s|\d|#|○')

    def parseParties(self, casetype_name, text):
        # 根据案件类型确定 当事人身份关键词
        result = []
        statusDict = {}
        lawyerExpr = ''
        if casetype_name == '刑事案件':
            statusDict = self.criminalStatus
            lawyerExpr = self.criminalLawyerExpr
        else:
            statusDict = self.civilStatus
            lawyerExpr = self.civilLawyerExpr
        # split出来的结果可能有很多空，用filter去掉
        lines = list(filter(None, self.docSplitPat.split(text)))
        parties = {}
        curParty = ''
        curPrior = 0
        for line in lines:
            if line == '':
                continue
            # 我认为在关键数据行里的tab，空格，\都是没有意义的，替换掉。不然会导致后面生成json报错。不过感觉会有坑。。
            line = re.sub(r'\s|\\', '', line)
            # print("++++++++++++++{}".format(line))
            for status, statusTuple in statusDict.items():

                # 用关键字拼正则表达式  解析当事人
                # 以诉讼地位关键词开头（如果跟被的在一行就会有问题，可是不怎么判断的话由于诉讼地位后面不一定有冒号，所以很容易解析错），
                # [\(（]?.*?[\)）]?诉讼地位后面可能跟着以中英文括号括起来的关键词 比如 原告（反诉原告）
                # [:：]? 后面可能有冒号也可能没有
                # (.*?)。 非贪婪模式匹配出剩下的内容
                # 事实证明基本不可能有一个正则能直接解析这个不规范的数据。。。。

                #匹配被告，被执行人等信息
                patterm = r'^({}([\(（].*?[\)）])?)[:：]?(.*)'.format(status)
                matchResut = re.match(patterm, line)

                if matchResut is not None:
                    # 如果解析到的优先级比当前的低，则说明头已经解析完了
                    if curPrior > statusTuple[1]:
                        return [str(x) for x in parties.values()]
                    # 解析当事人信息
                    party = Party()
                    # 诉讼地位
                    party.status = matchResut.group(1)
                    party.statusCode = statusTuple[0]
                    # SETP2 根据逗号解析当事人信息
                    # 注意这里group(2)是可能有可能无的，举个例子:上诉人（原审被告人）:李三XXXX.
                    # group(1) : 上诉人（原审被告人）
                    # group(2) :（原审被告人）        没有括号的话就是None
                    # group(3) : 李三XXXX
                    splits = re.split('\,|，|;|；|:|：|、', matchResut.group(3))
                    # 当事人名称
                    party.name = self.nameGeneralClearPat.sub('', splits[0])
                    if len(party.name) < 5 or (len(splits) > 1 and (splits[1] == '男' or splits[1] == '女')):
                        party.isCompany = False
                    else:
                        party.isCompany = True

                    curParty = "{}-{}".format(party.name, party.status)
                    # print("---------------{}".format(party))
                    # 防止重名，当事人姓名+诉讼地位作为key
                    parties[curParty] = party
                    # 注意一定要设置优先级
                    curPrior = statusTuple[1]
                    break
                if curParty != '':
                    # print("xxxxxxxxxxxxxxxxxxxxxxxx{}".format(line))
                    matchResut = re.match(lawyerExpr, line)
                    if matchResut is not None:
                        # 干你娘：把括号里的内容都拿掉,我认为括号里的东西都是可有可无的，解决这种问题：委托代理人彭传成（代理权限：特别授权，即代为调查、出庭、诉讼，代为承认、放弃诉讼请求，进行和解，提起反诉、上诉，代收代签法律文书），随县小林法律服务所法律工作者。
                        lawyerStr = re.sub(r'[\(（].*?[\)）]', '', matchResut.group(2))
                        # print("######{}".format(lawyerStr))
                        # 解析出来的结果可能 律师A,律师B，(均系或者系)XXX律所 ，两个律师之间可能是逗号，也可能是顿号，甚至分号
                        lawyers = list(filter(None, re.split(r'\,|，|、|;|；|：|：', lawyerStr)))
                        # filter以后可能是空
                        if len(lawyers) == 0:
                            break
                        # 有个傻比格式是'李玉贤、崔广雄，广东泽森律师事务所律师、实习律师'，这种还很多，根据逗号顿号拆，后面律所就有问题了,想办法解决一下这个
                        while len(lawyers) > 3 and len(lawyers[-1]) <= 5:  # 名字太短肯定不能是律所名称
                            lawyers = lawyers[0:-1]

                        # 如果是“xxx律师事务所律师”这种格式，把最后的律师两个字去掉,把前面的“系”“均系”也去掉
                        # 有个特别烦的“均为广东共阳律师事务所律师及律师助理”
                        lawyers[-1] = re.sub(r'^(分别|均|都)?(系|为|是)|(律师)?(及|和|、)?(实习|助理|执业|兼职|专职|职业|指派|指定)?律师$|法律工作者$', '',
                                             lawyers[-1])
                        # 最后只写律师事务，丢了“所”的。这种记录很多，丢雷楼母
                        lawyers[-1] = re.sub(r'律师事务$', '律师事务所', lawyers[-1])
                        if len(lawyers) > 1:  # 带律所
                            # 最多有两个代理律师，多的话肯定是有格式不规范的，所以这里只取前俩
                            for x in lawyers[0:-1 if len(lawyers) < 4 else 2]:
                                # 尽量过滤一下已知的错误,如果第二个字段是性别
                                if x == '男' or x == '女':
                                    break
                                # 第二个字段是生日 ,居然还有 “X年X月X日出生” 原文就是x年。。不是具体的数值。。。。我tm。。。
                                if re.match(r'.*[1-9].*', x) is not None or re.match(r'.*年.*月.*日.*', x) is not None:
                                    break
                                lawyerName = x
                                # 去除一些修饰词组
                                if len(lawyerName) > 3:
                                    # 很多书写不正规导致的常见错误过滤
                                    if self.lawyerFilterPat.match(lawyerName) is not None:
                                        break
                                    lawyerName = self.lawyerSpcWordClearPat.sub('', lawyerName)

                                lawyerName = self.nameGeneralClearPat.sub('', lawyerName)
                                if lawyerName != '':
                                    lawyer = Lawyer(lawyerName, lawyers[-1])
                                    parties[curParty].lawyer.append(lawyer)

                        else:  # 不带律所
                            lawyerName = lawyers[0]
                            # 去除一些修饰词组
                            if len(lawyerName) > 3:
                                # 很多书写不正规导致的常见错误过滤
                                if self.lawyerFilterPat.match(lawyerName) is not None:
                                    break
                                lawyerName = self.lawyerSpcWordClearPat.sub('', lawyerName)

                            lawyerName = self.nameGeneralClearPat.sub('', lawyerName)
                            if lawyerName != '':
                                lawyer = Lawyer(lawyerName, '')
                                parties[curParty].lawyer.append(lawyer)
                        break

        # hive 针对对象嵌套对象的结构处理有点问题啊 ,只好存储string
        return [str(x) for x in parties.values()]

    # 从后往上解析审判人员信息
    def reverseParseJustices(self, text):
        jutices = []
        lines = self.docSplitPat.split(text)
        # 解析审判人员信息从后往前解比较好
        lines.reverse()
        lines = list(filter(None, lines))  # 空行没有灵魂，去掉
        # 防止乱七八糟的内容，根据规则主审最多三个
        judegeCnt = 0
        # 找到第一条审判人员信息后标记一下，之后最多再往前找8行(空行不算)，可以避免很多正文里解审判人员信息的做错
        firstFound = -1
        for srcLine in lines:
            # 我认为在关键数据行里的tab，空格，\都是没有意义的，替换掉。还有括号里面的内容也都是没用的
            # 这里不能修改原始行的内容
            line = re.sub(r'\s|\\|([\(（].*?[\)）])|(\{.*?\})|([\[【].*?[\]】])|\?|？', '', srcLine)
            # 还得帮神族搞一下 发现有个 “&mi　d　dot;” 要先空格才能替换，220ea956-c3ed-4867-9251-230dd04cfdb8
            line = re.sub(r'&middot;', '·', line)
            # 上面的正则解出来可能有很多空元素
            if line == '':
                continue
            if firstFound > 0:  # 找到第一审判人员后开始计数
                firstFound += 1
            if firstFound > 8:  # 找到第一条审判人员信息后标记一下，之后最多再往前找8行(空行不算)，可以避免很多正文里解审判人员信息的做错 为啥是8呢。。。我就喜欢。
                break
            for (pat, useless) in self.justicePatterns:
                matchResult = pat.match(line)
                if matchResult is not None:
                    # 要把这种数据过滤掉 “审判员　丁志方独任审判。”这句话并不是最后的审判人员信息里的，是正文里的，这中格式很常见 79b50743-0af9-4c10-905e-3f957e118771
                    # 还有很多开头就是 院长 批示的 ec11391f-53e6-40a2-90ab-42461075c1a4
                    if matchResult.group(3) == '':
                        continue
                    if re.match('(.*独任.*)|^批示.*', matchResult.group(3)) is not None:
                        continue
                    # 多个审判人员可能出现在同一行,注意这里split出来的第一个元素肯定是空，因为都是以审判人员开头，前面的肯定是空，
                    juticesList = self.juticesPat.split(line)

                    index = 2
                    # 前面判断过匹配 审判人员，所以结果最少三个，如果存在index 1，就肯定会有2，有3肯定会有4以此类推
                    while index < len(juticesList):
                        judgeName = juticesList[index]
                        if len(judgeName) > 5:  # 为了避免很多没必要的正则匹配。所以名字如果大于5才进行正则判断 ， 因为最不讲究的也得写个 “张三一月一日” 吧。。。。
                            judgeName = self.clearDatePat.sub('', judgeName)
                        judgeName = self.nameGeneralClearPat.sub('', judgeName)

                        if len(judgeName) > 0:  # 处理完如果名字时是空的就丢掉吧
                            # 有几十个sb写成这种格式“人民人民审判员  罗安树”名字长度大于3防止真有人叫x人民的 14f47031-9390-47a3-a512-a9ac00f79c98
                            if len(judgeName) > 3:
                                judgeName = re.sub('(人民|执行|见习|无误)$', '', judgeName)
                            if len(judgeName) < 16:  # 百度说了中文名字目前自多15个字，太长的说明肯定接错了
                                # 这边为了获得statucode，还得重新遍历一次 ，搞成dict？
                                for (pattern, statusCode) in self.justicePatterns:
                                    if pattern.match(juticesList[index - 1]) is not None:
                                        jutice = Jutice(judgeName, juticesList[index - 1], statusCode)
                                        try:
                                            jsonJutice = json.loads(json.dumps(jutice.__dict__))
                                        except:
                                            print("JSONERROR :{}".format(srcLine))
                                        else:
                                            jutices.append(jsonJutice)
                                        if firstFound < 0:
                                            firstFound = 1
                                        if statusCode == 'JUDGE':
                                            judegeCnt += 1
                                        if judegeCnt >= 3:  # 一个case最多三个律师
                                            return jutices
                        index += 2
                    break
        return jutices

    # 根据法院名称分析法院的级别
    def parseCourtLvl(self, courtName):
        # 最高->高级->中级->基层
        if courtName is None:
            return None
        lvlList = ['最高', '高级', '中级']
        for lvl in lvlList:
            if re.match(r'.*{}.*'.format(lvl), courtName) is not None:
                return lvl
        # 默认返回基层
        return '基层'

    #获取律师姓名和律师事务所，不带有律师事务所的律师本次不予考虑
    def getLawyer(self, text):
        lawyer_accuser_pat = r'委托诉?讼?代理[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'
        lawyer_accused_pat = r'^辩护人[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'
        laywer_names = ''
        laywer_statuses = ''

        lines = list(filter(None, self.docSplitPat.split(text)))
        for line in lines:
            if line == '':
                continue
            # 我认为在关键数据行里的tab，空格，\都是没有意义的，替换掉。不然会导致后面生成json报错。不过感觉会有坑。。
            line = re.sub(r'\s|\\', '', line)
            matchResut = re.match(lawyer_accuser_pat, line)
            if matchResut is not None:
                # 干你娘：把括号里的内容都拿掉,我认为括号里的东西都是可有可无的，解决这种问题：委托代理人彭传成（代理权限：特别授权，即代为调查、出庭、诉讼，代为承认、放弃诉讼请求，进行和解，提起反诉、上诉，代收代签法律文书），随县小林法律服务所法律工作者。
                lawyerStr = re.sub(r'[\(（].*?[\)）]', '', matchResut.group(0))

                # 解析出来的结果可能 律师A,律师B，(均系或者系)XXX律所 ，两个律师之间可能是逗号，也可能是顿号，甚至分号
                lawyers = list(filter(None, re.split(r'\,|，|、|;|；|：|：', lawyerStr)))

                # filter以后可能是空
                if len(lawyers) == 0:
                    break

                # 如果是“xxx律师事务所律师”这种格式，把最后的律师两个字去掉,把前面的“系”“均系”也去掉
                # 有个特别烦的“均为广东共阳律师事务所律师及律师助理”
                lawyers[-1] = re.sub(r'^(分别|均|都)?(系|为|是)|(律师)?(及|和|、)?(实习|助理|执业|兼职|专职|职业|指派|指定)?律师$|法律工作者$', '', lawyers[-1])

                # 最后只写律师事务，丢了“所”的。这种记录很多，丢雷楼母
                lawyers[-1] = re.sub(r'律师事务$', '律师事务所', lawyers[-1])

                if len(lawyers) > 1:  # 带律所
                    # 最多有两个代理律师，多的话肯定是有格式不规范的，所以这里只取前俩
                    for x in lawyers[0:-1 if len(lawyers) < 4 else 2]:
                        # 尽量过滤一下已知的错误,如果第二个字段是性别
                        if x == '男' or x == '女':
                            break
                        # 第二个字段是生日 ,居然还有 “X年X月X日出生” 原文就是x年。。不是具体的数值。。。。我tm。。。
                        if re.match(r'.*[1-9].*', x) is not None or re.match(r'.*年.*月.*日.*', x) is not None:
                            break
                        lawyerName = x
                        # 去除一些修饰词组
                        if len(lawyerName) > 3:
                            # 很多书写不正规导致的常见错误过滤
                            if self.lawyerFilterPat.match(lawyerName) is not None:
                                break
                            lawyerName = self.lawyerSpcWordClearPat.sub('', lawyerName)

                        lawyerName = self.nameGeneralClearPat.sub('', lawyerName)
                        if lawyerName != '':
                            laywer_names = laywer_names + lawyerName + ','
                            laywer_statuses = laywer_statuses + lawyers[-1] + ','
                return laywer_names[:-1], laywer_statuses[:-1]

            matchResut = re.match(lawyer_accuser_pat, line)
            if matchResut is not None:
                # 干你娘：把括号里的内容都拿掉,我认为括号里的东西都是可有可无的，解决这种问题：委托代理人彭传成（代理权限：特别授权，即代为调查、出庭、诉讼，代为承认、放弃诉讼请求，进行和解，提起反诉、上诉，代收代签法律文书），随县小林法律服务所法律工作者。
                lawyerStr = re.sub(r'[\(（].*?[\)）]', '', matchResut.group(0))

                # 解析出来的结果可能 律师A,律师B，(均系或者系)XXX律所 ，两个律师之间可能是逗号，也可能是顿号，甚至分号
                lawyers = list(filter(None, re.split(r'\,|，|、|;|；|：|：', lawyerStr)))

                # filter以后可能是空
                if len(lawyers) == 0:
                    break

                # 如果是“xxx律师事务所律师”这种格式，把最后的律师两个字去掉,把前面的“系”“均系”也去掉
                # 有个特别烦的“均为广东共阳律师事务所律师及律师助理”
                lawyers[-1] = re.sub(r'^(分别|均|都)?(系|为|是)|(律师)?(及|和|、)?(实习|助理|执业|兼职|专职|职业|指派|指定)?律师$|法律工作者$', '',
                                     lawyers[-1])

                # 最后只写律师事务，丢了“所”的。这种记录很多，丢雷楼母
                lawyers[-1] = re.sub(r'律师事务$', '律师事务所', lawyers[-1])

                if len(lawyers) > 1:  # 带律所
                    # 最多有两个代理律师，多的话肯定是有格式不规范的，所以这里只取前俩
                    for x in lawyers[0:-1 if len(lawyers) < 4 else 2]:
                        # 尽量过滤一下已知的错误,如果第二个字段是性别
                        if x == '男' or x == '女':
                            break
                        # 第二个字段是生日 ,居然还有 “X年X月X日出生” 原文就是x年。。不是具体的数值。。。。我tm。。。
                        if re.match(r'.*[1-9].*', x) is not None or re.match(r'.*年.*月.*日.*', x) is not None:
                            break
                        lawyerName = x
                        # 去除一些修饰词组
                        if len(lawyerName) > 3:
                            # 很多书写不正规导致的常见错误过滤
                            if self.lawyerFilterPat.match(lawyerName) is not None:
                                break
                            lawyerName = self.lawyerSpcWordClearPat.sub('', lawyerName)

                        lawyerName = self.nameGeneralClearPat.sub('', lawyerName)
                        if lawyerName != '':
                            laywer_names = laywer_names + lawyerName + ','
                            laywer_statuses = laywer_statuses + lawyers[-1] + ','
                return laywer_names[:-1], laywer_statuses[:-1]

            return '',''




    def parseLawsuit(self, dataFrame):
        parties = []
        justices = []
        flag = 0
        # # mainbody without html
        # text = ''
        # if dataFrame.mainbody is not None:
        #     # 直接通过这个htmlRemovePat会出现问题，有的时候不正规的正文会出现<>,如docid =e0f19260-9c17-4a41-a885-a92d00a047b9
        #     # 加个判断div和html,确保是含有html格式的再去替换，但是如果既有html格式，正文还有有意义的<>，那就没办法了
        #     if dataFrame.mainbody.find('<div') > 0 \
        #             or dataFrame.mainbody.find('html') > 0 \
        #             or dataFrame.mainbody.find('font-') > 0 \
        #             or dataFrame.mainbody.find('span>') > 0 \
        #             or dataFrame.mainbody.find('<style') > 0:
        #         text = '\n'.join(self.htmlRemovePat.findall(dataFrame.mainbody))
        #         text = re.sub(r'<br/>', '\n', text)
        #         text = re.sub(r'\n+', '\n', text)
        #         # 神族专用
        #         text = re.sub(r'&middot;', '·', text)
        #     else:
        #
        #         text = dataFrame.mainbody
        # 干掉html转义符,比如 &#12295;  还有一个特殊字符�,
        text = self.spcSigClearPat.sub('', dataFrame.mainbody).encode('utf8')
        # if dataFrame.partyinfo is not None:
        #     # 如果partyinfo不是空，则根据partyinfo去解
        #     parties = self.parseParties(dataFrame.casetype_name, self.spcSigClearPat.sub('', dataFrame.partyinfo))
        #     if len(parties) > 0:
        #         flag = 1
        # 如果partyinfo是空，或者根据partyinfo没有解出来，尝试用mainbody去解一下
        # if flag == 0 and text != '':
        #     parties = self.parseParties(dataFrame.casetype_name, text)
        #     if len(parties) > 0:
        #         flag = 2


        #修改
        if text != "":
            lawyer_name, lawyer_status = self.getLawyer(text)




        # if dataFrame.mainbody is not None:
        #     # 尝试用tail解析一下审判人员信息
        #     justices = self.reverseParseJustices(self.spcSigClearPat.sub('', text))
        #     if len(justices) > 0:
        #         flag += 10
        # 如果 dataFrame.tail是空，后者根据tail解不出审判人员信息，尝试用mainbody去解一下，
        # 这里其实最好能跟前面解partyinfo合一起，这样一次遍历就行，不过逻辑不太好合，先这样吧
        # if flag // 10 == 0 and text != '':
        #     justices = self.reverseParseJustices(text)
        #     if len(justices) > 0:
        #         flag += 20
        # 时间格式各种各样，想办法统一一下
        # trialdate = ''
        # if dataFrame.trialdate is not None:
        #     trialdate = re.sub('[^0-9]', '', dataFrame.trialdate)
        return [dataFrame.casetypename,
                dataFrame.trialdate,
                dataFrame.court_name,
                dataFrame.trialround_name,
                dataFrame.actioncause_name,
                parties,
                justices]

    def display(self):
        for party in self.parties.values():
            print(party)


if __name__ == '__main__':
    parser = LawsuitParser()
    spark = SparkSession \
        .builder \
        .appName("PartyInfoParser") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("spark.debug.maxToStringFields", 1024 * 1024 * 10) \
        .config("spark.sql.parquet.output.committer.class", "org.apache.parquet.hadoop.ParquetOutputCommitter") \
        .enableHiveSupport() \
        .getOrCreate()

    schema = StructType([
        StructField("casetypename", StringType(), True),
        StructField("trialdate", StringType(), True),
        StructField("court_name", StringType(), True),
        StructField("trialround_name", StringType(), True),
        StructField("actioncause_name", StringType(), True),
        StructField("parties", StringType(), True),
        StructField("justices", StringType(), True)
    ])

    test_df = spark.sql("select substr(casetypename,2) as casetypename, mainbody, trialdate, court_name, trialround_name, actioncause_name from judrisk.judrisk_lawsuit_copy")
    # spark = SparkSession.builder.master("spark://emr-header-1:7077").appName("test").getOrCreate()
    testDF = spark.createDataFrame(test_df.rdd.map(lambda x: parser.parseLawsuit(x)), schema=schema)

    testDF.write.mode("overwrite").saveAsTable("judrisk.judrisk_lawsuit_1")

    spark.stop()