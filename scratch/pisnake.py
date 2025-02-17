import sys

from games.snake.Board import Board
from games.snake.Engine import Engine
from games.snake.Enums import WallSets
from games.snake.GameOptions import GameOptions

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