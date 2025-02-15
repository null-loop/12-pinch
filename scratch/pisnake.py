import sys

from screens.snake.Board import Board
from screens.snake.Engine import Engine
from screens.snake.Enums import WallSets
from screens.snake.GameOptions import GameOptions

game_options = GameOptions()
game_options.min_snake_count = 40
game_options.food_count = 100
game_options.wall_set = WallSets.NONE
game_options.refresh_walls()
game_board = Board(game_options, matrix)
game_engine = Engine(game_board, game_options)

game_engine.starting_spawn()

try:
    print("Press CTRL-C to stop.")
    while True:
        game_engine.turn()

except KeyboardInterrupt:
    sys.exit(0)