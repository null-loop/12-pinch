from random import randrange
from typing import List

from PIL import ImageColor

from games.Enums import EntityType
from games.life.GameOptions import GameOptions
from utils.matrix import ScreenMatrix

class GameBoard:
    def __init__(self, width, height, render_scale, matrix: ScreenMatrix):
        self.__entities = []
        self.__height = width
        self.__width =height
        self.__render_scale = render_scale
        self.__matrix = matrix
        self.__cell_colour_func = None

        for y in range(width):
            self.__entities.append([EntityType.EMPTY] * height)

    def set_cell_colour_func(self, func):
        self.__cell_colour_func = func

    def get(self, x, y) -> EntityType:
        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            return EntityType.EMPTY
        return self.__entities[x][y]

    def set(self, x, y, entity_type: EntityType):
        colour = self.__cell_colour_func(x, y, entity_type)

        self.set_with_colour(x, y, entity_type, colour)

    def set_with_colour(self, x, y, entity_type: EntityType, colour):
        self.__entities[x][y] = entity_type
        sx = x * self.__render_scale
        sy = y * self.__render_scale
        border = 1 if self.__render_scale > 3 else 0
        for rx in range(self.__render_scale - border):
            for ry in range(self.__render_scale - border):
                self.__matrix.set_pixel(rx + sx, ry + sy, colour[0], colour[1], colour[2])

    def get_random_empty_position(self)->List:
        # Randomise x,y until you find an empty location
        while True:
            x = self.__get_random_x()
            y = self.__get_random_y()
            if self.get(x,y) == EntityType.EMPTY:
                return [x,y]

    def width(self)->int:
        return self.__width
    def height(self)->int:
        return self.__height

    def __get_random_x(self)->int:
        return randrange(self.width())

    def __get_random_y(self)->int:
        return randrange(self.height())

    def count_neighbours(self, x, y):
        count = 0
        if x > 0:
            count += self.is_neighbour(x - 1, y - 1)
            count += self.is_neighbour(x - 1, y)
            count += self.is_neighbour(x - 1, y + 1)
        count += self.is_neighbour(x, y - 1)
        count += self.is_neighbour(x, y + 1)
        if x < self.__width - 1:
            count += self.is_neighbour(x + 1, y - 1)
            count += self.is_neighbour(x + 1, y)
            count += self.is_neighbour(x + 1, y + 1)
        return count

    def is_neighbour(self, x, y)->int:
        if y < 0 or y >= self.__height:
            return 0
        if self.__entities[x][y] == EntityType.CELL:
            return 1
        return 0

    def reset(self):
        for x in range(self.__width):
            for y in range(self.__height):
                self.set(x, y, EntityType.EMPTY)

    def fresh_render(self):
        for x in range(self.__width):
            for y in range(self.__height):
                entity_type = self.get(x,y)
                self.set(x, y, entity_type)