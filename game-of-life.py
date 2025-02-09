import sys

from life.Board import Board
from life.Engine import Engine
from life.GameOptions import GameOptions

game_options = GameOptions()
game_board = Board(game_options)
game_engine = Engine(game_board, game_options)
game_engine.starting_spawn()

try:
    print("Press CTRL-C to stop.")
    while True:
        game_engine.turn()

except KeyboardInterrupt:
    sys.exit(0)