# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/25 下午5:42
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 测试pyspark筛选出案由和当事
'''



import sys
import os
import datetime
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sc = SparkConf().setAppName("wordcount")
spark = SparkContext(conf=sc)
text_file_rdd = spark.textFile("hdfs:///tmp/pyspark/demo/organ_data/aa")

out_rdd = text_file_rdd.map(lambda line: line.split('|')[1])

short_rdd = out_rdd.filter(lambda line: len(line.split('。')))

out_rdd.saveAsTextFile('hdfs:///tmp/pyspark/demo/output')

spark.stop()