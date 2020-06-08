# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/20 下午1:13
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 将原先统计好的律师分值表，再拆开分别每个元素的分值
'''

import logging
import pymysql

conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
                       user='pg_db', password='ds930$232aH!@#FD', db='pg_simulate',
                       charset='utf8')

file_open = open('data.txt', 'r', encoding='utf8')
file_write = open('data_out.txt', 'w', encoding='utf8')

logging.basicConfig(filename='demo1.log',
                    filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

#获取法院对应关系
mapping_open = open('court_relation','r',encoding='utf8')
mapping_relation = {}
for line in mapping_open.readlines():
    words = line.strip().split('|')
    print(words)
    mapping_relation[words[0]] = words[1]

#将法院行切分和计数
def get_court_num(line):
    out_line=''
    mapping = {}
    words = line.split(',')
    for i in words:
        if i in mapping_relation:
            i = mapping_relation[i]
        if i not in mapping:
            mapping[i] = 1
        else:
            mapping[i] = mapping[i]+1
    for k in mapping:
        out_line=out_line+k+','+str(mapping[k])+'|'
    return out_line[:-1]

#将长列字符串切分为能计算的形式
def get_name_num(line):
    out_line=''
    mapping = {}
    words = line.split(',')
    for i in words:
        if i not in mapping:
            mapping[i] = 1
        else:
            mapping[i] = mapping[i]+1
    for k in mapping:
        out_line=out_line+k+','+str(mapping[k])+'|'
    return out_line[:-1]

#获取案由的分值
def get_cause_socre(q):
    score = 0
    if q >= 0.3:
        score = 5 if q > 0.6 else 50*q/3-5
    return str(float('%.2f' %score)*3)

#写出案由
def write_cause(cause_line):
    for cause in cause_line:
        cause_name,cause_num = cause.split(',')
        q = int(cause_num)/int(fields[6])
        score = get_cause_socre(q)
        file_write.write(fields[0] + '|' + name + '|' + organ + '|案由|case_name' + '|' + cause_name + '|' + 'case_score' + '|' + score + '\n')

#计算审理程序的分值
def get_trail_socre(r):
    score = 0
    if r >= 0.3:
        score = 5 if r > 0.8 else 10*r-3
    return str(float('%.2f' %score)*2)

#写出审理程序
def write_trail(trail_names):
    number_count = 0
    for trail in trail_names:
        trail_name, trail_num = trail.split(',')
        if '一审' in trail_name or '二审' in trail_name or '再审' in trail_name:
            number_count+=int(trail_num)
    for trail in trail_names:
        trail_name,trail_num = trail.split(',')
        r = int(trail_num)/number_count
        if '一审' in trail_name or '二审' in trail_name or '再审' in trail_name:
            score = get_trail_socre(r)
            file_write.write(fields[0] + '|' + name + '|' + organ + '|审理程序|trail_name' + '|' + trail_name + '|' + 'trail_score' + '|' + score + '\n')

#计算城市分值
def get_city_socre(r):
    score = 0
    if r >= 0.3:
        score = 5 if r > 0.8 else 10*r-3
    return str(float('%.2f' %score))

#写入城市
def write_city(city_names):
    for city in city_names:
        city_name,city_num = city.split(',')
        t = int(city_num)/int(fields[20])
        score = get_city_socre(t)
        file_write.write(fields[0] + '|' + name + '|' + organ + '|地域|city_name' + '|' + city_name + '|' + 'city_score' + '|' + score + '\n')

#计算法官分值
def get_judge_socre(r):
    score = 0
    if r >= 0:
        score = 5 if r > 0.3 else 50*r
    return str(float('%.2f' %score))

#写入法官
def write_judge(judge_names):
    for judge in judge_names:
        judge_name,judge_num = judge.split(',')
        t = int(judge_num)/int(fields[22])
        score = get_judge_socre(t)
        file_write.write(fields[0] + '|' + name + '|' + organ + '|审判人员|judge_name' + '|' + judge_name + '|' + 'judge_score' + '|' + score + '\n')

#计算法院分值
def get_court_socre(r):
    score = 0
    if r >= 0:
        score = 5 if r > 0.3 else 50*r
    return str(float('%.2f' %score))

#写入法院
def write_court(court_names):
    for court in court_names:
        court_name,court_num = court.split(',')
        t = int(court_num)/int(fields[18])
        score = get_court_socre(t)
        file_write.write(fields[0] + '|' + name + '|' + organ + '|管辖机构|court_name' + '|' + court_name + '|' + 'court_score' + '|' + score + '\n')

# 从数据库查询律师姓名和律所
def get_name_organ():
    sql_lawyer = "select lawyer_name, organ_name from pg_lawyer where id = {} ".format(int(fields[0]))
    cursor.execute(sql_lawyer)
    result = cursor.fetchall()
    cursor.close()
    return result[0][0], result[0][1]

# 主要运行程序
for line in file_open.readlines():
    cursor = conn.cursor()
    fields = line.strip().split('|')
    # 返回律师名称和律所名称
    name,organ = get_name_organ()
    # 写出诉讼经验
    file_write.write(fields[0]+'|'+name+'|'+organ+'|诉讼经验|work_ex'+'|'+fields[1]+'|'+'ex_soure'+'|'+fields[2]+'\n')
    # 写出文书总量
    file_write.write(fields[0] + '|' + name + '|' + organ + '|文书总量|doc_count' + '|' + fields[13]+'|'+'doc_soure'+'|'+fields[14]+'\n')
    # 写出年代理量
    file_write.write(fields[0] + '|' + name + '|' + organ + '|年代理量|year_doc_count' + '|' + fields[1] + '|' + 'year_doc_score' + '|' + fields[2] + '\n')
    # 写出客户类型
    file_write.write(fields[0] + '|' + name + '|' + organ + '|有标签客户|parties_company' + '|' + fields[23] + '|' + 'parties_company_soure' + '|' + fields[24] + '\n')
    file_write.write(fields[0] + '|' + name + '|' + organ + '|政府客户|parties_government' + '|' + fields[25] + '|' + 'parties_government_soure' + '|' + fields[26] + '\n')
    file_write.write(fields[0] + '|' + name + '|' + organ + '|非上市民营客户|parties_private' + '|' + fields[27] + '|' + 'parties_private_soure' + '|' + fields[28] + '\n')
    file_write.write(fields[0] + '|' + name + '|' + organ + '|个人客户|parties_person' + '|' + fields[29] + '|' + 'parties_person_soure' + '|' + fields[30] + '\n')

    # 写出案由
    write_cause(get_name_num(fields[9]).split('|'))
    write_cause(get_name_num(fields[7]).split('|'))
    write_cause(get_name_num(fields[5]).split('|'))

    #审理程序11
    trail_names = get_name_num(fields[11]).split('|')
    write_trail(trail_names)

    #法院17
    court_names = get_court_num(fields[17]).split('|')
    write_court(court_names)

    #城市19
    city_names = get_name_num(fields[19]).split('|')
    write_city(city_names)

    #审判人员21
    judge_names = get_name_num(fields[21]).split('|')
    write_judge(judge_names)