import sys
from time import sleep

from snake.Board import Board
from snake.Engine import Engine
from snake.GameOptions import GameOptions



game_options = GameOptions()
game_options.start_snake_count = 120
game_options.start_food_count = 1000
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