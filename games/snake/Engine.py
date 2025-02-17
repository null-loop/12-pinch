from PIL import ImageColor

from games import GameBoard
from games.Enums import EntityType
from games.snake.Enums import SnakeTurnResult
from games.snake.GameOptions import GameOptions
from games.snake.Snake import Snake


class Engine:
    def __init__(self, board: GameBoard, options: GameOptions):
        self.__board = board
        self.__board.set_cell_colour_func(self.__colour_cell_func)
        self.__snakes = []
        self.__options = options
        self.__turn = 0

    def starting_spawn(self):
        self.__spawn_foods(self.__options.food_count)
        self.__spawn_snakes(self.__options.min_snake_count)
        self.__board.set_many(self.__options.walls, EntityType.WALL)

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

    def __colour_cell_func(self, x, y, entity_type):
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.SNAKE: colour = ImageColor.getrgb("Green")
        if entity_type == EntityType.FOOD: colour = ImageColor.getrgb("Yellow")
        if entity_type == EntityType.WALL: colour = ImageColor.getrgb("Red")
        return colour

    def turn(self):

        food_to_spawn = 0
        for snake in self.__snakes:
            turn_result = snake.turn()
            if turn_result == SnakeTurnResult.ATE:
                food_to_spawn = food_to_spawn + 1
            if turn_result == SnakeTurnResult.SPLIT:
                food_to_spawn = food_to_spawn + 1
                if self.__options.reproduce:
                    split_snake = snake.split()
                    self.__snakes.append(split_snake)
            if turn_result == SnakeTurnResult.DIED:
                self.__snakes.remove(snake)

        self.__spawn_foods(food_to_spawn)
        if len(self.__snakes) < self.__options.min_snake_count:
            self.__spawn_snakes(self.__options.min_snake_count - len(self.__snakes))

    def fresh_render(self):
        self.__board.fresh_render()
        for snake in self.__snakes:
            snake.redraw_on_board()

    def reset(self):
        self.__board.reset()
        self.__snakes.clear()
        self.starting_spawn()