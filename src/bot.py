from copy import deepcopy
import logging
import sys
import random
import time

logging.basicConfig(filename='bot.log', level=logging.DEBUG)

class Bot():
    def __init__(self, game):
        self.__game = game
        self.__size = self.__game.get_size()
        self.__revealed_count = 0
        self.__bombs_count = self.__game.get_bombs_count()
        self.__placed_flags = 0
        self.__no_need_to_check_again = []
        self.__grid = []
        random.seed(time.time())

    def play(self):
        self.__reveal(random.randint(0, self.__size - 1), random.randint(0, self.__size - 1))
        self.__revealed_count += 1
        self.__grid = self.__game.get_grid()
        while self.__game.get_status() == 'in_game':
            self.__choose_best_move()
            self.__grid = self.__game.get_grid()

    def __choose_best_move(self):
        if not self.__naive_moves():
            self.__smart_move()
            time.sleep(10)
            #self.__random_move()

    def __smart_move(self):
        #Find all revealed cells that have a hidden neighbour(s)
        #Stocker les revealed cells et les hidden neighbours dans des sets
        revealed_cells_w_hidden_neighbour = set()
        hidden_neighbours = set()
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__grid[x][y] != None and self.__grid[x][y] > 0:
                    hidden_count, hidden_cells = self.__count_around(x, y, None)
                    if hidden_count > 0:
                        hidden_neighbours.update(hidden_cells)
                        revealed_cells_w_hidden_neighbour.add((x, y))

        logging.debug(hidden_neighbours)
        hidden_neighbours_by_regions = self.__divide_by_regions(hidden_neighbours)
        logging.debug(hidden_neighbours_by_regions)
        
        #Simule all bombs possibilities depending on values
        #nb de bombs max: self.__bombs_count - self.__placed_flags
        max_bombs = self.__bombs_count - self.__placed_flags
        simulations_grid = [[None for _ in range(self.__size)] for _ in range(self.__size)]
        simulations_count = 0
        #Probas des hiddens neighbours = nb simulated bombs / nb simulations
        #Probas des autres hiddens = nb restants - nb de bombs max / nb hiddens restants
        pass

    def __divide_by_regions(self, cells):
        all_regions = [[cells.pop()]]
        region = 0
        added = False
        while cells:
            current_region = deepcopy(all_regions[region])
            for x, y in current_region:
                neighbours = set([(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)])
                intersection = list(neighbours & cells)
                logging.debug('cells: ' + str(cells) + ', neighbours: ' + str(neighbours) + ', intersection: ' + str(intersection))
                for x_inter, y_inter in intersection:
                    cells.remove((x_inter, y_inter))
                    all_regions[region].append((x_inter, y_inter))
                    added = True
            if not added and cells:
                all_regions.append([cells.pop()])
                region += 1
                logging.debug('append new region: ' + str(all_regions[region]))
            added = False
        return all_regions

    def __reveal_random_in(self, cells):
        cell_to_reveal = random.choice(cells)
        self.__reveal(cell_to_reveal[0], cell_to_reveal[1])
        self.__revealed_count += 1

    def __random_move(self):
        hidden_cells = []
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__grid[x][y] == None:
                    hidden_cells.append((x, y)) 
        self.__reveal_random_in(hidden_cells)

    def __naive_moves(self):
        move_found = False
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__grid[x][y] != None and self.__grid[x][y] > 0 and (x, y) not in self.__no_need_to_check_again:
                    flags_around, cells = self.__count_around(x, y, -2)
                    hiddens_around, cells = self.__count_around(x, y, None)
                    if self.__grid[x][y] > flags_around:
                        if hiddens_around + flags_around == self.__grid[x][y]:
                            self.__put_flags_around(x, y)
                            move_found = True
                    else:
                        if hiddens_around > 0:
                            self.__reveal_around(x, y)
                            self.__revealed_count += hiddens_around
                            move_found = True
                        self.__no_need_to_check_again.append((x, y))
        return move_found

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
        cells = []
        count = 0
        if x > 0:
            count, cells = self.__count(x - 1, y, value, count, cells)
        if x < self.__size - 1:
            count, cells = self.__count(x + 1, y, value, count, cells)
        if y > 0:
            count, cells = self.__count(x, y - 1, value, count, cells)
        if y < self.__size - 1:
            count, cells = self.__count(x, y + 1, value, count, cells)
        if x > 0 and y > 0:
            count, cells = self.__count(x - 1, y - 1, value, count, cells)
        if x > 0 and y < self.__size - 1:
            count, cells = self.__count(x - 1, y + 1, value, count, cells)
        if x < self.__size - 1 and y > 0:
            count, cells = self.__count(x + 1, y - 1, value, count, cells)
        if x < self.__size - 1 and y < self.__size - 1:
            count, cells = self.__count(x + 1, y + 1, value, count, cells)
        return (count, cells)

    def __count(self, x, y, value, count, cells):
        if self.__grid[x][y] == value:
            count += 1
            cells.append((x, y))
        return (count, cells)

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
