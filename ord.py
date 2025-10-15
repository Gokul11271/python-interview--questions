# li=["a","B","c","D","e"]
# for i in li:
#     if  ( 'a'<= i <= 'z') :
#         print(i.upper())
#     elif ( 'A' <= i <= 'Z'):
#         print(i.lower())
#     else:
#         print("Invalid character")


# a="mam"
# if a==a[::-1]:
#     print("Palindrome")
# else:
#     print("Not a Palindrome")


# n = 3
# fact=1
# for i in range(1,n+1):
#     fact=fact*i
# print(fact)

# import math

# print(math.factorial(3))


# # Python code to demonstrate naive method
# # to compute factorial


# for i in range(1, n+1):
#     fact = fact * i

# print("The factorial of 23 is : ", end="")
# print(fact)


# l1=[1, 2, 3, 4, 5]
# l2=[6, 7, 8, 9, 10]
# l3=[l1, l2]
# print(l3)

# n=5
# fact=1
# for i in range(1,n+1):
#     fact=fact*i
# print(fact)


# import math
# math.factorial(5)
# print(math.factorial(5))



# li = [2, 15, 7, 24, 5]
# tar= 9
# for i in range(len(li)):
#     for j in range(i+1, len(li)):
#         if li[i] + li[j] == tar:
#             print(li[i], li[j])


# list1 = [3, 1, 4]
# list2 = [6, 2, 5]
# list1.extend(list2)
# print(list1)


# nums = [1, 2, 2, 3, 4, 4, 5]
# b=set(nums)
# print(list(b))
# Output: [1, 2, 3, 4, 5]


# nums = [12, 45, 67, 45, 89]
# # Output: 67
# second = sorted(list(nums))
# print(second[-2])  # Assuming nums is sorted in ascending order


# nums = [1, 2, 3, 4]
# # Output: [4, 3, 2, 1]
# print(nums[::-1])  # Reversing the list using slicing


# sq=[]
# for i in range(1,11):
#     sq.append(i**2)
# print(sq)  # Output: [1, 4, 9, 16



# nums = [10, 15, 22, 33, 42]
# nums2=[]
# for i  in range(len(nums)):
#     if  i%2==0:
#         nums2.append(nums[i])
# print(nums2)  # Output: [0, 2, 4] (indices of even numbers)




# s = "Gokul is preparing"
# # Output: 6
# c=0
# for i in s:
#     if i in 'aeiouAEIOU':
#         c+=1
# print(c)  # This will not work as intended, needs correction


# s = " Hello,Gokul! Are you ready?"
# # Output: "Hello Gokul Are you ready"
# result = ""
# for i in s:
#     if i not in '!':
#         result += i
#     else:
#         result += " "
# print(result)


# s = "banana"
# # Output: {'b': 1, 'a': 3, 'n': 2}
# count = {}
# for char in s:
#     count[char] = count.get(char, 0) + 1
# print(count)


# sentence = "I love Python programming"
# # Output: "programming Python love I"
# words = sentence.split()
# reversed_sentence = ' '.join(words[::-1])
# print(reversed_sentence)
# print(words[::-1])



# s = "Python is fun and educational"
# # Output: "educational"
# longest_word = max(s.split() , key=len)
# print(longest_word)  # This will print the longest word in the string

# s = "hello gokul welcome"
# # Output: "Hello Gokul Welcome"
# for i in s.split():
#     print(i)
#     print(i.capitalize())  # Capitalizes the first letter of each word


# s = "I love Java"
# replaced_string = s.replace("Java", "Python")
# print(replaced_string)  # Output: "I love Python"



# s = "Python is simple yet powerful"
# # Output: 5
# word_count = len(s.split())
# print(word_count)  # This will print the number of words in the string



# dicts = [{"a": 1, "b": 2}, {"c": 3, "d": 4}]
# Output:
# a: 1
# b: 2
# c: 3
# d: 4
# for d in dicts:
#     for k, v in d.items():
#         print(f"{k}: {v}")\



# d1 = {'a': 1, 'b': 2}
# d2 = {'b': 3, 'c': 4}
# # Output: {'a': 1, 'b': 3, 'c': 4}
# d1.update(d2)
# print(d1)  # This will merge d2 into d1, updating the value of



# n=8
# for n in range (n):
#     for j in range(2,n):
#         if n % j == 0:
#             print(n, "is not prime")
#             break
#     else:
#         print(n, "is a prime")




# m=8
# for i in range(m):
#     print()
#     for j in range(i):
#         print("*", end="")



# n=30
# for i in range(n):
#     if i%3==0 or i%5==0:
#         print(i,end=" ")


# n = 1234
# # Output: 1 + 2 + 3 + 4 = 10
# sum = 0
# while n > 0:
#         digit = n % 10
#         sum += digit
#         n //= 10
# print("Sum of digits:", sum)  # This will print the sum of the digits




# n=7
# fact=1
# for i in range(1,n+1):
#     fact *= i
# print(fact)  # This will print the factorial of n



# n = 4
# Output:
# 1
# 1 2
# 1 2 3
# 1 2 3 4
# for i in range(n):
#     print()
#     for j in range(i):
#         print(j + 1, end=" ")


# n = 153
# 1³ + 5³ + 3³ = 153 → Output: True

# # Check if one list is a sublist of another
# def is_sublist(larger, smaller):
#     return any(larger[i:i+len(smaller)] == smaller for i in range(len(larger) - len(smaller) + 1))

# # Example usage:
# list1 = [1, 2, 3, 4, 5]
# list2 = [3, 4]
# print(is_sublist(list1, list2))  # Output: True
     

# I= [1, 2, 2, 3, 3, 3, 4]  
# output = []
# for i in I:
#     if i not in output:
#         output.append(i)
# print(output)  # Output: [1, 2, 3, 4] (removing duplicates from the list)

# a = [2, 3, 4, 5, 6]
# b =[], sorted(a)
# print(b[::-2])  # Output: [6, 4, 2]


# s = "Python is great"
# words = s.split()
# reversed_words = ' '.join(words[::-1])
# print(reversed_words)  # Output: "great is Python"

# re=s.split()
# print(re[::-1])  # Output: ['Hello,', 'World!']


# n = 5
# for i in range(n):
#     print(' ' * (n - i - 1) + '* ' * (i + 1))


a = "imgokul"
aeiou = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
for char in a:
    if char in aeiou:
        aeiou[char] += 1
print(aeiou)  # Output: {'a': 1, 'e': 0, 'i': 1, 'o': 1, 'u': 1}