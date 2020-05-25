"""
@author : kennethAsher
@fole   : WSJudgeCase.py
@ctime  : 2020/5/18 9:52
@Email  : 1131771202@qq.com
@content: 从原始数据中拿到ws_judge所需要的数据
            id, judge_name, judge_status(职位),person_cnt(当事人数量), company_cnt(当事人公司数量),court,courtlevel,docid,casereason,casetype(案件类型),
            doctype,trialprocedure(审理程序),judgeyear,judgemonth,judgetime,伙伴名称，关联律师
"""

import os
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/untils/get_data/ws_judgecase.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

class WSJudgeCase():
    def __init__(self):
        self.data_input_path = '/mnt/disk2/data/sum_data/add_result/'
        self.data_out_path = '/mnt/disk2/data/sum_data/result/ws_judgecase/'
        self.pg_id_file = '/mnt/disk2/utils_data/judge/pg_user_judge_20200513.txt'
        self.cause_path = '/mnt/disk2/utils_data/pg_sm_cause_of_action.txt'

        self.judge_id_mapping = {}
        self.cause_mapping = {}

    def get_names(self, path):
        return os.listdir(path)

    def get_fields(self, line):
        return line.strip().split('|')

    def get_cause_mapping(self):
        logging.info('starting to write mapping of {}'.format('cause_mapping'))
        with open(self.cause_path, 'r', encoding='utf8') as cause_open:
            for line in cause_open.readlines():
                fields = self.get_fields(line)
                if len(fields[3]) > 1 and len(fields[1]) > 1:
                    self.cause_mapping[fields[3]] = fields[1]
                if len(fields[2]) > 1 and len(fields[1]) > 1:
                    self.cause_mapping[fields[2]] = fields[1]
                if len(fields[1]) > 1:
                    self.cause_mapping[fields[1]] = fields[1]
        cause_open.close()
        logging.info('ending to write mapping of {}'.format('cause_mapping'))

    def get_judges(self, judge, judges):
        judges_list = judges.split(',')
        for name in judges_list:
            if '书记' in name:
                judges_list.pop(judges_list.index(name))
        judges_list.pop(judges_list.index(judge))
        return judges_list

    # 组建审判人员idmapping， key为name-court value为id
    def get_judge_id_mapping(self):
        logging.info('starting to write mapping of {}'.format('judge_id_mapping'))
        with open(self.pg_id_file, 'r', encoding='utf8') as judge_id_open:
            for line in judge_id_open.readlines():
                fields = self.get_fields(line)
                id = fields[0]
                court_name = fields[1]
                judge_name = fields[2]
                key = judge_name + '-' + court_name
                self.judge_id_mapping[key] = id
        judge_id_open.close()
        logging.info('ending to write mapping of {}'.format('judge_id_mapping'))

    def get_cause_name(self, cause):
        cause_name = ''
        if cause not in self.cause_mapping:
            cause_name = ''
        elif len(cause) > 1:
            cause_name = self.cause_mapping[cause]
        return cause_name

    def write_ws_judgecase(self):
        names = self.get_names(self.data_input_path)
        for name in names:
            logging.info('starting reading file of {} to write result'.format(name))
            with open('{}{}'.format(self.data_input_path, name), 'r', encoding='utf8') as input_file, \
                 open('{}{}'.format(self.data_out_path, name), 'w', encoding='utf8') as out_file:
                for line in input_file.readlines():
                    fields = self.get_fields(line)
                    if len(fields[15]) > 2:
                        judges = fields[15].split(',')
                    else:
                        continue

                    for judge in judges:
                        if '书记' in judge:
                            break
                        if '-' in judge:
                            judge_name = judge.split('-')[1]
                            judge_status = judge.split('-')[0]
                        else:
                            break
                        court = fields[2]
                        key = judge_name+'-'+court
                        if key not in self.judge_id_mapping:
                            continue
                        _id = self.judge_id_mapping[key]
                        person_cnt = 0
                        company_cnt = 0
                        parties = fields[-1].split(',')
                        if len(parties)>0:
                            for party in parties:
                                if '个人' in party:
                                    person_cnt += 1
                                else:
                                    company_cnt += 1

                        court_level = fields[6]
                        doc_id = fields[0]
                        cause_name = self.get_cause_name(fields[18])
                        casetype = fields[11]
                        doc_type = fields[12]
                        trail = fields[10]
                        judge_year = fields[8] if len(fields[8])>1 else ''
                        judge_month = fields[9][:7].replace('-','') if len(fields[9])>1 else ''
                        judge_date = fields[9] if len(fields[9])>1 else ''
                        lawyer = ''
                        if len(fields[13])>1 and len(fields[14])>1:
                            lawyer = fields[13] + '-' + fields[14]
                        if len(fields[16])>1:
                            lawyer = lawyer+','+fields[16]
                        if len(fields[17])>1:
                            lawyer = lawyer+','+fields[17]

                        judge_list = ','.join(self.get_judges(judge, fields[15]))


                        out_line = _id+'|'+judge_name+'|'+judge_status+'|'+str(person_cnt)+'|'+str(company_cnt)+'|'+court+'|'+court_level+'|'+doc_id+\
                                   '|'+cause_name+'|'+casetype+'|'+doc_type+'|'+trail+'|'+judge_year+'|'+judge_month+'|'+judge_date+'|'+lawyer+'|'+judge_list+'\n'
                        out_file.write(out_line)
                input_file.close()
                out_file.close()

    def run(self):
        self.get_judge_id_mapping()
        self.get_cause_mapping()
        self.write_ws_judgecase()

if __name__ == '__main__':
    ws = WSJudgeCase()
    ws.run()