# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# @Time    : 2020/3/19 下午5:48
# @Author  : kennethAsher
# @Email   : 1131771202@qq.com
# @Content : 比较单条插入与批量插入速度
'''

import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers



es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'], http_auth=('elastic','TytxsP^tr!BvCayo') ,port=9200)
'''单条数据插入速度
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时约 {:.2f} 秒'.format(time.time() - start))
        return res
    return wrapper

@timer
def create_data():
    """ 写入数据 """
    for line in range(1000):
        es.index(index='test_word', doc_type='doc', body={'title': line})

if __name__ == '__main__':
    create_data()   # 执行结果大约耗时 14.01 秒
'''


'''批量插入速度'''
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时约 {:.2f} 秒'.format(time.time() - start))
        return res

    return wrapper
@timer
def batch_data():
    """ 批量写入数据 """
    action = [{
        "_index": "test_word",
        "_type": "doc",
        "_source": {
            "title": i
        }
    } for i in range(1000)]
    helpers.bulk(es, action)


if __name__ == '__main__':
    # create_data()
    batch_data()    #1000条耗时0.28秒




'''
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时约 {:.2f} 秒'.format(time.time() - start))
        return res

    return wrapper
@timer
def batch_data():
    """ 批量写入数据 """
    # 使用生成器
    for i in range(1, 100001, 1000):
        action = ({
            "_index": "s2",
            "_type": "doc",
            "_source": {
                "title": k
            }
        } for k in range(i, i + 1000))
        helpers.bulk(es, action)
'''