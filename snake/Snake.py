from random import randrange
from typing import List

from PIL import ImageColor

from snake.Board import Board
from snake.Enums import EntityType, SnakeTurnResult
from snake.ScoredMove import ScoredMove


class Snake:

    @classmethod
    def spawn_new_snake(cls, x, y, board):
        colour = [0, 0, randrange(230) + 25]
        return Snake([[x,y]], colour, board)

    @classmethod
    def split_new_snake(cls, parts, colour, board):
        colour[0] = 128
        return Snake(parts, colour, board)

    def __init__(self, parts:List, colour, board: Board):

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
        self.__colour = [0, 0, randrange(230) + 25]
        self.__length_to_split = 20
        self.redraw_on_board()

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

            old_length = len(self.__parts)

            # we're going to grow - so we only move the head, not the tail
            self.__move_head(new_head_position)

            new_length = len(self.__parts)

            length_delta = new_length - old_length
            if length_delta > 1:
                print(f'Grew more than 1! : {old_length} to {new_length}, a delta of {length_delta}')

            if new_length == 20 and self.__colour[0] == 128:
                print('Length 20 - Splitting!')
                return SnakeTurnResult.SPLIT
            elif self.__colour[0] == 128:
                print(f'Length {new_length} - Not splitting!')

            return SnakeTurnResult.ATE
        else:
            # we're not growing, so move the head and the tail
            self.__move_head(new_head_position)
            self.__move_tail()
            return SnakeTurnResult.MOVED

    def split(self):
        # split the parts of our current snake into ours and theirs
        my_parts = self.__parts[:10]
        their_parts = self.__parts[-10:]

        # update our parts
        self.__last_head_position = my_parts[1]
        self.__current_head_position = my_parts[0]
        self.__current_tail_position = my_parts[-1]

        # we're going to create a new snake
        new_snake = Snake.split_new_snake(their_parts, self.__colour, self.__board)
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

        max_look_ahead = 10
        food_weight = 2
        snake_weight = -1.1
        wall_weight = -1.1
        current_score = float(0.25) if has_momentum else float(0)
        current_look_ahead = 1
        projected_head_position = self.__current_head_position.copy()
        while current_look_ahead <= max_look_ahead:
            projected_head_position[0] = projected_head_position[0] + dx
            projected_head_position[1] = projected_head_position[1] + dy

            self.__overflow_position(projected_head_position)

            projected_entity = self.__board.get(projected_head_position[0], projected_head_position[1])
            projected_weight = 0
            if projected_entity == EntityType.SNAKE: projected_weight = snake_weight
            if projected_entity == EntityType.WALL: projected_weight = wall_weight
            if projected_entity == EntityType.FOOD: projected_weight = food_weight
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
