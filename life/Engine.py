import math
import random

from life.Board import Board
from life.Enums import EntityType
from life.GameOptions import GameOptions


class Engine:
    def __init__(self, board:Board, options:GameOptions):
        self.__board = board
        self.__options = options

    def starting_spawn(self):
        total_cells = self.__options.height * self.__options.width
        population = math.floor(total_cells / 3)
        for p in range(population):
            populated = False
            while not populated:
                x = random.randint(0, self.__options.width - 1)
                y = random.randint(0, self.__options.height - 1)
                e = self.__board.get(x, y)
                if e == EntityType.EMPTY:
                    self.__board.set(x, y, EntityType.CELL)
                    populated = True

    def turn(self):
        x = 1