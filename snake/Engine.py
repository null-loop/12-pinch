from snake.Board import Board
from snake.Enums import EntityType, SnakeTurnResult
from snake.GameOptions import GameOptions
from snake.Snake import Snake


class Engine:
    def __init__(self, board: Board, options: GameOptions):
        self.__board = board
        self.__snakes = []
        self.__options = options

    def starting_spawn(self):
        self.__spawn_foods(self.__options.start_food_count)
        self.__spawn_snakes(self.__options.start_snake_count)

    def __spawn_foods(self, count:int):
        if count != 0:
            for i in range(count):
                pos = self.__board.get_random_empty_position()
                self.__board.set(pos[0], pos[1], EntityType.FOOD)

    def __spawn_snakes(self, count:int):
        if count != 0:
            for i in range(count):
                pos = self.__board.get_random_empty_position()
                snake = Snake.from_xy(pos[0], pos[1], self.__board)
                self.__snakes.append(snake)

    def turn(self):
        food_to_spawn = 0
        for snake in self.__snakes:
            turn_result = snake.turn()
            if turn_result == SnakeTurnResult.ATE or turn_result == SnakeTurnResult.SPLIT:
                food_to_spawn = food_to_spawn + 1
            if turn_result == SnakeTurnResult.SPLIT:
                split_snake = snake.split()
                self.__snakes.append(split_snake)
            if turn_result == SnakeTurnResult.DIED:
                self.__snakes.remove(snake)

        self.__spawn_foods(food_to_spawn)
        if len(self.__snakes) < self.__options.start_snake_count:
            self.__spawn_snakes(self.__options.start_snake_count - len(self.__snakes))