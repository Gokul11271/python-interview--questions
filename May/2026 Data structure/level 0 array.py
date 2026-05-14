"ARRAYS (LISTS) Python uses Lists."

"""1. Find Something
max
min
sum
second largest

"""


# arr = [10,20,30,40,100,40]
# for i in arr:
#     for j in arr:
#        if i < j:
#           a=j
# print(a)

           


# print(max(arr))



# a=5
# greater=0
# for i in range(a):
    
#     for j in range(i+1,a):
#         print(i,j)
#         if i< j :
#             print("*********",i)
#             greater=j
# print(greater)


arr = [4, 7, 1, 9, 2000,70 ,30,203,44]
gt=arr[0]
for i in range(len(arr)):
    for j in range(i+1,len(arr)):
        if arr[i] > arr[j] :
          
            gt=arr[i]
print(gt)




