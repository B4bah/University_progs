lst = [20, 18, 14, 12, 13, 16, 19]
print(lst)

res = []

for i in range(len(lst)):
    for j in range(i+1, len(lst)):
        if lst[j] > lst[i]:
            res.append(j - i)
            break
    if i >= len(res):
        res.append(...)

print(res)




def prod(num):
    att = 0
    while att < 1000000:
        if '0' in str(att):
            att += 1
        res = 1
        for el in [int(x) for x in str(att)]:
            res *= el
        if res == num:
            return att
        att += 1


print(prod(200))

def func(bricks):

