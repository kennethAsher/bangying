"""
@author : kennethAsher
@fole   : es_insert_es_judgecase.py
@ctime  : 2020/5/18 17:43
@Email  : 1131771202@qq.com
@content: 将清洗好的judgecase数据上传至es
"""


from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
es = Elasticsearch(['http://es-cn-0pp14imrb00093moi.public.elasticsearch.aliyuncs.com'],
                   http_auth=('elastic','TytxsP^tr!BvCayo'),
                   port=9200)


# path = '/mnt/disk2/data/sum_data/result/ws_judgecase/'
path = 'D:\\es_data\\ws_judgecase\\'
names = os.listdir(path)
lst = []
for name in names:
    with open('{}{}'.format(path,name), 'r', encoding='utf8') as file_open:
        lines = file_open.readlines()
        k = len(lines)
        flag = 0
        for step,line in enumerate(lines):
            flag += 1
            fields = line.strip().split('|')
            lst.append(fields)
            _id = int(fields[0])
            judge_name = fields[1]
            judge_status = fields[2]
            person_cnt = int(fields[3])
            company_cnt = int(fields[4])
            court = fields[5]
            courtlevel = fields[6]
            docid = fields[7]
            casereason = fields[8]
            casetype = fields[9]
            doctype = fields[10]
            trialprocedure = fields[11]
            judgeyear = fields[12]
            judgemonth = fields[13]
            judgedate = fields[14]
            lawyer_list = []
            if len(fields[15])>2:
                lawyers = fields[15].split(',')
                for l in lawyers:
                    lawyer_list.append({'name':l.split('-')[0], 'office':l.split('-')[1]})
            lawyers = fields[15].split(',')
            judge_list = []
            if len(fields[16])>2:
                judges = fields[16].split(',')
                for j in judges:
                    judge_list.append(j.split('-')[-1])
            lst.append([_id,judge_name,judge_status,person_cnt,company_cnt, court, courtlevel,docid, casereason,casetype, doctype, trialprocedure,judgeyear,judgemonth,judgedate,lawyer_list,judge_list])
            if len(lst)> 1000 or k-1 == step:
                

                lst = []


            


def batch_data(lines,k):
    """ 批量写入数据 """
    while len(lines) > 0:
        the_lines = []
        for i in range(0, 1000):
            if len(lines) == 0:
                break
            the_lines.append(lines.pop(0))
        action = ({
            "_index": "test_pg_judge_info_ken",
            "_type": "doc",
            "_source": {
                "id": int(fields[0]),
                "name":fields[1],
                "court": fields[2],
                "court_level": fields[3],
                "earliest_year": fields[4],
                "judicial_doc_cnt":int(fields[6]),
                "last_year_judicial_cnt":int(fields[7]),
                "data_source":0,
                "court_proceeding_type":fields[8].replace('-','|')
            }
        } for fields in the_lines)
        helpers.bulk(es, action)
        k +=1000
        print('传输了{}条'.format(k))

if __name__ == '__main__':
    k = 0
    lines = []
    # path = '/mnt/disk1/data/utils_data/judge_data/judge_count/judge_count'
    path = 'D:\\judge_data\\judge_info\\judge_info_result'
    lines = load_data(lines, path)
    print('开始...')
    batch_data(lines,k)
    print('上传完成')