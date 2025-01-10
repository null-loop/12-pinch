import sys

from snake.Board import Board
from snake.Engine import Engine
from snake.Enums import WallSets
from snake.GameOptions import GameOptions

game_options = GameOptions()
game_options.start_snake_count = 40
game_options.start_food_count = 200
game_options.wall_set = WallSets.SQUARE
game_options.refresh_walls()
game_board = Board(game_options)
game_engine = Engine(game_board, game_options)

game_engine.starting_spawn()

try:
    print("Press CTRL-C to stop.")
    while True:
        game_engine.turn()

except KeyboardInterrupt:
    sys.exit(0)