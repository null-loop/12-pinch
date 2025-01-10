from random import randrange

from PIL import ImageColor

from snake.Board import Board
from snake.Enums import EntityType, SnakeTurnResult
from snake.ScoredMove import ScoredMove


class Snake:
    def __init__(self, x, y, board: Board):
        self.__last_head_position = [x,y]
        self.__current_head_position = [x,y]
        self.__current_tail_position = [x,y]
        self.__parts = [[x,y]]
        self.__board = board
        self.__colour = [randrange(230) + 25, randrange(230) + 25, randrange(230) + 25]
        self.__board.set_with_colour(x,y,EntityType.SNAKE, self.__colour)

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
        current_score = float(1) if has_momentum else float(0)
        current_look_ahead = 1
        projected_head_position = self.__current_head_position.copy()
        while current_look_ahead <= max_look_ahead:
            projected_head_position[0] = projected_head_position[0] + dx
            projected_head_position[1] = projected_head_position[1] + dy
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