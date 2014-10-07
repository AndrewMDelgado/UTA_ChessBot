class Coordinate(tuple) :

    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __add__(self, other):
        return tuple(sum(x) for x in zip(self, other))

    def __sub__(self, other):
        return self.__add__(-i for i in other)
