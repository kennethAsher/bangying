# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/24 下午6:48
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : pyspark--wordcount
'''

import sys
import os
import datetime
from pyspark import SparkConf,SparkContext
sc = SparkConf().setAppName("wordcount")
spark = SparkContext(conf=sc)
text_file = spark.textFile("hdfs:///tmp/pyspark/demo/input/a.txt")
word_cnt_rdd = text_file.flatMap(lambda line : line.split(' ')).\
    map(lambda word : (word, 1)).reduceByKey(lambda x, y: x + y)
word_cnt_rdd.saveAsTextFile('hdfs:///shw/wc')

spark.stop()