# Find all pairs with a given sum

# Input: [2,4,3,5,7,8,9], target=10

# Output: (2,8), (3,7), (4,6) (if exists)

# 👉 Practice your current concept.

# Input = [2,4,3,5,6,7,8,9]
# target=10
# for i in range(len(Input)):
#     print("i:",Input[i])
#     for j in range(len(Input)):
#      print("j:                 ",Input[j])
#      if Input[i]+Input[j]==  target :
#          print("oppppp",[Input[i],Input[j]])
arr1 = [10,20,30,40,50,60,70,80,90,100]
target=30
for i in range(len(arr1)):
    for j in range(i+1,len(arr1)):
        if i+j==target:
            print(arr1[i],arr1[j])