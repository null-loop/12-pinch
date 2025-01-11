from math import floor
from random import randrange
from typing import List

from PIL import ImageColor

from snake.Board import Board
from snake.Enums import EntityType, SnakeTurnResult
from snake.ScoredMove import ScoredMove

class SnakeTraits:

    def __init__(self):
        self.food_weight = float(2)
        self.wall_weight = float(-1.1)
        self.snake_weight = float(-1.1)

    def mutate(self):
        trait = randrange(3)
        trait_change = randrange(100) / float(200)
        neg = randrange(2)

        if neg == 1:
            trait_change = 0 - trait_change

        if trait == 0: self.food_weight = self.food_weight + trait_change
        if trait == 1: self.wall_weight = self.wall_weight + trait_change
        if trait == 2: self.snake_weight = self.snake_weight + trait_change

class Snake:

    @classmethod
    def spawn_new_snake(cls, x, y, board):
        colour_index = randrange(3)
        colour = [0,0,0]
        colour[colour_index] = randrange(255)
        traits = SnakeTraits()
        return Snake([[x,y]], traits, colour, board)

    @classmethod
    def split_new_snake(cls, new_parts:List, parent_traits, colour, board):
        #colour_index = randrange(3)
        #colour[colour_index] = randrange(230)+25
        traits = SnakeTraits()
        traits.snake_weight = parent_traits.snake_weight
        traits.food_weight = parent_traits.food_weight
        traits.wall_weight = parent_traits.wall_weight
        traits.mutate()

        return Snake(new_parts, traits, colour, board)

    def __init__(self, parts:List, traits, colour, board: Board):

        self.__traits = traits

        head_part = parts[0]
        tail_part = parts[-1]

        if len(parts) == 1:
            self.__last_head_position = head_part.copy()
        else:
            self.__last_head_position = parts[1].copy()

        self.__current_head_position = head_part.copy()
        self.__current_tail_position = tail_part.copy()
        self.__parts = parts.copy()
        self.__board = board
        self.__colour = colour
        self.__length_to_split = 40
        self.redraw_on_board()

    def print_state(self):
        print(f'Colour : {self.__colour[0]},{self.__colour[1]},{self.__colour[2]} - Snake_Weight : {self.__traits.snake_weight} - Food_Weight : {self.__traits.food_weight} - Wall_Weight : {self.__traits.wall_weight}')

    def redraw_on_board(self):
        for part in self.__parts:
            self.__board.set_with_colour(part[0], part[1], EntityType.SNAKE, self.__colour)

    def turn(self)->SnakeTurnResult:
        #Score the moves
        move_one = self.__score_move(dx=-1, dy=0)
        move_two = self.__score_move(dx=1, dy=0)
        move_three = self.__score_move(dx=0, dy=1)
        move_four = self.__score_move(dx=0, dy=-1)

        move = move_one
        if move_two.score > move.score: move = move_two
        if move_three.score > move.score: move = move_three
        if move_four.score > move.score: move = move_four

        new_head_position = [self.__current_head_position[0] + move.dx, self.__current_head_position[1] + move.dy]

        self.__overflow_position(new_head_position)

        target_entity = self.__board.get(new_head_position[0], new_head_position[1])

        if target_entity == EntityType.WALL or target_entity == EntityType.SNAKE:
            self.__clear_all_parts_from_board()
            return SnakeTurnResult.DIED
        elif target_entity == EntityType.FOOD:
            # we're going to grow - so we only move the head, not the tail
            self.__move_head(new_head_position)

            new_length = len(self.__parts)
            if new_length == self.__length_to_split:
                return SnakeTurnResult.SPLIT

            return SnakeTurnResult.ATE
        else:
            # we're not growing, so move the head and the tail
            self.__move_head(new_head_position)
            self.__move_tail()
            return SnakeTurnResult.MOVED

    def colour_string(self):
        return "{0}{1}{2}".format(self.__colour[0], self.__colour[1], self.__colour[2])

    def split(self):
        # split the parts of our current snake into ours and theirs
        split_length = floor(self.__length_to_split / 2)
        my_parts = self.__parts.copy()[:split_length]
        their_parts = self.__parts.copy()[-split_length:]

        # update our parts
        self.__last_head_position = my_parts[1]
        self.__current_head_position = my_parts[0]
        self.__current_tail_position = my_parts[-1]
        self.__parts = my_parts

        # we're going to create a new snake
        new_snake = Snake.split_new_snake(their_parts, self.__traits, self.__colour.copy(), self.__board)
        new_snake.redraw_on_board()
        return new_snake

    def __move_tail(self):
        self.__board.set(self.__current_tail_position[0], self.__current_tail_position[1], EntityType.EMPTY)

        if len(self.__parts) == 2:
            # if we're only 1 long - our tail is just our head
            self.__current_tail_position = self.__current_head_position.copy()
            self.__parts.pop(-1)
        else:
            # remove the last part
            self.__parts.pop(-1)
            # our tail pos is now the last item
            self.__current_tail_position = self.__parts[-1].copy()

    def __move_head(self, target_position):
        self.__last_head_position = self.__current_head_position.copy()
        self.__current_head_position = target_position
        self.__board.set_with_colour(target_position[0], target_position[1], EntityType.SNAKE, self.__colour)
        self.__parts.insert(0, target_position)

    def __clear_all_parts_from_board(self):
        for part in self.__parts:
            self.__board.set(part[0], part[1], EntityType.EMPTY)

    def __score_move(self, dx, dy)->ScoredMove:
        previous_dx = self.__current_head_position[0] - self.__last_head_position[0]
        previous_dy = self.__current_head_position[1] - self.__last_head_position[1]
        scored_move = ScoredMove()
        scored_move.dx = dx
        scored_move.dy = dy

        if previous_dx == dx and previous_dy == dy:
            has_momentum = True
        else:
            has_momentum = False

        max_look_ahead = 5
        current_score = float(0.25) if has_momentum else float(0)
        current_look_ahead = 1
        projected_head_position = self.__current_head_position.copy()
        while current_look_ahead <= max_look_ahead:
            projected_head_position[0] = projected_head_position[0] + dx
            projected_head_position[1] = projected_head_position[1] + dy

            self.__overflow_position(projected_head_position)

            projected_entity = self.__board.get(projected_head_position[0], projected_head_position[1])
            projected_weight = 0
            if projected_entity == EntityType.SNAKE: projected_weight = self.__traits.snake_weight
            if projected_entity == EntityType.WALL: projected_weight = self.__traits.wall_weight
            if projected_entity == EntityType.FOOD: projected_weight = self.__traits.food_weight
            projected_weight = projected_weight * (1 / current_look_ahead)
            current_score = current_score + projected_weight
            current_look_ahead = current_look_ahead + 1
        scored_move.score = current_score

        return scored_move

    def __overflow_position(self, position:List):
        if position[0] == self.__board.width():
            position[0] = 0
        elif position[0] == -1:
            position[0] = self.__board.width() - 1

        if position[1] == self.__board.height():
            position[1] = 0
        elif position[1] == -1:
            position[1] = self.__board.height() - 1
