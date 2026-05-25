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
f=0
for i in range(ip):
     f+=f+1
     
print(f)
