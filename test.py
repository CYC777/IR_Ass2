tmplist = ["11", "4", "6"]

def my_comparator(x, y):
    num1 = int(x)
    num2 = int(y)
    print num1
    print num2
    return num1 - num2
tmplist.sort(my_comparator)


print str(tmplist)
res = []
res.append("friend")
print res[0]
