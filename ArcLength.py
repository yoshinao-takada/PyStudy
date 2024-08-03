import math
class ArcLength:
    def __init__(self):
        self.radius = 0
        self.angle = 0

    def calculate_arc_length(self):
        result = 2 * math.pi * self.radius * self.angle / 360
        print(f"Length of an Arc is {result}")

a1 = ArcLength()
a1.radius = 9
a1.angle = 75
print(f"Angle is {a1.angle}")
print(f"Radius is {a1.radius}")
a1.calculate_arc_length()
