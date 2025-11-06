# Linear search
# Return index if found else -1


arr=[1,2,3]
b= arr[-1]
for i in arr:
    if  i == b:
        index=arr[-i]
        print("-",index)
    else:
        print(-1)
