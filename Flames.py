while True:
    print('- - - - - - - - - - Welcome to FLAMES World - - - - - - - - - -')

    print()
    a=input("Enter a boy name to check :")
    b=input("Enter a girl name to check :")
    bf,gf=a,b
    d={1:'Friend',2:'Love 💘',3:'Affection',4:'Marriage',5:'Enemy',6:'Sister'}
    for i in range(len(a)) :

        
        for j in range(len(b)):
            if a[i].lower()==b[j].lower():
                a=a.replace(a[i]," ",1)
                b=b.replace(b[j]," ",1)
    l=""
    for i in a+b:
        if i !=" ":
            l+=i
    check=len(l)%6
    print()
    print(f'There is a {d[check+1].upper()} between {bf} and {gf} ')

    print()
    print("- - - - - - - - - - - - - X- - - -  - - - - - - - - - X - - - - - - - - - - - - - - -")
    print()
    n=int(input("Enter 1 to continue checking the relationship --  0 to exit : "))
    if n==0:
          break
    else:
          pass
    