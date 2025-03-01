from enum import Enum

AxisMax = 2 ** 15 - 1


class GenericPS1ButtonMap(Enum):
    Num1 = 0
    Num2 = 1
    Num3 = 2
    Num4 = 3
    ShoulderLeft = 4
    ShoulderRight = 5
    TriggerLeft = 6
    TriggerRight = 7
    Select = 8
    Start = 9
    StickLeft = 10
    StickRight = 11


class GenericPS1DpadMap(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7
    NONE = 14
