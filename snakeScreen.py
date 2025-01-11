from snake.Board import Board
from snake.Engine import Engine
from snake.Enums import WallSets
from snake.GameOptions import GameOptions


class SnakeScreen:
    update_interval_seconds=0
    label="Snake"
    render_as_image = False

    def __init__(self):
        game_options = GameOptions()
        game_options.start_snake_count = 40
        game_options.start_food_count = 100
        game_options.wall_set = WallSets.NONE
        game_options.refresh_walls()
        game_board = Board(game_options)
        self.__game_engine = Engine(game_board, game_options)

    def fresh_render(self):
        self.__game_engine.fresh_render()

    def render(self):
        self.__game_engine.turn()
