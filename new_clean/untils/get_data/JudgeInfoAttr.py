"""
@author : kennethAsher
@fole   : JudgeInfoAttr.py
@ctime  : 2020/5/13 10:18
@Email  : 1131771202@qq.com
@content:
            上接整理好的add_result数据集
            整理出来judgeinfoattr所需要的数据
            judge_id，judge_name，court，type_code(CAUSE_OF_ACTION_2)，type_name(案由)，type_param_code（合同纠纷），type_param_name(合同纠纷)，      all_cnt(文书总数),      cnt（此typename总数）
                                                  RELATED_LAWYER               关联律师                赵川                       广东君孺律师事务所
                                                  COURT_PROCEEDING             审理程序                名称                       名称
                                                  PARTY_TYPE                   当事人类型               类型名称                   类型名称
                                                  COOPERATE_JUDGE              合作法官                法官名称                    法院

docid|title|court|province|city|area|court_level|docnum|year|date|trail|doctype|bookname|laeyername|organname|judge|friendlawyer|opponent|案由|party
92d0ca7a-89e9-4b45-b848-a93300e8741f|中国太平洋财产保险股份有限公司永康支公司与陈华雄保险人代位求偿权纠纷一审民事裁定书|浙江省永康市人民法院|浙江省|金华市|永康市|基层|(2018)浙0784民初4511号|2019||一审|民事案件|民事裁定书|张镇|浙江从周律师事务所|审判员-施红敏,书记员-李晟洁|徐华军-浙江从周律师事务所||保险人代位求偿权纠纷|原告-中国太平洋财产保险股份有限公司永康支公司-非上市民营,被告-陈华雄-个人

写出审判人员数据，
注意需要过滤掉书记员，我们mysql的数据库中没有过滤掉书记员

"""

import os
import logging

logging.basicConfig(filename='/mnt/disk1/log/python/untils/get_data/judge_info_attr.log',
                    filemode="w",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)

class JudgeInfoAttr():
    def __init__(self):
        # 审判人员id关系路径
        self.pg_id_path = '/mnt/disk2/utils_data/judge/pg_user_judge_20200513.txt'
        # 案由关系路径
        self.cause_path = '/mnt/disk2/utils_data/pg_sm_cause_of_action.txt'
        # 原始数据路径
        self.add_result_path = '/mnt/disk2/data/sum_data/add_result/'
        # 写出路径
        self.write_path = '/mnt/disk2/data/sum_data/result/judge_info_attr'
        # 案由字典
        self.cause_mapping = {}
        # 审判人员-id字典
        self.judge_id_mapping = {}
        # 审判人员案由字典
        self.judge_cause_mapping = {}
        # 审判人员文书数量字典
        self.judge_all_cnt = {}
        # 审判人员审理程序字段
        self.judge_trail_mapping = {}
        # 审判人员当事人类型字段
        self.judge_party_type_mapping = {}
        # 审判人员关联律师
        self.judge_friend_lawyer_mapping = {}
        # 审判人员关联法官
        self.judge_friend_judge_mapping = {}

    def get_dir_names(self, path):
        return os.listdir(path)

    def get_fields(self, line):
        return line.strip().split('|')

    # 从审判人员关系列中返回合作的审判人员，并且去掉其中的书记员
    def get_judges(self, judge, judges):
        judges_list = judges.split(',')
        for name in judges_list:
            if '书记' in name:
                judges_list.pop(judges_list.index(name))
        judges_list.pop(judges_list.index(judge))
        return judges_list

    # 根据当前字段插入mapping
    def insert_mapping(self, key, type,mapping):
        if len(type) > 1:
            if key in mapping:
                values = mapping[key]
                if type + '-' in values:
                    for value in values.split(','):
                        if type + '-' in value:
                            temp_old_value = value
                            num = int(value.split('-')[-1]) + 1
                            new_value = type + '-' + str(num)
                            mapping[key] = values.replace(temp_old_value, new_value)
                            break
                else:
                    mapping[key] = values + ',' + type + '-1'
            else:
                mapping[key] = type + '-1'

    # 组建cause的字典，key为当前的案由，返回值为2级案由名称
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

    # 根据输入的案由返回相应的二级案由，本次将没有收录的案由记录添加
    def get_cause_name(self, cause):
        cause_name = ''
        if cause not in self.cause_mapping:
            cause_name = ''
        elif len(cause) > 1:
            cause_name = self.cause_mapping[cause]
        return cause_name

    # 组建审判人员idmapping， key为name-court value为id
    def get_judge_id_mapping(self):
        logging.info('starting to write mapping of {}'.format('judge_id_mapping'))
        with open(self.pg_id_path, 'r', encoding='utf8') as judge_id_open:
            for line in judge_id_open.readlines():
                fields = self.get_fields(line)
                id = fields[0]
                court_name = fields[1]
                judge_name = fields[2]
                key = judge_name + '-' + court_name
                self.judge_id_mapping[key] = id
        judge_id_open.close()
        logging.info('ending to write mapping of {}'.format('judge_id_mapping'))

    # 组建输出数据所需要的mapping，key为name-court
    def get_judge_mappings(self):
        names = self.get_dir_names(self.add_result_path)
        for name in names:
            logging.info('starting reading file of {} to write mapping'.format(name))
            with open('{}{}'.format(self.add_result_path, name), 'r', encoding='utf8') as add_result_open:
                for line in add_result_open.readlines():
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
                        else:
                            break
                        key = judge_name + '-' + fields[2]
                        # 添加文书总量
                        if key in self.judge_all_cnt:
                            self.judge_all_cnt[key] = self.judge_all_cnt[key] + 1
                        else:
                            self.judge_all_cnt[key] = 1
                        # 添加案由字典
                        cause_name = self.get_cause_name(fields[-2])
                        if len(cause_name)>2:
                            self.insert_mapping(key, cause_name, self.judge_cause_mapping)

                        # 添加审理程序字典
                        trail = fields[10]
                        self.insert_mapping(key, trail, self.judge_trail_mapping)
                        # 添加当事人类型字段
                        party_line = fields[-1]
                        if len(party_line) > 1:
                            for party in party_line.split(','):
                                party_type = party.split('-')[-1]
                                self.insert_mapping(key, party_type, self.judge_party_type_mapping)
                        # 添加关联律师
                        if len(fields[13])>1 and len(fields[14])>1:
                            lawyer = fields[13] + '-' + fields[14]
                            self.insert_mapping(key, lawyer, self.judge_friend_lawyer_mapping)
                        if len(fields[16])>2:
                            friends = fields[16].split(',')
                            for friend in friends:
                                self.insert_mapping(key, friend, self.judge_friend_lawyer_mapping)
                        if len(fields[17]) > 2:
                            oppoents = fields[17].split(',')
                            for oppoent in oppoents:
                                self.insert_mapping(key, oppoent, self.judge_friend_lawyer_mapping)
                        # 添加关联法官
                        if ',' in fields[15]:
                            friends_judges = self.get_judges(judge, fields[15])
                            if len(friends_judges)>0:
                                for friends_judge in friends_judges:
                                    judge_name = friends_judge.split('-')[1]
                                    friend_judge = judge_name+'-'+fields[2]
                                    self.insert_mapping(key, friend_judge, self.judge_friend_judge_mapping)
            add_result_open.close()

    # 写出最终的judge_info_attr数据
    def write_judge_info_attr(self):
        names = self.get_dir_names(self.add_result_path)
        judge_info_attr_write = open(self.write_path, 'w', encoding='utf8')
        judge_set = set()
        for name in names:
            logging.info('starting reading file of {} to write result'.format(name))
            with open('{}{}'.format(self.add_result_path, name), 'r', encoding='utf8') as add_result_open:
                for line in add_result_open.readlines():
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
                        else:
                            break
                        court = fields[2]
                        key = judge_name+'-'+court
                        if key not in self.judge_id_mapping:
                            continue
                        _id = self.judge_id_mapping[key]
                        if _id in judge_set:
                            break
                        judge_set.add(_id)

                        if key in self.judge_cause_mapping:
                            cause = self.judge_cause_mapping[key]
                        else:
                            cause = ''
                        if key in self.judge_all_cnt:
                            all_cnt = str(self.judge_all_cnt[key])
                        else:
                            all_cnt = ''
                        if key in self.judge_trail_mapping:
                            trail = self.judge_trail_mapping[key]
                        else:
                            trail = ''
                        if key in self.judge_party_type_mapping:
                            party = self.judge_party_type_mapping[key]
                        else:
                            party = ''
                        if key not in self.judge_friend_lawyer_mapping:
                            lawyer = self.judge_friend_lawyer_mapping[key]
                        else:
                            lawyer = ''
                        if key in self.judge_friend_judge_mapping:
                            judge = self.judge_friend_judge_mapping[key]
                        else:
                            judge = ''
                        out_line = judge_name+'|'+court+'|'+_id+'|'+cause+'|'+all_cnt+'|'+trail+'|'+party+'|'+lawyer+'|'+judge+'\n'
                        judge_info_attr_write.write(out_line)
            add_result_open.close()
        judge_info_attr_write.close()

    def run(self):
        self.get_cause_mapping()
        self.get_judge_id_mapping()
        self.get_judge_mappings()
        self.write_judge_info_attr()




'''
if len(cause_name) > 1:
    if key in self.judge_cause_mapping:
        values = self.judge_cause_mapping[key]
        if cause_name + '-' in values:
            for value in values.split(','):
                if cause_name + '-' in value:
                    temp_old_value = value
                    num = int(value.split('-')[1]) + 1
                    new_value = cause_name + '-' + str(num)
                    self.judge_cause_mapping[key] = values.replace(temp_old_value, new_value)
                    break
        else:
            self.judge_cause_mapping[key] = values + ',' + cause_name + '-1'

    else:
        self.judge_cause_mapping[key] = cause_name + '-1'
# 添加审理程序字典
trail = fields[10]
if len(trail) > 1:
    if key in self.judge_trail_mapping:
        values = self.judge_trail_mapping[key]
        if trail + '-' in values:
            for value in values.split(','):
                if trail + '-' in value:
                    temp_old_value = value
                    num = int(value.split('-')[1]) + 1
                    new_value = trail + '-' + str(num)
                    self.judge_trail_mapping[key] = values.replace(temp_old_value, new_value)
                    break
        else:
            self.judge_trail_mapping[key] = values + ',' + trail + '-1'

    else:
        self.judge_trail_mapping[key] = trail + '-1'
        
        
        
2607773302
'''
