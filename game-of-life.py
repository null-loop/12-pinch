import sys

from life.Board import Board
from life.Engine import Engine
from life.GameOptions import GameOptions

game_options = GameOptions()
game_options.height = 128
game_options.width = 128
game_options.render_scale = 1
game_board = Board(game_options)
game_engine = Engine(game_board, game_options)
game_engine.starting_spawn()

try:
    print("Press CTRL-C to stop.")
    while True:
        game_engine.turn()

except KeyboardInterrupt:
    sys.exit(0)