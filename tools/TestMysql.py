#!/usr/bin/env python
# -*- coding: utf8 -*-
""" 
@brief : 
@author: linzx
@file  : TestSpark.py
@ctime : 2019/4/28 11:21
"""
import mysql.connector

from LawsuitParser import *

import re
from pyspark.sql import SparkSession


def analyzeJudge(cursor):
    cursor.execute("select name from pg_user_judge_bak WHERE NAME LIKE '%*%' ")
    i=0
    pat=re.compile(r'(&.{1,7};)|(二[О0０Ｏ〇○oO零].*)|�|\+|-|\?|？|([a-zA-Z])|：|:|;|；|=|［|］|（|）|/|_|／|<|﹤|>|﹥|&|＊|\*|\s|\d|#|○')
    for record in cursor:
        if re.match(r'.*[a-wyzA-WYZ\d].*',record[0]) is not None:
            print("{}       {}".format(record[0],pat.sub('',record[0])))
            i+=1
    print("count==",i)

if __name__ == "__main__":

    # spark = SparkSession \
    #     .builder \
    #     .appName("PartyInfoParser") \
    #     .getOrCreate()
    # # spark.sql("use pgdata")
    # mysqlDf = spark.read.format("jdbc").options(url="jdbc:mysql://39.97.101.52:3310/prism1",
    #                                             driver="com.mysql.jdbc.Driver",
    #                                             dbtable="pg_user_judge_syn",
    #                                             user="root", password="H0qZXCwvUvgs6F7N").load()
    # mysqlDf.select("*").createOrReplaceTempView("pg_tv_mysqljudge")
    # rst=spark.sql("select max(id)+1 as id from pg_tv_mysqljudge").collect()
    # for x  in rst:
    #     print(x.id)


    spark = SparkSession \
        .builder \
        .appName("PartyInfoParser") \
        .getOrCreate()
    mysqlConn = mysql.connector.connect(host="39.97.101.52", port=3310, user="root", password="H0qZXCwvUvgs6F7N",
                                        database="prism1")
    cursor = mysqlConn.cursor()
    # analyzeJudge(cursor)
    cursor.execute("select t1.docid as docid,"
                   "t1.title as title,"
                   "t1.caseno as caseno,"
                   "t1.trialprocedure as trialprocedure,"
                   "t1.judgetime as judgetime,"
                   "t1.court as court,"
                   "t1.casetype as casetype,"
                   "t1.doctype as doctype,"
                   "IFNULL(t1.partyinfo,'') as partyinfo,"
                   "IFNULL(t1.tail,'') as tail,"
                   "t1.plaintext as plaintext,"
                   "t1.casereason as casereason ,"
                   "'中级' as courtlevel,"
                   "'北京' as province,"
                   "'北京' as city,"
                   "'北京' as region "
                   " from company_lawsuit t1 "
                   " where docid in('f9fdc73d-2eae-45dc-9cfe-a989012bc63a'"
                   ",'5372567a-98d0-4bee-85d7-a8500114363f'"
                   ",'5800d937-c7f4-494d-8de0-a8fe00424e67')")

    parser = LawsuitParser()
    result = []
    for record in cursor:
        result.append(record)
        # print(record)
    newdf = spark.createDataFrame(result,
                                  ['docid', 'title', 'caseno', 'trialprocedure', 'judgetime',
                                   'court', 'casetype', 'doctype', 'partyinfo', 'tail', 'plaintext',
                                   'casereason', 'courtlevel', 'province', 'city', 'region'])
    # df = newdf.rdd.map(lambda x: parser.parseLawsuit(x)).collect()
    #
    # for x in df:
    #     print("*" * 300)
    #     print("{}--{}\n------------".format(x[0], x[1]))
    #     for party in x[1]:
    #         print(party)
    #     for y in x[1]:
    #         print(y)

    # # 解析当事人信息
    newdf = spark.createDataFrame(newdf.rdd.map(lambda x: parser.parseLawsuit(x)),
                                  ['docid', 'parties', 'justices'])
    newdf.printSchema()

    #
    # # 将结果写hive表
    # newdf.write.mode("overwrite").saveAsTable("pg_ws_parsed")
    # count = spark.sql("select parties from pg_ws_partyinfo ").rdd.map(lambda x: 1 if len(x.parties) > 0 else 0).reduce(
    #     lambda x, y: x + y)
    # print("*********************==={}".format(count))

    spark.stop()
