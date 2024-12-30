'''CS 211 - Josh Jilot - 4/18/2023
Lab 3 - Inheritance in Classes'''
import math

class Shape3D:

    def __init__(self):
        raise NotImplementedError("Abstract class cannot be instantiated")

    def volume(self) -> float:
        raise NotImplementedError("Not implemented for abstract class")

    def area(self) -> float:
        raise NotImplementedError("Not implemented for abstract class")

    def print_info(self):
        return f'Area: {self.area()}, Volume: {self.volume()}'

class Cylinder(Shape3D):
    '''like a tall circle!'''
    def __init__(self, radius: float, height: float):
        '''cylinder info is calculated using radius and height'''
        self.radius = radius
        self.height = height

    def volume(self) -> float:
        return math.pi * self.radius**2 * self.height

    def area(self) -> float:
        return 2 * math.pi * self.radius**2 +\
            2 * math.pi * self.radius * self.height

class Cuboid(Shape3D):
    '''almost a cube...sometimes it is!'''
    def __init__(self, width: float, length: float, height: float):
        '''cuboid info is calculated using their 3 dimensions'''
        self.width = width
        self.height = height
        self.length = length

    def volume(self) -> float:
        return self.width * self.length * self.height
    
    def area(self) -> float:
        return 2 * self.width * self.length +\
            2 * self.width * self.height +\
            2 * self.length * self.height

class Cube(Cuboid):
    '''always a cube!'''
    def __init__(self, width: float):
        self.width = width
        self.height = width
        self.length = width
