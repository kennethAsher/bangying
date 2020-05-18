"""
@author : kennethAsher
@fole   : delete_create_table.py
@ctime  : 2020/1/13 17:14
@Email  : 1131771202@qq.com
@content: 删除就得es表并且插入新的表
"""

from elasticsearch import Elasticsearch

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

# 删除
result = es.indices.delete(index='test_pg_judge_info_attr_ken', ignore=[400, 404])
print(result)
# 创建
result = es.indices.create(index='test_pg_judge_info_attr_ken', ignore=400)
print(result)
