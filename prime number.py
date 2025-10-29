num = int(input("Enter a number: "))

if num > 1:
    for i in range(2, num):
        if num % i == 0:
            print("Not Prime")
            break
    else:
        print("Prime")
else:
    print("Not Prime")

def isprime(num):
    for i in range(2, num-1):
        if num % i == 0:
            return False      
    else:
        return True
        


def prime_n(n):
    for i in range(2, n+1):
        if isprime(i):
            print(i)


n=10
for n in range(2,n):
        for i in range(2, n):
            if n % i ==0 :
                print(n, "is  not prime")
                break
        else:
              print(n, "is a prime") 
