st=input()
strrev=""
for i in range(len(st)-1,-1,-1):
    strrev+=st[i]  
    print(strrev) 
if st==strrev:
    print("Palindrome")
else:
    print("Not Palindrome")
    

# st = input("Enter a string: ")
# strrev = st[::-1]

# print("Reversed:", strrev)

# if st == strrev:
#     print("Palindrome")
# else:
#     print("Not Palindrome")
