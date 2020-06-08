#!/usr/bin/env python
# -*- coding: utf8 -*-
""" 
@brief : 
@author: linzx
@file  : ExtractJudgeInfo.py
@ctime : 2019/5/14 8:51
"""

import re
import json
from pyspark.sql import SparkSession
from pyspark.sql import functions


def extractJudgeWithCaseDeatail(df):
    '''解析jutices字段，flagMap成一对多的记录'''
    judgeCase = []
    # 后续的统计不需要记录当事人跟律师的关系，所以这里可以分开处理
    lawyers = []  # 案件出现的律师列表
    judges = []  # 案件中出现法官列表
    companies=[]
    persons=[]
    for record in df.parties:
        try:
            party = json.loads(record)
        except:
            print("JSONERROR :{}-{}".format(df.docid, record))
        else:
            # 统计公司和个人数
            if party['isCompany']:
                companies.append(party)
            else:
                persons.append(party)
            # 统计案件中出现的律师数
            lawyers = party['lawyer']

    # justices字段是个对象arrary
    for judge in df.justices:
        # 如果庭审人员的身份是法官
        if judge["statusCode"] == 'JUDGE':
            # 这里把法官在案件里的地位也带出去 用tuple
            judges.append((judge['name'], judge['status']))
    # judge是个tuple
    for judge in judges:
        partners = [x[0] for x in judges]  # 案件中出现的所有法官
        partners.remove(judge[0])  # 把自己移除以后就是合作的法官了
        judgeCase.append([judge[0],  # 法官姓名
                          judge[1],  # 案件中法官的身份
                          len(persons),  # 案件中出现的个人数量
                          len(companies),  # 案件中出现的企业数量
                          persons,
                          companies,
                          lawyers,  # 案件中出现的律师列表
                          partners,
                          df.court,
                          df.courtlevel,
                          df.docid,
                          df.casereason,
                          df.casetype,
                          df.doctype,
                          df.trialprocedure,
                          df.judgeyear,
                          df.judgemonth,
                          df.judgetime,
                          df.parties,
                          df.justices])

    return judgeCase

def NVL(s,v=None):
    return ('' if v is None else v) if s is None else s

def extractJudgeWithLawyer(df):
    '''解析jutices字段，flagMap成一对多的记录'''
    judgeWithLawyer = []
    for lawyer in df.lawyers:
        # # 将json字符串转成dict
        judgeWithLawyer.append([df.judge_name,
                                df.court,
                                lawyer.get('name'),
                                lawyer.get('office')])
    return judgeWithLawyer


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("JudgeInfoExtractor") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
        .config("spark.yarn.executor.memoryOverhead", "2G") \
        .enableHiveSupport() \
        .getOrCreate()
    spark.sql("use pgdata")
    mysqlDf = spark.read.format("jdbc").options(url="jdbc:mysql://172.17.128.240:3310/prism1",
                                                driver="com.mysql.jdbc.Driver",
                                                dbtable="pg_user_judge_syn",
                                                user="root", password="H0qZXCwvUvgs6F7N").load()
    mysqlDf.select("*").createOrReplaceTempView("pg_tv_mysqljudge")
    rst = spark.sql("select max(id)+1 as id from pg_tv_mysqljudge").collect()
    maxId=0
    # 获得以下最大的id
    for x in rst:
        maxId=x.id
    print("max judge id {}".format(maxId))
    # 备份表防止出错
    mysqlDf.write.mode('overwrite').jdbc(url='jdbc:mysql://172.17.128.240:3310/prism1',
                                         table='pg_user_judge_syn_bak',
                                         properties={"driver": "com.mysql.jdbc.Driver",
                                                     "user": "root",
                                                     "password": "H0qZXCwvUvgs6F7N"})

    # print("##" * 50)
    # mysqlDf.printSchema()

    # 分解审判人员信息，获取法官信息，这个时候还没法获得法官id
    df = spark.sql("select docid,court,courtlevel,casereason,casetype,doctype,trialprocedure,judgeyear,judgemonth,judgetime,parties,justices "
                   "from pgdata.pg_ws_parsed ")\
        .rdd.flatMap(lambda x: extractJudgeWithCaseDeatail(x))

    # 创建法官与文书的映射关系 这里没法生成id，因为还没按法官跟法院合并
    spark.createDataFrame(df, ['judge_name', 'judge_status', 'person_cnt', 'company_cnt','persons','companies',
                               'lawyers', 'partners', 'court', 'courtlevel',
                               'docid', 'casereason','casetype','doctype', 'trialprocedure', 'judgeyear','judgemonth',
                               'judgetime', 'parties', 'justices']) \
        .write \
        .mode("overwrite") \
        .saveAsTable("pg_ws_judgecase")

    # 汇集法官参与过的审判程序,结果是"一审|二审"
    judgeWithProc=spark.sql("select distinct judge_name,court,trialprocedure from pg_ws_judgecase")
    judgeWithProc=judgeWithProc.rdd.map(lambda x:(NVL(x.judge_name)+'-'+NVL(x.court),(x.judge_name,x.court,x.trialprocedure)))\
        .reduceByKey(lambda x,y:[x[0],x[1],NVL(x[2])+'|'+NVL(y[2])],numPartitions=3000)\
        .map(lambda  x:x[1])

    spark.createDataFrame(judgeWithProc,['judge_name','court','court_proceeding_type'])\
        .createOrReplaceTempView("pg_tv_judge_proc")
    # inti=0
    # rst.show(100)

    judgeStatDf = spark.sql("SELECT base.judge_name as name,"
                            "base.court,"
                            "base.courtlevel as court_level,"
                            "base.earliest_year,"
                            "base.judicial_doc_cnt,"
                            "las.last_year_judicial_cnt "
                            "FROM  "
                            "   (SELECT judge_name ,"
                            "    court ,"
                            "    courtlevel,"
                            "    MIN(judgeyear) AS earliest_year ,"
                            "    COUNT(1) AS judicial_doc_cnt  "
                            "    FROM pg_ws_judgecase  "
                            "    GROUP BY judge_name,court,courtlevel) base "
                            "LEFT  OUTER  JOIN "
                            "   (SELECT judge_name,"
                            "    court,"
                            "    COUNT(1) AS last_year_judicial_cnt "
                            "    FROM pg_ws_judgecase "
                            "    WHERE judgeyear =YEAR(current_timestamp) - 1"
                            "    GROUP  BY judge_name,court) as las "
                            "ON (base.judge_name = las.judge_name "
                            "    AND nvl(base.court,'1') = nvl(las.court,'1'))")  # 注意null字段不能判断等于

    # 增加唯一的索引列，后创建个视图方便使用sql
    judgeStatDf.withColumn('idx', functions.monotonically_increasing_id()).createOrReplaceTempView("pg_tv_judge_stat")

    # 关联mysql数据源，有id的填写上id
    judgeInfoDf = spark.sql("SELECT nvl(base.id,stat.idx+{}) as id, "  # 如果id为空，就用idx作为id
                            "  stat.name,"
                            "  stat.court,"
                            "  stat.court_level,"
                            "  stat.earliest_year,"
                            "  stat.judicial_doc_cnt,"
                            "  stat.last_year_judicial_cnt,"
                            "  base.create_time, "
                            "  nvl(base.data_source,1) as data_source ,"
                            "  proc.court_proceeding_type "
                            "FROM pg_tv_judge_stat stat "
                            "LEFT OUTER  JOIN pg_tv_mysqljudge base "
                            "on stat.name=base.name "
                            "  AND nvl(stat.court,'1')=nvl(base.court,'1') "
                            "LEFT OUTER JOIN pg_tv_judge_proc proc "
                            "on stat.name=proc.judge_name "
                            "  AND nvl(stat.court,'1')=nvl(proc.court,'1') ".format(maxId))

    # 持久化到hive
    judgeInfoDf.write.mode("overwrite").saveAsTable("pg_judge_info")

    # 持久化到mysql  注意这里不能直接把 judgeInfoDf持久化到mysql，会有问题！！！！！！
    spark.sql("select * from pg_judge_info") \
        .write.mode('overwrite') \
        .option("truncate", "true") \
        .jdbc(url='jdbc:mysql://172.17.128.240:3310/prism1',
              table='pg_user_judge_syn',
              properties={"driver": "com.mysql.jdbc.Driver",
                          "user": "root",
                          "password": "H0qZXCwvUvgs6F7N"})

    # 按案由统计
    statByCase = spark.sql("select info.id as judge_id, "
                           "stat.judge_name as judge_name,"
                           "stat.court,"
                           "stat.type_code,"
                           "stat.type_name,"
                           "stat.type_param_code,"
                           "stat.type_param_name,"
                           "info.judicial_doc_cnt as all_cnt,"
                           "stat.cnt "
                           "from (select judge_name,court,"
                           "  'CAUSE_OF_ACTION_2' as type_code,'案由' as type_name,"
                           "  casereason as type_param_code,casereason as type_param_name,COUNT(1) as cnt "
                           "  FROM pg_ws_judgecase "
                           "  GROUP BY judge_name,court,casereason ) as stat "
                           "LEFT OUTER JOIN pg_judge_info info "
                           "ON  nvl(stat.judge_name,'1')=nvl(info.name,'1') "
                           "  and nvl(stat.court,'1')=nvl(info.court,'1') ")

    # 按审理程序统计
    statByProcd = spark.sql("select info.id as judge_id, "
                            "stat.judge_name as judge_name,"
                            "stat.court,"
                            "stat.type_code,"
                            "stat.type_name,"
                            "stat.type_param_code,"
                            "stat.type_param_name,"
                            "info.judicial_doc_cnt as all_cnt,"
                            "stat.cnt "
                            "from (select judge_name,court,"
                            "  'COURT_PROCEEDING' as type_code,'审理程序' as type_name,"
                            "  trialprocedure as type_param_code,trialprocedure as type_param_name,COUNT(1) as cnt "
                            "  FROM pg_ws_judgecase "
                            "  GROUP BY judge_name,court,trialprocedure ) as stat "
                            "LEFT OUTER JOIN pg_judge_info info "
                            "ON  nvl(stat.judge_name,'1')=nvl(info.name,'1') "
                            "  and nvl(stat.court,'1')=nvl(info.court,'1') ")

    # 按当事人类型统计 公司
    statByCompany = spark.sql("select info.id as judge_id, "
                              "stat.judge_name as judge_name,"
                              "stat.court,"
                              "stat.type_code,"
                              "stat.type_name,"
                              "stat.type_param_code,"
                              "stat.type_param_name,"
                              "info.judicial_doc_cnt as all_cnt,"
                              "stat.cnt "
                              "from (select judge_name,court,"
                              "  'PARTY_TYPE' as type_code,'当事人类型' as type_name,"
                              "  '公司' as type_param_code,'公司' as type_param_name,sum(company_cnt) as cnt "
                              "  FROM pg_ws_judgecase "
                              "  GROUP BY judge_name,court ) as stat "
                              "LEFT OUTER JOIN pg_judge_info info "
                              "ON  nvl(stat.judge_name,'1')=nvl(info.name,'1') "
                              "  and nvl(stat.court,'1')=nvl(info.court,'1') ")
    # 按当事人类型统计 个人
    statByPerson = spark.sql("select info.id as judge_id, "
                             "stat.judge_name as judge_name,"
                             "stat.court,"
                             "stat.type_code,"
                             "stat.type_name,"
                             "stat.type_param_code,"
                             "stat.type_param_name,"
                             "info.judicial_doc_cnt as all_cnt,"
                             "stat.cnt "
                             "from (select judge_name,court,"
                             "  'PARTY_TYPE' as type_code,'当事人类型' as type_name,"
                             "  '个人' as type_param_code,'个人' as type_param_name,sum(person_cnt) as cnt "
                             "  FROM pg_ws_judgecase "
                             "  GROUP BY judge_name,court ) as stat "
                             "LEFT OUTER JOIN pg_judge_info info "
                             "ON  nvl(stat.judge_name,'1')=nvl(info.name,'1') "
                             "  and nvl(stat.court,'1')=nvl(info.court,'1') ")

    # 拆解合作法官数组
    partnerDf = spark.sql("select judge_name,court,partners from pg_ws_judgecase") \
        .rdd \
        .flatMap(lambda x: [[x.judge_name, x.court, partner] for partner in x.partners])
    spark.createDataFrame(partnerDf, ['judge_name', 'court', 'partner']) \
        .createOrReplaceTempView('pg_tv_partner')
    # 按合作法官统计
    statByPartner = spark.sql("select info.id as judge_id, "
                              "stat.judge_name as judge_name,"
                              "stat.court,"
                              "stat.type_code,"
                              "stat.type_name,"
                              "stat.type_param_code,"
                              "stat.type_param_name,"
                              "info.judicial_doc_cnt as all_cnt,"
                              "stat.cnt "
                              "from (select judge_name,court,"
                              "  'COOPERATE_JUDGE' as type_code,'合作法官' as type_name,"
                              "  partner as type_param_code,court as type_param_name,count(*) as cnt "
                              "  FROM pg_tv_partner "
                              "  GROUP BY judge_name,court,partner ) as stat "
                              "LEFT OUTER JOIN pg_judge_info info "
                              "ON  nvl(stat.judge_name,'1')=nvl(info.name,'1') "
                              "  and nvl(stat.court,'1')=nvl(info.court,'1') ")

    # 拆解律师数组
    lawyerDf = spark.sql("select judge_name,court,lawyers from pg_ws_judgecase") \
        .rdd \
        .flatMap(lambda x: extractJudgeWithLawyer(x))
    spark.createDataFrame(lawyerDf, ['judge_name', 'court', 'lawyer_name', 'lawyer_office']) \
        .createOrReplaceTempView('pg_tv_lawyer')
    # 按合作律师统计
    statByLawyer = spark.sql("select info.id as judge_id, "
                             "stat.judge_name as judge_name,"
                             "stat.court,"
                             "stat.type_code,"
                             "stat.type_name,"
                             "stat.type_param_code,"
                             "stat.type_param_name,"
                             "info.judicial_doc_cnt as all_cnt,"
                             "stat.cnt "
                             "from (select judge_name,court,"
                             "  'RELATED_LAWYER' as type_code,'关联律师' as type_name,"
                             "  lawyer_name as type_param_code,lawyer_office as type_param_name,count(*) as cnt "
                             "  FROM pg_tv_lawyer "
                             "  GROUP BY judge_name,court,lawyer_name,lawyer_office ) as stat "
                             "LEFT OUTER JOIN pg_judge_info info "
                             "ON  nvl(stat.judge_name,'1')=nvl(info.name,'1') "
                             "  and nvl(stat.court,'1')=nvl(info.court,'1') ")

    # 合并 写入最终结果表
    resultDf = statByCase.unionAll(statByProcd) \
        .unionAll(statByCompany) \
        .unionAll(statByPerson) \
        .unionAll(statByPartner) \
        .unionAll(statByLawyer)
    resultDf.write.mode("overwrite").saveAsTable("pg_judge_info_attr")

    spark.stop()
