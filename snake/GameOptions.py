from typing import List

from snake.Enums import WallSets


class GameOptions:
    height=128
    width=128
    start_food_count=20
    start_snake_count=20
    starting_wall_positions=[]
    wall_set=WallSets.NONE

    def __starting_wall_positions(self)->List:
        # default shape - the edges
        positions = []
        for x in range(self.width):
            positions.append([x,0])
            positions.append([x,self.height - 1])
        for y in range(self.height):
            positions.append([0,y])
            positions.append([self.width - 1,y])
        return positions

    def refresh_walls(self):
        if self.wall_set == WallSets.SQUARE:
            self.starting_wall_positions = self.__starting_wall_positions()