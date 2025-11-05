# Find the maximum and minimum element

# Output both value and index.

# 👉 Loop through array, compare, store best.


arr = [5,8,3,9,1]
print(len(arr))
large=0
for i in arr:
    if i >= large:
        large = i
print(large)
