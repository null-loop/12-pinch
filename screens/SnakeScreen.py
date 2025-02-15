from PIL import Image
from numpy import asarray

from screens.snake.Board import Board
from screens.snake.Engine import Engine
from screens.snake.GameOptions import GameOptions
from utils.matrix import ScreenMatrix


class SnakeScreen:
    update_interval_seconds=0
    label="Snake"
    render_as_image = False

    def __init__(self, matrix: ScreenMatrix):
        self.__game_options = GameOptions()
        self.__game_options.start_snake_count = 100
        self.__game_options.start_food_count = 40
        self.__game_board = Board(self.__game_options, matrix)
        self.__game_engine = Engine(self.__game_board, self.__game_options)
        self.__spawned = False
        self.__preset = 0
        self.__presets = ['NoWalls','snake_frame_1.png']

    def focus(self):
        if not self.__spawned:
            self.__load_preset()
            self.__spawned = True
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
        if preset != 'NoWalls':
            walls = []
            image = Image.open('./assets/snake_presets/' + preset)
            data = asarray(image)
            for y in range(len(data)):
                row = data[y]
                for x in range(len(row)):
                    p = row[x]
                    if p[0] < 100: walls.append([x,y])
            self.__game_options.walls = walls
        else:
            self.__game_options.walls = []
        self.__game_engine.reset()

    def program_up(self):
        self.__game_options.start_snake_count = self.__game_options.start_snake_count + 10
        self.__load_preset()

    def program_down(self):
        self.__game_options.start_snake_count = self.__game_options.start_snake_count - 10
        if self.__game_options.start_snake_count <= 0:
            self.__game_options.start_snake_count = 1
        self.__load_preset()