# 2. Constructor (__init__())
# Problem 1

# Inside the editor, complete the following steps:

# Create a class called Person.
# Add an __init__ method that takes name and age.
# Store both values inside the object.
# Create an object called p1 with:
# Name: "John"
# Age: 25

class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
p1=Person("Gokul",21)
print(p1.name,p1.age)


# Problem 2

# Create a class called Laptop.

# Constructor should take:
# brand
# price
# Store them in the object.
# Create an object:
# Dell
# 65000

class Laptop:
    def __init__(self,brand,price):
        self.brand=brand
        self.price=price
new=Laptop("Dell",65000)
print(new.brand,new.price)
