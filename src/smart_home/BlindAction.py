from enum import Enum


class BlindAction(Enum):
    Blind1Up = 1
    Blind2Up = 2
    Blind3Up = 3
    Blind4Up = 4
    Blind5Up = 5
    Blind1Down = 6
    Blind2Down = 7
    Blind3Down = 8
    Blind4Down = 9
    Blind5Down = 10
    AllUp = 11
    AllDown = 12
    AllUp2 = 13
    AllDown2 = 14


class Blind(Enum):
    Blind1 = 1
    Blind2 = 2
    Blind3 = 3
    Blind4 = 4
    Blind5 = 5
    All = 6
