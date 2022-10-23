"""
Let's try to develop some data structures in python. Specially graph traversal - Breadth first and Depth first.

SOLID - stands for 5 principals :
Single Responsibility
Open for extension, closed for modification
Liskov substitution
Interface Segregation
Dependency Inversion
"""

class Order:

    def pay(self):
        print("Im paying")

ord = Order()
ord.pay()
