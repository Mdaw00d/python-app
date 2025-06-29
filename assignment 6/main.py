from abc import ABC, abstractmethod

#using self
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def display(self):
        print("Name:", self.name)
        print("Marks:", self.marks)

student1 = Student("Maryam", 92)
student1.display()

#using counter
class Counter:
    count = 0 

    def __init__(self):
        Counter.count += 1

    @classmethod
    def display_count(cls):
        print("Total objects created:", cls.count)

obj1 = Counter()
obj2 = Counter()
obj3 = Counter()

Counter.display_count()

# Public Variables and Methods
class Car:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(self.brand, "car is starting...")

my_car = Car("Toyota")
print("Brand:", my_car.brand)
my_car.start()

#Class Variables and Class Methods
class Car:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(self.brand, "car is starting...")

my_car = Car("Toyota")
print("Brand:", my_car.brand)
my_car.start()

# Static Variables and Static Methods
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

result = MathUtils.add(5, 3)
print("Sum:", result)

#Constructors and Destructors
class Logger:
    def __init__(self):
        print("Logger object created.")

    def __del__(self):
        print("Logger object destroyed.")

log = Logger()
del log

#Access Modifiers: Public, Private, and Protected
class Employee:
    def __init__(self, name, salary, ssn):
        self.name = name            # public
        self._salary = salary       # protected
        self.__ssn = ssn            # private

emp = Employee("Maryam", 50000, "123-45-6789")

print("Name:", emp.name)           
print("Salary:", emp._salary)      
print("SSN:", emp.__ssn) 

#The super() Function
class Person:
    def __init__(self, name):
        self.name = name

class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def display(self):
        print(self.name, "teaches", self.subject)

t1 = Teacher("Mr. Ahmed", "Math")
t1.display()

# Abstract Classes and Methods


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

r = Rectangle(5, 3)
print("Area:", r.area())

#Instance Methods
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says Woof!")

dog1 = Dog("Buddy", "Golden Retriever")
dog1.bark()

#Class Methods
class Book:
    total_books = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author
        Book.increment_book_count()

    @classmethod
    def increment_book_count(cls):
        cls.total_books += 1

book1 = Book("1984", "George Orwell")
book2 = Book("To Kill a Mockingbird", "Harper Lee")

print("Total books:", Book.total_books)

#Static Methods
class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return (c * 9/5) + 32

temp = TemperatureConverter.celsius_to_fahrenheit(25)
print("Temperature in Fahrenheit:", temp)

#Composition
class Engine:
    def start(self):
        print("Engine is starting...")

class Car:
    def __init__(self, engine):
        self.engine = engine

    def start_car(self):
        self.engine.start()
        print("Car is ready to go!")

engine = Engine()
car = Car(engine)
car.start_car()

# Aggregation
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def display(self):
        print(f"{self.name} - {self.position}")

class Department:
    def __init__(self, department_name, employee):
        self.department_name = department_name
        self.employee = employee

    def display_department(self):
        print(f"Department: {self.department_name}")
        self.employee.display()

employee1 = Employee("Alice", "Manager")
department1 = Department("HR", employee1)

department1.display_department()

#Method Resolution Order (MRO) and Diamond Inheritance
class A:
    def show(self):
        print("Class A")

class B(A):
    def show(self):
        print("Class B")

class C(A):
    def show(self):
        print("Class C")

class D(B, C):
    pass

d = D()
d.show()

#Function Decorators
def log_function_call(func):
    def wrapper():
        print("Function is being called")
        func()
    return wrapper

@log_function_call
def say_hello():
    print("Hello, World!")

say_hello()

#Class Decorators
def add_greeting(cls):
    def greet(self):
        return "Hello from Decorator!"
    cls.greet = greet
    return cls

@add_greeting
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")
print(p.greet())

#Property Decorators: @property, @setter, and @deleter
class Product:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            print("Price cannot be negative.")
        else:
            self._price = value

    @price.deleter
    def price(self):
        print("Deleting the price attribute.")
        del self._price

product = Product(100)
print(product.price)  

product.price = 120  
print(product.price)

del product.price

#callable() and __call__()
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

multiplier = Multiplier(5)
print(callable(multiplier))
result = multiplier(10)
print(result)

#Creating a Custom Exception
class InvalidAgeError(Exception):
    pass

def check_age(age):
    if age < 18:
        raise InvalidAgeError("Age must be 18 or older")

try:
    check_age(16)
except InvalidAgeError as e:
    print(f"Error: {e}")

#Make a Custom Class Iterable
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current

countdown = Countdown(5)
for number in countdown:
    print(number)




          