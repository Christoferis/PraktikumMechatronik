from enum import Enum


class test(Enum):
    E = 1
    F = 2
    S = 3


print(test(1))
print(test(2))
print(test(3))
print(type(test(test.E).name))
print(test("F"))