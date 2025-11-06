# Find duplicates in an array

# Input: [1,2,3,2,1,4]

# # Output: 1,2

Input = [1,2,3,2,1,4]
dup= []
for i in Input:
    if i not in dup:
        dup.append(i)
    else:
        print(i)