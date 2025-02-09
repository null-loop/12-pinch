from life.Board import Board
from life.GameOptions import GameOptions


class Engine:
    def __init__(self, board:Board, options:GameOptions):
        self.__board = board
        self.__options = options