import math
import random

from life.Board import Board
from life.Enums import EntityType


class GameOptions:
    height=128
    width=128

    def seed(self, board:Board):
        total_cells = self.height * self.width
        population = math.floor(total_cells / 3)
        for p in range(population):
            populated = False
            while not populated:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                e = board.get(x, y)
                if e == EntityType.EMPTY:
                    board.set(x, y, EntityType.CELL)
                    populated = True

