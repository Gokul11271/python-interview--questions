# Reverse the array

# Without using built-in reverse methods.

# 👉 Use two-pointer swapping or slicing.


arr=[1,2,3,4,5,6]
print(arr[::-1])

arr1=[ ]
for i in arr[::-1]:
    arr1.append(i)
print(arr1)