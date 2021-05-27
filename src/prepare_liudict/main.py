import itertools
# generate string files separated by 'c' s

一碼字 = 'abcdefghijklmnopqrstuvwxyz'
二碼字 =  itertools.product(一碼字, repeat=2)
三碼字 =  itertools.product(一碼字, repeat=3)
# 四碼字 =  itertools.combinations_with_replacement(一碼字, 4)

三碼字 = list(三碼字)
四碼字 = {}
for letter in 一碼字:
    四碼字[letter] = list(map(lambda x: letter+''.join(x), 三碼字))

print(四碼字['b'])


def 碼字化長串(碼字):
    l = []
    for 字碼 in  map(lambda x: ''.join(x), 碼字):
        l.append(字碼)
        l.append(" c ")
    return l

with open("二碼字.txt", "w", encoding='utf-8') as f:
    f.write(''.join(碼字化長串(二碼字)))

with open("三碼字.txt", "w", encoding='utf-8') as f:
    f.write(''.join(碼字化長串(三碼字)))

# for letter in 一碼字:
#     with open(f"四{letter}碼字.txt", "w", encoding='utf-8') as f:
#         f.write(''.join(碼字化長串(四碼字[letter])))

# for letter in 一碼字:
#     with open(f"四{letter}碼字中文.txt", "w", encoding='utf-8') as f:
#         f.write('中文')

# def 長串化碼字(string):
#     print(string.split(' c '))

# d = {}

# def update_dict_for(幾):
#     with open(f"{幾}碼字中文.txt", "r", encoding='utf-8') as f:
#         string = f.read()
#         string = string.split("七")
#         # print(len(string))

#     with open(f"{幾}碼字.txt", 'r', encoding='utf-8') as f:
#         keys = f.read()
#         keys = keys.split(" c ")
#         # print(len(keys))
    
#     assert len(keys) == len(string)
#     for (k, s) in (zip(keys, string)):
#         if s != '':
#             d[k] = s

# list(map(update_dict_for, ["二","三"]+[f"四{letter}" for letter in 一碼字]))

# with open("字典.txt", 'w', encoding='utf-8') as f:
#     f.write(str(d))