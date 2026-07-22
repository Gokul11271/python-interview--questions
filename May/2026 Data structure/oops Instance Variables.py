# 4. Instance Variables
# Problem 1

# Create a class called Student.

# Constructor should store

# name
# age
# department

# Create two objects with different values.

# Print every object's details.

class Student :
    def __init__(self,name,age,department):
        self.name=name
        self.age=age
        self.department=department
    def display(self):
        print(self.name,self.age,self.department)
      
new = Student("Gokul",21,"cs")
new2 = Student("amil",22,"da")
new.display()
new2.display()
