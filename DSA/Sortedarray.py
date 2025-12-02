list=[10,22,34,500,67,89,18,23]
print(list)
print()
for i in range(len(list)):
    for j in range(i+1,len(list)):
        if list[i]>list[j]:
            list[i],list[j]=list[j],list[i]
print(list) 