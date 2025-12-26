def sorted_squared_best(array):
    return sorted(x *x for x in array )

print(sorted_squared_best([1,5,2,3]))

# this is nlog(n)- Algorithm 