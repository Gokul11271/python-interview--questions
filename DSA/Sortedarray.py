list=[5,4,3,1,2]
print(list)
print()
for i in range(len(list)):
    for j in range(i+1,len(list)):
        # print(list[i],list[j])
        if list[i]<list[j]:
            list[i],list[j]=list[j],list[i]
            # print(list[i],list[j])
    print(list,"the is the inner loop list")
    
print(list[1]) 
