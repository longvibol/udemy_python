def sorted_squared_best(array):
    n = len(array)
    i,j = 0, n-1
    res =[0]*n
    for k in reversed(range(n)):
        if array[i] > array[j]:
            res[k] = array[i]**2
            i+=1
        else:
            res[k] = array[j]**2
            j-=1
    print(res)
    return res

sorted_squared_best([1,2,3,4])