from PIL import Image
from numpy import asarray

from screens.life.Board import Board
from screens.life.Engine import Engine, Position
from screens.life.GameOptions import GameOptions


class LifeScreen:
    update_interval_seconds=0
    label="Game of Life"
    render_as_image = False

    def __init__(self, matrix):
        game_options = GameOptions()
        game_options.height = 64
        game_options.width = 64
        game_options.render_scale = 2
        game_board = Board(game_options, matrix)
        self.__game_engine = Engine(game_board, game_options)
        self.__spawned = False
        self.__preset = 0
        self.__random_spawn_ratio = 3
        self.__presets = ['Random','acorn.png','gosper-glider-gun.png','r-pentomino.png','block-layer.png']

    def focus(self):
        if not self.__spawned:
            self.__load_preset()
        else:
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
        if preset == 'Random':
            self.__game_engine.random_spawn(self.__random_spawn_ratio)
        else:
            image = Image.open('./assets/life_presets/' + preset)
            data = asarray(image)
            positions = []
            for y in range(len(data)):
                row = data[y]
                for x in range(len(row)):
                    p = row[x]
                    if p[0] < 100: positions.append(Position(x,y))
            self.__game_engine.spawn_from_array(positions)
        self.__spawned = True

    def program_up(self):
        if self.__preset == 0:
            self.__random_spawn_ratio = self.__random_spawn_ratio + 1
            self.__load_preset()

    def program_down(self):
        if self.__preset == 0:
            self.__random_spawn_ratio = self.__random_spawn_ratio - 1
            if self.__random_spawn_ratio <= 0:
                self.__random_spawn_ratio = 1
            self.__load_preset()