from enum import Enum

class EntityType(Enum):
    EMPTY = 0
    SNAKE = 1
    FOOD = 2
    WALL = 3

class SnakeTurnResult(Enum):
    MOVED = 0
    ATE = 1
    DIED = 2
    SPLIT = 3

class WallSets(Enum):
    NONE = 0
    SQUARE = 1