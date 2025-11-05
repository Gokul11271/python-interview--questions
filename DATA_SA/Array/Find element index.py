# Find element index

# Input: arr = [5,8,3,9,1], target = 9

# Output: 3



arr = [5,8,3,9,1]
target = 9
for i in range(len(arr)): #total number array index value 
    if arr[i]==target: #array [index] = value so arr[i] accesing the arr elements present in the array
        print(i)       #i carry the index value    