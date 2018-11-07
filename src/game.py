from drawer import Drawer
import getch
import time
import os
import signal
import random

MIN_BOMBS = 0.05
MAX_BOMBS = 0.35
MIN_SIZE = 10
MAX_SIZE = 50

class Game():
    def __init__(self, size, bombs_proportion):
        random.seed(time.time())

        self.__size = size
        if self.__size < MIN_SIZE:
            self.__size = MIN_SIZE
        if self.__size > MAX_SIZE:
            self.__size = MAX_SIZE

        if bombs_proportion < MIN_BOMBS:
            bombs_proportion = MIN_BOMBS
        if bombs_proportion > MAX_BOMBS:
            bombs_proportion = MAX_BOMBS
        self.__bombs_count = int(bombs_proportion * self.__size**2)
        
        self.__grid = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        self.__grid_mask = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        self.__bombs_placed = False

        self.__drawer = Drawer(self.__size)
        self.__cursor = {'x': 0, 'y': 0}

        self.__status = 'in_game'
        self.__hidden_count = self.__size**2 - self.__bombs_count
    
    def __del__(self):
        os.system('setterm -cursor on')

    def go(self):
        os.system('setterm -cursor off')
        print(str(self.__size) + 'x' + str(self.__size) + ' ' + str(self.__bombs_count) + ' bombs')
        while self.__status == 'in_game':
            self.__drawer.draw(self.__grid, self.__grid_mask, self.__cursor)
            user_char = getch.getch()
            if user_char == 'h':
                if self.__cursor['x'] > 0:
                    self.__cursor['x'] -= 1
            if user_char == 'j':
                if self.__cursor['y'] < self.__size - 1:
                    self.__cursor['y'] += 1
            if user_char == 'k':
                if self.__cursor['y'] > 0:
                    self.__cursor['y'] -= 1
            if user_char == 'l':
                if self.__cursor['x'] < self.__size - 1:
                    self.__cursor['x'] += 1
            if user_char == 'f':
                self.__update_flag()
            if user_char == ' ':
                if not self.__bombs_placed:
                    self.__place_bombs()
                self.__show_cell(self.__cursor['x'], self.__cursor['y'])
            if user_char == 'a':
                if not self.__bombs_placed:
                    self.__place_bombs()
                self.__show_around()
        self.__drawer.display_end_screen(self.__status, self.__grid, self.__grid_mask, self.__cursor)

    def __show_around(self):
        x = self.__cursor['x']
        y = self.__cursor['y']
        if x > 0 and y > 0:
            self.__show_cell(x - 1, y - 1)
        if x > 0:
            self.__show_cell(x - 1, y)
        if x > 0 and y < self.__size - 1:
            self.__show_cell(x - 1, y + 1)
        if y > 0:
            self.__show_cell(x, y - 1)
        if y < self.__size - 1:
            self.__show_cell(x, y + 1)
        if x < self.__size - 1 and y > 0:
            self.__show_cell(x + 1, y - 1)
        if x < self.__size - 1:
            self.__show_cell(x + 1, y)
        if x < self.__size - 1 and y < self.__size - 1:
            self.__show_cell(x + 1, y + 1)

    def __show_cell(self, x, y):
        if self.__grid_mask[x][y] == 0:
            self.__hidden_count -= 1
            self.__grid_mask[x][y] = 1
            if self.__grid[x][y] == -1:
                self.__status = 'lost'
            elif self.__hidden_count == 0:
                self.__status = 'won'
            else:
                if self.__grid[x][y] == 0:
                    self.__flood_empty(x, y)

    def __flood_empty(self, x, y):
        if x > 0:
            if self.__grid_mask[x - 1][y] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x - 1][y] = 1
                if self.__grid[x - 1][y] == 0:
                    self.__flood_empty(x - 1, y)
        if y > 0:
            if self.__grid_mask[x][y - 1] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x][y - 1] = 1
                if self.__grid[x][y - 1] == 0:
                    self.__flood_empty(x, y - 1)
        if x < self.__size - 1:
            if self.__grid_mask[x + 1][y] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x + 1][y] = 1
                if self.__grid[x + 1][y] == 0:
                    self.__flood_empty(x + 1, y)
        if y < self.__size - 1:
            if self.__grid_mask[x][y + 1] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x][y + 1] = 1
                if self.__grid[x][y + 1] == 0:
                    self.__flood_empty(x, y + 1)
        if x > 0 and y > 0:
            if self.__grid_mask[x - 1][y - 1] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x - 1][y - 1] = 1
                if self.__grid[x - 1][y - 1] == 0:
                    self.__flood_empty(x - 1, y - 1)
        if x > 0 and y < self.__size - 1:
            if self.__grid_mask[x - 1][y + 1] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x - 1][y + 1] = 1
                if self.__grid[x - 1][y + 1] == 0:
                    self.__flood_empty(x - 1, y + 1)
        if x < self.__size - 1 and y > 0:
            if self.__grid_mask[x + 1][y - 1] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x + 1][y - 1] = 1
                if self.__grid[x + 1][y - 1] == 0:
                    self.__flood_empty(x + 1, y - 1)
        if x < self.__size - 1 and y < self.__size - 1:
            if self.__grid_mask[x + 1][y + 1] != 1:
                self.__hidden_count -= 1
                self.__grid_mask[x + 1][y + 1] = 1
                if self.__grid[x + 1][y + 1] == 0:
                    self.__flood_empty(x + 1, y + 1)

    def __update_flag(self):
        x = self.__cursor['x']
        y = self.__cursor['y']
        if self.__grid_mask[x][y] == 2:
            self.__grid_mask[x][y] = 0
        elif self.__grid_mask[x][y] == 0:
            self.__grid_mask[x][y] = 2
            

    def __place_bombs(self):
        for _ in range(self.__bombs_count):
            bomb_placed = False
            while not bomb_placed:
                x = random.randint(0, self.__size - 1)
                y = random.randint(0, self.__size - 1)
                if x != self.__cursor['x'] and y != self.__cursor['y'] and self.__grid[x][y] != -1:
                    bomb_placed = True
                    self.__grid[x][y] = -1
        for y in range(self.__size):
            for x in range(self.__size):
                if self.__grid[x][y] != -1:
                    self.__grid[x][y] = self.__count_bombs_in_neighbourhood(x, y)
        self.__bombs_placed = True

    def __count_bombs_in_neighbourhood(self, x, y):
        count = 0
        if x > 0 and y > 0 and self.__grid[x - 1][y - 1] == -1:
            count += 1
        if x > 0 and self.__grid[x - 1][y] == -1:
            count += 1
        if x > 0 and y < self.__size - 1 and self.__grid[x - 1][y + 1] == -1:
            count += 1
        if y > 0 and self.__grid[x][y - 1] == -1:
            count += 1
        if y < self.__size - 1 and self.__grid[x][y + 1] == -1:
            count += 1
        if x < self.__size - 1 and y > 0 and self.__grid[x + 1][y - 1] == -1:
            count += 1
        if x < self.__size - 1 and self.__grid[x + 1][y] == -1:
            count += 1
        if x < self.__size - 1 and y < self.__size - 1 and self.__grid[x + 1][y + 1] == -1:
            count += 1
        return count

