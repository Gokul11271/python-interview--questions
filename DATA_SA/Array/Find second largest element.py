# Find second largest element

# Without sorting — O(n) time.

arr=[100,200,300,400,500]
arr1=[]
for i in range(len(arr)):
    for j in arr:
        if i > j :
          arr1.append(i)
        print(i)