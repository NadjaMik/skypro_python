import math


def square(x):
    x = float(x)
    sq = x*x
    return math.ceil(sq)


x = input("Введите длину стороны квадрата: ")
print("Площадь квадрата ", square(x))
