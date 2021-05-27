## get zidian, traditional chr prioritized

import re
import os
#os.chdir(r'C:\Users\victo\Documents\my projet\bosh')


load = True
if load:
    with open('boshiamydict.txt', 'r', encoding='utf-8') as file:
        table = file.read()

    table = table[300:].replace('\n', '  ')
else:
    table = """ㄅㄚ
    笆-> ZCL   吧-> OCL   朳-> TBN   捌-> ,DB   捌-> jonr  捌-> jodr  扒-> JBN
    扒-> jbav  扒-> jba   豝-> EQC   豝-> eqcl  八-> B     粑-> MCL   羓-> BHC
    羓-> bhcl  疤-> LBC   疤-> lbclv 疤-> lbcl  芭-> RCL   仈-> PBNV  仈-> pbn
    釟-> ABNV  釟-> abn   叭-> OBNV  叭-> obn   巴-> CL    巴-> cllv  巴-> cll
    哵-> OODR  哵-> OONR   """.replace('\n', '  ')

def get_zidian():
    dict_table = {}
    indexes = [m.start() for m in re.finditer("->", table)]
    for index in indexes:
        sng, code = (table[index-1], table[index+3:index+7])
        if sng in dict_table.keys():
            dict_table[sng].append(code)
        else:
            dict_table[sng] = [code]
    return dict_table

zidian = get_zidian()



