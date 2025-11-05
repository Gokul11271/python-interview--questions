name="gokul"

count=0
for i in name:
    if i in 'aeiouAEIOU':
        print(i,end='')   
        count+=1
print(f"\nNumber of vowels in {name} is {count}")
print(f"\nReversed name is {name[::-1]}")
print(f"\n {name}")




n = 3
fact=0
for i in range(1,n+1):
    fact +=i
print(fact)

s = "Interview"
count = 0
# Output: 4
for i in s:
    if i in 'aeiouAEIOU':
        count += 1
        print(i, end=' ')
else:
    print("\n",count)




lst = [10, 25, 5, 89, 12]

largest = lst[0]  # Start with the first element
for num in lst:
    if num > largest:
        largest = num

print("Largest number:", largest)  # Output: 89

