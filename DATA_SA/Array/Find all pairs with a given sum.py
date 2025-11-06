# Find all pairs with a given sum

# Input: [2,4,3,5,7,8,9], target=10

# Output: (2,8), (3,7), (4,6) (if exists)

# 👉 Practice your current concept.

Input = [2,4,3,5,6,7,8,9]
target=10
for i in range(len(Input)):
    print("i:",Input[i])
    for j in range(len(Input)):
     print("j:                 ",Input[j])
     if Input[i]+Input[j]==  target :
         print("oppppp",[Input[i],Input[j]])
           