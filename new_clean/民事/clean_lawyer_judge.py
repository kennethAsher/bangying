# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/9 1:10 下午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 在民事案件中清洗出律师，律所，审判人员以及合作律师对售后律师
'''


import re
import os
import logging

logging.basicConfig(filename='/Users/by-webqianduan/OneDrive/pycharm/bangying/log/clean_oc/民事/clean_lawyer_judge.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

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

def get_judges(judge_types, judges):
    fields_type = judge_types.split(',')
    fields_judge = judges.split(',')
    type_judge = ''
    flag = len(fields_judge) if len(fields_judge) < len(fields_type) else len(fields_type)
    for i in range(flag):
        # if len(fields_judge[i])<2:
        #     continue
        type_judge = type_judge + ',' + fields_type[i] + '-' + fields_judge[i]
    return type_judge[1:]

def get_names(path):
    return os.listdir(path)

def write_lawyer_judge(open_dir, write_dir, names):
    file_write = open(write_dir, 'w', encoding='utf8')
    for step, name in enumerate(names):
        logging.info('执行第{}个文件{}'.format(step, name))
        file_open = open('{}{}'.format(open_dir,name), 'r', encoding='utf8')
        for line in file_open.readlines():
            line = htmlRemovePat.sub('', line)
            judges = ''
            type_judge = ''
            doc_num = line.split('|')[0]
            lines = docSplitPat.split(line)
            # 清洗审判人员
            i=0
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
                    if len(judge_types)<2:
                        continue
                    type_judge = get_judges(judge_types,judges[:-1])
                    break
            # 清洗律师
            name_list = []
            friends = ""
            oppnent = ""
            flag = 0
            for line in lines:
                if '一案' in line:
                    if len(name_list) == 0:
                        if '-' in type_judge:
                            file_write.write(doc_num+'|||'+type_judge+"||\n")
                        else:
                            file_write.write(doc_num + '|||||\n')
                    break
                line = re.sub(r'\s|\\', '', line)
                if opponents_pat.match(line) is not None:
                    flag = 1
                matchResut = re.match(lawyer_accuser_pat, line)
                if matchResut is not None:
                    lawyerStr = re.sub(r'[\(（].*?[\)）]', '', matchResut.group(0))
                    lawyers = list(filter(None, re.split(r'\,|，|、|;|；|：|：|:', lawyerStr)))
                    if len(lawyers) == 0:
                        break
                    # lawyers[-1] = re.sub(r'(分别|均|都)?(系|为|是)|(律师)?(及|和|、)?(实习|助理|执业|兼职|专职|职业|指派|指定)?律师$|法律工作者$|执行$|专职$|(.*(援助|服务|中心|指定).*)|(.*(X|M|H|Ｘ|×|x|m).*)|省|市', '', lawyers[-1])
                    lawyers[-1] = re.sub(
                        r'执行$|(律师)?专职$|律师$|(.*(援助|服务|中心|法律工作者|实习|助理|执业|兼职|职业|指派|指定|某).*)|(.*(X|M|H|Ｘ|×|x|m).*)|省|市', '',
                        lawyers[-1])
                    lawyers[-1] = re.sub(r'律师事务$|律师律事务$', '律师事务所', lawyers[-1])
                    if ('律师事务所' not in lawyers[-1]) or (len(lawyers[-1]) < 3) or ('事务' in lawyers[0]):
                        break
                    if len(lawyers) > 1:
                        for x in lawyers[0:-1]:
                            if x == '男' or x == '女':
                                continue
                            if re.match(r'.*[1-9].*', x) is not None or re.match(r'.*年.*月.*日.*', x) is not None:
                                continue
                            lawyerName = x.split('人')[-1]
                            #有的文书总存在将律师的名字写为地区名，有的以群众、文化程度来命名，有的使用甲，乙来命名
                            if (lawyerName.endswith('省') or ('省' in lawyerName and len(lawyerName)>3)) \
                                    or (lawyerName.endswith('市') or ('市' in lawyerName and len(lawyerName)>3))\
                                    or (lawyerName.endswith('县') or ('县' in lawyerName and len(lawyerName)>3))\
                                    or (lawyerName.endswith('区') or ('区' in lawyerName and len(lawyerName)>3))\
                                    or '身份' in lawyerName or lawyerName.endswith('族') or lawyerName.endswith('群众')\
                                    or lawyerName.endswith('文化') or lawyerName.startswith('男') or lawyerName.startswith('女')\
                                    or '联系' in lawyerName or '电话' in lawyerName:
                                continue
                            if len(lawyerName) > 3:
                                if lawyerFilterPat.match(lawyerName) is not None:
                                    lawyerName = lawyerFilterPat.sub('', lawyerName)
                            lawyerName = nameGeneralClearPat.sub('', lawyerName)
                            if lawyers[-1].endswith('分所'):
                                lawyers[-1] = lawyers[-1].split('律师事务所')[0]+'律师事务所'
                            if lawyers[-1].startswith('系') or lawyers[-1].startswith('均系') or lawyers[-1].startswith('为'):
                                lawyers[-1] = organ_split_pat.split(lawyers[-1])[-1]
                            if len(lawyerName) > 1 and len(lawyers[-1]) > 5:
                                if lawyerName in name_list:
                                    continue
                                if flag == 0:
                                    friends = friends+','+lawyerName+'-'+lawyers[-1]
                                if flag == 1:
                                    oppnent = oppnent+','+lawyerName+'-'+lawyers[-1]
                                name_list.append(lawyerName)
            if len(friends) > 0: friends = friends[1:].split(',')
            if len(oppnent) > 0: oppnent = oppnent[1:].split(',')
            if len(friends) > 0:
                for friend in friends:
                    temp_friends = friends.copy()
                    del temp_friends[temp_friends.index(friend)]
                    file_write.write(
                        doc_num + '|' + friend.split('-')[0] + '|' + friend.split('-')[
                            -1] + '|' + type_judge + '|' + ','.join(
                            temp_friends) + '|' + ','.join(oppnent) + '\n')
            if len(oppnent) > 0:
                for oppo in oppnent:
                    temp_oppnent = oppnent.copy()
                    del temp_oppnent[temp_oppnent.index(oppo)]
                    file_write.write(
                        doc_num + '|' + oppo.split('-')[0] + '|' + oppo.split('-')[-1] + '|' + type_judge + '|' + ','.join(
                            temp_oppnent) +'|' + ','.join(friends) + '\n')

        file_open.close()
        logging.info('执行第{}个文件{}结束'.format(step, name))
    file_write.close()
    logging.info('全部文件执行完成')


def run(open_dir, write_dir):
    names = get_names(open_dir)
    write_lawyer_judge(open_dir, write_dir, names)


if __name__ == '__main__':
    open_dir = '/Users/by-webqianduan/data/organ_data/'
    file_write = '/Users/by-webqianduan/data/lawyer_judge/lawyer_data'
    run(open_dir, file_write)