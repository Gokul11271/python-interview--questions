"""SECTION 8 — Beginner Logic Building"""


"Fibonacci Series"
ip=5
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
ip=5
c,n=0,0
for i in range(ip):
    if i == 0 or i ==1:
        n=i
        print(i)
    elif i > 1:
        sum=c+n
        print(sum)
         