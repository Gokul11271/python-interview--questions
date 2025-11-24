arr = [10, 20, 5, 90, 56]
count=0
maz=arr[0]

for i  in arr:
    count+=1
    print(count,"max[]",maz,"less than",arr,i )
    if maz<=i:
        maz=i
       
print(maz,"*")