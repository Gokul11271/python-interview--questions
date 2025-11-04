arr = [10, 20, 30, 40]
print(arr[0])    # 10 (first element)
print(arr[2])    # 30

# Negative indices
print(arr[-1])   # 40 (last)
print(len(arr))  # 4

# safe access check to avoid IndexError
i = 5
if 0 <= i < len(arr):
    print(arr[i])
else:
    print("index out of range")
