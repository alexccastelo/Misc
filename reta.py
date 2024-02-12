class Rectangle:

    def __init__(self, length, width):
        self.__length = length
        self.__width = width

    def get_area(self):
        return self.__length * self.__width

    def get_perimeter(self):
        return 2 * (self.__length + self.__width)


length = int(input("largura: "))
width = int(input("altura: "))
rectangle = Rectangle(length, width)
print("Área:", rectangle.get_area(), "e perímetro:", rectangle.get_perimeter())
