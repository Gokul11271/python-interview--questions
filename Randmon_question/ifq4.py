"""Write a program check two vales are poiting to
the same memory or not if same memory display
the address of the two values or else display the
type of the values"""


a=input()
b=input()
if a==b:
 print("id of the value",id(a))
else:
 print("type of the value",id(a), print() ,id(b))


#id () # function is used to get the address of the value
# type() # function is used to get the type of the value
