ip=[1,2,3,4,5]

#[5,4,3,2,1]
# for i in range(len(ip)):
#     pass
    
        
#        if i == j :
#            ip[i],ip[j]=ip[j],ip[i]
#            print(ip[i],ip[j])
# print(ip)
    
# n=len(ip)

# for i in range(len(ip)):
#     for j in range(i+1,n):
#      if i <j :
#         ip[i],ip[j]=ip[j],ip[i]
# print(ip)

#largest
# arr=[1,2,3,40,5]
# maxii=0
# for i in range(len(arr)):
    
#     if maxii<arr[i]:
#         maxii=arr[i]
# print(maxii)

#largest single traversal 

arr=[5,3,8,2,90,10]
maximun=0
for i in range(len(arr)):
    if maximun < arr[i]:
        maximun=arr[i]
print("Largest",maximun)

#smallest single traversal


arr=[5,3,8,2,90,10]
maximun=arr[0]

for i in range(len(arr)):
    if maximun > arr[i]:
        maximun=arr[i]
print("smallest",maximun)

sum=0
for j in range (len(arr)):
    sum+=arr[j]
print("sum of total ",sum)

count=0
acount=0
for k in range(len(arr)):
    if k % 2 ==0:
        count+=1
    else:
        acount+=1
print(count, " =  total even number")
print(acount, " =  total odd number")