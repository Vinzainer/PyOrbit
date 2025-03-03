import math
from Point import Point

class Body:
    def __init__(self, location, mass, velocity, size, name = "", color = ""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.size = size
        self.name = name
        self.color = color