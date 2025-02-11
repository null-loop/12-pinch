from PIL import Image
from numpy import asarray

from screens.life.Board import Board
from screens.life.Engine import Engine, Position
from screens.life.GameOptions import GameOptions


class LifeScreen:
    update_interval_seconds=0
    label="Game of Life"
    render_as_image = False

    def __init__(self):
        game_options = GameOptions()
        game_options.height = 64
        game_options.width = 64
        game_options.render_scale = 2
        game_board = Board(game_options)
        self.__game_engine = Engine(game_board, game_options)
        self.__spawned = False
        self.__preset = 0
        self.__presets = ['Random','acorn.png','gosper-glider-gun.png','r-pentomino.png']

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
        a = None # no-op
        self.__preset = index - 1

    def __load_preset(self):
        preset = self.__presets[self.__preset]
        if preset == 'Random':
            self.__game_engine.random_spawn(3)
        else:
            image = Image.open('./assets/' + preset)
            data = asarray(image)
            positions = []
            for x in range(len(data)):
                col = data[x]
                for y in range(len(col)):
                    p = col[y]
                    if p[0] > 0: positions.append(Position(x,y))
            self.__game_engine.spawn_from_array(positions)

        self.__spawned = True
