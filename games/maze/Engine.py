import random
import sys
import time
from enum import Enum

from PIL import ImageColor

from games.Enums import EntityType
from games.GameBoard import GameBoard

class Turn:
    x = 0
    y = 0
    turns = []

class State(Enum):
    NOT_STARTED = 0
    PROGRESSING = 1
    RETURNING = 2

class MazeGenerator:
    _UP = (0,1)
    _LEFT = (-1, 0)
    _RIGHT = (1, 0)
    _DOWN = (0, -1)
    def __init__(self, board: GameBoard, step):
        self.__step = step
        self.__board = board
        self.__visited = []
        sys.setrecursionlimit(5000)

    def generate(self):
        self.__visited = [(1, 1)]
        self.__visit(1,1)
        print('MazeGenerator-Complete')

    def __visit(self, x, y):
        self.__board.set(x, y, EntityType.EMPTY)
        while True:
            unvisited = []
            # find which of our neighbouring spaces we've not visited before...
            if y > 1 and (x, y - 2) not in self.__visited:
                unvisited.append(self._UP)
            if y < self.__board.height() - 2 and (x, y + 2) not in self.__visited:
                unvisited.append(self._DOWN)
            if x > 1 and (x - 2, y) not in self.__visited:
                unvisited.append(self._LEFT)
            if x < self.__board.width() - 2 and (x + 2, y) not in self.__visited:
                unvisited.append(self._RIGHT)

            if len(unvisited) == 0:
                # we've hit a dead end
                return
            else:
                next_direction = random.choice(unvisited)
                next_x = x
                next_y = y

                if next_direction == self._UP:
                    next_y = y - 2
                    self.__board.set(x, y - 1, EntityType.EMPTY) # connection
                if next_direction == self._DOWN:
                    next_y = y + 2
                    self.__board.set(x, y + 1, EntityType.EMPTY) # connection
                if next_direction == self._LEFT:
                    next_x = x - 2
                    self.__board.set(x - 1, y, EntityType.EMPTY) # connection
                if next_direction == self._RIGHT:
                    next_x = x + 2
                    self.__board.set(x + 1, y, EntityType.EMPTY) # connection

                self.__visited.append((next_x, next_y))
                self.__visit(next_x, next_y)

class Engine:
    def __init__(self, board: GameBoard):
        self.__board = board
        self.__board.set_cell_colour_func(self.__colour_cell_func)
        self.__generation_step = 1/500
        self.__solver_step = 1/10
        self.__maze_entrance = ()
        self.__maze_exit = ()
        self.__trail = []
        self.__turns = []
        self.__state = State.NOT_STARTED

    def __colour_cell_func(self, x, y, entity_type):
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.WALL:
            colour = [10,10,255]
        if entity_type == EntityType.CELL:
            r = (x / self.__board.width()) * 256
            b = 50
            g = (y / self.__board.height()) * 256
            colour = [r, g, b]
        return colour

    def turn(self):
        # The solver runs in here! Consider a slowdown
        a = None

    def spawn_maze(self):
        # reset the board to all walls
        self.__board.start_new_canvas()
        self.__board.reset_to_type(EntityType.WALL)
        self.__board.finish_canvas()
        # reset game state
        self.__trail.clear()
        self.__turns.clear()
        self.__state = State.NOT_STARTED
        # The generator runs in here - write to the board as it goes
        generator = MazeGenerator(self.__board, self.__generation_step)
        generator.generate()
        print("Engine-spawn_maze-Complete")
        # Carves out the maze. Consider a slowdown
        # Then pick an entrance and an exit - carve from board - set __maze_entrance and __maze_exit