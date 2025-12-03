# Input: l1 = [2,4,3], l2 = [5,6,4]
# Output: [7,0,8]

l1 = [2,4,3]
l2 = [5,6,4]
# sum=0
# for i in range(len(l1)):
#     for j in range(len(l2)):
#     #  print(l1[i],"+",l2[j],"=",l1[i]+l2[j])
#      sum=l1[i]+l2[j]
#      print(sum)
for i in l1:
   
    for j in l2:
        print(i,j)
        print(i+j)
        i+=1
        
        break
       