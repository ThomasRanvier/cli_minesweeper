import sys
import time

class Bot():
    def __init__(self, game):
        self.__game = game
        self.__size = self.__game.get_size()
        self.__revealed_count = 0
        self.__bombs_count = self.__game.get_bombs_count()
        self.__placed_flags = 0
        self.__no_need_to_check = []
        self.__grid = []

    def play(self):
        mid = int(self.__size / 2) - 1
        self.__reveal(mid, mid)
        self.__revealed_count += 1
        self.__grid = self.__game.get_grid()
        #while self.__game.get_status() == 'in_game':
        self.__choose_best_move()
            #grid = self.__game.get_grid()

    def __choose_best_move(self):
        self.__naive_moves()

    def __naive_moves(self):
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__grid[x][y] != None and self.__grid[x][y] > 0 and (x, y) not in self.__no_need_to_check:
                    flags_around = self.__count_around(x, y, -2)
                    hiddens_around = self.__count_around(x, y, None)
                    if self.__grid[x][y] > flags_around:
                        if hiddens_around + flags_around == self.__grid[x][y]:
                            self.__put_flags_around(x, y)
                    #else:
                        #self.__reveal_around(x, y)
                        #self.__revealed_count += hiddens_around
                        #self.__no_need_to_check.append((x, y))

    def __put_flags_around(self, x, y):
        if x > 0:
            if self.__grid[x - 1][y] == None:
                self.__put_flag(x - 1, y)
        if x < self.__size - 1:
            if self.__grid[x + 1][y] == None:
                self.__put_flag(x + 1, y)
        if y > 0:
            if self.__grid[x][y - 1] == None:
                self.__put_flag(x, y - 1)
        if y < self.__size - 1:
            if self.__grid[x][y + 1] == None:
                self.__put_flag(x, y + 1)
        if x > 0 and y > 0:
            if self.__grid[x - 1][y - 1] == None:
                self.__put_flag(x - 1, y - 1)
        if x > 0 and y < self.__size - 1:
            if self.__grid[x - 1][y + 1] == None:
                self.__put_flag(x - 1, y + 1)
        if x < self.__size - 1 and y > 0:
            if self.__grid[x + 1][y - 1] == None:
                self.__put_flag(x + 1, y - 1)
        if x < self.__size - 1 and y < self.__size - 1:
            if self.__grid[x + 1][y + 1] == None:
                self.__put_flag(x + 1, y + 1)

    def __put_flag(self, x, y):
        self.__go_to(x, y)
        self.__game.update_flag()
        self.__placed_flags += 1
        self.__grid[x][y] = -2
                    
    def __count_around(self, x, y, value):
        count = 0
        if x > 0:
            count += 1 if self.__grid[x - 1][y] == value else 0
        if x < self.__size - 1:
            count += 1 if self.__grid[x + 1][y] == value else 0
        if y > 0:
            count += 1 if self.__grid[x][y - 1] == value else 0
        if y < self.__size - 1:
            count += 1 if self.__grid[x][y + 1] == value else 0
        if x > 0 and y > 0:
            count += 1 if self.__grid[x - 1][y - 1] == value else 0
        if x > 0 and y < self.__size - 1:
            count += 1 if self.__grid[x - 1][y + 1] == value else 0
        if x < self.__size - 1 and y > 0:
            count += 1 if self.__grid[x + 1][y - 1] == value else 0
        if x < self.__size - 1 and y < self.__size - 1:
            count += 1 if self.__grid[x + 1][y + 1] == value else 0
        return count

    def __reveal_around(self, x, y):
        self.__go_to(x, y)
        self.__game.reveal_around()

    def __reveal(self, x, y):
        self.__go_to(x, y)
        self.__game.reveal_cell()

    def __go_to(self, x, y):
        current_cursor = self.__game.get_cursor()
        while current_cursor['x'] > x:
            current_cursor['x'] -= 1
            self.__game.go_left()
        while current_cursor['x'] < x:
            current_cursor['x'] += 1
            self.__game.go_right()
        while current_cursor['y'] > y:
            current_cursor['y'] -= 1
            self.__game.go_up()
        while current_cursor['y'] < y:
            current_cursor['y'] += 1
            self.__game.go_down()
