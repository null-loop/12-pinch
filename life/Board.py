from PIL import ImageColor

from life.Enums import EntityType
from life.GameOptions import GameOptions

from matrix import set_matrix_point
from PIL import ImageColor

from life.Enums import EntityType
from life.GameOptions import GameOptions
from matrix import set_matrix_point


class Board:
    def __init__(self, options:GameOptions):
        self.__entities = []
        self.__height = options.height
        self.__width = options.width
        self.__render_scale = options.render_scale

        for y in range(options.width):
            self.__entities.append([EntityType.EMPTY] * options.height)

    def get(self, x, y) -> EntityType:
        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            return EntityType.EMPTY
        return self.__entities[x][y]

    def set(self, x, y, entity_type: EntityType):
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.CELL:
            r = (x / self.__width) * 256
            b = (y / self.__height) * 256
            g = 50
            colour = [r,g,b]
        self.set_with_colour(x, y, entity_type, colour)

    def set_with_colour(self, x, y, entity_type: EntityType, colour):
        self.__entities[x][y] = entity_type
        sx = x * self.__render_scale
        sy = y * self.__render_scale
        border = 1 if self.__render_scale > 3 else 0
        for rx in range(self.__render_scale - border):
            for ry in range(self.__render_scale - border):
                set_matrix_point(rx + sx, ry + sy, colour[0], colour[1], colour[2])

    def count_neighbours(self, x, y):
        count = 0
        if x > 0:
            count += self.is_neighbour(x - 1, y - 1)
            count += self.is_neighbour(x - 1, y)
            count += self.is_neighbour(x - 1, y + 1)
        count += self.is_neighbour(x, y - 1)
        count += self.is_neighbour(x, y + 1)
        if x < self.__width:
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
