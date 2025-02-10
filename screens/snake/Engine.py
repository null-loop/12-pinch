from screens.snake.Board import Board
from screens.snake.Enums import EntityType, SnakeTurnResult
from screens.snake.GameOptions import GameOptions
from screens.snake.Snake import Snake


class Engine:
    def __init__(self, board: Board, options: GameOptions):
        self.__board = board
        self.__snakes = []
        self.__options = options
        self.__turn = 0

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
                snake = Snake.spawn_new_snake(pos[0], pos[1], self.__board)
                self.__snakes.append(snake)

    def __print_state(self):
        print(f'Turn {self.__turn}')
        print(f'Snake count: {len(self.__snakes)}')
        ordered_snakes = self.__snakes.copy()
        ordered_snakes.sort(key=lambda x: x.colour_string())

        for snake in ordered_snakes:
            snake.print_state()

    def turn(self):

        if self.__turn % 1000 == 0:
            self.__print_state()
        self.__turn = self.__turn + 1

        food_to_spawn = 0
        for snake in self.__snakes:
            turn_result = snake.turn()
            if turn_result == SnakeTurnResult.ATE:
                food_to_spawn = food_to_spawn + 1
            if turn_result == SnakeTurnResult.SPLIT:
                food_to_spawn = food_to_spawn + 1
                split_snake = snake.split()
                self.__snakes.append(split_snake)
            if turn_result == SnakeTurnResult.DIED:
                self.__snakes.remove(snake)

        self.__spawn_foods(food_to_spawn)
        if len(self.__snakes) < self.__options.start_snake_count:
            self.__spawn_snakes(self.__options.start_snake_count - len(self.__snakes))

    def fresh_render(self):
        self.__board.fresh_render()
        for snake in self.__snakes:
            snake.redraw_on_board()