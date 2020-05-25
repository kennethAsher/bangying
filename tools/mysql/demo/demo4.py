"""
@author : kennethAsher
@fole   : demo4.py
@ctime  : 2020/5/20 14:52
@Email  : 1131771202@qq.com
@content: 将律师数据插入到律师表中，合并律师，
"""

import pymysql
conn = pymysql.connect(host='rm-2zet9m2x33kh23506o.mysql.rds.aliyuncs.com',
                        user='pg_db',
                        password='ds930$232aH!@#FD',
                        db='pg_test',
                        charset='utf8')
cursor = conn.cursor()


'''
#北京
file_in = open('card_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set lawyer_type='{}', lawyer_state = '{}', organ_name = '{}', organ_type = '{}', person_in_charge = '{}', organ_state='{}',organ_phone='{}',organ_addr='{}', organ_name_orgin='{}' where lawyer_license_no = '{}'"\
        .format(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13],fields[14], fields[3])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()

file_in = open('name_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set lawyer_license_no = '{}', lawyer_type='{}', lawyer_state = '{}', organ_name = '{}', organ_type = '{}', person_in_charge = '{}', organ_state='{}',organ_phone='{}',organ_addr='{}', organ_name_orgin='{}' where lawyer_name = '{}' and  organ_name_orgin='{}'"\
        .format(fields[3],fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13],fields[14], fields[1], fields[14])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()

file_in = open('new_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    sql = "insert into pg_lawyer(lawyer_name,lawyer_sex,lawyer_license_no,lawyer_type,lawyer_state,organ_name,organ_type,unified_social_credit_code,person_in_charge,organ_state,organ_phone,organ_addr,organ_name_orgin) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
        .format(fields[1],fields[2],fields[3],fields[4],fields[5],fields[7],fields[8],fields[9],fields[10],fields[11],fields[12],fields[13],fields[14])
    cursor.execute(sql)
    if step % 1000 == 0:
        print(step)
    conn.commit()
'''



'''
#江苏
file_in = open('card_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set area='{}', organ_name = '{}', education = '{}', id_card_no = '{}', lawyer_type='{}', organ_name_orgin='{}' where lawyer_license_no = '{}'"\
        .format(fields[1],fields[4],fields[8],fields[9],fields[10],fields[11], fields[2])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()

file_in = open('name_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set area='{}',lawyer_license_no = '{}', organ_name = '{}', education = '{}', id_card_no = '{}', lawyer_type='{}', organ_name_orgin='{}' where lawyer_name = '{}' and  organ_name_orgin='{}'" \
        .format(fields[1],fields[2], fields[4], fields[8], fields[9], fields[10], fields[11], fields[3],fields[11])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()

file_in = open('new_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    sql = "insert into pg_lawyer(area,lawyer_license_no,lawyer_name,organ_name,education, id_card_no, lawyer_type, organ_name_orgin) values('{}','{}','{}','{}','{}','{}','{}','{}')"\
        .format(fields[1],fields[2],fields[3], fields[4], fields[8], fields[9], fields[10], fields[11])
    cursor.execute(sql)
    if step % 1000 == 0:
        print(step)
    conn.commit()
'''

'''
#辽宁
file_in = open('card_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set organ_name = '{}',lawyer_sex='{}', nation='{}',id_card_no = '{}' ,education = '{}', cellphone = '{}', lawyer_type='{}', organ_name_orgin='{}' where lawyer_license_no = '{}'"\
        .format(fields[2],fields[3],fields[4],fields[5],fields[6],fields[7], fields[9], fields[-1],fields[11])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()

file_in = open('name_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set organ_name = '{}',lawyer_sex='{}', nation='{}',id_card_no = '{}' ,education = '{}', cellphone = '{}', lawyer_type='{}',lawyer_license_no = '{}' where lawyer_name = '{}' and  organ_name_orgin='{}'" \
        .format(fields[2],fields[3],fields[4],fields[5],fields[6],fields[7], fields[9],fields[11], fields[1],fields[-1])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()


file_in = open('new_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    sql = "insert into pg_lawyer(lawyer_name,organ_name,lawyer_sex,nation,id_card_no,education,cellphone,lawyer_type,organ_name_orgin) values('{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
        .format(fields[1],fields[2],fields[3], fields[4], fields[5], fields[6], fields[9], fields[11], fields[-1])
    cursor.execute(sql)
    if step % 1000 == 0:
        print(step)
    conn.commit()
'''




'''
#上海
file_in = open('card_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set lawyer_name = '{}',organ_name = '{}',lawyer_sex='{}', age = {},nation='{}',education = '{}', lawyer_type='{}',political_status = '{}' , cert_no = '{}',agency_in_charge = '{}', organ_name_orgin='{}' where lawyer_license_no = '{}'"\
        .format(fields[1],fields[3],fields[4],int(fields[5]),fields[6],fields[7],fields[8], fields[9],fields[10],fields[15], fields[-1],fields[2])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()


file_in = open('name_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set organ_name = '{}',lawyer_sex='{}', age = {},nation='{}',education = '{}', lawyer_type='{}',political_status = '{}' , cert_no = '{}',agency_in_charge = '{}',lawyer_license_no = '{}' where lawyer_name = '{}' and  organ_name_orgin='{}'" \
        .format(fields[3],fields[4],int(fields[5]),fields[6],fields[7],fields[8], fields[9],fields[10],fields[15],fields[2], fields[1],fields[-1])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()


file_in = open('new_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    sql = "insert into pg_lawyer(lawyer_name,organ_name,lawyer_sex,age,nation,education,lawyer_type,political_status,cert_no,agency_in_charge,lawyer_license_no,organ_name_orgin) values('{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}')"\
        .format(fields[1],fields[3],fields[4],int(fields[5]),fields[6],fields[7],fields[8], fields[9],fields[10],fields[15],fields[2],fields[-1])
    # print(sql)
    cursor.execute(sql)
    if step % 1000 == 0:
        print(step)
    conn.commit()
'''

'''
#深圳

file_in = open('card_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set lawyer_name = '{}',lawyer_sex='{}',organ_name = '{}', lawyer_type='{}', cert_no = '{}', political_status = '{}', organ_phone='{}' ,organ_name_orgin='{}' where lawyer_license_no = '{}'"\
        .format(fields[1],fields[3],fields[4],fields[5],fields[6],fields[11],fields[-2], fields[-1],fields[8])
    print(sql)
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()


file_in = open('name_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    # print(fields[4],fields[5],fields[7],fields[8],fields[10],fields[11],fields[12],fields[13], fields[3])
    sql = "update pg_lawyer set lawyer_sex='{}',organ_name = '{}', lawyer_type='{}', cert_no = '{}', political_status = '{}', organ_phone='{}' ,lawyer_license_no = '{}' where lawyer_name = '{}' and  organ_name_orgin='{}'" \
        .format(fields[3],fields[4],fields[5],fields[6],fields[11],fields[-2], fields[8],fields[1],fields[-1])
    cursor.execute(sql)
    if step%1000==0:
        print(step)
    conn.commit()
'''

file_in = open('new_temp', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    sql = "insert into pg_lawyer(lawyer_sex,organ_name,lawyer_type,cert_no,political_status,organ_phone,lawyer_license_no,lawyer_name,organ_name_orgin) values('{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
        .format(fields[3],fields[4],fields[5],fields[6],fields[11],fields[-2], fields[8],fields[1],fields[-1])
    print(sql)
    cursor.execute(sql)
    if step % 1000 == 0:
        print(step)
    conn.commit()





'''
file_in = open('C:\\Users\\GG257\\Desktop\\LiaoNinglayer.txt', 'r', encoding='utf8')
for step,line in enumerate(file_in.readlines()):
    fields = line.strip().split('|')
    sql = "update pg_lawyer set id_card_no = '{}',political_status='{}' where lawyer_license_no = '{}'"\
        .format('',fields[4], fields[11])
    cursor.execute(sql)
    if step % 1000 == 0:
        print(step)
    conn.commit()
'''




cursor.close()
conn.close()
