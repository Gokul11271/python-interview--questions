# Example 1:

# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.


s="abcabcbb"
for i in range(len(s)):
    for j in range(len(s)):
        if s[i]==s[j]:

         print("i =",s[i],"j =",s[j])


    break