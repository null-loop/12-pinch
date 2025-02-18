import math
import time

from games.maze.Engine import Engine
from screens.GameScreen import GameScreen


def calculate_board_size(zoom_level:int):
    size = math.floor(128 / zoom_level)
    if size % 2 == 0: size = size - 1
    return size

class MazeScreen(GameScreen):
    update_interval_seconds=0
    label="Maze Runner"

    def __init__(self, matrix):
        super().__init__(matrix, calculate_board_size, lambda: Engine(self._game_board))
        self.__spawned = False

    def focus(self):
        if not self.__spawned:
            super(MazeScreen, self)._rebuild_board_and_engine()
            self._game_engine.spawn_maze()
            self.__spawned = True
        else:
            self._game_board.fresh_render()
        time.sleep(5)
        print("MazeScreen-focus-Complete")

    def tick(self):
        self._game_engine.turn()

    def reset(self):
        self.__spawned = True
        self._game_engine.spawn_maze()

    def preset(self, index):
        a = None

    def program_up(self):
        a = None

    def program_down(self):
        a = None