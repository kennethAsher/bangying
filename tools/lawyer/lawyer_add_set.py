"""
@author: kennethAsher
@fole  : lawyer_add_set.py
@ctime : 2019/12/26 10:40
@Email : 1131771202@qq.com
"""


# file_in = open('D:\\part_06_out.txt', 'r', encoding='utf8')




# def get_set(fields):
#     # flag = 0
#     casereson_set = set()
#     trialprocedure_set = set()
#     file_in2 = open('D:\\lawyer\\lawyer_merge\\lawyer_merge.txt', 'r', encoding='utf8')
#     for line1 in file_in2.readlines():
#         # if flag%10000 == 0:
#         #     print('flag:',flag)
#         # flag = flag+1
#         fd1 = line1.strip().split('|')
#         if fields[6] == fd1[6] and fields[7] == fd1[7]:
#             casereson_set.add(fields[4])
#             trialprocedure_set.add(fields[5])
#     return casereson_set,trialprocedure_set
#


def get_mapping(f):
    mapping = {}
    file_in1 = open('D:\\lawyer\\lawyer_merge\\lawyer_merge.txt', 'r', encoding='utf8')
    for line in file_in1.readlines():
        if f%10000 == 0:
            print('mapping:',f)
        f = f+1
        fields = line.strip().split('|')
        key_case = fields[6]+fields[7]+'c'
        key_trial = fields[6]+fields[7]+'t'
        if key_case in mapping:
            mapping[key_case].add(fields[4])
        if key_trial in mapping:
            mapping[key_trial].add(fields[5])
        if key_case not in mapping:
            mapping[key_case] = set()
            mapping[key_case].add(fields[4])
        if key_trial not in mapping:
            mapping[key_trial] = set()
            mapping[key_trial].add(fields[5])
    file_in1.close()
    return mapping




if __name__ == '__main__':
    f = 0
    k = 0
    mapping = get_mapping(f)
    file_in = open('D:\\lawyer\\lawyer_merge\\lawyer_merge.txt', 'r', encoding='utf8')
    file_out = open('D:\\lawyer\\lawyer_add_set\\lawyer_add_set.txt', 'w', encoding='utf8')
    for line in file_in.readlines():
        if k % 10000 == 0:
            print(k)
        k = k + 1
        fields = line.strip().split('|')
        key_case = fields[6] + fields[7] + 'c'
        key_trial = fields[6] + fields[7] + 't'
        casereson_set = mapping[key_case]
        trialprocedure_set = mapping[key_trial]
        file_out.write(line.strip() + f'|{list(casereson_set)}|{list(trialprocedure_set)}\n')
    file_in.close()
    file_out.close()