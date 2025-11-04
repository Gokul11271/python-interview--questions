arr = [1,2,3,4,5,6,7,8,9,10]
print(len(arr))
target = 7

for i in range(len(arr)):  # i = index (0..9)
    if arr[i] == target:
        print("value of the target:", arr[i])
        print("index of the array:", i)
fdv