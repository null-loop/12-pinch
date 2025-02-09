import math
import random

from life.Board import Board
from life.Enums import EntityType
from life.GameOptions import GameOptions

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        # Algo!
        births = []
        deaths = []
        # For each position, evaluate rules
        for ex in range(self.__options.width):
            for ey in range(self.__options.height):
                current = self.__board.get(ex, ey)
                neighbour_count = self.__board.count_neighbours(ex, ey)
                # Add death / birth to array
                if current == EntityType.CELL:
                    if neighbour_count < 2 or neighbour_count > 3:
                        deaths.append(Position(ex, ey))
                else:
                    if neighbour_count == 3:
                        births.append(Position(ex, ey))

        # Once complete - apply the arrays to the board
        for p in births:
            self.__board.set(p.x, p.y, EntityType.CELL)

        for p in deaths:
            self.__board.set(p.x, p.y, EntityType.EMPTY)

    def reset(self):
        self.__board.reset()
        self.starting_spawn()