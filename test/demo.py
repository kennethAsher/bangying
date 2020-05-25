"""
@author: kennethAsher
@fole  : demo.py
@ctime : 2020/1/8 14:24
@Email : 1131771202@qq.com
"""



# money_pat = re.compile(r'[0-9]')

# def cceptCost_2_subjectCost(money):
#     if money <= 50:
#         return 10000
#     if money <= 2300:
#         return (money-50)/0.025 + 10000
#     if money <= 4300:
#         return (money-2300)/0.02 + 100000
#     if money <= 8800:
#         return (money-4300)/0.015 + 200000
#     if money <= 13800:
#         return (money-8800)/0.01 + 500000
#     if money <= 22800:
#         return (money-13800)/0.009 + 1000000
#     if money <= 46800:
#         return (money-22800)/0.008 + 2000000
#     if money <= 81800:
#         return (money - 46800) / 0.007 + 5000000
#     if money <= 141800:
#         return (money - 81800) / 0.006 + 10000000
#     if money > 141800:
#         return (money - 141800) / 0.005 + 20000000

# accept_pat = re.compile(r'保全费(\d+(\.\d+)?)元')
# accpet_split_pat = re.compile(r'(原告|被告|[承负]担)')
# line = '本案受理费3521元，减半收取1761元，诉讼保全费，合计诉讼费3106元，由五被告负担'
# a = accept_pat.findall(line.replace('，','').replace(',',''))
# print()
# l = accpet_split_pat.split(a)
# print(l)
# for i in l:
#     print(i)


# juticesPat = re.compile(r'(院长'
#                         r'|审判长'
#                         r'|审[判理]员|代审[判理]员|代理审[判理]员|助理审[判理]员|人民审[判理]员|助审员'
#                         r'|法官助理'
#                         r'|执行员'
#                         r'|人[民员]陪[审判]员?|陪[审判]员?|代理陪[审判]员?'
#                         r'|书记[员]?|代理书记[员]?|代书记[员]?|实习书记[员]?|见习书记[员]?)[:：]?')
# line = '审判长门伟审判员于青审判员王天松二〇一四年一月三日书记员陈屹崧'
# list = juticesPat.split(line)
# print(list)
