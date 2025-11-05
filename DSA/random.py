# arr = [1,2,3,4,5,6,7,8,9,10]
# print(len(arr))
# target = 7

# for i in range(len(arr)):  # i = index (0..9)
#     if arr[i] == target:
#         print("value of the target:", arr[i])
#         print("index of the array:", i)
arr = [10,20,30,40,50,60,70,80,90,100]
target=30
for i in range(len(arr)):
    for j in range(i+1,len(arr)):
        if i+j==target:
            print(arr[i],arr[j])
            


for i in arr:
    for j in arr:
        if i + j== target:
            print(i, j)
