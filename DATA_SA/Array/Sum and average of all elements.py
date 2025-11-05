# Output: total sum and average value.

arr=[1,2,3,4,5,6]
sum=0
avg=0
for i in arr:
    sum+=i
    avg =sum/len(arr)

print(f"sum of values {sum }, average of the array: {avg}")