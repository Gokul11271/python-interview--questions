"""SECTION 6 — Basic Arrays

"""

# arr=[1,2,3,4]
# for i in arr:
#     print(i)

# """sum"""
# arr=[1,2,3]
# sum=0
# for i in arr:
#     sum+=i
# print(sum)

"""Problem 25 — Largest Element

Input:

[4,8,2,9] """

ip=[4,8,2,9,]
for i in range(len(ip)):
    for j in range(len(ip)):
        if ip[i]>ip[j]:
             largest=ip[i]
print(largest)