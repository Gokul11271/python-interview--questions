"""SECTION 8 — Beginner Logic Building"""


"Fibonacci Series"
# ip=5
"op = 0 1 1 2 3"
# answer=0
# print(answer)
# for i in range(ip):
#     answer+=i
#     if answer==0:
#         continue
#     print(answer)

# ip=5
# current=0
# previous=0
# for i in range(5):
#     if i==0 or i==1:
#         print(i) 
#         previous =i
#         print(previous,"prrrr")
#         print(current,"crrr")
#     elif i>1:
                     
#      previous+=current+previous
#      current=previous

#      print(previous)
#      print("current",current)


#     |c  |n  | s | O |
# 
# | 1 | 0 | 1 | 1 | 0 |
# | 2 | 1 | 1 | 2 | 1 |
# | 3 | 1 | 2 | 3 | 1 |
# | 4 | 2 | 3 | 5 | 2 |
# | 5 | 3 | 5 | 8 | 3 |
# | 6 | 5 | 8 | 13 | 5 |
# | 7 | 8 | 13 | 21 | 8 |
# ip=5
# c=0
# n=0
# s=1
# for i in range(ip):
#     if i ==0 or i==1:
#         n=i
#         print(i)
#     elif i > 1:
#         c=n
#         print("iteration",i,"current = ",c)
#         n=s
#         print("iteration",i,"new = ",n)
#         s=c+n
#         print("Total",s)


# ip = 5
# a, b = 0, 1
# for i in range(ip):
#     print(a)
#     a, b = b, a + b




"""  so prime number can a like can only did by same and 1 only it should not divid by any other number except 1 and itself"""

""" example 2 → Divisible only by 1 and 2 → ✅ Prime

3 → Divisible only by 1 and 3 → ✅ Prime

4 → Divisible by 1, 2, and 4 → ❌ Not prime (because it has more than two factors)

5 → Divisible only by 1 and 5 → ✅ Prime"""

# prime=10
# for i in range(2,prime):
#     if i ==2:
#         print("it is a prime",i)
#     elif i ** 0.5 < 2:
#         print("it is a prime number",    i)
#     else:
#         print("it is not prime")

# print("3",3 **0.5)
# print("4",4 **0.5)
# print("5",5 **0.5)
# print("6",6 **0.5)
# print("7",7 **0.5)
# print("8",8 **0.5)
# print("9",9 **0.5)

# a=7**0.5
# print(7%a)


# print(3%2)
# print(4%2)
# print(5%2)
# print(6%2)
# print(11%2)
# print(7%2)



# n=7
# for i in range(7,0,-1):
#     if i != n or i != 1:
#          pass
#     elif n % i ==0:
#             print(" it is not a prime",i)
#             continue

#     elif i==n or i == 1:
#         if n % i ==0 :
#             print(" it is a prime")



# n=7
# count=0
# for i in range(1,n+1):
#     if (n % i ==0):
#         count+=1
#         print(i)
#         # print(count)
# if count==2:
#         print("it is a prime number")
# else:
#         print("not a prime number")



# ip = 10
# count=0
# for i in range(1,ip+1):
#        if count==2:
#             print("it is a prime number",i)
#        for j in range(1,ip+1):
#             if i%j==0 :
#                   count +=1


"""Problem 33 — Count Prime Numbers in Range

Input:

1 to 10

Output:

2 3 5 7

"""
# n=5
# count=0
# for i in range(1,n+1):
#     if n % i ==0 :
#         print(i)
#         count+=1
# if count==2:
#     print("i")
# else:
#     print("n")
        

# n=10

# for i in range(2,n+1):
#     count=0
#     for j in range(1,i+1):
       
#        if i % j ==0:
#           count+=1
          
#     if count==2:
#        print(i)
         

"section 9 search"
     
