# Python Inheritance

## 1. Basic Inheritance

Inheritance allows one class to use the methods of another class. It helps us reuse existing code instead of writing the same methods again.

### Code

    class Animal:
        def eat(self):
            print("Animal is eating")


    class Dog(Animal):
        def bark(self):
            print("Dog is barking")


    d = Dog()
    d.eat()
    d.bark()

### Output

    Animal is eating
    Dog is barking

### Explanation

- **`class Animal:`** creates a parent class named `Animal`.
- **`eat()`** is a method defined inside the parent class.
- **`class Dog(Animal):`** creates a child class that inherits from `Animal`. The parentheses specify which class it inherits from.
- **`bark()`** is a method defined inside the `Dog` class.
- **`d = Dog()`** creates an object of the `Dog` class.
- **`d.eat()`** calls the `eat()` method inherited from `Animal`.
- **`d.bark()`** calls the `bark()` method defined inside `Dog`.

Notice that we never defined the `eat()` method inside `Dog`, but we can still call it using the `Dog` object. This is possible because `Dog` inherits from `Animal`.

**Remember:** A child class can use the methods of its parent class and also have its own methods.

---

## 2. Inheritance with `__init__()`

The `__init__()` method is used to initialize an object's attributes when an object is created. In inheritance, a child class can define its own `__init__()` method while inheriting other methods from its parent.

### Code

    class Person:
        def __init__(self, name):
            self.name = name

        def introduce(self):
            print(f"My name is {self.name}")


    class Student(Person):
        def __init__(self, name, course):
            self.name = name
            self.course = course

        def show_course(self):
            print(f"I am studying {self.course}")


    s1 = Student("Ali", "Python")

    s1.introduce()
    s1.show_course()

### Output

    My name is Ali
    I am studying Python

### Explanation

- **`class Person:`** creates the parent class.
- **`__init__(self, name)`** accepts a name when an object is initialized.
- **`self.name = name`** stores the name inside the object.
- **`introduce()`** displays the person's name.
- **`class Student(Person):`** creates a child class that inherits from `Person`.
- **`__init__(self, name, course)`** defines a constructor for `Student` that accepts both a name and a course.
- **`self.name = name`** stores the student's name.
- **`self.course = course`** stores the student's course.
- **`show_course()`** displays the course the student is studying.
- **`s1 = Student("Ali", "Python")`** creates a student object with the name `Ali` and the course `Python`.

When we call `s1.introduce()`, Python finds the method in the parent class, `Person`, and executes it. When we call `s1.show_course()`, Python executes the method defined in `Student`.

Notice that `Student` has its own `__init__()` method. Therefore, the parent's constructor does not run automatically. We assign `self.name = name` directly in the child class to initialize the name.

**Remember:** A child class can inherit methods from its parent while defining its own attributes and methods.

---

## Quick Revision

| Concept | Meaning |
|---|---|
| Inheritance | Reusing methods from another class |
| Parent class | The class being inherited from |
| Child class | The class that inherits from another class |
| `__init__()` | Initializes an object's attributes |
| `self` | Refers to the current object |
| Object | An instance of a class |