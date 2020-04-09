"""
@author: kennethAsher
@fole  : local_lawyer_mysql.py
@ctime : 2019/12/20 20:28
@Email : 1131771202@qq.com
"""
import os
import pymysql

data_dir = 'D:\\lawyer\\lawyer_out\\'
def insert_mysql(name):
    print(data_dir+name)
    file_open = open(data_dir+name, 'r', encoding='utf-8')
    # id = 1000695272
    conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com', user='pg_db', password='ds930$232aH!@#FD', db='pg_simulate', charset='utf8')
    cursor = conn.cursor()
    i = 0
    for line in file_open.readlines():
        i = i+1
        if i%1000 ==0:
            print(i)
        fields = line.strip().split('|')
        sql = 'select id from pg_lawyer_copy1 where lawyer_name="{}" and organ_name="{}"'.format(fields[5], fields[6])
        cursor.execute(sql)
        info1 = cursor.fetchone()
        if info1 is None:
            # id = id + 1
            item = (fields[5],None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,fields[6],None,None,None,None,None,None,None,
                    None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,
                    None,None,None,)
            sql = 'insert into `pg_lawyer_copy2` ( `lawyer_name`, `lawyer_sex`,`id_card_no`,`political_status`,`birthday`,`nation`,`education`,' \
                  '`lawyer_license_no`,`lawyer_license_date`,`lawyer_type`,`lawyer_state`,`cert_no`,`cert_type`,`cellphone`,`telephone`,`email`,`addr`,' \
                  '`organ_name`,`organ_type`,`unified_social_credit_code`,`person_in_charge`,`organ_state`,`organ_phone`,`organ_addr`,`agency_in_charge`,`professional_field`,`personal_profile`,' \
                  '`teacher`,`school`,`graduation`,`province`,`city`,`county`,`litigation_start_date`,`user_id`,`main_client`,`classic_case`,' \
                  '`social_duties`,`publication`,`honor`,`other_follow_info`,`role_ids`,`field_ids`,`position`,`appellation`,`area`,`head_img_url`,' \
                  '`agent_year`,`all_cnt`,`is_collection`,`new_task`,`practice_lawyer_type`,`trainee_lawyer_card`) values (%s, %s,%s, %s,%s, %s,' \
                  '%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,' \
                  '%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)'
            cursor.execute(sql, item)

    #没有提交成功是因为插入语句没有commit
    conn.commit()
    cursor.close()
    conn.close()

dirs = os.listdir(data_dir)
for dir in dirs:
    insert_mysql(dir)