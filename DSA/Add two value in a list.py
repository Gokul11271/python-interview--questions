# Input: l1 = [2,4,3], l2 = [5,6,4]
# Output: [7,0,8]

# l1 = [2,4,3]
# l2 = [5,6,4]

# sum=0
# for i in range(len(l1)):
#     for j in range(len(l2)):
#     #  print(l1[i],"+",l2[j],"=",l1[i]+l2[j])
#      sum=l1[i]+l2[j]
#      print(sum)

# l1 = [1,2,3]
# l2 = [4,5,10]
# carry=0
# count=0
# for i in range(len(l1) -1,-1,-1):
#  for j in range(len(l2)-1,-1,-1):
#   sum=l1[i]+l2[i]+carry
#   print(carry,"💖")
  
# #   print(count,"=",sum)
#   if sum > 9:
#    carry=sum//10
#    sum=sum%10
# #    print(carry,"carry")
#    print(sum,"sum + carry")
#    print(carry)
#   else:
#    print(sum,"sum 🔥",end=" ")
#    carry=0



l1 = [1,2,3]
l2 = [4,5,10]
carry=0

for i in range(len(l1) -1,-1,-1):
#  for j in range(len(l2)-1,-1,-1):
  sum=l1[i]+l2[i]+carry
#   print(carry,"💖")
  
#   print(count,"=",sum)
  if sum > 9:
   carry=sum//10 #13 1
   sum=sum%10 # 3
#    print(carry,"carry")
   print(sum,end=" ")
#    print(carry)
  else:
   print(sum,end=" ")
   carry=0