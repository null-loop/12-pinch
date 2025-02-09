from life.Board import Board
from life.Engine import Engine
from life.GameOptions import GameOptions


class LifeScreen:
    update_interval_seconds=0
    label="Game of Life"
    render_as_image = False

    def __init__(self):
        game_options = GameOptions()
        game_options.height = 64
        game_options.width = 64
        game_options.render_scale = 2
        game_board = Board(game_options)
        self.__game_engine = Engine(game_board, game_options)
        self.__game_engine.starting_spawn()

    def fresh_render(self):
        self.__game_engine.reset()

    def render(self):
        self.__game_engine.turn()