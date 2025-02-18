from games.GameBoard import GameBoard
from utils.matrix import ScreenMatrix


class GameScreen:
    zoom_level = 1
    def __init__(self, matrix: ScreenMatrix, board_size_func, engine_func):
        self.__board_size_func = board_size_func
        self.__engine_func = engine_func
        self.__matrix = matrix
        self._game_board = None
        self._game_engine = None

    def _rebuild_board_and_engine(self):
        size = self.__board_size_func(self.zoom_level)
        self.__game_board = GameBoard(size, size, self.zoom_level, self.__matrix)
        self.__game_engine = self.__engine_func()

    def zoom_in(self):
        self.zoom_level = self.zoom_level + 1
        self._rebuild_board_and_engine()
        self.reset()

    def zoom_out(self):
        self.zoom_level = self.zoom_level - 1
        if self.zoom_level <= 0: self.zoom_level = 1
        self._rebuild_board_and_engine()
        self.reset()

    def reset(self):
        a = None