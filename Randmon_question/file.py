import os

print(os.getcwd())  

file=open('test_file.txt', 'r')  # Create a new file in the new directory
for i in file:
    print(i.strip())  # Print each line without extra spaces
file.close()