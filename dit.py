s=['apple','banana','cherry','date','elderberry','fig','grape']   
l=[]
for i in range(len(s)):
    if len(s[i])%2==0:
        l.append((s[i],len(s[i])))
    else:
        l.append((s[i],i))
print(l)
        

s=['apple','orange','ant','banana','cherry','date','elderberry','fig','grape']   
d={}
for i in range(len(s)):
    if len([i]) not in d:
        d[len(s[i])] = [s[i]]
    else:
       d[len(s[i])].append([s[i]])
print(d)



num=1234
sum = 0
while num>0:
   sum = num%10
   num = num//10

print(sum)


num=1234
rev = 0
while num>0:
    rev *=10
    rev += num%10
    num = num//10
print(rev)

num=9551
a,b=num%10,0
num//=10
while num>9:
    b+=num%10
    num//=10
a+=numv
print(a==b)
