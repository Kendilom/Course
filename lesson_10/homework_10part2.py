from math import sqrt


class Figure:
    def get_area(self):
        pass

    def get_perimeter(self):
        pass

class Rectangle(Figure):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def get_area(self):
        return self.__width * self.__height

    def get_perimeter(self):
        return 2 * (self.__width + self.__height)

class Square(Figure):
    def __init__(self, side):
        self.__side = side

    def get_area(self):
        return self.__side**2

    def get_perimeter(self):
        return 4*self.__side

class RightTriangle(Figure):

    def __init__(self, side_a, side_b):
        self.__side_a = side_a
        self.__side_b = side_b

    def get_area(self):
        return self.__side_a * self.__side_b / 2

    def get_perimeter(self):
        hypotenuse = sqrt((self.__side_a**2) + (self.__side_b**2))
        return hypotenuse + self.__side_a + self.__side_b

t = RightTriangle(3,4)
s = Square(5)
r = Rectangle(3,4)
figures = [t, s, r]
for i in figures:
    print(f'Фигура: {type(i).__name__}')
    print(f'Площадь: {i.get_area()}')
    print(f'Периметр: {i.get_perimeter()}')
