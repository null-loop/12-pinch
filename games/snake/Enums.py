from enum import Enum

class SnakeTurnResult(Enum):
    MOVED = 0
    ATE = 1
    DIED = 2
    SPLIT = 3