"""
@author: kennethAsher
@fole  : lawyer_add_provice.py
@ctime : 2019/12/25 19:45
@Email : 1131771202@qq.com
"""


import re
import os

provincePat = re.compile(r'.*(河北|山西|辽宁|吉林|黑龙江|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|海南|四川|贵州|云南|陕西|甘肃|青海|台湾).*')
cityPat = re.compile(r'.*(北京|天津|上海|重庆|邯郸|邢台|衡水|石家庄|保定|沧州|廊坊|张家口|承德|秦皇岛|唐山|大同|朔州|忻州|阳泉|吕梁|晋中|长治'
                     r'|晋城|临汾|运城|沈阳市|大连市|鞍山市|抚顺市|本溪市|丹东市|锦州市|营口市|阜新市|辽阳市|盘锦市|铁岭市|朝阳市|葫芦岛市'
                     r'|长春市|吉林市 |四平市|辽源市|通化市|白山市 |松原市|白城市'
                     r'|哈尔滨市|齐齐哈尔市|牡丹江市|佳木斯市|七台河市|大庆市|黑河市|绥化市|伊春市|鹤岗市|双鸭山市|鸡西市'
                     r'|南京|无锡|徐州|常州|苏州|南通|连云港|淮安|盐城|扬州|镇江|泰州|宿迁'
                     r'|杭州市|湖州市|嘉兴市|金华市|丽水市|宁波市|衢州市|绍兴市|台州市|温州市|舟山市'
                     r'|宿州|淮北|亳州|阜阳|蚌埠|淮南|滁州|六安|马鞍山|安庆|芜湖|铜陵|宣城|池州|黄山'
                     r'|福州市|厦门市|泉州市|漳州市|莆田市|宁德市|龙岩市|三明市|南平市'
                     r'|南昌市|九江市|上饶市|抚州市|宜春市|吉安市|赣州市|景德镇市|萍乡市|新余市|鹰潭市'
                     r'|济南|青岛|淄博|威海|烟台|东营|潍坊|日照|德州|泰安|莱芜|菏泽|临沂|枣庄|济宁|聊城|滨州'
                     r'|郑州|开封|洛阳|平顶山|焦作|鹤壁|新乡|安阳|濮阳|许昌|漯河|三门峡|南阳|商丘|信阳|周口|驻马店|济源'
                     r'|武汉|黄石|襄阳|荆州|宜昌|十堰|孝感|荆门|鄂州|黄冈|咸宁|随州'
                     r'|长沙|株洲|湘潭|衡阳|邵阳|岳阳|常德|张家界|益阳|郴州|永州|怀化|娄底'
                     r'|珠海|汕头|佛山|韶关|湛江|肇庆|江门|茂名|惠州|梅州|汕尾|河源|阳江|清远|东莞|中山|潮州|揭阳|云浮|广州|深圳'
                     r'|成都|绵阳|自贡|攀枝花|泸州|德阳|广元|遂宁|内江|乐山|资阳|宜宾|南充|雅安|达州|广安|巴中|眉山'
                     r'|贵阳|六盘水|遵义|安顺|毕节|铜仁'
                     r'|昆明|曲靖|玉溪|昭通|丽江|普洱|保山|临沧|楚雄州|红河州|迪庆州|文山州|西双版纳州|大理州|德宏州|怒江州'
                     r'|西安| 宝鸡|咸阳|铜川|渭南|延安|榆林|汉中|安康|商洛'
                     r'|兰州|嘉峪关|金昌|白银|天水|武威|张掖|酒泉|平凉|庆阳|定西|陇南'
                     r'|西宁|海东|德令哈|格尔木|玉树).*')

def get_area(str):
    area = ''
    if '分所' in str:
        fields = str.strip().split('事务所')
        area = fields[-1].replace('分所', '')
        if ('县' in area) or ('市' in area):
            return area
        else:
            return area + '市'
    else:
        match = cityPat.match(str)
        if match is not None:
            # print(match.group(1)+'市')
            return match.group(1) + '市'
        match = provincePat.match(str)
        if match is not None:
            # print(match.group(1) + '省')
            return match.group(1) + '省'
    return area

def add_area(input_dir, out_dir, name):
    file_in = open('{}{}'.format(input_dir,name), 'r', encoding='utf8')
    file_out = open('{}{}'.format(out_dir,name), 'w', encoding='utf8')
    k = 0
    for line in file_in.readlines():
        if k % 10000 == 0:
            print(k)
        k = k+1
        fields = line.strip().split('|')
        str = fields[7].strip()

        area = get_area(str)
        file_out.write(line.strip()+'|'+area+'\n')


data_dir = 'D:\\lawyer\\\lawyer_add_id\\'
out_dir = 'D:\\lawyer\\lawyer_add_province\\'
dirs = os.listdir(data_dir)
for dir in dirs:
    add_area(data_dir, out_dir, dir)