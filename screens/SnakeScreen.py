from screens.snake.Board import Board
from screens.snake.Engine import Engine
from screens.snake.Enums import WallSets
from screens.snake.GameOptions import GameOptions


class SnakeScreen:
    update_interval_seconds=0
    label="Snake"
    render_as_image = False

    def __init__(self):
        game_options = GameOptions()
        game_options.start_snake_count = 100
        game_options.start_food_count = 40
        game_options.wall_set = WallSets.NONE
        game_options.refresh_walls()
        game_board = Board(game_options)
        # TODO: One day worry about the walls!
        self.__game_engine = Engine(game_board, game_options)
        self.__spawned = False

    def fresh_render(self):
        if not self.__spawned:
            self.__game_engine.starting_spawn()
            self.__spawned = True
        self.__game_engine.fresh_render()

    def render(self):
        self.__game_engine.turn()
