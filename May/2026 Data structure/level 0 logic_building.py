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

ip=5
current=0
previous=0
for i in range(5):
    if i==0 or i==1:
        print(i) 
        previous =i
        if i ==1:
         print(previous)
previous+=current+previous
current=previous

print(previous)
print("current",current)