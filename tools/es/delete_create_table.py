"""
@author : kennethAsher
@fole   : delete_create_table.py
@ctime  : 2020/1/13 17:14
@Email  : 1131771202@qq.com
@content: 删除就得es表并且插入新的表
"""

from elasticsearch import Elasticsearch

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)

# # 删除
# result = es.indices.delete(index='test_1', ignore=[400, 404])
# print(result)
# # 创建
# result = es.indices.create(index='test_1', ignore=400)
# print(result)

# 设置字段数据类型的新建表
mapping = {
     "properties":{
         "partners":{
            "type":"nested"
         },
         "opponents":{
            "type":"nested"
         },
         "justices":{
            "type":"nested"
         }
     }
  }
es.indices.delete(index='test_pg_ws_lawyercase_ken', ignore=[400, 404])
es.indices.create(index='test_pg_ws_lawyercase_ken', ignore=400)
result = es.indices.put_mapping(index='test_pg_ws_lawyercase_ken', doc_type='doc', body=mapping)
print(result)


#ignore 如果报此类错误的话，不会终止程序
# 创建
# result = es.indices.create(index='pg_lawyer_info_attr_ken', ignore=400)

# 删除
# result = es.indices.delete(index='news', ignore=[400, 404])

#插入--crete需要指定id
# data = {'title': '美国留给伊拉克的是个烂摊子吗', 'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm13231'}
# result = es.create(index='news', doc_type='politics', id=1, body=data)
#--index，不需要指定id
# data = {'title': '美国留给伊拉克的是个烂摊子吗??', 'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm??'}
# result = es.index(index='news', doc_type='politics', body=data)

#更新，指定id即可
# data = {
#     'title': '美国留给伊拉克的是个烂摊子吗',
#     'url': ['http://view.news.qq.com/zt2011/usa_iraq/index.htm','http://view.news.qq.com/zt2011/usa_iraq/index.htm12','http://view.news.qq.com/zt2011/usa_iraq/index.htm343'],
#     'date': '2011-12-16'
# }
# result = es.update(index='news', doc_type='politics', body=data, id=1)
# result = es.index(index='news', doc_type='politics', body=data, id=1)

#删除  指定id
# result = es.delete(index='news', doc_type='politics', id=1)

#设置表的格式
# mapping = {
#     'properties':{
#         'title':{
#             'type': 'text',
#             'analyzer': 'ik_max_word',
#             'search_analyzer': 'ik_max_word'
#         }
#     }
# }
# es.indices.delete(index='news', ignore=[400, 404])
# es.indices.create(index='news', ignore=400)
# result = es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
# datas = [
#     {'title':'美国留给伊拉克的是个烂摊子吗','url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm','date': '2011-12-16'},
#     {'title': '公安部：各地校车将享最高路权','url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml','date': '2011-12-16'},
#     {'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船','url': 'https://news.qq.com/a/20111216/001044.htm','date': '2011-12-17'},
#     {'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首','url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml','date': '2011-12-18'}
# ]
# #
# for data in datas:
#     result = es.index(index='news', doc_type='politics', body=data)
#     print(result)

#查询：查询所有
# result = es.search(index='test_pg_ws_lawyercase_ken', doc_type='politics')
#通过全文检索
# dsl = {'query':{'match':{'docid':'aef6203d-370e-4247-9979-a86500962ded'}}}
# result = es.search(index='test_pg_ws_lawyercase_ken', doc_type='doc', body=dsl)
# print(result)

# 查询某个字段的所有
# dsl = { "_source":"docid"}
# query = es.search(index='pg_ws_parsed', body=dsl, scroll='5m',size=100)
# results = query['hits']['hits'] # es查询出的结果第一页
# total = query['hits']['total']  # es查询出的结果总量
# scroll_id = query['_scroll_id'] # 游标用于输出es查询出的所有结果
#
# for i in range(0, int(total/100)+1):
#     # scroll参数必须指定否则会报错
#     query_scroll = es.scroll(scroll_id=scroll_id,scroll='5m')['hits']['hits']
#     results += query_scroll
# ln = set()
# for hits in results:
#     ln.add(hits['_source']['docid'])
# for line in ln:
#     file_out.write(line.strip()+'\n')