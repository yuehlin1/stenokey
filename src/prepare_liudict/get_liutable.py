from get_zidian import zidian
from collections import Counter

# from zidian Dict[character, malist] to Dict[ma, characterlist]


# print(zidian)

# remove ma that is not optimal, i.e. not written with lowercase

cooptimal = []

# print(zidian["冰"])
for (k, vlist) in zidian.items():
    zidian[k] = list(filter(lambda x: x.upper()==x, vlist))
    cooptimal.append(len(zidian[k]))
        
cooptimal = Counter(cooptimal)
# print(cooptimal)
# print(zidian['冰'])
    
    
ma_dian = {}

for (zi, ma_list) in zidian.items():
    for ma in ma_list:
        # zi will be replaced if they share the same ma
        ma_dian[ma] = zi


with open("liu_standard.txt", 'w', encoding='utf-8') as f:
    for (ma, zi) in ma_dian.items():
        f.write(f"{ma.strip()} {zi.strip()}\n")