from drawer import Drawer
import getch
import time
import os
import random
from copy import deepcopy

MIN_BOMBS = 0.05
MAX_BOMBS = 0.35
MIN_SIZE = 10
MAX_SIZE = 50

class Game():
    def __init__(self, size, bombs_proportion, no_cursor=False, no_drawing=False):
        random.seed(time.time())
        self.__no_cursor = no_cursor
        self.__no_drawing = no_drawing

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
        self.__hidden_count = self.__size**2 - self.__bombs_count
        
        self.__grid = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        self.__grid_mask = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        self.__bombs_placed = False
        
        self.__cursor = {'x': 0, 'y': 0}
        self.__status = 'in_game'

        self.__drawer = Drawer(self.__size, self.__bombs_count)
        self.__drawer.draw(self.__grid, self.__grid_mask, self.__cursor)
        
    def play_as_player(self):
        while self.__status == 'in_game':
            user_char = getch.getch()
            self.__action(user_char)
    
    def __action(self, user_char):
        if user_char == 'h':
            self.go_left()
        if user_char == 'j':
            self.go_down()
        if user_char == 'k':
            self.go_up()
        if user_char == 'l':
            self.go_right()
        if user_char == 'H':
            self.go_max_left()
        if user_char == 'J':
            self.go_max_down()
        if user_char == 'K':
            self.go_max_up()
        if user_char == 'L':
            self.go_max_right()
        if user_char == 'f':
            self.update_flag()
        if user_char == ' ':
            self.reveal_cell()
        if user_char == 'a':
            self.reveal_around()

    def __draw(self):
        if self.__status == 'in_game':
            if not self.__no_drawing:
                self.__drawer.draw(self.__grid, self.__grid_mask, self.__cursor)
        else:
            self.__drawer.display_end_screen(self.__status, self.__grid, self.__grid_mask, self.__cursor)

    def reveal_around(self):
        if self.__status == 'in_game':
            if not self.__bombs_placed:
                self.__place_bombs()
            self.__reveal_around()
            self.__draw()

    def reveal_cell(self):
        if self.__status == 'in_game':
            if not self.__bombs_placed:
                self.__place_bombs()
            self.__reveal_cell(self.__cursor['x'], self.__cursor['y'])
            self.__draw()
    
    def go_max_right(self):
        if self.__status == 'in_game':
            self.__cursor['x'] = self.__size - 1
            if not self.__no_cursor:
                self.__draw()

    def go_max_up(self):
        if self.__status == 'in_game':
            self.__cursor['y'] = 0
            if not self.__no_cursor:
                self.__draw()

    def go_max_left(self):
        if self.__status == 'in_game':
            self.__cursor['x'] = 0
            if not self.__no_cursor:
                self.__draw()

    def go_max_down(self):
        if self.__status == 'in_game':
            self.__cursor['y'] = self.__size - 1
            if not self.__no_cursor:
                self.__draw()

    def go_right(self):
        if self.__status == 'in_game' and self.__cursor['x'] < self.__size - 1:
            self.__cursor['x'] += 1
            if not self.__no_cursor:
                self.__draw()

    def go_up(self):
        if self.__status == 'in_game' and self.__cursor['y'] > 0:
            self.__cursor['y'] -= 1
            if not self.__no_cursor:
                self.__draw()

    def go_left(self):
        if self.__status == 'in_game' and self.__cursor['x'] > 0:
            self.__cursor['x'] -= 1
            if not self.__no_cursor:
                self.__draw()

    def go_down(self):
        if self.__status == 'in_game' and self.__cursor['y'] < self.__size - 1:
            self.__cursor['y'] += 1
            if not self.__no_cursor:
                self.__draw()

    def update_flag(self):
        if self.__status == 'in_game':
            x = self.__cursor['x']
            y = self.__cursor['y']
            if self.__grid_mask[x][y] == 2:
                self.__grid_mask[x][y] = 0
            elif self.__grid_mask[x][y] == 0:
                self.__grid_mask[x][y] = 2
            self.__draw()

    def __reveal_around(self):
        x = self.__cursor['x']
        y = self.__cursor['y']
        if x > 0 and y > 0 and self.__status == 'in_game':
            self.__reveal_cell(x - 1, y - 1)
        if x > 0 and self.__status == 'in_game':
            self.__reveal_cell(x - 1, y)
        if x > 0 and y < self.__size - 1 and self.__status == 'in_game':
            self.__reveal_cell(x - 1, y + 1)
        if y > 0 and self.__status == 'in_game':
            self.__reveal_cell(x, y - 1)
        if y < self.__size - 1 and self.__status == 'in_game':
            self.__reveal_cell(x, y + 1)
        if x < self.__size - 1 and y > 0 and self.__status == 'in_game':
            self.__reveal_cell(x + 1, y - 1)
        if x < self.__size - 1 and self.__status == 'in_game':
            self.__reveal_cell(x + 1, y)
        if x < self.__size - 1 and y < self.__size - 1 and self.__status == 'in_game':
            self.__reveal_cell(x + 1, y + 1)

    def __reveal_cell(self, x, y):
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
        queue = [(x, y)]
        while queue:
            cell = queue.pop(0)
            if cell[0] > 0:
                new_cell = self.__flood(cell[0] - 1, cell[1])
                if new_cell != None:
                    queue.append(new_cell)
            if cell[1] > 0:
                new_cell = self.__flood(cell[0], cell[1] - 1)
                if new_cell != None:
                    queue.append(new_cell)
            if cell[0] < self.__size - 1:
                new_cell = self.__flood(cell[0] + 1, cell[1])
                if new_cell != None:
                    queue.append(new_cell)
            if cell[1] < self.__size - 1:
                new_cell = self.__flood(cell[0], cell[1] + 1)
                if new_cell != None:
                    queue.append(new_cell)
            if cell[0] > 0 and cell[1] > 0:
                new_cell = self.__flood(cell[0] - 1, cell[1] - 1)
                if new_cell != None:
                    queue.append(new_cell)
            if cell[0] > 0 and cell[1] < self.__size - 1:
                new_cell = self.__flood(cell[0] - 1, cell[1] + 1)
                if new_cell != None:
                    queue.append(new_cell)
            if cell[0] < self.__size - 1 and cell[1] > 0:
                new_cell = self.__flood(cell[0] + 1, cell[1] - 1)
                if new_cell != None:
                    queue.append(new_cell)
            if cell[0] < self.__size - 1 and cell[1] < self.__size - 1:
                new_cell = self.__flood(cell[0] + 1, cell[1] + 1)
                if new_cell != None:
                    queue.append(new_cell)
        if self.__hidden_count == 0:
            self.__status = 'won'
    
    def __flood(self, x, y):
        cell = None
        if self.__grid_mask[x][y] != 1:
            self.__hidden_count -= 1
            self.__grid_mask[x][y] = 1
            if self.__grid[x][y] == 0:
                cell = (x, y)
        return cell

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

    def get_cursor(self):
        return deepcopy(self.__cursor)
    
    def get_status(self):
        return self.__status

    def get_size(self):
        return self.__size

    def get_bombs_count(self):
        return self.__bombs_count

    def get_grid(self):
        grid = deepcopy(self.__grid)
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__grid_mask[x][y] == 0:
                    grid[x][y] = None
                elif self.__grid_mask[x][y] == 2:
                    grid[x][y] = -2
        return grid
