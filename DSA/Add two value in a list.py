# Input: a = [2,4,3], b = [5,6,4]
# Output: [7,0,8]

# a = [2,4,3]
# b = [5,6,4]

# sum=0
# for i in range(len(a)):
#     for j in range(len(b)):
#     #  print(a[i],"+",b[j],"=",a[i]+b[j])
#      sum=a[i]+b[j]
#      print(sum)

# a = [1,2,3]
# b = [4,5,10]
# carry=0
# count=0
# for i in range(len(a) -1,-1,-1):
#  for j in range(len(b)-1,-1,-1):
#   sum=a[i]+b[i]+carry
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



a = [-1,2,3]
b = [4,5,-10]

carry=0


for i in range(len(a) -1,-1,-1):
#  for j in range(len(b)-1,-1,-1):
  sum=a[i]+b[i]+carry
#   print(carry,"💖")
  
#   print(count,"=",sum)
  if sum > 9:
   carry=sum//10 #13 1
   sum=sum%10 # 3
#    print(carry,"carry")
   print(sum,end=" ")
#    print(carry)
  else:
   print((sum),end=" ")
   carry=0