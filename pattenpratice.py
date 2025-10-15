# n=5
# # for i in range(n):
# #     print()
# #     for j in range(n) :
# #         if i==0:
# #          print("*", end=" ")


# # for i in range(n):
# #     print()
# #     for j in range(n) :
# #         if j==0:
# #          print("*", end=" ")




# # for i in range(n):
# #     print()
# #     for j in range(n) :
# #         if j==0  or i==0 or i==n-1 or j==n-1 or i==j:
# #          print("*", end=" ")
# #         else:
# #            print(" ",end=" ")

             
# # for i in range (n):
# #     print()
# #     for j in range(i):
# #         print("*",end=" ")

# # print()


# # for i in range(n):
# #     print()
# #     for j in range(n):
# #      if (i==0 and j==n-1) or (i==n//2 and j==n-1) or (i==n-1 and j==n-1):
# #         print(" ",end=" ")
# #      elif i==0 or j==0 or i==n-1 or j==n-1 or i==n//2:   
# #         print ("*",end=" ")
# #      else:
# #         print(" ",end=" ")

# #D

# # for i in range(n):
# #     print()
# #     for j in range(n):
# #       if (i==0 and j==n-1) or (i==n-1 and j==n-1 ):
# #          print(" ",end=" ")
# #       elif i==0 or j==0 or i==n-1 or j==n-1:
# #          print("*",end=" ")
# #       else:
# #          print(" ",end=" ")

# #G

# # for i in range (n):
# #     print()
# #     for j in range(n):
    
# #       if (i==0 and j==0)or (i==n-1 and j==0) or (i==n-1 and j==n-1):
# #           print(" ",end=" ")
# #       elif i==0 or j==0 or i==n-1 or (i==n//2 and i+j!=3) or (j==n-1 and i==3) :
# #          print("*",end=" ")
# #       else:
# #          print(" ",end=" ")



# # for i in range(n):
# #     print()
# #     for j in range(n):
# #         if i!=n//2 :
# #             print(" ",end=" ")
# #         elif i==n//2 :
# #             print("*",end=" ")
# #         else:
# #             print(" ",end=" ") 


# # a,b=10,20
# # print(a,b)
# # a,b=b,a
# # print(a,b)
# # # Example of ternary operator in Python
# # x = 5
# # result = "Even" if x % 2 == 0  else "Odd"
# # print(f"{x} is {result}")


# # for i in range(n):
# #     print(" " * (n - i - 1), end="")  # print leading spaces
# #     print("* " * (i + 1))             # print stars with space
# # print()




# ascii_value = 65

# for i in range(n):
#     for j in range(i+1):
#         alphabet = chr(ascii_value)
#         print(alphabet, end=" ")
    
#     ascii_value += 1
#     print()
#  # or print(chr(ord('a')))

# a = 65  # Use integer for ASCII value
# asc = a  # Initialize asc with starting ASCII value
# for i in range(n):
#     print()
#     for j in range(i + 1):
#         value = chr(asc)
#         print(value, end=" ")
#     asc += 1
# print()
# print()
# a = '5'
# b = '5'
# c = int(a) + int(b)
# print(c)  # This will output 10
# #i need op as 10


# a={100:"100",101:"200",103:"300"}
# print(max(a.values()))
# print(max(a.keys()))


# a=[]
# a.append(input())
# print(a)