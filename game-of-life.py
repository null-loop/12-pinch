from life.Board import Board
from life.Engine import Engine
from life.GameOptions import GameOptions

options = GameOptions()
board = Board(options)
engine = Engine(board, options)

board.seed()
