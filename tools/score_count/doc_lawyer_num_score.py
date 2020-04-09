#!/usr/bin/python3
# -*- coding: utf8 -*-
'''
@Time   : 2020/2/10 1:51 PM 
@Author : kennethAsher
@content: 将清洗好的数据分值进行计算和归类，结果能放在数据库中
'''

import datetime
import re

government_pat = re.compile(r'.*(委|办公室|局|会|办|政协|部|政府|党校|部朝阳大街|信|中心|委银州区|厅|史馆|科学院|科院|事馆)$')

file_case = open('/Users/kenneth-mac/data/lawyer_separate_out/xaf_1', 'r', encoding='utf8')
file_out = open('/Users/kenneth-mac/data/merge_out', 'w', encoding='utf8')

family_names_open = open('/Users/kenneth-mac/data/lawyer_score/family_names.txt', 'r', encoding='utf8')
labels_company_open = open('/Users/kenneth-mac/data/lawyer_score/labels_firm.txt', 'r', encoding='utf8')

#清洗含有（）的客户
def clean_str(word):
    word = word.strip()
    if '（' in word:
        start_index = word.index('（')
        if '）' in word:
            end_index = word.index('）')
            word = word[:start_index]+word[end_index+1:]
        else:
            word = word[:start_index]
    return word

# 返回形式姓氏和有标签的企业
def get_set(family_names_open,labels_company_open):
    family1_set = set()
    family2_set = set()
    family3_set = set()
    labels_set = set()
    for family in family_names_open.readlines():
        family = family.strip()
        if len(family) == 1:
            family1_set.add(family)
        if len(family) == 2:
            family2_set.add(family)
        if len(family) == 3:
            family3_set.add(family)
    for label in labels_company_open.readlines():
        labels_set.add(clean_str(label.strip()))
    return family1_set, family2_set, family3_set, labels_set

# 调整案由层级mapping
def get_cause_mapping():
    cause_mapping4_3 = {}
    cause_mapping3_2 = {}
    cause_mapping2_1 = {}
    cause_name = set()
    cause_file = open('/Users/kenneth-mac/data/lawyer_score/pg_sm_cause_of_action.txt', 'r', encoding='utf8')
    for line in cause_file.readlines():
        fields = line.split('|')
        if fields[3].strip() not in cause_mapping4_3:
            if fields[3].strip() is not None:
                cause_mapping4_3[fields[3].strip()] = fields[2].strip()
        if fields[2].strip() not in cause_mapping3_2:
            if fields[2].strip() is not None:
                cause_mapping3_2[fields[2].strip()] = fields[1].strip()
        if fields[1].strip() not in cause_mapping2_1:
            if fields[1].strip() is not None:
                cause_mapping2_1[fields[1].strip()] = fields[0].strip()
        cause_name.add(fields[0])
    cause_file.close()
    return cause_mapping4_3,cause_mapping3_2, cause_mapping2_1, cause_name

#获得当事人加权分值
def get_parties_score(num):
    if num < 0.3:
        return 0
    elif num > 0.8:
        return 10
    else:
        return 2*((10*num)-3)

# 构建mapping用作工具
def getting_mapping(path):
    file_case = open(path, 'r', encoding='utf8')
    # 最低的年限
    year_mapping = {}
    # 裁判文书的总量
    doc_count_mapping = {}
    # 审理程序
    trail_mapping = {}
    # 管辖机构
    court_mapping = {}
    # 所在市区
    city_mapping = {}
    # 审判人员
    jud_mapping = {}
    # 争议类型
    cause_mapping = {}
    # 客户类型
    parties_mapping = {}

    for line in file_case.readlines():
        fields = line.strip().split('|')
        year = int(fields[3].split('-')[0])

        # 年份的map
        if fields[0] not in year_mapping:
            year_mapping[fields[0]] = year
        elif year < year_mapping[fields[0]]:
            year_mapping[fields[0]] = year
        else:
            pass

        # 文书总量的map
        if fields[0] not in doc_count_mapping:
            doc_count_mapping[fields[0]] = 1
        else:
            doc_count_mapping[fields[0]] = doc_count_mapping[fields[0]] + 1

        # 审理程序
        if fields[5].strip() is not None:
            if fields[0] not in trail_mapping:
                trail_mapping[fields[0]] = fields[5].strip()
            else:
                trail_mapping[fields[0]] = trail_mapping[fields[0]]+','+fields[5].strip()

        # 管辖机构
        if fields[4].strip() is not None:
            if fields[0] not in court_mapping:
                court_mapping[fields[0]] = fields[4].strip()
            else:
                court_mapping[fields[0]] = court_mapping[fields[0]]+','+fields[4].strip()

        # 所在城市
        if fields[11].strip() != '':
            if fields[0] not in city_mapping:
                city_mapping[fields[0]] = fields[11].strip()
            else:
                city_mapping[fields[0]] = city_mapping[fields[0]]+','+fields[11].strip()

        # 审判人员
        if fields[9].strip() != '':
            if fields[0] not in jud_mapping:
                jud_mapping[fields[0]] = fields[9].strip()
            else:
                jud_mapping[fields[0]] = jud_mapping[fields[0]] + ',' + fields[9].strip()

        # 审理程序
        if fields[6].strip() != '':
            if fields[0] not in cause_mapping:
                cause_mapping[fields[0]] = fields[6].strip()
            else:
                cause_mapping[fields[0]] = cause_mapping[fields[0]] + ',' + fields[6].strip()

        # 当事人类型的map
        if fields[14].strip != '':
            if fields[0] not in parties_mapping:
                parties_mapping[fields[0]] = fields[14].strip()
            else:
                parties_mapping[fields[0]] = parties_mapping[fields[0]]+ ',' + fields[14].strip()
    return year_mapping, doc_count_mapping, trail_mapping, court_mapping, city_mapping, jud_mapping, cause_mapping, parties_mapping

# 返回年代理量
def get_year_doc(year, doc_count):
    return doc_count/year
if __name__ == '__main__':
    k = 0
    year_mapping, doc_count_mapping, trail_mapping, court_mapping, city_mapping, jud_mapping, cause_mapping, parties_mapping = getting_mapping('/Users/kenneth-mac/data/lawyer_separate_out/xaf')
    family1_set, family2_set, family3_set, labels_set = get_set(family_names_open, labels_company_open)
    lawyer_set = set()
    for line in file_case.readlines():
        fields = line.strip().split('|')
        #1.1诉讼经验
        k = k + 1
        if k % 100 == 0:
            print(k)
        if fields[0] not in lawyer_set:
            lawyer_set.add(fields[0])
            year = datetime.datetime.now().year - year_mapping[fields[0]]
            year_score = 0 if year < 3 else (year*5-10)/3
            year_score = 5 if year_score>5 else year_score
            year_line = fields[0] + '|' + str(year) + '|' +str(float('%.2f' %year_score))

            #1.2争议类型
            cause_mapping4_3,cause_mapping3_2, cause_mapping2_1, cause_name = get_cause_mapping()
            cause = cause_mapping[fields[0]]
            cause_fields = cause.strip().split(',')
            cause_1=''
            cause_2=''
            cause_3=''
            cause_4=''

            for field in cause_fields:
                if field in cause_mapping4_3:
                    cause_4 = cause_4+','+field
                    cause_3 = cause_3+','+cause_mapping4_3[field]
                    cause_2 = cause_2+','+cause_mapping3_2[cause_mapping4_3[field]]
                    cause_1 = cause_1+','+cause_mapping2_1[cause_mapping3_2[cause_mapping4_3[field]]]
                if field in cause_mapping3_2:
                    cause_3 = cause_3+','+field
                    cause_2 = cause_2+','+cause_mapping3_2[field]
                    cause_1 = cause_1 + ',' + cause_mapping2_1[cause_mapping3_2[field]]
                if field in cause_mapping2_1:
                    cause_2 = cause_2+','+field
                    cause_1 = cause_1+','+cause_mapping2_1[field]
                if field in cause_name:
                    cause_1 = cause_1+','+field
            cause_1 = cause_1[1:] if cause_1 is not None else cause_1
            cause_2 = cause_2[1:] if cause_2 is not None else cause_2
            cause_3 = cause_3[1:] if cause_3 is not None else cause_3
            cause_4 = cause_4[1:] if cause_4 is not None else cause_4
            cause_1_num = 0 if cause_1 == '' else len(cause_1.split(','))
            cause_2_num = 0 if cause_2 == '' else len(cause_2.split(','))
            cause_3_num = 0 if cause_3 == '' else len(cause_3.split(','))
            cause_4_num = 0 if cause_4 == '' else len(cause_4.split(','))
            cause_line = year_line + '|' + cause_1+'|'+str(cause_1_num)+'|'+cause_2+'|'+str(cause_2_num)+'|'+cause_3+'|'+str(cause_3_num)+'|'+cause_4+'|'+str(cause_4_num)

            #1.3审理程序
            trail = trail_mapping[fields[0]]
            trail_num = 0 if trail == '' else len(trail.split(','))
            trail_line = cause_line + '|' + str(trail_mapping[fields[0]]) +'|'+ str(trail_num)

            #2.1文书总量
            doc_count = doc_count_mapping[fields[0]]
            doc_count_score = 0 if doc_count <=6 else (doc_count*5-30)/84
            doc_count_score = 5 if doc_count_score>5 else doc_count_score
            doc_count_line = trail_line + '|' + str(doc_count_mapping[fields[0]]) + '|' +str(float('%.2f' %doc_count_score))

            #2.2年代理量
            year_doc = get_year_doc(datetime.datetime.now().year - year_mapping[fields[0]], doc_count_mapping[fields[0]])
            year_doc_score = 0 if year_doc<=3 else (year_doc*5-15)/9
            year_doc_score = 5 if year_doc_score>5 else year_doc_score
            year_doc_line = doc_count_line + '|' + str(year_doc) + '|' + str(float('%.2f' %year_doc_score))

            #2.4管辖机构
            court = court_mapping[fields[0]]
            court_num = 0 if court == '' else len(court.split(','))
            court_line = year_doc_line +'|'+ court+'|'+ str(court_num)

            #2.5所在城市
            city = city_mapping[fields[0]]
            city_num = 0 if city == '' else len(city.split(','))
            city_line = court_line+'|'+city +'|'+str(city_num)

            #2.6审判人员
            jud = '' if fields[0] not in jud_mapping else jud_mapping[fields[0]]
            jud_num = 0 if jud == '' else len(jud.split(','))
            jud_line = city_line +'|' + jud +'|'+ str(jud_num)

            #2.3客户类型
            parties = parties_mapping[fields[0]]
            # print(parties)
            parties_company = 0         #有标签的企业计数
            parties_company_score = 0   #有标签的企业分值
            parties_gevernment = 0      #政府计数
            parties_gevernment_score = 0#政府分值
            parties_private = 0         #非上市民营企业计数
            parties_private_score = 0   #非上市民营企业分值
            parties_person = 0          #个人计数
            parties_person_score = 0    #个人分值
            parties_list = parties.split(',')
            count = len(parties_list)
            if count > 0:
                for party in parties_list:
                    party = party.strip()
                    match = government_pat.match(party)
                    if party in labels_set:
                        parties_company = parties_company+1
                        continue
                    elif match is not None:
                        parties_gevernment = parties_gevernment + 1
                        continue
                    elif (party[:1] in family1_set or party[:2] in family2_set or party[:3] in family3_set) and len(party) <= 5:
                        parties_person = parties_person + 1
                        continue
                    else:
                        parties_private = parties_private + 1
                        continue

                parties_company_score = str(float('%.2f' %(get_parties_score(parties_company/count))))
                parties_gevernment_score = str(float('%.2f' %(get_parties_score(parties_gevernment/count))))
                parties_private_score = str(float('%.2f' %(get_parties_score(parties_private/count))))
                parties_person_score = str(float('%.2f' %(get_parties_score(parties_person/count))))

            parties_line = jud_line + '|' + str(parties_company) + '|' + parties_company_score + '|' + str(parties_gevernment) +\
                           '|' + parties_gevernment_score + '|' + str(parties_private) + '|' + parties_private_score + '|' + \
                           str(parties_person)+ '|' + parties_person_score

            file_out.write(parties_line+'\n')


    file_case.close()
    file_out.close()