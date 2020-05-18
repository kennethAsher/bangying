# -*- coding:utf-8 -*-


from elasticsearch import Elasticsearch

def get_mapping_action(dir_name, i):
    mapping = {}
    actions = open(dir_name, 'r', encoding='utf8')
    for line in actions.readlines():
        mapping[line.strip()] = "CAUSE_OF_ACTION_{}".format(i)
    return mapping

es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)
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

#测试
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
# result = es.search(index='news', doc_type='politics')
#通过全文检索
# dsl = {'query':{'match':{'title':'中国 领事馆'}}}
# result = es.search(index='news', doc_type='politics', body=dsl)
# print(result)

#查询某个字段的所有
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

mapping1 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action.txt", 1)
mapping2 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action2.txt", 2)
mapping3 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action3.txt", 3)
mapping4 = get_mapping_action("D:\\lawyer\\cause_of_action\\cause_of_action4.txt", 4)
mapping = dict(list(mapping1.items()) + list(mapping2.items()) + list(mapping3.items()) + list(mapping4.items()))

def insert_cause(fields):
    if fields[5] not in mapping:
        return
    data_cause = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": mapping[fields[5]],
                  "type_name": "案由", "type_param_code": fields[5], "type_param_name": fields[5],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_cause)

def insert_court(fields):
    data_court = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": "COURT_OR_ARBITRATION_AGENCY",
                  "type_name": "管辖机构", "type_param_code": fields[3], "type_param_name": fields[3],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_court)

def insert_area(fields):
    data_area = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": "WORK_AREA",
                  "type_name": "地域", "type_param_code": fields[9], "type_param_name": fields[9],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_area)

def insert_proceeding(fields):
    data_proceeding = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                  "type_code": "COURT_PROCEEDING",
                  "type_name": "审理程序", "type_param_code": fields[4], "type_param_name": fields[4],
                  "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
    es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_proceeding)

def insert_judge(fields):
    if fields[8] == "":
        pass
    if ',' not in fields[8]:
        data_judge = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                           "type_code": "JUDGE_PERSON",
                           "type_name": "审判人员", "type_param_code": fields[8], "type_param_name": fields[8],
                           "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
        es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_judge)
    if ',' in fields[8]:
        lists = fields[8].split(',')
        for i in lists:
            data_judge = {'lawyer_id': int(fields[0]), 'lawyer_name': fields[6], "lawyer_organ_name": fields[7],
                               "type_code": "JUDGE_PERSON",
                               "type_name": "审判人员", "type_param_code": i, "type_param_name": i,
                               "first_year": fields[2][:4], "casereason_set":fields[10], "trialprocedure_set":fields[11]}
            es.index(index='pg_lawyer_info_attr_ken', doc_type='doc', body=data_judge )
file_in = open("D:\\lawyer\\lawyer_add_set\\lawyer_add_set.txt", 'r', encoding='utf8')
k = 0
for line in file_in.readlines():
    if k % 100 == 0:
        print(k)
    k = k+1
    fields = line.strip().split('|')
    fields[10] = fields[10].replace('[',"").replace(']','').replace("'","").split(',')
    fields[11] = fields[11].replace('[', "").replace(']', '').replace("'", "").split(',')
    insert_cause(fields)
    insert_court(fields)
    insert_area(fields)
    insert_proceeding(fields)
    insert_judge(fields)

# dsl = {'query':{'match':{'type_name':'案由'}}}
# result = es.search(index='pg_lawyer_info_attr_ext', doc_type='doc', body=dsl)
# print(result)