a=input()
if 'a'<=a<='z'  or 'A'<=a<='Z' :
    print("it is an alphabet")
else:
    print("it is a number")
        #'a'<=i<='z' or 'A'<=i<='Z' or '0'<=i<='9'

a = input()

try:
    int(a)
    print("it is an integer")
except ValueError:
    try:
        float(a)
        print("it is a float")
    except ValueError:
        try:
            complex(a)
            print("it is a complex number")
        except ValueError:
            print("it is not a number")