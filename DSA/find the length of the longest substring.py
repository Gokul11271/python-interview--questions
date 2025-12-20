# Example 1:

# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.


number ="abcabcbb"
length= 0
for i in range(len(number)):
    for j in range (i+1,len(number)):
        print(number[i] , number[j])
        count +=1
        
        if number[i] == number[j]:
         print("repeated",number[i] , number[j])
         count=0
         break
        