import math
import random

from PIL import ImageColor

from life.Enums import EntityType
from life.GameOptions import GameOptions

from matrix import set_matrix_point

class Board:
    def __init__(self, options:GameOptions):
        self.__entities = []
        self.__height = options.height
        self.__width = options.width

        for y in range(options.width):
            self.__entities.append([EntityType.EMPTY] * options.height)

    def get(self, x, y) -> EntityType:
        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            return EntityType.EMPTY
        return self.__entities[x][y]

    def set(self, x, y, entity_type: EntityType):
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.CELL: colour = ImageColor.getrgb("Red")
        self.set_with_colour(x, y, entity_type, colour)

    def set_with_colour(self, x, y, entity_type: EntityType, colour):
        self.__entities[x][y] = entity_type
        set_matrix_point(x, y, colour[0], colour[1], colour[2])

    def seed(self):
        total_cells = self.__height * self.__width
        population = math.floor(total_cells / 3)
        for p in range(population):
            populated = False
            while not populated:
                x = random.randint(0, self.__width - 1)
                y = random.randint(0, self.__height - 1)
                e = self.get(x, y)
                if e == EntityType.EMPTY:
                    self.set(x, y, EntityType.CELL)
                    populated = True