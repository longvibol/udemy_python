list = [s**2 for s in [1, 2, 3, 4, 5]]
new_list = [ x for x in list if x%2 ==0]
print(new_list)