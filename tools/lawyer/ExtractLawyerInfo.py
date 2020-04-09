#!/usr/bin/env python
# -*- coding: utf8 -*-
""" 
@brief : 
@author: linzx
@file  : ExtractLawyerInfo.py
@ctime : 2019/5/10 9:25
"""

import re
import json
from pyspark.sql import SparkSession
from operator import add

global_lawyers = {}

def extractLawyerWithCaseDeatail(df):
    lawyers = []
    allLawyers = []  # 用来判断哪些是合作律师，哪些是对手律师
    for record in df.parties:
        # # 将json字符串转成dict
        try:
            party = json.loads(record)
        except json.JSONDecodeError:
            # lawyers.append(['ERROR',
            #                 record,  # 这种error记录 把原始的party字符串写进去看看啥原因
            #                 123456789,
            #                 df.docid,
            #                 df.casereason,
            #                 df.trialprocedure,
            #                 df.judgeyear,
            #                 df.court,
            #                 df.courtlevel,
            #                 df.province,
            #                 df.city,
            #                 df.region,
            #                 'UNKNOWN',  # 当事人诉讼地位
            #                 True,  # 当事人是公司还是个人
            #                 #                  df.parties,Ns
            #                 df.justices
            #                 ])
            print("JSONERROR record:{}-{}".format(record, df.docid))
        else:
            # 遍历当事人的律师，如果没有律师的记录都忽略掉
            for lawyer in party['lawyer']:
                global global_lawyers
                lawyerId = None
                # 根据律师姓名查询 可能的律师
                candidates = global_lawyers.get(lawyer["name"])
                if candidates is not None:
                    # 如果只有一个候选人，那就不判断律师，就是他了
                    if len(candidates) == 1:
                        # 虽然是个for循环其实只跑一次。。。不知道怎么取出disc的value - -！
                        for (loffice, lid) in candidates.items():
                            lawyerId = lid
                            '''
                            这里要干一件事。。如果只有一个同名律师，这样的话吧 这个所属律师定位到 律师资料中的这个律所
                            这样才能保证后续统计是不会出现一个lawyerid有多条记录
                            '''
                            lawyer["office"] = loffice
                    else:
                        # 如果有多个同名律师，就按律所匹配，匹不上拉到,这里要不get 别用[]
                        lawyerId = candidates.get(lawyer["office"])
                # 存储的是个tuple
                allLawyers.append((party["statusCode"], lawyer))
                lawyers.append([lawyer["name"],
                                lawyer["office"],
                                lawyerId,
                                party["statusCode"],  # 当时人身份  占个坑 回头会被替换掉
                                party["statusCode"],  # 当时人身份 占个坑
                                df.docid,
                                df.casereason,
                                df.casetype,
                                df.doctype,
                                df.trialprocedure,
                                df.judgeyear,
                                df.judgemonth,
                                df.court,
                                df.courtlevel,
                                df.province,
                                df.city,
                                df.region,
                                party["status"],  # 当事人诉讼地位
                                party["isCompany"],  # 当事人是公司还是个人
                                df.justices
                                ])
    result = []
    for x in lawyers:
        partners = []
        opponents = []
        for y in allLawyers:  # y是个两个元素的tuple
            # 如果当前法官身份与 该法官身份相同,但是姓名或律所不同（把自己去掉），则为合作律师
            if x[3] == y[0] and (x[0] != y[1]['name'] or x[1] != y[1]['office']):
                partners.append(y[1])
            # 如果地位不同，则为对手律师
            if x[3] != y[0]:
                opponents.append(y[1])
        # 把之前留的占位字段替换掉
        x[3] = partners
        x[4] = opponents
        result.append(x)
    return result

def extractLawyerWithJudge(df):
    '''解析jutices字段，flagMap成一对多的记录'''
    lawyerWithJudge = []
    # justices 是对象array
    for judge in df.justices:
        if judge.get("statusCode") is not None and judge["statusCode"] == 'JUDGE':
            lawyerWithJudge.append([df.lawyer_id,
                                    df.lawyer_name,
                                    df.lawyer_organ_name,
                                    df.court,
                                    judge.get('name')])
    return lawyerWithJudge

def extractLawyerWithPartner(df):
    '''解析partners字段，flagMap成一对多的记录'''
    lawyerWithPartner = []
    # partners 是对象array
    for partner in df.partners:
        lawyerWithPartner.append([df.lawyer_id,
                                  df.lawyer_name,
                                  df.lawyer_organ_name,
                                  partner['name'],
                                  partner['office']])
    return lawyerWithPartner

def extractLawyerWithOpponent(df):
    '''解析opponents字段，flagMap成一对多的记录'''
    lawyerWithOpponent = []
    # opponents 是对象array
    for opponent in df.opponents:
        lawyerWithOpponent.append([df.lawyer_id,
                                   df.lawyer_name,
                                   df.lawyer_organ_name,
                                   opponent['name'],
                                   opponent['office']])
    return lawyerWithOpponent

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("LawyerInfoExtractor") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .enableHiveSupport() \
        .getOrCreate()
    spark.sql("use pgdata")

    lawyers = spark.sql("select lawyer_name,organ_name,id from pg_lawyer").collect()
    # 加载全局律师信息
    for lawyer in lawyers:
        if global_lawyers.get(lawyer.lawyer_name) is None:
            global_lawyers[lawyer.lawyer_name] = {lawyer.organ_name: lawyer.id}
        else:
            global_lawyers[lawyer.lawyer_name][lawyer.organ_name] = lawyer.id
    # 生成律师文书关系明细信息
    df = spark.sql("select docid,casereason,casetype,doctype,trialprocedure,judgeyear,judgemonth,"
                   "court,courtlevel,province,city,region,parties,justices "
                   "from pgdata.pg_ws_parsed")

    # ndf=df.rdd.flatMap(lambda x:extractLawyerWithCaseDeatail(x))
    # rst=ndf.collect()
    # print("len=========================={}".format(len(rst)))
    # for x  in rst:
    #     print("----------{}".format(x))

    # df.rdd.flatMap(lambda x: extractLawyerWithCaseDeatail(x)).map(lambda x:x)
    newdf = spark.createDataFrame(df.rdd.flatMap(lambda x: extractLawyerWithCaseDeatail(x)),
                                  ['lawyer_name', 'lawyer_organ_name', 'lawyer_id',
                                   'partners', 'opponents', 'docid',
                                   'casereason','casetype','doctype', 'trialprocedure',
                                   'judgeyear','judgemonth', 'court', 'courtlevel', 'province', 'city', 'region',
                                   'partyStatus', 'partyType', 'justices'])

    newdf.write.mode("overwrite").saveAsTable("pg_ws_lawyercase")
    # 统计律师基本信息
    lawyerBaseDf = spark.sql("select base.lawyer_id as lawyer_id,"
                             "base.lawyer_name as lawyer_name ,"
                             "base.lawyer_organ_name as lawyer_organ_name, "
                             "base.all_cnt as all_cnt,"
                             "base.all_cnt_f as all_cnt_f,"
                             "lastyear.last_year_cnt as last_year_cnt,"
                             "lastyear.last_year_cnt_f as last_year_cnt_f,"
                             "base.first_year as first_year,"
                             "base.first_year_f as first_year_f "
                             "from "
                             "(select lawyer_id,lawyer_name,lawyer_organ_name, "
                             "   count(*) as all_cnt,"
                             "    (5*count(*)-30)/84 as all_cnt_f,"  # 所有案件算分 = （5*文书总量-30）／84
                             "    min(case  when judgeyear='' or judgeyear is null then '2099' else judgeyear end) as first_year ," # 这列很多是‘’,nvl没有用
                             "   (5*nvl(YEAR(CURRENT_TIMESTAMP) - cast(min(case  when judgeyear='' or judgeyear is null then '2099' else judgeyear end) as int) +1,0) -10 ) / 3 as first_year_f"
                             "   FROM pg_ws_lawyercase "
                             "    GROUP BY lawyer_id,lawyer_name,lawyer_organ_name) as base "
                             "    LEFT OUTER  JOIN "
                             "     (SELECT lawyer_id,lawyer_name,lawyer_organ_name, "
                             "      COUNT (*) as last_year_cnt,"  # 最近一年数量
                             "      (5*COUNT(*)-15)/9 as last_year_cnt_f "  # 最近一年算分
                             "       FROM  pg_ws_lawyercase WHERE judgeyear =YEAR(current_timestamp) - 1 "
                             "       GROUP BY lawyer_id,lawyer_name,lawyer_organ_name) as lastyear "
                             "on(nvl(base.lawyer_id,1)=nvl(lastyear.lawyer_id,1) "
                             "   and base.lawyer_name=lastyear.lawyer_name"
                             "   and nvl(base.lawyer_organ_name,'1')=nvl(lastyear.lawyer_organ_name,'1'))")
    # result = spark.createDataFrame(lawyerBaseDf,
    #                               ['lawyer_id','lawyer_name', 'lawyer_organ_name',
    #                                'all_cnt', 'all_cnt_f', 'last_year_cnt', 'last_year_cnt_f',
    #                                'first_year', 'first_year_f'])
    lawyerBaseDf.write.mode("overwrite").saveAsTable("pg_lawyer_info")
    lawyerBaseDf.write.mode('overwrite').option("truncate", "true") \
        .jdbc(url='jdbc:mysql://172.17.128.240:3310/prism1',
              table='pg_lawyer_info',
              properties={"driver": "com.mysql.jdbc.Driver",
                          "user": "root",
                          "password": "H0qZXCwvUvgs6F7N"})

    # 按案由统计
    statByCase = spark.sql("select stat.lawyer_id, "
                           "stat.lawyer_name,"
                           "stat.lawyer_organ_name,"
                           "stat.type_code,"
                           "stat.type_name,"
                           "stat.type_param_code,"
                           "stat.type_param_name,"
                           "info.all_cnt,"
                           "stat.cnt,"
                           "50* stat.cnt/info.all_cnt/3-5 as cnt_f "
                           "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                           "  'CAUSE_OF_ACTION_2' as type_code,'案由' as type_name,"
                           "  casereason as type_param_code,casereason as type_param_name,COUNT(1) as cnt "
                           "  FROM pg_ws_lawyercase "
                           "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,casereason ) as stat "
                           "LEFT OUTER JOIN pg_lawyer_info info "
                           "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                           "  and stat.lawyer_name=info.lawyer_name "
                           "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")
    # # 按审理程序统计
    statByProcd = spark.sql("select stat.lawyer_id, "
                            "stat.lawyer_name,"
                            "stat.lawyer_organ_name,"
                            "stat.type_code,"
                            "stat.type_name,"
                            "stat.type_param_code,"
                            "stat.type_param_name,"
                            "info.all_cnt,"
                            "stat.cnt,"
                            "10* stat.cnt/info.all_cnt-3 as cnt_f "
                            "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                            "  'COURT_PROCEEDING' as type_code,'审理程序' as type_name,"
                            "  trialprocedure as type_param_code,trialprocedure as type_param_name,COUNT(1) as cnt "
                            "  FROM pg_ws_lawyercase "
                            "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,trialprocedure ) as stat "
                            "LEFT OUTER JOIN pg_lawyer_info info "
                            "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                            "  and stat.lawyer_name=info.lawyer_name "
                            "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")

    # 按管辖机构(法院)统计
    statByCourt = spark.sql("select stat.lawyer_id, "
                            "stat.lawyer_name,"
                            "stat.lawyer_organ_name,"
                            "stat.type_code,"
                            "stat.type_name,"
                            "stat.type_param_code,"
                            "stat.type_param_name,"
                            "info.all_cnt,"
                            "stat.cnt,"
                            "50* stat.cnt/info.all_cnt/3 as cnt_f "
                            "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                            "  'COURT_OR_ARBITRATION_AGENCY' as type_code,'管辖机构' as type_name,"
                            "  court as type_param_code,court as type_param_name,COUNT(1) as cnt "
                            "  FROM pg_ws_lawyercase "
                            "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,court ) as stat "
                            "LEFT OUTER JOIN pg_lawyer_info info "
                            "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                            "  and stat.lawyer_name=info.lawyer_name "
                            "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")
    # 按法院层级统计
    statByCourtLevel = spark.sql("select stat.lawyer_id, "
                                 "stat.lawyer_name,"
                                 "stat.lawyer_organ_name,"
                                 "stat.type_code,"
                                 "stat.type_name,"
                                 "stat.type_param_code,"
                                 "stat.type_param_name,"
                                 "info.all_cnt,"
                                 "stat.cnt,"
                                 "10* stat.cnt/info.all_cnt-3 as cnt_f "
                                 "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                                 "  'COURT_LEVEL' as type_code,'法院层级' as type_name,"
                                 "  courtlevel as type_param_code,courtlevel as type_param_name,COUNT(1) as cnt "
                                 "  FROM pg_ws_lawyercase "
                                 "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,courtlevel ) as stat "
                                 "LEFT OUTER JOIN pg_lawyer_info info "
                                 "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                                 "  and stat.lawyer_name=info.lawyer_name "
                                 "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")

    # 按地域统计
    statByCity = spark.sql("select stat.lawyer_id, "
                           "stat.lawyer_name,"
                           "stat.lawyer_organ_name,"
                           "stat.type_code,"
                           "stat.type_name,"
                           "stat.type_param_code,"
                           "stat.type_param_name,"
                           "info.all_cnt,"
                           "stat.cnt,"
                           "10* stat.cnt/info.all_cnt-3 as cnt_f "
                           "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                           "  'WORK_AREA' as type_code,'地域' as type_name,"
                           "  city as type_param_code,city as type_param_name,COUNT(1) as cnt "
                           "  FROM pg_ws_lawyercase "
                           "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,city ) as stat "
                           "LEFT OUTER JOIN pg_lawyer_info info "
                           "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                           "  and stat.lawyer_name=info.lawyer_name "
                           "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")
    # 按当事人性质（公司 or 个人）统计
    statByPartyType = spark.sql("select stat.lawyer_id, "
                                "stat.lawyer_name,"
                                "stat.lawyer_organ_name,"
                                "stat.type_code,"
                                "stat.type_name,"
                                "stat.type_param_code,"
                                "stat.type_param_name,"
                                "info.all_cnt,"
                                "stat.cnt,"
                                "10* stat.cnt/info.all_cnt-3 as cnt_f "
                                "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                                "  'PARTY_TYPE' as type_code,'当事人类型' as type_name,"
                                "  CASE WHEN partyType THEN '公司' ELSE '个人' END AS type_param_code,"
                                "  CASE WHEN partyType THEN '公司' ELSE '个人' END AS type_param_name,"
                                "  COUNT(1) as cnt "
                                "  FROM pg_ws_lawyercase "
                                "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,partyType ) as stat "
                                "LEFT OUTER JOIN pg_lawyer_info info "
                                "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                                "  and stat.lawyer_name=info.lawyer_name "
                                "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")

    # 按审判人员统计 这个需要去解析 justices的法官字段
    judgeDf = spark.sql("select lawyer_id,lawyer_name,lawyer_organ_name,court,justices from pg_ws_lawyercase")

    spark.createDataFrame(judgeDf.rdd.flatMap(lambda x: extractLawyerWithJudge(x)),
                          ['lawyer_id', 'lawyer_name', 'lawyer_organ_name', 'court', 'judge']).createOrReplaceTempView(
        'pg_tv_lawyerjudge')
    statByJudege = spark.sql("select stat.lawyer_id, "
                             "stat.lawyer_name,"
                             "stat.lawyer_organ_name,"
                             "stat.type_code,"
                             "stat.type_name,"
                             "stat.type_param_code,"
                             "stat.type_param_name,"
                             "info.all_cnt,"
                             "stat.cnt,"
                             "10* stat.cnt/info.all_cnt-3 as cnt_f "
                             "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                             "  'JUDGE_PERSON' as type_code,'审判人员' as type_name,"
                             "  judge as type_param_code,court as type_param_name,COUNT(1) as cnt "
                             "  FROM pg_tv_lawyerjudge "
                             "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,court,judge ) as stat "
                             "LEFT OUTER JOIN pg_lawyer_info info "
                             "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                             "  and stat.lawyer_name=info.lawyer_name "
                             "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")

    # 按年代理量统计
    statByYear = spark.sql("select stat.lawyer_id, "
                           "stat.lawyer_name,"
                           "stat.lawyer_organ_name,"
                           "stat.type_code,"
                           "stat.type_name,"
                           "stat.type_param_code,"
                           "stat.type_param_name,"
                           "info.all_cnt,"
                           "stat.cnt,"
                           "0 as cnt_f "
                           "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                           "  'YEAR_AGENT_NUM' as type_code,'年代理量' as type_name,"
                           "  judgeyear as type_param_code,judgeyear as type_param_name,COUNT(1) as cnt "
                           "  FROM pg_ws_lawyercase "
                           "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,judgeyear ) as stat "
                           "LEFT OUTER JOIN pg_lawyer_info info "
                           "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                           "  and stat.lawyer_name=info.lawyer_name "
                           "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")

    # 按合作律师统计 这个需要去解析 partners字段
    partnerDf = spark.sql("select lawyer_id,lawyer_name,lawyer_organ_name,partners from pg_ws_lawyercase")

    spark.createDataFrame(partnerDf.rdd.flatMap(lambda x: extractLawyerWithPartner(x)),
                          ['lawyer_id',
                           'lawyer_name',
                           'lawyer_organ_name',
                           'cooprate_lawyer',
                           'cooprate_lawyer_office']).createOrReplaceTempView('pg_tv_lawyerpartner')
    statByPartner = spark.sql("select stat.lawyer_id, "
                              "stat.lawyer_name,"
                              "stat.lawyer_organ_name,"
                              "stat.type_code,"
                              "stat.type_name,"
                              "stat.type_param_code,"
                              "stat.type_param_name,"
                              "info.all_cnt,"
                              "stat.cnt,"
                              "0 as cnt_f "
                              "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                              "  'COOPERATE_LAWYER' as type_code,'合作律师' as type_name,"
                              "  cooprate_lawyer as type_param_code,cooprate_lawyer_office as type_param_name,"
                              "  COUNT(1) as cnt "
                              "  FROM pg_tv_lawyerpartner "
                              "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,cooprate_lawyer,cooprate_lawyer_office ) as stat "
                              "LEFT OUTER JOIN pg_lawyer_info info "
                              "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                              "  and stat.lawyer_name=info.lawyer_name "
                              "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")
    # 按对手律师统计 这个需要去解析 opponents字段
    opponentDf = spark.sql("select lawyer_id,lawyer_name,lawyer_organ_name,opponents from pg_ws_lawyercase")

    spark.createDataFrame(opponentDf.rdd.flatMap(lambda x: extractLawyerWithOpponent(x)),
                          ['lawyer_id',
                           'lawyer_name',
                           'lawyer_organ_name',
                           'opposing_lawyer',
                           'opposing_lawyer_office']).createOrReplaceTempView('pg_tv_lawyeropponent')
    statByOpponent = spark.sql("select stat.lawyer_id, "
                               "stat.lawyer_name,"
                               "stat.lawyer_organ_name,"
                               "stat.type_code,"
                               "stat.type_name,"
                               "stat.type_param_code,"
                               "stat.type_param_name,"
                               "info.all_cnt,"
                               "stat.cnt,"
                               "0 as cnt_f "
                               "from (select lawyer_id,lawyer_name,lawyer_organ_name,"
                               "  'OPPOSING_LAWYER' as type_code,'对手律师' as type_name,"
                               "  opposing_lawyer as type_param_code,opposing_lawyer_office as type_param_name,"
                               "  COUNT(1) as cnt "
                               "  FROM pg_tv_lawyeropponent "
                               "  GROUP BY lawyer_id,lawyer_name,lawyer_organ_name,opposing_lawyer,opposing_lawyer_office ) as stat "
                               "LEFT OUTER JOIN pg_lawyer_info info "
                               "ON (nvl(stat.lawyer_id,1)=nvl(info.lawyer_id,1)  "
                               "  and stat.lawyer_name=info.lawyer_name "
                               "  and nvl(stat.lawyer_organ_name,'1')=nvl(info.lawyer_organ_name,'1')) ")
    resultDf = statByCase.unionAll(statByProcd) \
        .unionAll(statByCourt) \
        .unionAll(statByCourtLevel) \
        .unionAll(statByCity) \
        .unionAll(statByPartyType) \
        .unionAll(statByJudege) \
        .unionAll(statByYear) \
        .unionAll(statByPartner) \
        .unionAll(statByOpponent)
    resultDf.write.mode("overwrite").saveAsTable("pg_lawyer_info_attr")

    spark.stop()
