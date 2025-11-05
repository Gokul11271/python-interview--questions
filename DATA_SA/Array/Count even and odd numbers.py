# Count even and odd numbers

# Input: [1,2,3,4,5,6]

# Output: even=3, odd=3

arr=[1,2,3,4,5,6]
even=0
odd=0
for i in arr:
    if i %2 ==0:
        even +=1
    else:
        odd +=1
print(f"even :{even} odd: { odd}")