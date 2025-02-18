from random import randrange, choice
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
        sys.setrecursionlimit(10000)

    def generate(self):
        self.__visited = [(1, 1)]
        self.__visit(1,1)

    def __visit(self, x, y):
        self.__board.set(x, y, EntityType.EMPTY)
        while True:
            unvisited = []
            # find which of our neighbouring spaces we've not visited before...
            if y > 1 and self.__board.get(x, y - 2) == EntityType.WALL:
                unvisited.append(self._UP)
            if y < self.__board.height() - 2 and self.__board.get(x, y + 2) == EntityType.WALL:
                unvisited.append(self._DOWN)
            if x > 1 and self.__board.get(x - 2, y) == EntityType.WALL:
                unvisited.append(self._LEFT)
            if x < self.__board.width() - 2 and self.__board.get(x + 2, y) == EntityType.WALL:
                unvisited.append(self._RIGHT)

            if len(unvisited) == 0:
                # we've hit a dead end
                return
            else:
                next_direction = choice(unvisited)
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

                self.__visit(next_x, next_y)
                time.sleep(self.__step)

class Engine:
    def __init__(self, board: GameBoard):
        self.__board = board
        self.__board.set_cell_colour_func(self.__colour_cell_func)
        self.__generation_step = 1/500
        self.__solver_step = 1/1000
        self.__maze_entrance = ()
        self.__maze_exit = ()
        self.__trail = []
        self.__turns = []
        self.__state = State.NOT_STARTED
        self.__returning_to = None

    def __colour_cell_func(self, x, y, entity_type):
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.WALL:
            colour = [200,200,200]
        if entity_type == EntityType.SOLVER:
            r = (x / self.__board.width()) * 256
            b = 50
            g = (y / self.__board.height()) * 256
            colour = [r, g, b]
        return colour

    def turn(self):
        fin = False
        # The solver runs in here! Consider a slowdown
        if self.__state == State.NOT_STARTED:
            self.__trail.append(self.__maze_entrance)
            self.__board.set(self.__maze_entrance[0], self.__maze_entrance[1], EntityType.SOLVER)
            self.__state = State.PROGRESSING
        elif self.__state == State.PROGRESSING:
            current = self.__trail[-1]
            can_move = self.__board.get_immediate_neighbours(current[0], current[1], EntityType.EMPTY)
            # if we've returned to a previous turn - remove those turns from the possible moves
            if self.__returning_to is not None:
                print(f'Excluding existing turns from pos {self.__returning_to.x},{self.__returning_to.y}')
                print(f'{self.__returning_to.turns}')
                for already_turned in self.__returning_to.turns:
                    can_move.remove(already_turned)
            if len(can_move) == 0:
                # if we're already returning to a turn, then trim that turn
                if self.__returning_to is not None:
                    self.__turns.pop()
                # we're now returning to the last turn
                self.__state = State.RETURNING
                if len(self.__turns) == 0:
                    fin = True
                else:
                    self.__returning_to = self.__turns[-1]
                    print(f"Can't move - returning to {self.__returning_to.x},{self.__returning_to.y}")
            else:
                if self.__maze_exit in can_move:
                    fin = True
                else:
                    next_move = can_move[0]
                    if self.__returning_to is not None:
                        # now record the next turn we're making
                        self.__returning_to.turns.append(next_move)
                        self.__returning_to = None
                    else:
                        # if this is a turn we need to add that to our list
                        if len(can_move) > 1:
                            print(f"Adding new turn at {current[0]},{current[1]} - first move to {next_move[0]},{next_move[1]}")
                            this_turn = Turn()
                            this_turn.x = current[0]
                            this_turn.y = current[1]
                            this_turn.turns = [next_move]
                            self.__turns.append(this_turn)
                    self.__trail.append(next_move)
                    self.__board.set(next_move[0],next_move[1],EntityType.SOLVER)
                    print(f'Moved to {next_move[0]},{next_move[1]}')
        elif self.__state == State.RETURNING:
            # keep trimming __trail until we hit __returning_to
            current = self.__trail[-1]
            print(f"Returning to {self.__returning_to.x},{self.__returning_to.y} - we're at {current[0]},{current[1]}")
            if current[0] == self.__returning_to.x and current[1] == self.__returning_to.y:
                self.__state = State.PROGRESSING
                print('Continuing')
            else:
                trimmed = self.__trail.pop()
                self.__board.set(trimmed[0],trimmed[1],EntityType.EMPTY)
                print(f'Trimmed {trimmed[0]},{trimmed[1]}')

        # check when we've solved the maze - and start another one!
        if fin:
            time.sleep(10)
            self.spawn_maze()
        else:
            time.sleep(self.__solver_step)

    def spawn_maze(self):
        # reset the board to all walls
        self.__board.start_new_canvas()
        self.__board.reset_to_type(EntityType.WALL)
        self.__board.finish_canvas()
        # reset game state
        self.__trail.clear()
        self.__turns.clear()
        self.__state = State.NOT_STARTED
        self.__returning_to = None
        # The generator runs in here - write to the board as it goes
        generator = MazeGenerator(self.__board, self.__generation_step)
        generator.generate()
        # Carves out the maze. Consider a slowdown
        # Then pick an entrance and an exit - carve from board - set __maze_entrance and __maze_exit
        found_entrance = False
        while not found_entrance:
            pos_y = randrange(self.__board.height())
            if self.__board.get(1, pos_y) == EntityType.EMPTY:
                found_entrance = True
                self.__maze_entrance = (0, pos_y)
                self.__board.set(0, pos_y, EntityType.EMPTY)

        found_exit = False
        while not found_exit:
            pos_y = randrange(self.__board.height())
            if self.__board.get(self.__board.width() - 2, pos_y) == EntityType.EMPTY:
                found_exit = True
                self.__maze_entrance = (self.__board.width() - 1, pos_y)
                self.__board.set(self.__board.width() - 1, pos_y, EntityType.EMPTY)