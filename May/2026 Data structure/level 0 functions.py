"""Function is a block of resuable code which will exacute untill it is called by their own function name """
"in python we use the def as keword for function "


"simple function"
"syntax   def funtionname ():"
"                     condition or statement "
"                     which execture at lest one time "

# def sum():
#     t = 10 + 340
#     print(t)

# sum()


# def total(a,b):
#     tt=a+b
#     print(tt)

# total(10,100)

# def square(n):
#     return n * n

# result = square(4)

# print(result)



"""  Practice 4

Create functions:

find largest of 2 numbers
check even/odd
calculate factorial  """

# def largest(a,b):
#     if a>b :
#         return(a)
#     else:
#         return(b)
# result = largest(100 ,500)

# print(result)

# def even(e):
#     if e % 2 ==0:
#         return("even numeber")
#     else:
#         return("not even num")
    
# print(even(3))

# f=5
# a=1
# for i in range(1,f+1):
#     a*=i   
# print(a)


def fact(f):
    a=1
    for i in range(1,f+1):
        a*=i
    return(a)
print(fact(3))
print(fact(5))

for i in range(1,11):
    print(fact(i), end=" ")