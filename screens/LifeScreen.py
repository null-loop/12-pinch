import math

from PIL import Image
from numpy import asarray

from games.life.Engine import Engine, Position
from screens.GameScreen import GameScreen


def calculate_board_size(zoom_level:int):
    size = math.floor(128 / zoom_level)
    if size % 2 == 0: size = size - 1
    return size

class LifeScreen(GameScreen):
    update_interval_seconds=0
    label="Game of Life"

    def __init__(self, matrix):
        super().__init__(matrix, calculate_board_size, lambda: Engine(self._game_board))
        self.__spawned = False
        self.__preset = 0
        self.__random_spawn_ratio = 3
        self.__presets = ['Random','acorn.png','gosper-glider-gun.png','r-pentomino.png','block-layer.png']

    def focus(self):
        if not self.__spawned:
            super(LifeScreen, self)._rebuild_board_and_engine()
            self.__load_preset()
        else:
            self._game_engine.fresh_render()

    def tick(self):
        self._game_engine.turn()

    def reset(self):
        self.__load_preset()

    def preset(self, index):
        self.__preset = index - 1
        self.__load_preset()

    def __load_preset(self):
        preset = self.__presets[self.__preset]
        if preset == 'Random':
            self._game_engine.random_spawn(self.__random_spawn_ratio)
        else:
            image = Image.open('./assets/life_presets/' + preset)
            data = asarray(image)
            positions = []
            for y in range(len(data)):
                row = data[y]
                for x in range(len(row)):
                    p = row[x]
                    if p[0] < 100: positions.append(Position(x,y))
            self._game_engine.spawn_from_array(positions)
        self.__spawned = True

    def program_up(self):
        if self.__preset == 0:
            self.__random_spawn_ratio = self.__random_spawn_ratio - 1
            self.__load_preset()

    def program_down(self):
        if self.__preset == 0:
            self.__random_spawn_ratio = self.__random_spawn_ratio + 1
            if self.__random_spawn_ratio <= 1:
                self.__random_spawn_ratio = 2
            self.__load_preset()