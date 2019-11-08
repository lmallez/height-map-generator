#!/bin/python3


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def newColor(self, color, coef=0.5):
        red = self.r * (1 - coef) + color.r * coef
        yellow = self.g * (1 - coef) + color.g * coef
        blue = self.b * (1 - coef) + color.b * coef
        return Color(red, yellow, blue)

    def merge(self, color, coef=0.5):
        self.r = int(abs(self.r * (1 - coef) + color.r * coef))
        self.g = int(abs(self.g * (1 - coef) + color.g * coef))
        self.b = int(abs(self.b * (1 - coef) + color.b * coef))

    def add(self, color):
        self.r += color.r
        self.g += color.g
        self.b += color.b
        return

    def alpha(self, alpha):
        self.a = alpha
        a = alpha / 255
        self.r = (1 - a) * self.r + a * self.r
        self.g = (1 - a) * self.g + a * self.g
        self.b = (1 - a) * self.b + a * self.b
        return

    def toStr(self):
        return "#%02x%02x%02x" % (self.r, self.g, self.b)

    r = 0
    g = 0
    b = 0
    a = 255


class Tint:
    def __init__(self, x, y, min, max):
        self.min = min
        self.max = max
        self.x = x
        self.y = y

    def isInside(self, x):
        return self.x <= x < self.y

    def getColor(self, x):
        diff = (x - self.x) / (self.y - self.x)
        return self.min.newColor(self.max, coef=diff)

    min = Color
    max = Color
    x = 0
    y = 0
