l = [('two', 2), ('five', 5), ('three', 3)]

m = l.sort(key=lambda x:-x[1])
# m = sorted(l, key=lambda x:-x[1])

print(l)
print(m)