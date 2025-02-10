import sys

from screens.life.Board import Board
from screens.life.Engine import Engine
from screens.life.GameOptions import GameOptions

game_options = GameOptions()
game_options.height = 42
game_options.width = 42
game_options.render_scale = 3
game_board = Board(game_options)
game_engine = Engine(game_board, game_options)
game_engine.starting_spawn()

try:
    print("Press CTRL-C to stop.")
    turn_count=0
    while True:
        turn_count+=1
        game_engine.turn()
        print(f"Turn {turn_count}")

except KeyboardInterrupt:
    sys.exit(0)