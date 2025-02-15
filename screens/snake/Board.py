from random import randrange
from typing import List

from PIL import ImageColor

from screens.snake.Enums import EntityType
from screens.snake.GameOptions import GameOptions
from utils.matrix import ScreenMatrix


class Board:
    def __init__(self, options: GameOptions, matrix: ScreenMatrix):
        self.__entities = []
        self.__height = options.height
        self.__width = options.width
        self.__matrix = matrix

        for y in range(options.width):
            self.__entities.append([EntityType.EMPTY] * options.height)

        for pos in options.starting_wall_positions:
            self.set(pos[0],pos[1],EntityType.WALL)

    def width(self)->int:
        return self.__width

    def height(self)->int:
        return self.__height

    def get(self, x, y) -> EntityType:
        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            return EntityType.EMPTY
        return self.__entities[x][y]

    def set(self, x, y, entity_type: EntityType):
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.SNAKE: colour = ImageColor.getrgb("Green")
        if entity_type == EntityType.FOOD: colour = ImageColor.getrgb("Yellow")
        if entity_type == EntityType.WALL: colour = ImageColor.getrgb("Red")
        self.set_with_colour(x, y, entity_type, colour)

    def set_with_colour(self, x, y, entity_type: EntityType, colour):

        self.__entities[x][y] = entity_type
        self.__matrix.set_pixel(x, y, colour[0], colour[1], colour[2])

    def get_random_empty_position(self)->List:
        # Randomise x,y until you find an empty location
        while True:
            x = self.__get_random_x()
            y = self.__get_random_y()
            if self.get(x,y) == EntityType.EMPTY:
                return [x,y]

    def __get_random_x(self)->int:
        return randrange(self.width())

    def __get_random_y(self)->int:
        return randrange(self.height())

    def fresh_render(self):
        for x in range(self.width()):
            for y in range(self.height()):
                entity_type = self.get(x,y)
                if entity_type != EntityType.SNAKE:
                    self.set(x, y, entity_type)

    def reset(self):
        for x in range(self.__width):
            for y in range(self.__height):
                self.set(x, y, EntityType.EMPTY)