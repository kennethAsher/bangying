#-*- coding:utf-8 -*-
"""
@author: kennethAsher
@fole  : lawyer_friend.py
@ctime : 2019/12/30 15:56
@Email : 1131771202@qq.com
"""
import re



docSplitPat = re.compile(r'\.|。|\n')
lawyer_accuser_pat = r'委托诉?讼?(代理人|辩护人|代理|辩护)[人]?([\(（].*[\)）])?[:：]?(.*律师(事务所)?)'
opponents_pat = re.compile(r'被告[人]?|被上诉|被|原审被告|被申请[人]?|被执行[人]?|被异议[人]?|罪犯')
lawyerFilterPat = re.compile(
            r'(.*(事务所|执业证号|援助|法律|中心|公司|一般代理|代理权限|一般授权|特别授权|特别代理|工作单位|专职律师|委托|代理|辩护|上诉|代表|第三人).*)|(^上[述列].*)|(^[该系].*)')
nameGeneralClearPat = re.compile(
            r'(&.{1,7};)|([\(（].*?[\)）])|(<.*?>)|(二[ｏﾷ◎ㅇоΟО0０Ｏ〇◯○oO零].*)|�|\+|-|\?|？|([a-zA-Z])|\"|\'|`|、|：|∶|:|;|；|=|［|］|（|）|/|_|／|<|﹤|>|﹥|&|＊|\*|\s|\d|#|○|Ｘ|×|某|丨')

file_open = open("D:\\lawyer\\lawyers_data\\part_01.txt", 'r', encoding='utf-8')
file_out = open("D:\\part_00_out.txt", 'w', encoding='utf-8')
k =1
for line in file_open.readlines():
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
    line_num = 1
    flag = 0
    for line in lines:
        if line_num > 20:
            break
        line_num = line_num+1
        if line == '':
            continue
        line = re.sub(r'\s|\\', '', line)
        if opponents_pat.match(line) is not None:
            flag = 1
        matchResut = re.match(lawyer_accuser_pat, line)
        if matchResut is not None:
            lawyerStr = re.sub(r'[\(（].*?[\)）]', '', matchResut.group(0))
            lawyers = list(filter(None, re.split(r'\,|，|、|;|；|：|：', lawyerStr)))
            if len(lawyers) == 0:
                break
            # lawyers[-1] = re.sub(r'(分别|均|都)?(系|为|是)|(律师)?(及|和|、)?(实习|助理|执业|兼职|专职|职业|指派|指定)?律师$|法律工作者$|执行$|专职$|(.*(援助|服务|中心|指定).*)|(.*(X|M|H|Ｘ|×|x|m).*)|省|市', '', lawyers[-1])
            lawyers[-1] = re.sub(r'执行$|(律师)?专职$|(.*(援助|服务|中心|法律工作者|实习|助理|执业|兼职|职业|指派|指定).*)|(.*(X|M|H|Ｘ|×|x|m).*)|省|市','', lawyers[-1])
            lawyers[-1] = re.sub(r'律师事务$|律师律事务$', '律师事务所', lawyers[-1])
            if ('律师事务所' not in lawyers[-1]) or (len(lawyers[-1]) < 3) or ('事务' in lawyers[0]):
                break
            if len(lawyers) > 1:
                for x in lawyers[0:-1]:
                    if x == '男' or x == '女':
                        break
                    if re.match(r'.*[1-9].*', x) is not None or re.match(r'.*年.*月.*日.*', x) is not None:
                        break
                    lawyerName = x
                    if len(lawyerName) > 3:
                        if lawyerFilterPat.match(lawyerName) is not None:
                            # print(lawyerName)
                            lawyerName = lawyerFilterPat.sub('', lawyerName)
                            # print(lawyerName)
                    lawyerName = nameGeneralClearPat.sub('', lawyerName)
                    if len(lawyerName) > 1:
                        if flag == 0:
                            friends += lawyerName+'-'+lawyers[-1] + ','
                        if flag == 1:
                            opponents += lawyerName+'-'+lawyers[-1] + ','
    file_out.write(friends + '|' + opponents + '\n')
file_open.close()
file_out.close()