# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/4/15 11:11 上午
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 开始整那些标的额啦
'''

import re
import os
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

mapping = {
	     "properties":{
		     "comments":{
			    "type":"nested"
			 }
		 }
  }
es.indices.delete(index='test_1', ignore=[400, 404])
# es.indices.create(index='test_1', ignore=400)
# result = es.indices.put_mapping(index='test_1', doc_type='doc', body=mapping)
# print(result)


#
# data = {
#   "title":"Nest eggs",
#   "body":  "Making your money work...",
#   "tags":  [ "cash", "shares" ],
#   "comments":[
#      {
# 	  "name":    "John Smith",
#       "comment": "Great article",
#       "age":     28,
#       "stars":   4,
#       "date":    "2014-09-01"
# 	 },
# 	 {
#       "name":    "Alice White",
#       "comment": "More like this please",
#       "age":     31,
#       "stars":   5,
#       "date":    "2014-10-22"
#      }
#   ]
# }
# es.index(index='test_1', doc_type='doc', body=data)



#通过全文检索
# dsl = {
#     'query':{
#         "bool":{
#             "must":[
#                 {"match":{"comments.name":"Alice"}},
#                 {"match":{"comments.age":28}}
#             ]
#         }
#     }
# }
# result = es.search(index='test_1', doc_type='doc', body=dsl)
# print(result)