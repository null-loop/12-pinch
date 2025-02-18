import math

from games.GameBoard import GameBoard
from games.snake.Engine import Engine
from games.snake.GameOptions import GameOptions
from screens.GameScreen import GameScreen
from utils.matrix import ScreenMatrix

def calculate_board_size(zoom_level:int):
    return math.floor(128 / zoom_level)

class SnakeScreen(GameScreen):
    update_interval_seconds=0
    label="Snake"

    def __init__(self, matrix: ScreenMatrix):
        super().__init__(matrix, calculate_board_size, lambda : Engine(self.__game_board, self.__game_options))
        self.__game_options = GameOptions()
        self.__game_options.min_snake_count = 100
        self.__game_options.food_count = 40
        self.__spawned = False
        self.__preset = 0
        self.__presets = ['NoWalls','ToggleReproduction','SnakeCount','FoodCount']

    def focus(self):
        if not self.__spawned:
            super(SnakeScreen, self).rebuild_board_and_engine()
            self.__load_preset()
        self.__game_engine.fresh_render()

    def tick(self):
        self.__game_engine.turn()

    def reset(self):
        self.__load_preset()

    def preset(self, index):
        self.__preset = index - 1
        self.__load_preset()

    def __load_preset(self):
        preset = self.__presets[self.__preset]
        if preset == 'ToggleReproduction':
            self.__game_options.reproduce = not self.__game_options.reproduce
            self.__preset = 0
        else:
            self.__game_options.walls = []
        self.__game_engine.reset()
        self.__spawned = True

    def program_up(self):
        if self.__preset == 3:
            self.__game_options.food_count = self.__game_options.food_count + 10
        else:
            self.__game_options.min_snake_count = self.__game_options.min_snake_count + 10
        self.__load_preset()

    def program_down(self):
        if self.__preset == 3:
            self.__game_options.food_count = self.__game_options.food_count - 10
            if self.__game_options.food_count <= 0:
                self.__game_options.food_count = 1
        else:
            self.__game_options.min_snake_count = self.__game_options.min_snake_count - 10
            if self.__game_options.min_snake_count <= 0:
                self.__game_options.min_snake_count = 1
        self.__load_preset()