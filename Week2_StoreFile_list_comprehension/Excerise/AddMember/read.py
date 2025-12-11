name=['a.txt','b.txt','c.txt']

for i in name:
    file = open(i, 'r')
    a=file.read()
    print(a)
file.close()