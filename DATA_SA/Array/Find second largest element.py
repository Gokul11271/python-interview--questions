# Find second largest element

# Without sorting — O(n) time.





arr1 = [10,20,30,40,50,60,70,80,90,100]
target=30
for i in range(len(arr1)):
    for j in range(i+1,len(arr1)):
        if i+j==target:
            print(arr1[i],arr1[j])
