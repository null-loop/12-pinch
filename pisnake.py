import sys
from enum import Enum
from random import randrange
from typing import List

from matrix import set_matrix_point
from PIL import ImageColor

class EntityType(Enum):
    EMPTY = 0
    SNAKE = 1
    FOOD = 2
    WALL = 3

class SnakeTurnResult(Enum):
    MOVED = 0
    ATE = 1
    DIED = 2

class GameOptions:
    height=128
    width=128
    start_food_count=20
    start_snake_count=20
    starting_wall_positions=[]

    def __int__(self):
        self.refresh_walls()

    def __starting_wall_positions(self)->List:
        # default shape - the edges
        print("Setting up starting wall positions")
        positions = []
        for x in range(self.width):
            positions.append([x,0])
            positions.append([x,self.height - 1])
        for y in range(self.height):
            positions.append([0,y])
            positions.append([self.width - 1,y])
        return positions

    def refresh_walls(self):
        self.starting_wall_positions = self.__starting_wall_positions()

class Board:
    def __init__(self, options:GameOptions):
        self.__entities = []
        self.__height = options.height
        self.__width = options.width

        for y in range(options.height):
            self.__entities.append([EntityType.EMPTY] * options.width)

        for pos in options.starting_wall_positions:
            self.set(pos[0],pos[1],EntityType.WALL)

    def width(self)->int:
        return self.__width

    def height(self)->int:
        return self.__height

    def get(self, x, y) -> EntityType:
        #print(x)
        #print(y)
        return self.__entities[x][y]

    def set(self, x, y, entity_type: EntityType):
        self.__entities[x][y] = entity_type
        colour = ImageColor.getrgb("Black")
        if entity_type == EntityType.SNAKE: colour = ImageColor.getrgb("Yellow")
        if entity_type == EntityType.FOOD: colour = ImageColor.getrgb("Green")
        if entity_type == EntityType.WALL: colour = ImageColor.getrgb("Red")
        set_matrix_point(x, y, colour[0], colour[1], colour[2])

    def get_random_empty_position(self)->List:
        # Randomise x,y until you find an empty location
        while True:
            x = self.__get_random_x()
            y = self.__get_random_y()
            if self.get(x,y) == EntityType.EMPTY:
                return [x,y]

    def __get_random_x(self)->int:
        return randrange(self.width())

    def __get_random_y(self)->int:
        return randrange(self.height())

class ScoredMove:
    dx = 0
    dy = 0
    score = 0

class Snake:
    def __init__(self, x, y, board: Board):
        self.__last_head_position = [x, y]
        self.__current_head_position = [x,y]
        self.__current_tail_position = [x, y]
        self.__parts = [[x,y]]
        self.__board = board
        self.__board.set(x,y,EntityType.SNAKE)

    def turn(self)->SnakeTurnResult:
        last_dx = self.__current_head_position[0] - self.__last_head_position[0]
        last_dy = self.__current_head_position[1] - self.__last_head_position[1]
        #Score the moves
        move_one = self.__score_move(-1, 0, last_dx, last_dy)
        move_two = self.__score_move(0, 1, last_dx, last_dy)
        move_three = self.__score_move(1, 0, last_dx, last_dy)
        move_four = self.__score_move(0, -1, last_dx, last_dy)

        all_moves = [move_one, move_two, move_three, move_four]

        all_moves.sort(key=lambda m: m.score)
        all_moves.reverse()

        move = all_moves[0]
        new_head_position = [self.__current_head_position[0] + move.dx, self.__current_head_position[1] + move.dy]

        target_entity = self.__board.get(new_head_position[0], new_head_position[1])

        if target_entity == EntityType.WALL or target_entity == EntityType.SNAKE:
            self.__clear_all_parts_from_board()
            return SnakeTurnResult.DIED
        elif target_entity == EntityType.FOOD:
            # we're going to grow - so we only move the head, not the tail
            self.__move_head(new_head_position)
            return SnakeTurnResult.ATE
        else:
            # we're not growing, so move the head and the tail
            self.__move_head(new_head_position)
            self.__move_tail()
            return SnakeTurnResult.MOVED

    def __move_tail(self):
        self.__board.set(self.__current_tail_position[0], self.__current_tail_position[1], EntityType.EMPTY)
        tail_index = len(self.__parts) - 1
        self.__parts.pop(tail_index)
        tail_index = tail_index - 1
        self.__current_tail_position = [self.__parts[tail_index][0], self.__parts[tail_index][1]]

    def __move_head(self, target_position):
        self.__last_head_position = self.__current_head_position
        self.__current_head_position = target_position
        self.__board.set(target_position[0], target_position[1], EntityType.SNAKE)
        self.__parts.insert(0, target_position)

    def __clear_all_parts_from_board(self):
        for part in self.__parts:
            self.__board.set(part[0], part[1], EntityType.EMPTY)

    def __score_move(self, dx, dy, previous_dx, previous_dy)->ScoredMove:
        scored_move = ScoredMove()
        scored_move.dx = dx
        scored_move.dy = dy

        if previous_dx == dx and previous_dy == dy:
            has_momentum = True
        else:
            has_momentum = False

        max_look_ahead = 4
        food_weight = 1
        snake_weight = -1
        wall_weight = -2
        current_score = 1 if has_momentum else 0
        current_look_ahead = 1
        projected_head_position = self.__current_head_position
        while current_look_ahead <= max_look_ahead:
            projected_head_position[0] = projected_head_position[0] + dx
            projected_head_position[1] = projected_head_position[1] + dy
            projected_entity = self.__board.get(projected_head_position[0], projected_head_position[1])
            projected_weight = 0
            match projected_entity:
                case EntityType.SNAKE:
                    projected_weight = snake_weight
                case EntityType.FOOD:
                    projected_weight = food_weight
                case EntityType.WALL:
                    projected_weight = wall_weight
            projected_weight = projected_weight * (1 / current_look_ahead)
            current_score = current_score + projected_weight
        scored_move.score = current_score

        return scored_move

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
                snake = Snake(pos[0], pos[1], self.__board)
                self.__snakes.append(snake)

    def turn(self):
        food_to_spawn = 0
        snakes_to_spawn = 0
        for snake in self.__snakes:
            turn_result = snake.turn()
            if turn_result == SnakeTurnResult.ATE:
                food_to_spawn = food_to_spawn + 1
            if turn_result == SnakeTurnResult.DIED:
                snakes_to_spawn = snakes_to_spawn + 1
                self.__snakes.remove(snake)
        self.__spawn_foods(food_to_spawn)
        self.__spawn_snakes(snakes_to_spawn)

game_options = GameOptions()
game_board = Board(game_options)
game_engine = Engine(game_board, game_options)

game_engine.starting_spawn()

try:
    print("Press CTRL-C to stop.")
    game_engine.turn()

except KeyboardInterrupt:
    sys.exit(0)