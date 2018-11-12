from copy import deepcopy
from termcolor import colored
import time
import sys
import os

class Drawer():
    def __init__(self, size, bombs_count):
        self.__size = size
        self.__clear = True
        self.__first_draw = False
        os.system('setterm -cursor off')
        print(str(self.__size) + 'x' + str(self.__size) + ' ' + str(bombs_count) + ' bombs')
    
    def __del__(self):
        os.system('setterm -cursor on')
        if self.__clear:
            os.system('clear')
    
    def draw(self, grid, grid_mask, cursor, shockwave=None, clean=True):
        if self.__first_draw:
            sys.stdout.write(self.__size * '\033[F')
        self.__first_draw = True
        for y in range(self.__size):
            line = ''
            for x in range(self.__size):
                char, color, bold, background = self.__get_cell(x, y, cursor, grid, grid_mask, shockwave)
                if bold and background != None:
                    char = colored(char, color, background, attrs=['bold'])
                elif bold and background == None:
                    char = colored(char, color, attrs=['bold'])
                elif not bold and background != None:
                    char = colored(char, color, background)
                else:
                    char = colored(char, color)
                line += char
                if x < self.__size - 1:
                    line += ' '
            print(line + '\033[K')

    def __get_cell(self, x, y, cursor, grid, grid_mask, shockwave=None):
        char = '?'
        color = 'grey'
        bold = False
        background = None
        added = False
        if shockwave != None:
            if shockwave[x][y] == 2:
                background = 'on_red'
                bold = True
                added = True
                char = '#'
            elif shockwave[x][y] == 3:
                color = 'red'
                added = True
                char = '#'
        if not added:
            if grid_mask[x][y] == 1:
                if grid[x][y] > 0:
                    char = grid[x][y]
                    if grid[x][y] == 1:
                        color = 'blue'
                    elif grid[x][y] == 2:
                        color = 'green'
                    elif grid[x][y] == 3:
                        color = 'magenta'
                    elif grid[x][y] == 4:
                        color = 'cyan'
                    elif grid[x][y] == 5:
                        color = 'yellow'
                    elif grid[x][y] == 6:
                        color = 'blue'
                    elif grid[x][y] == 7:
                        color = 'green'
                    elif grid[x][y] == 8:
                        color = 'magenta'
                elif grid[x][y] == 0:
                    char = ' '
                elif grid[x][y] == -1:
                    char = 'o'
                    color = 'red'
            elif grid_mask[x][y] == 2:
                char = 'F'
                color = 'cyan'
                bold = True
        if x == cursor['x'] and y == cursor['y']:
            background = 'on_white'
            bold = True
        return (char, color, bold, background)

    def display_end_screen(self, statut, grid, grid_mask, cursor):
        if statut == 'lost':
            self.__display_shockwave(grid, grid_mask, cursor)
        self.__quit(grid, grid_mask, statut, cursor)

    def __quit(self, grid, grid_mask, statut, cursor):
        self.__clear = False
        self.draw(grid, grid_mask, cursor)
        print('')
        sys.stdout.write('\033[F\033[K')
        print('\n')
        print('You lost, :/' if statut == 'lost' else 'GG, you won ! :)')
        print('\n')
        
    def __display_shockwave(self, grid, grid_mask, cursor):
        shockwave_out = False
        shockwave = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
        iterations = 0
        shockwave_2 = set()
        shockwave_3 = set()
        while not shockwave_out:
            start = time.process_time()
            if iterations == 0 or iterations == 2 or iterations == 4 or iterations == 6 or iterations == 8:
                shockwave[cursor['x']][cursor['y']] = 2
                shockwave_2.add((cursor['x'], cursor['y']))
            self.draw(grid, grid_mask, cursor, shockwave)

            shockwave_1 = set()
            shockwave_out = True
            for x, y in shockwave_2:
                shockwave_out = False
                if x > 0:
                    if shockwave[x - 1][y] == 0:
                        shockwave[x - 1][y] = 1
                        shockwave_1.add((x - 1, y))
                if y > 0:
                    if shockwave[x][y - 1] == 0:
                        shockwave[x][y - 1] = 1
                        shockwave_1.add((x, y - 1))
                if x < self.__size - 1:
                    if shockwave[x + 1][y] == 0:
                        shockwave[x + 1][y] = 1
                        shockwave_1.add((x + 1, y))
                if y < self.__size - 1:
                    if shockwave[x][y + 1] == 0:
                        shockwave[x][y + 1] = 1
                        shockwave_1.add((x, y + 1))
                shockwave[x][y] = 3
                shockwave_3.add((x, y))
            shockwave_2 = set()

            for x, y in shockwave_1:
                if grid[x][y] == -1:
                    grid_mask[x][y] = 1
                shockwave[x][y] = 2
                shockwave_2.add((x, y))

            shockwave_3_mem = deepcopy(shockwave_3)
            for x, y in shockwave_3_mem:
                exploding_in_neighbourhood = False
                if x > 0:
                    if shockwave[x - 1][y] == 2:
                        exploding_in_neighbourhood = True
                if y > 0:
                    if shockwave[x][y - 1] == 2:
                        exploding_in_neighbourhood = True
                if x < self.__size - 1:
                    if shockwave[x + 1][y] == 2:
                        exploding_in_neighbourhood = True
                if y < self.__size - 1:
                    if shockwave[x][y + 1] == 2:
                        exploding_in_neighbourhood = True
                if not exploding_in_neighbourhood:
                    shockwave[x][y] = 0
                    shockwave_3.remove((x, y))
            sleep_time = max(0, 0.05 - (time.process_time() - start))
            time.sleep(sleep_time)
            iterations += 1
