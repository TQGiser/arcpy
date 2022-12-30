import math


class Triangle():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def angleA(self):
        v = (math.acos((self.b ** 2 + self.c ** 2 - self.a ** 2) / (2 * self.b * self.c)))* 180 / math.pi
        return v

    def angleB(self):
        v = (math.acos((self.a ** 2 + self.c ** 2 - self.b ** 2) / (2 * self.a * self.c))) * 180 / math.pi
        return v

    def angelC(self):
        v = (math.acos((self.b ** 2 + self.a ** 2 - self.c ** 2) / (2 * self.a * self.b))) * 180 / math.pi
        return v


tri1 = Triangle(3, 4, 5)
print(tri1.angleA())
print(tri1.angleB())
print(tri1.angelC())
